# wiktionary-zh-extract

tools for extracting data from Wiktionary



If you just need the files this generates, consider going through the GitHub releases and downloading the latest one.

The general pipeline is to start with the `dump-extract` folder to generate articles.xml and modules.xml from Wiktionary dump data. Then use article-parse and dial-syn-parse to generate cleaner JSON files of this data (articledata.json and dial.json).

