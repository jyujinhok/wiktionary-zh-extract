from tqdm import tqdm
import xml.etree.ElementTree as ET
import json
import argparse
import regex as re

from wiktionary_to_baxter import wiktionary_to_baxter

PREFIX = "Module:zh/data/ltc-pron/"

parser = argparse.ArgumentParser()
parser.add_argument("input", nargs="?", default="./ltc.xml", help="ltc.xml file from dump-extract (default './ltc.xml'")

if __name__ == "__main__":
    args = parser.parse_args()
    tree = ET.parse(args.input)

    root = tree.getroot()

    out = {}

    for child in tqdm(root):
        title = child.find('title').text
        if title.startswith(PREFIX):
            title = title[len(PREFIX):]
        if re.search(r"^\p{Han}$", title):
            text = child.find("text").text.strip()
            text = re.sub(r"^return", "", text)
            text = re.sub(r"--.*\n", "\n", text)
            try:
                datastrings = eval(text)
            except (SyntaxError, NameError):
                raise ValueError(f"Check page for '{title}'")
            output = []
            for datastring in datastrings:
                try:
                    output.append((datastring, wiktionary_to_baxter(datastring)))
                except ValueError:
                    print(f"Warning: entry {title} has a malformed datastring {datastring}")
            out[title] = output

    with open("ltc.json", "w") as outfile:
        json.dump(out, outfile, ensure_ascii = False)
    print("Written to ltc.json")

#     och = json.load(open("../och-bs-parse/och_BS.json"))
#     nogoods = []
#     ltc_inventory = set()
#     och_inventory = set()
#     cleaned_ltc = {}
#     cleaned_och = {}
#     for ch in och:
#         if ch not in out: continue
#         och_b = {e[1].replace("ae", "æ").replace("ea", "ɛ").replace("+", "ɨ").replace("X", "").replace("H", "").replace("'", "ʔ").replace('"', "ʔ") for e in och[ch]}
#         ltc_b = {e[1].replace("ɛɨ", "ɛ").replace("X", "").replace("H", "") for e in out[ch]}
#         och_inventory |= och_b
#         ltc_inventory |= ltc_b
#         cleaned_och[ch] = och_b
#         cleaned_ltc[ch] = ltc_b
#         # if any("y" in b for b in och_b):
#         if len(och_b) <= len(ltc_b) and och_b - ltc_b:
#             nogoods.append((ch, och_b, ltc_b))

# # current nogoods: 423
