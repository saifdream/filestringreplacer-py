import os
from shutil import copyfile
from urllib.parse import unquote
from PIL import Image


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


def get_file_list():
    path = '/chitra/Project/Python/ImageDownloader/img'

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            # if '.txt' in file:
            files.append(os.path.join(r, file))

    # for f in files:
    #     print(f)

    print(len(files))
    return files


def main():
    unique_files = set()
    replaceable_files = {}
    received_files = get_file_list()

    for rf in received_files:
        print(rf)
        receive_file_name = unquote(rf.split('/')[-1])

        is_in_set = receive_file_name in unique_files

        print(len(unique_files))
        if len(unique_files) > 0:
            is_duplicate = False
            unique_file_name = ""
            for uf in unique_files.copy():
                unique_hash_file = Image.open("unique/" + uf)
                receive_hash_file = Image.open(rf)

                is_duplicate = dhash(unique_hash_file) == dhash(receive_hash_file)
                print(is_duplicate)
                if is_duplicate:
                    unique_file_name = unquote(uf.split('/')[-1])
                    break

            if is_duplicate:
                print("duplicate copy")
                copyfile(rf, "duplicate/" + receive_file_name)
                replaceable_files['rename_to_'+unique_file_name] = unique_file_name
                replaceable_files['rename_from_'+receive_file_name] = receive_file_name
            else:
                if not is_in_set:
                    unique_files.add(receive_file_name)
                    if not os.path.isfile("unique/" + receive_file_name):
                        print("unique copy")
                        copyfile(rf, "unique/" + receive_file_name)

        else:
            if not is_in_set:
                unique_files.add(unquote(rf.split('/')[-1]))
                if not os.path.isfile("unique/" + receive_file_name):
                    print("unique copy")
                    copyfile(rf, "unique/" + receive_file_name)

    print(unique_files)
    print(replaceable_files)


if __name__ == '__main__':
    main()
