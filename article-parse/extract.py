from tqdm import tqdm
import xml.etree.ElementTree as ET
import sys
import re
import json
import wikitextparser as wtp
import argparse

REGEXES = [None, None, re.compile("(?:^|\n)==([^=]+)==\n"), re.compile("\n===([^=]+)===\n")]

def extract_toplevel_templates(text):
    in_template = False
    addl_templates = 0
    for i in range(0, len(text)):
        if text[i] == '{' and text[i + 1] == '{':
            if in_template:
                addl_templates += 1
            else:
                in_template = true


def sections(page, level):
    splits = re.split(REGEXES[level], page)
    out = {}
    # skip first half-match if it exists
    skip_one = len(splits) % 2
    for i in range(skip_one, len(splits), 2):
        out[splits[i]] = splits[i + 1]
    return out

def etyms_for_page(page):
    languages = sections(page, 2)
    if "Chinese" not in languages:
        page = "\n\n" + page
        languages = sections(page, 2)
        if "Chinese" not in languages:
            return None
    language = languages["Chinese"]
    secs = sections(language, 3)
    etyms = {}
    for sec in secs:
        if sec.startswith("Etymology "):
            etyms[sec[len("Etymology "):]] = secs[sec]
        if sec.startswith("Pronunciation "):
            etyms[sec[len("Pronunciation "):]] = secs[sec]

    if len(etyms) == 0:
        etyms["0"] = language
    return etyms

def extract_for_etym(text, title, derivations):
    pron = {}
    dials = []
    wikitext = wtp.parse(text)
    for template in wikitext.templates:
        name = template.name.strip()
        if name == "zh-pron":
            for arg in template.arguments:
                pron[arg.name.strip()] = arg.value.strip()
        if name == "zh-dial":
            if len(template.arguments) > 0:
                dials.append(template.arguments[0].value)
            else:
                dials.append("self")
        if name == "see derivation subpage" and derivations:
            dials += derivations[title]

    return (pron, dials)

def extract_for_page(page, title, derivations):
    etyms = etyms_for_page(page)
    if not etyms:
        return None
    out = {}
    for etym in etyms:

        pron, dials = extract_for_etym(etyms[etym], title, derivations)
        obj = {}
        if pron:
            obj["pron"] = pron
        if dials:
            obj["dial"] = dials
        if obj:
            out[etym] = obj
    return out

parser = argparse.ArgumentParser()
parser.add_argument("input", nargs="?", default="./articles.xml", help="articles.xml file from dump-extract (default './articles.xml'")

if __name__ == "__main__":
    args = parser.parse_args()
    print("Loading xml file...")
    tree = ET.parse(args.input)
    root = tree.getroot()
    derivations = {}
    print("Preparsing derivation subpages...")
    for page in tqdm(root):
        title = page.find("title").text
        if not "/derived terms" in title:
            continue
        title = title.split("/")[0]
        text = page.find("text").text
        extracted = extract_for_etym(text, title, None)
        if extracted:
            derivations[title] = extracted[1]
    print(f"Found {len(derivations)} derivation pages")
    out = {}
    print("Parsing article data...")
    for page in tqdm(root):
        title = page.find("title").text
        text = page.find("text").text
        extracted = extract_for_page(text, title, derivations)
        if extracted:
            out[title] = extracted
    print("Writing to disk...")

    json.dump(out, open("articledata.json", "w"), ensure_ascii = False)
