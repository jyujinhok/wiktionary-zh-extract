from tqdm import tqdm
import xml.etree.ElementTree as ET
import sys
import subprocess
import json

PREFIX = "Module:zh/data/dial-syn/"
tree = ET.parse("modules.xml")

root = tree.getroot()

out = {}

for child in tqdm(root):
    title = child.find('title').text
    if title.startswith(PREFIX):
        title = title[len(PREFIX):]

    body = child.find("text")
    with open("moduletest.lua", "w") as module:
        module.write(body.text)
    run = subprocess.run(["lua", "runner.lua"], capture_output = True)
    if run.returncode != 0:
        print("Skipping", title)
        continue
    # print(run.stdout)
    out[title] = json.loads(run.stdout)

with open("dial.json", "w") as outfile:
    json.dump(out, outfile, ensure_ascii = False)
print("Written to dial.json")