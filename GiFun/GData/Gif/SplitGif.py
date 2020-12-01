import os
from PIL import Image


def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    预处理通过图像来确定模式(全模式或加法模式)。
    必要的，因为评估单个框架是不可靠的。需要知道模式
    在处理所有帧之前。
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def processImage(path):
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(path)['mode']

    im = Image.open(path)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    try:
        while True:
            print
            "saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile)

            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            如果GIF使用本地颜色表，每个框架都有自己的调色板。
            如果没有，我们需要将全局调色板应用到新框架上。
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            这个文件是一个“部分”模式的GIF，其中帧更新一个不同大小的区域到整个图像?
            如果是这样，我们需要通过将新框架粘贴到前面的框架上来构建新框架。
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            #存储到gif所在目录
            new_frame.save('%s-%d.png' % (''.join(path.split('.')[:-1]), i), 'PNG')

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass


def main():
    processImage('AIwave.gif')


    
if __name__ == "__main__":
    main()
