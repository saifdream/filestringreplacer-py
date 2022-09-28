import os
import time
from difflib import SequenceMatcher
from shutil import copyfile
from urllib.parse import unquote
from PIL import Image
import concurrent.futures


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


def get_file_list(path):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))

    print(len(files))
    return files


def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def duplicate_file_finder(unique_file, matcher_file):
    # print('matcher_file, unique_file: %s, %s' % (matcher_file, unique_file))
    unique_hash_file = Image.open("unique/" + unique_file)
    receive_hash_file = Image.open(matcher_file)

    is_same = dhash(unique_hash_file) == dhash(receive_hash_file)
    return is_same


def main():
    first_start_time = time.time()
    text = open("csv/product_old.csv", "r")
    output = ""
    unique_files = set()
    received_files = get_file_list('/chitra/Project/Python/ImageDownloader/img')
    received_files.sort(reverse=False)

    idx = 0
    for rf in received_files:
        idx = idx + 1
        print(idx)
        receive_file_name = unquote(rf.split('/')[-1])
        is_in_set = receive_file_name in unique_files

        if len(unique_files) > 0:
            is_duplicate = False
            unique_file_name = ""
            unique_files = set(sorted(unique_files, reverse=True))

            sorted_unique_files = [u if similar(receive_file_name, u) > 0.0 else print("less than zero") for u in unique_files]
            if len(sorted_unique_files) == 0:
                sorted_unique_files = [u if similar(receive_file_name, u) == 0.0 else print("equal zero") for u in unique_files]

            # receive_file = [rf]
            # with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
            #     for unique_file, is_duplicate_result in zip(unique_files, executor.map(duplicate_file_finder, unique_files, receive_file)):
            #         print("is_duplicate is: %s" % is_duplicate_result)
            #         print("unique_file is: %s" % unique_file)
            #         is_duplicate = is_duplicate_result
            #         unique_file_name = unique_file

            with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
                future_to_uf = {executor.submit(duplicate_file_finder, uf, rf): uf for uf in sorted_unique_files}
                for future in concurrent.futures.as_completed(future_to_uf):
                    uf = future_to_uf[future]
                    try:
                        is_duplicate = future.result()
                        if is_duplicate:
                            unique_file_name = uf
                            executor.shutdown()
                            break
                    except Exception as exc:
                        print('%r generated an exception: %s' % (uf, exc))
                    else:
                        # print('future is %s' % future)
                        pass

            if is_duplicate:
                if not os.path.isfile("duplicate/" + receive_file_name):
                    print("duplicate copy")
                    copyfile(rf, "duplicate/" + receive_file_name)
                output = ''.join([i for i in text]).replace(receive_file_name, unique_file_name)
                # print(output)
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

    print(output)
    x = open("csv/product_new.csv", "w")
    x.write(output)
    x.close()
    text.close()
    print("Final --- %s seconds --- " % (time.time() - first_start_time))


if __name__ == '__main__':
    main()
