import argparse
import logging
import os
import pprint
import time

is_verbose = False
shall_rename_json = False

takeout_base_folder = None
files_to_process = []
image_files = []
files_to_rename = []


def analyse_arguments():
    global takeout_base_folder
    global is_verbose
    global shall_rename_json

    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument('-t', '--takeout', help="Specify the folder where your google takeout images are stored.")
    parser.add_argument('-v', '--verbose', help="Print verbose logging", action='store_true')
    parser.add_argument('-r', '--rename-json', help="Rename the json files automatically to match the media file.",
                        action='store_true')

    try:
        args = parser.parse_args()
        if args is None:
            print('Some error occurred. Aborting.')

        takeout_base_folder = args.takeout
        is_verbose = args.verbose
        shall_rename_json = args.rename_json

    except argparse.ArgumentError as e:
        print(f'Some error occurred: {e}. Aborting.')
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


def rename_json_files():
    for src, target, _ in files_to_rename:
        try:
            if is_verbose:
                print(f'Rename \n{src} to \n{target}')

            os.rename(src, target)
        except Exception as _:
            print(f'Error renaming file from \n{src} to \n{target}: \n{str(_)}')


def get_patched_json(json: str) -> str:
    def patch_numbering(numbering_json: str) -> str:
        if not numbering_json.endswith(')'):
            return numbering_json

        index = numbering_json.rfind('(')
        if index == -1:
            return numbering_json

        length = len(numbering_json) - index
        number = numbering_json[index:]
        patched = numbering_json[:-length]

        extension_index = patched.rfind(".")
        if extension_index == -1:
            return numbering_json

        extension = patched[extension_index:]
        patched = f'{patched[:extension_index]}{number}{extension}'
        return patched

    def patch_missing_letter(letter_json: str) -> str:
        if letter_json.endswith('.jp'):
            letter_json += 'g'
        elif letter_json.endswith('.JP'):
            letter_json += 'G'

        return letter_json

    def patch_missing_extension_jpg(double_json: str):
        if not double_json.endswith('.'):
            return double_json

        double_json = double_json + 'jpg'
        return double_json

    def patch_missing_extension_mp4(double_json: str):
        if not double_json.endswith('.m'):
            return double_json

        double_json = double_json + 'p4'
        return double_json

    def patch_missing_bracket(bracket_json: str) -> str:
        if bracket_json.rstrip('0123456789').endswith("("):
            return bracket_json + ')'

        return bracket_json

    json = patch_numbering(json)
    json = patch_missing_letter(json)
    json = patch_missing_extension_jpg(json)
    json = patch_missing_bracket(json)
    json = patch_missing_extension_mp4(json)
    return json


def match_files():
    json: str
    for json in files_to_process:
        without_ext = json[:-5]
        if without_ext in image_files:
            # found an exact wanted match - this json file can be ignored
            continue

        found_num = 0
        patched_json = get_patched_json(without_ext)
        if patched_json != without_ext:
            found = list(filter(lambda _: _.startswith(patched_json), image_files))
            found_num = len(found)
            if found_num == 1:
                media_file = found[0]
                corrected_file = f'{media_file}.json'
                files_to_rename.append((json, corrected_file, media_file))
                continue

        print(f"media file cannot be found ({found_num}): {json} ({without_ext})")


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

    if is_verbose:
        print('These files will be renamed:')
        for src, target, media in files_to_rename:
            print(f'\nfrom <{src}>\nto   <{target}>\nfor  <{media}>')

    if shall_rename_json:
        start = time.monotonic()
        print('Renaming files now...')
        rename_json_files()
        end = time.monotonic()
        print(f'renaming files took {end - start:.{2}} seconds (files to rename: {len(files_to_rename)})')


if __name__ == "__main__":
    main()
