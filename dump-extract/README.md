# Wiktionary dump extracter


Given an up to date `../sql-lemma-fetcher/chinese_lemmas.csv`, `enwiktionary-DATE-pages-articles-multistream-index.txt`, and `enwiktionary-DATE-pages-articles-multistream.xml.bz2` files, this will generate `articles.xml` and `modules.xml` containing just the articles of chinese lemmas, and just the zh-dial-syn data.

The chinese_lemmas.csv file is checked in but the other two need to be downloaded from [here](https://dumps.wikimedia.org/enwiktionary/latest/). The filenames are hardcoded but should probably be updated to be passed in via argparse.