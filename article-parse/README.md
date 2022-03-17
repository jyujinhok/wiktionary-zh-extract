# article-parse

This takes in an articles.xml file (copied in from `../dump-extract`) and generates `articledata.json`, a JSON file with relevant article data.

The json file will contain a map of dictionary entries, with each entry containing a map of etymology numbers (0 if there is no number) to the etymology entry, with "dial" and "pron" fields containing any dialectical map templates found and pronunciation data. This does _not_ handle [dial-pron](https://en.wiktionary.org/wiki/Module:zh/data/dial-pron) data, only the pronunciations given in the `zh-pron` template.