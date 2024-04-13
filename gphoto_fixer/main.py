import argparse
import logging

takeout_base_folder = None


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


def main():
    analyse_arguments()


if __name__ == "__main__":
    main()
