#!/usr/bin/env python3
import argparse
import db
import requests


def parse_cmd_line():
    parser = argparse.ArgumentParser(description="Output a report of checked links. Outputs to 'results-[current_time].csv'",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--database", default="data.sqlite",
                        help="sqlite database file to populate.")
    args = parser.parse_args()
    return args.database


def resolve_link(url):
    try:
        r = requests.get(url)
        return r
    except Exception as e:
        return repr(e)


def get_final_url(r):
    if len(r.history) > 0:
        return r.url


def main():
    db_file = parse_cmd_line()
    database = db.DB(db_file)

    # Check links, a batch at a time.
    count = 0
    while link_manifest := database.get_links():
        if len(link_manifest) == 0:
            print("No more links to check.")
        for link in link_manifest:
            r = resolve_link(link['url'])
            if isinstance(r, requests.models.Response):
                print(r.status_code)
                response_data = {
                    'link': link['id'],
                    'status_code': r.status_code,
                    'final_url': get_final_url(r)
                }
            else:
                response_data = {
                    'link': link['id'],
                    'status_code': r,
                    'final_url': '',
                }
            print(response_data)
            database.add_response(response_data)
        count += 1
        if count > 99:
            break


if __name__ == '__main__':
    main()