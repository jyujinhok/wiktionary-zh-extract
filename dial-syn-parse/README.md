# dial-syn-parse

This takes in a modules.xml file (copied in from `../dump-extract`) and generates `dial.json`, a JSON file with relevant dialectical map data.

The json file will contain a map of dictionary entries that are _headwords_ for dialectical synonym data, with each entry containing a map of locations to a list of synonyms.