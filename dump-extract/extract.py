import bz2
from tqdm import tqdm
import xml.etree.ElementTree as ET
import argparse
from os.path import exists
from sys import exit

MW_HEADER = """<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="en">"""
MW_FOOTER = """</mediawiki>"""
def get_lemma_map():
    lemmas = set()
    with open("../sql-lemma-fetcher/enwikt_chinese_lemmas.csv", "r") as csvfile:
        for line in tqdm(csvfile.readlines()):
            lemmas.add(line.strip())
    return lemmas

def get_offsets(index_txt_filename, predicate):
    curroffset = 0
    split = ""
    mustyield = False
    with open(index_txt_filename, "rb") as file:
        lines = bz2.decompress(file.read()).decode("utf-8").strip().split("\n")
        for line in tqdm(lines):
            split = line.strip().split(':', 2)
            offset = int(split[0])
            if offset != curroffset:
                if mustyield:
                    yield [curroffset, offset]
                mustyield = False
                curroffset = offset
            article = split[2]
            if predicate(article):
                mustyield = True

def write_xml(index_txt_filename, xml_filename, outfile, predicate):
    print("\tCalculating offsets:")
    offsets = list(get_offsets(index_txt_filename, predicate))
    print("\tExtracting data:")
    with open(xml_filename, "rb") as bigfile:
        decompressed = None
        string = ""
        root = {}
        for offset in tqdm(offsets):
            bigfile.seek(offset[0])
            data = None
            if offset[1]:
                data = bigfile.read(offset[1] - offset[0])
            else:
                data = bigfile.read()
            decompressed = bz2.decompress(data)
            string =  "<mediawiki>" + decompressed.decode("utf-8")
            if offset[1]:
                string += "</mediawiki>"
            root = ET.fromstring(string)
            for child in root:
                title = child.find("title")
                if not predicate(title.text.strip()):
                    continue
                newpage = ET.Element('page')
                newpage.append(title)
                newpage.append(child.find("revision").find("text"))
                ET.ElementTree(newpage).write(outfile, encoding = "unicode")

def get_md5(filepath, blocksize = 2**20):
    import hashlib
    checksum = hashlib.md5()
    with open(filepath, "rb") as file:
        while True:
            buf = file.read(blocksize)
            if not buf:
                break
            checksum.update(buf)
    return checksum.hexdigest()

def download_with_progress(url, output_path):
    r = requests.get(url, stream=True)
    total_size_in_bytes = int(r.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
    with open(output_path, "wb") as file:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

parser = argparse.ArgumentParser()
parser.add_argument("date", nargs="?", default="latest", help="date of dump to extract (default 'latest'). format should be YYYYMMDD")
parser.add_argument("-d", "--download", help="download dump before processing. note: dump download is > 1gb", action=argparse.BooleanOptionalAction)
parser.add_argument("-f", "--force", help="force overwriting local download", action=argparse.BooleanOptionalAction)

if __name__ == "__main__":
    args = parser.parse_args()
    index_txt_filename = f"enwiktionary-{args.date}-pages-articles-multistream-index.txt.bz2"
    xml_filename = f"enwiktionary-{args.date}-pages-articles-multistream.xml.bz2"
    if args.download:
        import requests
        url_base = f"https://dumps.wikimedia.org/enwiktionary/{args.date}/"
        download_xml = False
        download_index_txt = False
        if args.force:
            download_xml = True
            download_index_txt = True
        else:
            md5_url = url_base + "md5sums.txt"
            r = requests.get(url_base + f"enwiktionary-{args.date}-md5sums.txt")
            for line in r.text.split("\n"):
                try:
                    checksum, filename = line.split("  ", 1)
                except ValueError:
                    continue
                if filename.strip().endswith("-pages-articles-multistream.xml.bz2"):
                    xml_checksum = checksum
                elif filename.strip().endswith("-pages-articles-multistream-index.txt.bz2"):
                    index_txt_checksum = checksum
            try:
                if get_md5(index_txt_filename) != index_txt_checksum:
                    print("Index file does not match checksum")
                    download_index_txt = True
            except FileNotFoundError:
                print("Index file not found")
                download_index_txt = True
            try:
                if get_md5(xml_filename) != xml_checksum:
                    print("XML dump file does not match checksum")
                    download_xml = True
            except FileNotFoundError:
                print("XML dump file not found")
                download_xml = True
        if download_index_txt:
            print(f"Downloading {args.date} index file...")
            download_with_progress(url_base + index_txt_filename, index_txt_filename)
        else:
            print("Local index file passes checksum. Using local file...")
        if download_xml:
            print(f"Downloading {args.date} XML dump file...")
            download_with_progress(url_base + xml_filename, xml_filename)
        else:
            print("Local xml dump file passes checksum. Using local file...")

    if exists(index_txt_filename) and exists(xml_filename):
        print("Constructing lemma map...")
        lemmas = get_lemma_map()
        lemma_predicate = lambda x: x in lemmas or (x.endswith("/derived terms") and x.split("/")[0] in lemmas)
        dial_predicate = lambda x: x.startswith("Module:zh/data/dial-syn/")


        modules = open("modules.xml", "w")
        modules.write("<modules>")
        print("Extracting module data...")
        write_xml(index_txt_filename, xml_filename, modules, dial_predicate)
        modules.write("</modules>")

        articles = open("articles.xml", "w")
        articles.write("<pages>")
        print("Extracting article data...")
        write_xml(index_txt_filename, xml_filename, articles, lemma_predicate)
        articles.write("</pages>")
    else:
        if not exists(index_txt_filename):
            print("Index file not present")
        if not exists(xml_filename):
            print("XML dump file not present")
        print("Download with '--download' option")
        exit(1)
