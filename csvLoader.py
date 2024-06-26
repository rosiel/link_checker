#!/Users/rlefaive/.venv/bin/python

import optparse
import csv
import os
import db


def parse_cmd_line():
    parser = optparse.OptionParser(usage="%prog [options] INPUT_FILE")
    parser.add_option("-d", "--database", dest="database", default="data.sqlite",
                      help="Sqlite file to populate. [default: %default]")

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.error("Need at least one csv input file on the command line. It must have headers 'record' and 'url'.")

    for arg in args:
        if not arg.endswith('.csv'):
            parser.error("Input must be a csv file.")

    return opts.database, args


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
