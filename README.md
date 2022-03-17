# wiktionary-zh-extract

tools for extracting data from Wiktionary


The general pipeline is to start with the `dump-extract` folder to generate articles.xml and modules.xml from Wiktionary dump data. Then use article-parse and dial-syn-parse to generate cleaner JSON files of this data.