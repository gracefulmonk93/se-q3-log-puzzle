#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

__author__ = "Leann James with help from Jordan Haagenson"

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    # +++your code here+++
    animal_pattern = r'GET (\S*puzzle\S*)'
    places_pattern = r'GET (\S*puzzle/\w-\w{4}-\w{4}\S*)'
    puzzle_pieces = []
    with open(filename, 'r') as f:
        file_read = f.read()
        if re.search(places_pattern, file_read) is not None:
            matches = re.findall(places_pattern, file_read)
            matches = sorted(matches, key=lambda x: x[-8:-4])
        else:
            matches = re.findall(animal_pattern, file_read)
            matches = sorted(matches)
        matches = ['http://code.google.com' + match for match in matches]
        for url in matches:
            if url not in puzzle_pieces:
                puzzle_pieces.append(url)
        return puzzle_pieces


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(f'{dest_dir}/index.html', 'w') as html:
        html.write('<body>')
        for url in enumerate(img_urls):
            with open(f'{dest_dir}/img{str(url[0])}.jpg', 'wb'):
                filename = f'{dest_dir}/img{str(url[0])}.jpg'
                urllib.request.urlretrieve(url[1], filename)
            html.write(f'<img src="img{str(url[0])}.jpg">')
        html.write('\n</body>')


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    read_urls(parsed_args.logfile)
    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
