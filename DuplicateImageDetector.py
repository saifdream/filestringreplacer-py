import hashlib
from PIL import Image


def main():
    # with open('test-data/a.jpg', 'rb') as f:
    #     image_file = f.read()
    # # image_file = open('test-data/a.jpg').read()
    # hashlib.md5(image_file).hexdigest()
    #
    # with open('test-data/b.jpg', 'rb') as f:
    #     image_file_modified = f.read()
    # # image_file_modified = open('test-data/b.jpg').read()
    # hashlib.md5(image_file_modified).hexdigest()
    #
    # test_image = Image.open('test-data/a.jpg')
    #
    # # The image is an RGB image with a size of 8x8 pixels.
    # print('Image Mode: %s' % test_image.mode)
    #
    # print('Width: %s px, Height: %s px' % (test_image.size[0], test_image.size[1]))
    #
    # # Get the pixel values from the image and print them into rows based on the image's width.
    # width, height = test_image.size
    # pixels = list(test_image.getdata())
    #
    # for col in range(width):
    #     print(pixels[col:col + width])
    #
    # img = Image.open('test-data/c.jpg')
    # width, height = img.size
    # pixels = list(img.getdata())
    #
    # for col in range(width):
    #     print(pixels[col:col + width])
    #
    # difference = []
    # for row in range(height):
    #     for col in range(width):
    #         if col != width:
    #             difference.append(pixels[col + row] > pixels[(col + row) + 1])
    #
    # for col in range(width - 1):
    #     print(difference[col:col + (width - 1)])

    def dhash(image, hash_size=8):
        # Grayscale and shrink the image in one step.
        image = image.convert('L').resize(
            (hash_size + 1, hash_size),
            Image.ANTIALIAS,
        )
        pixels = list(image.getdata())
        # Compare adjacent pixels.
        difference = []
        for row in range(hash_size):
            for col in range(hash_size):
                pixel_left = image.getpixel((col, row))
                pixel_right = image.getpixel((col + 1, row))
                difference.append(pixel_left > pixel_right)
        # Convert the binary array to a hexadecimal string.
        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2 ** (index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
        return ''.join(hex_string)

    orig = Image.open('test-data/ohm-1.jpg')
    modif = Image.open('test-data/ohm-1.jpg')
    # print(dhash(orig))
    # print(dhash(modif))
    print(dhash(orig) == dhash(modif))


if __name__ == '__main__':
    main()