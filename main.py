import logging
import sys
import os
import argparse
import shelve
import json
from datetime import datetime, timedelta
from pathlib import Path

import httpx
import re

DISABLE_CACHE = True if 'DISABLE_CACHE' in os.environ else False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream=sys.stderr)

def init_cache(path:Path) -> shelve.Shelf:
    path.parent.mkdir(parents=True, exist_ok=True)
    shelf = shelve.open(str(path), writeback=True)
    return shelf

class TideForecast:
    __slots__ = ['location', 'time', 'height', 'date', 'type']
    def __init__(self, location, time, height, date, type):
        self.location = location
        self.time = time
        self.height = height
        self.date = date
        self.type = type

    def to_json(self):
        return json.dumps({'location':self.location, 'date':self.date, 'time':self.time, 'hieght': self.height, 'type': self.type})

def retrieve_low_tide_page(client: httpx.Client, url: str) -> httpx.Response|None:
    resp = client.get(url)
    try:
        resp.raise_for_status()
        return resp

    except httpx.HTTPError as err:
        logging.error(err)
        return None


def extract_low_tide_data(name:str, data: httpx.Response|None) -> list[TideForecast]:
    if data is None:
        logging.debug("data is None")
        return []

    data_content = data.content.decode()

    start_pos = data_content.index('window.FCGON = ')
    end_pos = data_content[start_pos:].index(';\n//]]>')

    content = json.loads(data_content[start_pos+len('window.FCGON = '):start_pos+end_pos])

    out = []
    for day in content.get('tideDays', []):
        for tide in day.get('tides',[]):
            if tide.get('timestamp') > day.get('sunrise') and tide.get('timestamp') < day.get('sunset') and tide.get('type') == 'low' :
                out.append(TideForecast(location=name, date=day.get('date'), time=tide.get('time').strip(), height=tide.get('height'), type="low"))
    return out


def main(cache_path: Path, location_url_map: dict[str,str], output_path: Path): 
    cache = init_cache(cache_path)
    # limit the cache slots to at most once per day
    day_slot = int(datetime.utcnow().timestamp())//86400
    with httpx.Client() as client, output_path.open('w') as out_fh:
        for name, url in location_url_map.items():
            slot = f'{day_slot}-{url}'
            logging.info(f'collecting {name} tide information')
            low_tide_data: httpx.Response|None
            if slot in cache and not DISABLE_CACHE:
                low_tide_data = cache[slot]
                logging.info(f'found {name} tide info in cache; {len(getattr(low_tide_data, "content", ""))} bytes')
            else:
                low_tide_data = retrieve_low_tide_page(client, url)
                cache[slot] = low_tide_data
                logging.info(f'recieved {len(getattr(low_tide_data,"content", ""))} bytes')
            forecasts = extract_low_tide_data(name, low_tide_data)
            out_fh.writelines((f.to_json()+"\n" for f in forecasts))

    cache.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="main", description="gets low tide data from tide-forecast.com")
    parser.add_argument('--cache', required=True, help="Cache File (eg. `/tmp/cache.shelf`; ie. python shelf)")
    parser.add_argument('--output', required=True, help="Output File NDJSON (eg. `./output.ndjson`)")
    parser.add_argument('--input', required=True, help="Input File JSON (eg. `./input.json`; ie. JSON object)")
    args = parser.parse_args()
    
    cache_path = Path(args.cache)
    output_path = Path(args.output)
    location_url_map = json.loads(Path(args.input).read_text())
    
    main(cache_path, location_url_map, output_path)
