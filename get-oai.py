import requests, sys, time
import regex as re
from pathlib import Path

# This script uses the OAI-PMH service to load sets greater than 50,000 papers

## Read the arxiv API terms of use: https://info.arxiv.org/help/api/tou.html

resumption_pattern = re.compile(r"<resumptionToken cursor=\"\d+\" completeListSize=\"\d+\">(.*)</resumptionToken>")

limit = 500
largest = limit

# get the target set (eg cs) and make sure there exists a directory for it
target = sys.argv[1]
Path(target).mkdir(parents=True, exist_ok=True)

url = "http://export.arxiv.org/oai2"
query = "cat:{}".format(target)

results = requests.get("{}?verb=ListRecords&metadataPrefix=arXiv&set={}".format(url, target))
print(results.status_code)
text = results.text

start = 1
filename = "{}/results{:05d}.xml".format(target, start)

# write the file
with open(filename, "w") as writer:
    writer.write(text)

match = resumption_pattern.search(text)
if match:
    resumption_token = match.group(1)
else:
    resumption_token = None



while resumption_token != None:
    start += 1000
    time.sleep(5.2)
    print(start, resumption_token, end="\t")

    filename = "{}/results{:06d}.xml".format(target, start)

    text = ""
    results = requests.get("{}?verb=ListRecords&resumptionToken={}".format(url, resumption_token))
    print(results.status_code)
    if results.status_code != 200:
        print(results.reason, results.text)
    text = results.text

    match = resumption_pattern.search(text)
    if match:
        resumption_token = match.group(1)
    else:
        resumption_token = None
    
    # write the file
    with open("{}/results{:06d}.xml".format(target, start), "w") as writer:
        writer.write(text)

    # add more time between requests:
    # "When using the legacy APIs (including OAI-PMH, RSS, and the arXiv API), make no more than one request every three seconds, and limit requests to a single connection at a time."
    



