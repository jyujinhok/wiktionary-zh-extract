from tqdm import tqdm
import xml.etree.ElementTree as ET
import sys
import subprocess
import json
import argparse

PREFIX = "Module:zh/data/dial-syn/"

parser = argparse.ArgumentParser()
parser.add_argument("input", nargs="?", default="./modules.xml", help="modules.xml file from dump-extract (default './modules.xml'")

if __name__ == "__main__":
    args = parser.parse_args()
    tree = ET.parse(args.input)

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
