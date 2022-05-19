# Repository data collector

- Collects the following data using Scrapy for each link: repository name, description, link, number of stars, number of forks, number of watching, number of commits, info about the latest commit (author, name, UTC datetime),  number of releases, info about the latest release (version, creation datetime, changelog) 
- Stores data in MongoDB database

## Installation

```sh
pip install scrapy
pip install pymongo
```
## Usage
python3 convert.py [--csv2parquet | --parquet2csv <src-filename> <dst-filename>] | [--get-schema <filename>] | [--help]
scrapy crawl reviewspider -a start_urls=<file_name1,file_name2,...>

## Example
1. scrapy crawl reviewspider -a start_urls="https://github.com/scrapy,https://github.com/celery/"
2. scrapy crawl reviewspider -a start_urls="https://github.com/scrapy"

## Example
1. Conversion of files from a csv format to a parquet format.
```sh
python convert.py --csv2parquet dir/src-file.csv dir/dst-file.parquet
```
2. Conversion of files from a parquet format to a csv format.
```sh
python convert.py --parquet2csv dir/src-file.parquet dir/dst-file.csv
```
3. Getting the schema of the parquet file.
```sh
python convert.py --get-schema dir/src-file.parquet 
```
4. Getting info about convert.py
```sh
python convert.py --help
```