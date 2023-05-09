import requests, sys, time
import regex as re
from pathlib import Path

## Read the arxiv API terms of use: https://info.arxiv.org/help/api/tou.html

total_pattern = re.compile(r"  <opensearch:totalResults xmlns:opensearch=\"http://a9.com/-/spec/opensearch/1.1/\">(\d+)</opensearch:totalResults>")


limit = 500
largest = limit

# get the target category (eg cs.CL) and make sure there exists a directory for it
target = sys.argv[1]
Path(target).mkdir(parents=True, exist_ok=True)

url = "http://export.arxiv.org/api/query"
query = "cat:{}".format(target)

start = 0
while start < largest:
    print(start, end="\t")

    filename = "{}/results{:04d}.xml".format(target, start)
    filepath = Path(filename)
    if filepath.exists() and filepath.stat().st_size > 900:
        # if we're restarting, we may not have read the total number of records
        if largest == 500:
            with open(filename) as reader:
                for line in reader:
                    match = total_pattern.search(line)
                    if match:
                        largest = int(match.group(1))
                        break

        print("exists, skipping")
        start += limit
        continue

    text = ""
    attempts = 0

    # the download sometimes fails, in which case the returned file is short, less than 900 characters
    # try to get it a couple more times, but keep going otherwise
    while attempts < 3:
        results = requests.get("{}?search_query={}&start={}&max_results={}".format(url, query, start, limit))
        print(results.status_code)
        text = results.text

        if len(text) < 900:
            print("request failed, retrying")
            attempts += 1
            time.sleep(3)
        else:
            break
    
    # check the file for the number of total results
    match = total_pattern.search(text)
    if match:
        largest = int(match.group(1))
    
    # write the file
    with open("{}/results{:04d}.xml".format(target, start), "w") as writer:
        writer.write(text)

    # add more time between requests:
    # "When using the legacy APIs (including OAI-PMH, RSS, and the arXiv API), make no more than one request every three seconds, and limit requests to a single connection at a time."
    time.sleep(3)

    # update the start position
    start += limit



