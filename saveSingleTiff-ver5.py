#!/usr/bin/env python
# coding: utf-8

from skimage.io import imread, imsave
import javabridge
import bioformats
import xml.etree.ElementTree as ET
from bioformats import load_image, get_omexml_metadata, get_metadata_options
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import argparse
import re
from joblib import Parallel, delayed

def getLifMetadata(lif_file):
    lif_metadata = get_omexml_metadata(lif_file)
    et_root = ET.fromstring(lif_metadata)
    lif_series = [child.attrib.get('Name') for child in et_root if re.search(".*Image", child.tag) is not None]

    return(lif_series)


def check_img(img, px_dim, ch_dim):
    return((img.shape[0]==px_dim) & (img.shape[2]==ch_dim))

def save_single_tiff(img, basename, out_path):
    # print('{},{}'.format(basename,img.shape))
    for ch_idx in range(img.shape[2]):
        save_name = basename + "_Ch" + str(ch_idx) + ".tiff"
        imsave(os.path.join(out_path,save_name), img[:,:,ch_idx], check_contrast=False)

parser = argparse.ArgumentParser("Print lif file metadata")
parser.add_argument('Path', metavar='path', type=str, help='Path with .lif files')
parser.add_argument('Output', metavar='out', type=str, help='Path for single tiff output')
parser.add_argument('Pixels', metavar='px', type=int, help='Pixel dimension of image', default=2048)
parser.add_argument('Channels', metavar='ch', type=int, help='Number of channels', default=4)

app_args = parser.parse_args()
input_path = app_args.Path
px_dim = app_args.Pixels
ch_dim = app_args.Channels
out_path = app_args.Output
print('{},{},{},{}'.format(input_path, out_path, px_dim, ch_dim))

if not os.path.isdir(input_path):
    print('The path specified does not exist.')
    sys.exit()


javabridge.start_vm(class_path=bioformats.JARS)

lif_files = [os.path.join(input_path, file) for file in os.listdir(input_path) if re.search(".*lif$", file) is not None]

for lif_file in lif_files:
    lif_series = getLifMetadata(lif_file)
    lif_redate = re.search(r'.*/([0-9]{6}).*', lif_file)
    lif_date = lif_redate[1]
    prev_image_desc = ""
    img_nr = 1
    for i, series_name in enumerate(lif_series):
        img = load_image(lif_file, series=i, rescale=False)
        if check_img(img, px_dim, ch_dim) == True:
            series_redesc = re.search(r'([0-9]{1,2}h)/([0-9]+nmol)/.*',series_name)
            series_desc = series_redesc[1] + "_" + series_redesc[2]
            if series_desc == prev_image_desc:
                img_nr = img_nr + 1
            else:
                img_nr = 1
            basename = lif_date + "_" + series_desc + "_" + str(img_nr)
            save_single_tiff(img, basename, out_path)
            print('{} saved as {}'.format(series_name,basename))
            prev_image_desc = series_desc

javabridge.kill_vm()
