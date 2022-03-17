import bz2
import csv
from tqdm import tqdm
import xml.etree.ElementTree as ET
import sys

MW_HEADER = """<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="en">"""
MW_FOOTER = """</mediawiki>"""
def get_lemma_map():
    lemmas = set()
    with open("../sql-lemma-fetcher/enwikt_chinese_lemmas.csv", "r") as csvfile:
        for line in tqdm(csvfile.readlines()):
            lemmas.add(line.strip())
    return lemmas

# def partial_extract():
#     with open("enwiktionary-20220220-pages-articles-multistream.xml.bz2", "rb") as fin:
#         fin.seek(1118871045)
#         data = fin.read()

#         print(bz2.decompress(data))

# partial_extract()
# sys.exit(1)

def get_offsets(predicate):
    curroffset = 0
    split = ""
    mustyield = False
    with open("enwiktionary-20220220-pages-articles-multistream-index.txt", "r") as file:
        for line in tqdm(file.readlines()):
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

    # if mustyield:
    #     yield [curroffset, None]

def write_xml(outfile, predicate):
    print("\tCalculating offsets:")
    offsets = list(get_offsets(predicate))
    print("\tExtracting data:")
    with open("enwiktionary-20220220-pages-articles-multistream.xml.bz2", "rb") as bigfile:
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

print("Constructing lemma map...")
lemmas = get_lemma_map()
lemma_predicate = lambda x: x in lemmas or (x.endswith("/derived terms") and x.split("/")[0] in lemmas)
dial_predicate = lambda x: x.startswith("Module:zh/data/dial-syn/")


# print("Extracting module offsets...")
# offsets = list(get_offsets(dial_predicate))
# print(len(offsets))
modules = open("modules.xml", "w")
modules.write("<modules>")
print("Extracting module data...")
write_xml(modules, dial_predicate)
modules.write("</modules>")

articles = open("articles.xml", "w")
articles.write("<pages>")
print("Extracting article data...")
write_xml(articles, lemma_predicate)
articles.write("</pages>")