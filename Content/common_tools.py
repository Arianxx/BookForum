import os

from PIL import Image


def crop_img(img, NEW_WIDTH, NEW_HEIGHT):
    """
    裁剪上传的图片

    :param img: 一个ImageField对象
    :param NEW_WIDTH: 想获得的宽度
    :param NEW_HEIGHT: 想获得的高度
    :return: 裁剪后的PIL.Image图片对象
    """
    path = img.path
    img = Image.open(path)

    # 如果图片两边都大于想获得的长宽，缩小图片以获得最多信息
    width, height = img.size
    if height > NEW_HEIGHT and width > NEW_WIDTH:
        img = img.resize((NEW_WIDTH, int(height * (NEW_WIDTH / width))))
        img.load()

    # 如果图片任意边小于想要获得的宽度，放大到想要获得的宽度，以便于裁剪
    width, height = img.size
    if height < NEW_HEIGHT:
        scale = NEW_HEIGHT / height
        width = width * scale
        height = NEW_HEIGHT
        img = img.resize((int(width), int(height)))
        img.load()

    width, height = img.size
    if width < NEW_WIDTH:
        scale = NEW_WIDTH / width
        height = height * scale
        width = NEW_WIDTH
        img = img.resize((int(width), int(height)))
        img.load()

    # 在正中裁剪想要的图片
    size = (
        (width - NEW_WIDTH) // 2,
        (height - NEW_HEIGHT) // 2,
        (width - NEW_WIDTH) // 2 + NEW_WIDTH,
        (height - NEW_HEIGHT) // 2 + NEW_HEIGHT,
    )
    new_img = img.crop(size)
    img.close()
    new_img.save(path)

    return new_img


def delete_img(img):
    real_path = img.path
    default_path = img.field.default.replace('/', '\\')

    if not default_path in real_path:
        os.remove(real_path)

    return True
