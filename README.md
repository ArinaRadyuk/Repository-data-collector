# Repository data collector

- Collects the following data using Scrapy for each link: repository name, description, link, number of stars, number of forks, number of watching, number of commits, info about the latest commit (author, name, UTC datetime),  number of releases, info about the latest release (version, creation datetime, changelog) 
- Stores data in MongoDB database

## Installation

```sh
pip install scrapy
pip install pymongo
```
## Usage
1. make sure you are in scrapy_task folder
2. scrapy crawl reviewspider -a start_urls=<file_name1,file_name2,...>

## Example
1. scrapy crawl reviewspider -a start_urls="https://github.com/scrapy,https://github.com/celery/"
2. scrapy crawl reviewspider -a start_urls="https://github.com/scrapy"

## Understanding the project

### items.py

The main goal of scraping is to extract unstructured data and convert it to meaningful, structured data.
There are several dataclasses: GithubItem, which contains information about repository id,name, description, link, number of stars, number of forks, number of watching, number of commits,  number of releases.
