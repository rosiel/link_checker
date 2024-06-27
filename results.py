#!/usr/bin/env python3
import argparse
import csv
import datetime
import db

fieldnames = ['id', 'record', 'url', 'status_code', 'final_url', 'timestamp']


def parse_cmd_line():
    parser = argparse.ArgumentParser(description="Output a report of checked links. Outputs to 'results-[current_time].csv'",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--database", default="data.sqlite",
                        help="sqlite database file to populate.")
    parser.add_argument("-t", "--timestamp", default="1901-01-01",
                        help="only export results registered later than this timestamp.")
    args = parser.parse_args()
    return args.database, args.timestamp


def create_output_filename():
    current_time = datetime.datetime.now()
    return 'results-{}.csv'.format(current_time.isoformat()).replace(':','')


def filter_results(results):
    # Ignore results where the result was 200 and there was no final url.
    results = [row for row in results if not (row['status_code'] == '200' and row['final_url'] == '')]
    return results


def main():
    db_file, timestamp = parse_cmd_line()
    database = db.DB(db_file)
    results = database.get_responses(timestamp)
    with open(create_output_filename(), 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        dict_results = [dict(row) for row in results]
        dict_results = filter_results(dict_results)
        writer.writerows(dict_results)


if __name__ == '__main__':
    main()
