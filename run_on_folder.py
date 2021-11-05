#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 20:22:32 2019

@author: pedrofRodenas
"""

import blur_wavelet
import os
import argparse
import json
import cv2


def find_images(input_dir):
    extensions = [".jpg", ".png", ".jpeg"]

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in extensions:
                yield os.path.join(root, file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='run Haar Wavelet blur detection on a folder')
    parser.add_argument('-i', '--input_dir', dest="input_dir",
                        type=str, required=True, help="directory of images")
    parser.add_argument('-s', '--save_path', dest='save_path',
                        type=str, help="path to save output")
    parser.add_argument("-t", "--threshold", dest='threshold',
                        type=float, default=35, help="blurry threshold")
    parser.add_argument("-d", "--decision", dest='MinZero',
                        type=float, default=0.001, help="MinZero Decision Threshold")
    args = parser.parse_args()

    results = []

    for input_path in find_images(args.input_dir):
        try:
            I = cv2.imread(input_path)
            per, blurext = blur_wavelet.blur_detect(I, args.threshold)
            if per < args.MinZero:
                classification = True
            else:
                classification = False
            results.append({"input_path": input_path, "per": per,
                           "blur extent": blurext, "is blur": classification})
            print("{0}, Per: {1:.5f}, blur extent: {2:.3f}, is blur: {3}".format(
                input_path, per, blurext, classification))

        except Exception as e:
            print(e)
            pass

    if args.save_path:

        assert os.path.splitext(args.save_path)[
            1] == ".json", "You must include the extension .json on the end of the save path"

        with open(args.save_path, 'w') as outfile:
            json.dump(results, outfile, sort_keys=True, indent=4)
            outfile.write("\n")
