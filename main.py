from fastapi import FastAPI
from pathlib import Path
import json
import re


app = FastAPI()

LOG_FILE = "apache_logs"
STATE_FILE = "log_state.json"
BATCH_SIZE = 100


# LOG_PATTERN = re.compile(
#     r'(?P<ipaddress>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] '
#     r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
#     r'(?P<status_code>\d{3}) (?P<bytes_sent>\S+) '
#     r'"(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
# )

# def parse_log_line(line):
#     match = LOG_PATTERN.match(line)
#     if match:
#         return match.groupdict()
#     return None


def get_last_index():
    if Path(STATE_FILE).exists():
        with open(STATE_FILE) as f:
            return json.load(f).get("last_index", 0)
    return 0

def update_last_index(idx):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_index": idx}, f)

# def load_and_parse_logs():
#     with open(LOG_FILE) as f:
#         lines = f.readlines()
#     return [parse_log_line(line) for line in lines if parse_log_line(line)]

# all_logs = load_and_parse_logs()

def load_logs():
    if Path(LOG_FILE).exists():
        with open(LOG_FILE) as f:
            return f.readlines()
    return []

@app.get("/logs")
def get_logs():
    lines = load_logs()
    start = get_last_index()
    end = start + BATCH_SIZE
    batch = lines[start:end]
    update_last_index(min(end, len(lines)))

    return {
        "raw_logs": [line.strip() for line in batch],
        "start_index": start,
        "end_index": min(end, len(lines)),
        "total_logs": len(lines)
    }