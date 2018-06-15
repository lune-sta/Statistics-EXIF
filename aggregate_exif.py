import sys, os
import numpy
from PIL import Image
from PIL.ExifTags import TAGS



def get_exif(file):
    try:
        with Image.open(file) as im:
            exif_raw = im._getexif()
    except:
        return {}

    # delete MakerNote
    exif_raw.pop(0x927c, None)

    exif = {}

    for tag_id, value in exif_raw.items():
        exif[TAGS.get(tag_id, tag_id)] = value

    return exif


def is_jpeg(file):
    return os.path.splitext(file)[1].lower() in ('.jpeg', '.jpg')

def dredge_jpegs(path):
    if os.path.isfile(path):
        if is_jpeg(path):
            return path
        else:
            return None

    for root, _, files in os.walk(path):
        for file in files:
            if is_jpeg(file):
                yield os.path.join(root, file)


def main():
    data = []

    for jpeg in dredge_jpegs(sys.argv[-1]):
        focal_length = get_exif(jpeg).get('FocalLengthIn35mmFilm')

        if focal_length:
            data.append(focal_length)

    data = numpy.array(data, dtype='u2')

    print(data)


if __name__ == "__main__":
    main()