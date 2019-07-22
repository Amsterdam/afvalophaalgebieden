#!/usr/bin/env python
"""
Download the latest shapefiles.
"""
import os
import shutil
import argparse
import pprint
import requests
import zipfile
import errno


def create_dir_if_not_exists(directory):
    """
    Create directory if it does not yet exists.
    Args:
        Specify the name of directory, for example: `dir/anotherdir`
    Returns:
        Creates the directory if it does not exists, of return the error message.
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def unzip(path, filename_as_folder=False):
    """Find all .zip files and unzip in root.
       use filename_as_folder=True
       to unzip to subfolders with name of zipfile.
    """
    for filename in os.listdir(path):
        if filename.endswith(".zip"):
            name = os.path.splitext(os.path.basename(filename))[0]
            if not os.path.isdir(name):
                try:
                    file = os.path.join(path, filename)
                    zip = zipfile.ZipFile(file)
                    if filename_as_folder:
                        directory = os.path.join(path, name)
                        os.mkdir(directory)
                        print("Unzipping {} to {}".format(filename, directory))
                        zip.extractall(directory)
                    else:
                        print("Unzipping {} to {}".format(filename, path))
                        zip.extractall(path)
                except zipfile.BadZipfile:
                    print("BAD ZIP: " + filename)
                    try:
                        os.remove(file)
                    except OSError as e:
                        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                            raise  # re-raise exception if a different error occured


def download_file(file_location, target):
    print("Downloading File from", file_location)
    file = requests.get(file_location, stream=True)
    file.raise_for_status()
    with open(target, 'wb') as f:
        file.raw.decode_content = True
        shutil.copyfileobj(file.raw, f)
    print("Downloaded as", target)


def download_all_files(purl, download_directory):
    """Download files from data catalog response id"""
    create_dir_if_not_exists(download_directory)

    METADATA_URL = 'https://api.data.amsterdam.nl/dcatd/datasets/{}'.format(purl)
    print("Downloading metadata from", METADATA_URL)
    metadata_res = requests.get(METADATA_URL)
    metadata_res.raise_for_status()

    metadata = metadata_res.json()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(metadata)

    for item in metadata['dcat:distribution']:
        if item.get('dcat:mediaType') == 'application/x-zipped-shp':
            #filename = result['url'].split('/')[-1]
            filename = "{}.zip".format(item['dct:title'].replace(' ', '_').lower())
            print('Downloading {}'.format(item['dct:title']))
            download_file(item['dcat:accessURL'], os.path.join(download_directory, filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get data from data catalog')
    parser.add_argument('purl', help='Insert purl id from data catalog, for example: qji2W_HBpWUWyg')
    parser.add_argument('data_path', help='Insert folder path, for example: app/data')
    args = parser.parse_args()
    download_all_files(args.purl, args.data_path)
    unzip(args.data_path)
