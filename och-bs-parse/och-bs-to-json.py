from tqdm import tqdm
import xml.etree.ElementTree as ET
import json
import argparse
import regex as re

# from wiktionary_to_baxter import wiktionary_to_baxter

PREFIX = "Module:zh/data/och-pron-BS/"

parser = argparse.ArgumentParser()
parser.add_argument("input", nargs="?", default="./och_BS.xml", help="och_BS.xml file from dump-extract (default './och_BS.xml'")

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
            text = re.sub(r"{", "[", text)
            text = re.sub(r"}", "]", text)
            try:
                out[title] = eval(text)
            except (SyntaxError, NameError):
                raise ValueError(f"Check page for '{title}'")

    with open("och_BS.json", "w") as outfile:
        json.dump(out, outfile, ensure_ascii = False)
    print("Written to och_BS.json")
