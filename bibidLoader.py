#!/Users/rlefaive/.venv/bin/python
import csv
import optparse
import os
import db
import xml.etree.ElementTree as ET
import requests


def get_links_for_bibid(bibid):
    links = []
    url = 'https://islandpines.roblib.upei.ca/opac/extras/supercat/retrieve/marcxml/record/{}'.format(bibid)
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

def parse_cmd_line():
    parser = optparse.OptionParser(usage="%prog [options] INPUT_FILE")
    parser.add_option("-d", "--database", dest="database", default="data.sqlite",
                      help="Sqlite file to populate. [default: %default]")

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.error("Need at least one csv input file on the command line. It must have headers 'record' and 'url'.")

    for arg in args:
        if not arg.endswith('.csv') and not arg.endswith('.txt'):
            parser.error("Input must be a .csv or .txt file.")

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
            reader = csv.reader(fp)
            for row in reader:
                bibid = row[0]
                if bibid == 'id':
                    continue
                links = get_links_for_bibid(bibid)
                database.add_links(links)

if __name__ == '__main__':
    main()
