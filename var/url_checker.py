import sys
from csv import reader
import re
import unicodedata
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib
table_path = "_data/main_tool_and_resource_list.csv"
registries = {'biotools':'https://bio.tools/', 'fairsharing':'https://fairsharing.org/FAIRsharing.', 'tess':'https://tess.elixir-europe.org/search?q='}

def client(url):
    """API object fetcher"""
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=15)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    try: 
        r = session.get(url, timeout=2 )
        if r.status_code != requests.codes.ok:
            raise Exception(f"{url} gives {r.status_code}")
        else:
            return True
    except Exception as e:
        raise Exception(f"{url} gives {r.status_code}")

with open(table_path, 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    # Check file as empty
    if header != None:
        # Looping over rows and adding its contents to the main dict
        for row_index, row in enumerate(csv_reader):
            tool = {}
            tool_name = row[0]
            for col_index, cell in enumerate(row):
                if header[col_index] == 'registry':
                    output = {}
                    if cell:# Only include keys if there are values
                        for registry in re.split(', |,', cell):
                            reg, identifier = re.split(':|: ', registry)
                            url = f"{registries[reg]}{identifier}"
                            client(url)
                elif header[col_index] == 'link':
                    if cell:
                        client(cell)