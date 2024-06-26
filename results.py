#!/Users/rlefaive/.venv/bin/python
import csv
import datetime
import db

db_file = 'data.sqlite'
fieldnames = ['id', 'record', 'url', 'status_code', 'final_url', 'timestamp']


def create_output_filename():
    current_time = datetime.datetime.now()
    return 'results-{}.csv'.format(current_time.isoformat()).replace(':','')

def filter_results(results):
    # Ignore results where the result was 200 and there was no final url.
    results = [row for row in results if not (row['status_code'] == '200' and row['final_url'] == '')]
    return results


def main():
    database = db.DB(db_file)
    results = database.get_responses('1901-01-01')
    with open(create_output_filename(), 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        dict_results = [dict(row) for row in results]
        dict_results = filter_results(dict_results)
        writer.writerows(dict_results)


if __name__ == '__main__':
    main()
