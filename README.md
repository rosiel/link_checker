# Link Checker

A python3 tool to check the validity of URLs in bibliographic records.

Sample output:
```
id,record,url,status_code,final_url,timestamp
136,510017,http://epe.lac-bac.gc.ca/100/201/301/annual_cnsc_staff_report_safety/index.html,404,https://epe.lac-bac.gc.ca/100/201/301/annual_cnsc_staff_report_safety/index.html,2024-06-26 08:22:30
```

## Quick Usage

Given `input.csv` is a CSV file of links to check, containing headers `record` (the record ID) and `url` (the link) (see below for other options):

```bash
./csvLoader.py input.csv    # Populates the database, data.sqlite, with links to check.
./linkCheck.py              # Checks the link and stores the resuts. Run this until it doesn't check any more.
./results.py                # Outputs the results in a results-[timestamp].csv.
```

## Installation

Use pip to install the required libraries:

```python
pip install -r requirements.txt
```


## Workflow

The general workflow is:
* add documents to the `links` table (either through `csvLoader.py` or `bibidLoader.py`)
* run `linkCheck.py` to populate the `results` table from the `links` table. Only links that don't have a corresponding entry in the `results` table will be processed.
* run `results.py` to generate an output spreadsheet.

### CSV Loader

If you already have a spreadsheet of the links to check, use `csvLoader.py` to 
add them to the links table. The input csv must have columns `record` and `url`.
If an existing entry exists in the link table with identical `record` and `url` 
then the link will not be added. The path to the csv file or files is given on 
the command line as a positional argument:

```bash
./csvLoader.py input.csv
```

### Bib ID Loader

If you are using Evergreen, then you can provide a list of id's of records. They
can be in a .txt or .csv file, but they must be in the first column if it is a 
csv. A header for the column of bib ids, if it exists, must equal `id`. The 
file name or names must be provided as a command line positional argument:

```bash
./bibidLoader.py ids.txt
```

## Options

### Database name

By default, the data will be stored in a database file called `data.sqlite`. 
This can be configured using the `-d` or `--database` option on the command 
line.

## Authors

Rosie Le Faive (@rosiel on Github)

## License

[MIT](https://choosealicense.com/licenses/mit/)
