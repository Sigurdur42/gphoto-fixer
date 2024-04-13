import argparse
import logging

takeout_base_folder = None
files_to_process = []
image_files = []


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


def main():
    analyse_arguments()

    print(f'Scanning folder {takeout_base_folder}...')
    scan_directory(takeout_base_folder)
    print(f'Found {len(files_to_process)} json files and {len(image_files)} image files')


if __name__ == "__main__":
    main()
