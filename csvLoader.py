#!/usr/bin/env python3
import argparse
import csv
import link_checker.db as db
import os


def parse_cmd_line():
    parser = argparse.ArgumentParser(description="Load links from a CSV file with headers [record, url] into an sqlite"
                                                 "database.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_files', metavar='INPUT_FILE', nargs='+', help="CSV file[s] to process.")
    parser.add_argument("-d", "--database", default="data.sqlite",
                        help="sqlite database file to populate.")

    args = parser.parse_args()

    for arg in args.input_files:
        if not arg.endswith('.csv'):
            parser.error("INPUT_FILE must be a csv file.")

    return args.database, args.input_files


def main():
    # Get input values
    db_filename, input_files = parse_cmd_line()

    # Initialize the db object
    database = db.DB(db_filename)

    # Iterate through input files.
    for input_file in input_files:
        if not os.path.exists(input_file):
            print("File [{}] not found.".format(input_file))
            continue
        with open(input_file, 'r', newline='\n') as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                # Put each link in the link table in the database
                database.add_link(row)


if __name__ == '__main__':
    main()
