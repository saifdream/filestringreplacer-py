import os


if __name__ == '__main__':
    path = '/chitra/Project/Python/ImageDownloader/img'

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            # if '.txt' in file:
            files.append(os.path.join(r, file))

    for f in files:
        print(f)

    print(len(files))