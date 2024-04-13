import argparse
import logging
import time

takeout_base_folder = None
files_to_process = []
image_files = []
files_to_rename = []


def analyse_arguments():
    global takeout_base_folder
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument('-t', '--takeout', help="Specify the folder where your google takeout images are stored.")

    try:
        args = parser.parse_args()
        if args is None:
            print('Some error occurred. Aborting.')

        takeout_base_folder = args.takeout

    except argparse.ArgumentError as e:
        print('Some error occurred. Aborting.')
        exit(-1)

    print(f"Will work in folder {takeout_base_folder}")


def is_json_file(file: str):
    return file.lower().endswith('.json')


def scan_directory(dir_to_scan):
    import os
    with os.scandir(dir_to_scan) as scan:
        for entry in scan:
            if entry.is_file():

                if is_json_file(entry.name):
                    files_to_process.append(entry.path)
                else:
                    image_files.append(entry.path)

            elif entry.is_dir():
                scan_directory(entry)


def get_patched_json(json: str) -> str:
    if not json.endswith(')'):
        return json

    index = json.rfind('(')
    if index == -1:
        return json

    length = len(json) - index
    number = json[index:]
    patched = json[:-length]

    extension_index = patched.rfind(".")
    if extension_index == -1:
        return json

    extension = patched[extension_index: ]
    patched = f'{patched[:extension_index]}{number}{extension}'
    return patched


def match_files():
    json: str
    for json in files_to_process:
        without_ext = json[:-5]
        if without_ext in image_files:
            # found an exact wanted match - this json file can be ignored
            continue

        patched_json = get_patched_json(without_ext)
        if patched_json != without_ext:
            if patched_json in image_files:
                # patched numbering in file - (1) etc.
                files_to_rename.append(patched_json)
                print(f'Fixing numbering in json file {json} -> {without_ext}')
                continue

        print(f"media file cannot be found: {json}")


def main():
    analyse_arguments()

    start = time.monotonic()
    print(f'Scanning folder {takeout_base_folder}...')
    scan_directory(takeout_base_folder)
    end = time.monotonic()
    print(f'Found {len(files_to_process)} json files and {len(image_files)} image files in {end - start:.{2}} seconds')

    start = time.monotonic()
    print('Matching files now...')
    match_files()
    end = time.monotonic()
    print(f'Matching files took {end - start:.{2}} seconds (files to rename: {len(files_to_rename)})')


if __name__ == "__main__":
    main()
