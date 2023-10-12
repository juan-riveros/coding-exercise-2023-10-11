# Gridium Coding Exercise

> While I normally wouldn't include this in a repo, I did include sample output as the `output.ndjson` file.

## Getting Started

```bash
git clone https://github.com/juan-riveros/coding-exercise-2023-10-11
python3 -m venv --copies venv
venv/bin/pip install -r requirements.txt
```

## Usage

### Command Help Message

```bash
> ./venv/bin/python main.py --help

usage: main [-h] --cache CACHE --output OUTPUT

gets low tide data from tide-forecast.com

options:
  -h, --help       show this help message and exit
  --cache CACHE    cache file (eg. `/tmp/cache.shelf`; ie. python shelf)
  --output OUTPUT  Output File NDJSON (eg. `./output.ndjson`)
```

### Run 

```bash
> ./venv/bin/python main.py --cache /tmp/cache.shelf --output ./output.ndjson
2023-10-11 20:08:18,052 - root - INFO - collecting Half Moon Bay, California tide information
2023-10-11 20:08:18,053 - root - INFO - found Half Moon Bay, California tide info in cache; 372034 bytes
2023-10-11 20:08:18,054 - root - INFO - collecting Huntington Beach, California tide information
2023-10-11 20:08:18,055 - root - INFO - found Huntington Beach, California tide info in cache; 368092 bytes
2023-10-11 20:08:18,056 - root - INFO - collecting Providence, Rhode Island tide information
2023-10-11 20:08:18,057 - root - INFO - found Providence, Rhode Island tide info in cache; 359602 bytes
2023-10-11 20:08:18,058 - root - INFO - collecting Wrightsville Beach, North Carolina tide information
2023-10-11 20:08:18,058 - root - INFO - found Wrightsville Beach, North Carolina tide info in cache; 357379 bytes
```

### Clear Cache

While you can just delete the cache file you specify or just point somewhere else, you can also set the environment variable `DISABLE_CACHE` and this will skip the cache.

```bash
> DISABLE_CACHE=yes ./venv/bin/python main.py --cache /tmp/cache.shelf --output ./output.ndjson
2023-10-11 20:13:50,015 - root - INFO - collecting Half Moon Bay, California tide information
2023-10-11 20:13:50,664 - httpx - INFO - HTTP Request: GET https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest "HTTP/1.1 200 OK"
2023-10-11 20:13:50,737 - root - INFO - recieved 372034 bytes
2023-10-11 20:13:50,739 - root - INFO - collecting Huntington Beach, California tide information
2023-10-11 20:13:51,292 - httpx - INFO - HTTP Request: GET https://www.tide-forecast.com/locations/Huntington-Beach/tides/latest "HTTP/1.1 200 OK"
2023-10-11 20:13:51,366 - root - INFO - recieved 368092 bytes
2023-10-11 20:13:51,368 - root - INFO - collecting Providence, Rhode Island tide information
2023-10-11 20:13:51,936 - httpx - INFO - HTTP Request: GET https://www.tide-forecast.com/locations/Providence-Rhode-Island/tides/latest "HTTP/1.1 200 OK"
2023-10-11 20:13:51,982 - root - INFO - recieved 359602 bytes
2023-10-11 20:13:51,984 - root - INFO - collecting Wrightsville Beach, North Carolina tide information
2023-10-11 20:13:52,532 - httpx - INFO - HTTP Request: GET https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest "HTTP/1.1 200 OK"
2023-10-11 20:13:52,570 - root - INFO - recieved 357379 bytes
```
