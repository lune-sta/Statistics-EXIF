import sys
import os
from concurrent.futures import ProcessPoolExecutor

import numpy
from matplotlib import pyplot
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


def get_focal_length(file):
    try:
        with Image.open(file) as im:
            # 0x920a: 'FocalLength'
            frac = im._getexif().get(0x920a)
            return frac[0] / frac[1]
    except:
        return None


def is_jpeg(file):
    return os.path.splitext(file)[1].lower() in ('.jpeg', '.jpg')


def dredge_jpegs(path):
    if os.path.isfile(path):
        if is_jpeg(path):
            yield path
        return

    for root, _, files in os.walk(path):
        for file in files:
            if is_jpeg(file):
                yield os.path.join(root, file)


def main():

    jpeg_files = dredge_jpegs(sys.argv[-1])

    with ProcessPoolExecutor() as executor:
        focal_length_list = list(filter(None, executor.map(get_focal_length, jpeg_files)))

    numpy_data = numpy.array(focal_length_list, dtype='u2')

    pyplot.hist(numpy_data, bins=50)
    pyplot.show()


if __name__ == "__main__":
    main()
