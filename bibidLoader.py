#!/usr/bin/env python3
import argparse
import csv
import db
import os
import requests
import xml.etree.ElementTree as ET


def parse_cmd_line():
    parser = argparse.ArgumentParser(description="From a file of Evergreen bib ids, load any 856 links into an sqlite "
                                                 "database.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_files', metavar='INPUT_FILE', nargs='+',
                        help="Text or csv file[s] to process.\nFor CSV, bib ids must be in the first column. ")
    parser.add_argument("-d", "--database", default="data.sqlite",
                        help="sqlite database file to populate.")
    parser.add_argument("-e", "--evergreen", default="https://islandpines.roblib.upei.ca",
                        help="url of an Evergreen catalogue.")

    args = parser.parse_args()

    for arg in args.input_files:
        if not arg.endswith('.csv') and not arg.endswith('.txt'):
            parser.error("INPUT_FILE must be a csv or txt file.")

    return args.database, args.evergreen, args.input_files


def get_links_for_bibid(eg_url, bibid):
    links = []
    url = '{}/opac/extras/supercat/retrieve/marcxml/record/{}'.format(eg_url, bibid)
    try:
        r = requests.get(url)
        marcxml = ET.fromstring(r.text)
        marc_links = marcxml.findall("./{*}record/{*}datafield[@tag='856']")
        for marc_link in marc_links:
            link = {}
            link['record'] = bibid
            link['ind2'] = marc_link.attrib['ind2']
            link['url'] = marc_link.find("./{*}subfield[@code='u']").text
            links.append(link)
    except Exception as e:
        print(repr(e))
    return links


def main():
    # Get input values
    db_filename, eg_url, input_files = parse_cmd_line()

    # Initialize the db object
    database = db.DB(db_filename)

    # Iterate through input files.
    for input_file in input_files:
        if not os.path.exists(input_file):
            print("File [{}] not found.".format(input_file))
            continue
        with open(input_file, 'r', newline='\n') as fp:
            reader = csv.reader(fp)
            for row in reader:
                bibid = row[0]
                if bibid == 'id':
                    continue
                links = get_links_for_bibid(eg_url, bibid)
                database.add_links(links)

if __name__ == '__main__':
    main()
