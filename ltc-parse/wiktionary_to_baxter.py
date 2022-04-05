import re

INIT_TYPE = {
    "幫": 1, "帮": 1, "非": 1, "滂": 2, "敷": 2,
    "並": 3, "并": 3, "奉": 3, "明": 4, "微": 4,
    "端": 5, "透": 6, "定": 7, "泥": 8, "知": 9,
    "徹": 10, "澄": 11, "孃": 12, "娘": 12, "精": 13,
    "清": 14, "從": 15, "从": 15, "心": 16, "邪": 17,
    "莊": 18, "庄": 18, "初": 19, "崇": 20, "生": 21,
    "俟": 22, "章": 23, "昌": 24, "常": 25, "禪": 25,
    "禅": 25, "書": 26, "书": 26, "船": 27, "見": 28,
    "见": 28, "溪": 29, "谿": 29, "羣": 30, "群": 30,
    "疑": 31, "曉": 32, "晓": 32, "匣": 33, "影": 34,
    "于": 35, "云": 35, "雲": 35, "以": 36, "來": 37,
    "来": 37, "日": 38
}

FIN_CONV = {
    "冬": "沃", "東": "屋", "江": "覺", "鍾": "燭", "眞": "質",
    "臻": "櫛", "諄": "術", "痕": "麧", "魂": "沒", "欣": "迄",
    "文": "物", "寒": "曷", "桓": "末", "元": "月", "刪": "黠",
    "山": "鎋", "仙": "薛", "先": "屑", "唐": "鐸", "陽": "藥",
    "庚": "陌", "耕": "麥", "清": "昔", "青": "錫", "登": "德",
    "蒸": "職", "侵": "緝", "談": "盍", "嚴": "業", "凡": "乏",
    "銜": "狎", "咸": "洽", "鹽": "葉", "添": "怗", "覃": "合"
}

FIN_TYPE = {
    "冬": 5, "沃": 6, "鍾": 7, "燭": 8, "江": 9,
    "覺": 10, "之": 19, "魚": 22, "模": 23, "虞": 24,
    "咍": 41, "灰": 42, "臻": 46, "諄": 47, "櫛": 51,
    "術": 52, "痕": 53, "麧": 54, "魂": 55, "沒": 56,
    "欣": 57, "迄": 58, "文": 59, "物": 60, "寒": 61,
    "桓": 62, "曷": 63, "末": 64, "豪": 89, "肴": 90,
    "蕭": 93, "歌": 94, "蒸": 133, "尤": 136, "侯": 137,
    "幽": 138, "談": 143, "盍": 144, "嚴": 145, "凡": 146,
    "業": 147, "乏": 148, "銜": 149, "狎": 150, "咸": 151,
    "洽": 152, "添": 157, "怗": 158, "帖": 158, "覃": 159,
    "合": 160
}

FIN_TYPE_OPEN = {
    "微開": 20, "微合": 21, "泰開": 25, "泰合": 26, "廢開": 27, "廢合": 28,
    "夬開": 29, "夬合": 30, "佳開": 31, "佳合": 32, "皆開": 33, "皆合": 34,
    "齊開": 39, "齊合": 40, "元開": 65, "元合": 66, "月開": 67, "月合": 68,
    "刪開": 69, "刪合": 70, "黠開": 71, "黠合": 72, "山開": 73, "山合": 74,
    "鎋開": 75, "鎋合": 76, "先開": 85, "先合": 86, "屑開": 87, "屑合": 88,
    "唐開": 101, "唐合": 102, "鐸開": 103, "鐸合": 104, "陽開": 105, "陽合": 106,
    "藥開": 107, "藥合": 108, "耕開": 117, "耕合": 118, "麥開": 119, "麥合": 120,
    "清開": 121, "清合": 122, "昔開": 123, "昔合": 124, "青開": 125, "青合": 126,
    "錫開": 127, "錫合": 128, "登開": 129, "登合": 130, "德開": 131, "德合": 132,
    "職開": 134, "職合": 135
}

FIN_TYPE_DENG_OPEN = {
    "支三開": 11, "支三合": 12, "支重鈕三開": 13, "支重鈕三合": 14,
    "脂三開": 15, "脂三合": 16, "脂重鈕四開": 15, "脂重鈕四合": 16,
    "脂重鈕三開": 17, "脂重鈕三合": 18,
    "祭三開": 35, "祭三合": 36, "祭重鈕四開": 35, "祭重鈕四合": 36, 
    "祭重鈕三開": 37, "祭重鈕三合": 38,
    "戈一合": 95, "戈三開": 96, "戈三合": 97,
    "仙三開": 77, "仙三合": 78, "仙重鈕三開": 79, "仙重鈕三合": 80,
    "薛三開": 81, "薛三合": 82, "薛重鈕三開": 83, "薛重鈕三合": 84,
    "麻二開": 98, "麻二合": 99, "麻三開": 100,
    "陌二開": 113, "陌二合": 114, "陌三開": 115, "陌三合": 116,
    "庚二開": 109, "庚二合": 110, "庚三開": 111, "庚三合": 112, 
    "庚重鈕三開": 111, "庚重鈕三合": 112
}

FINAL_DENG = {
    "東一": 1, "東三": 2, "屋一": 3, "屋三": 4,
    "宵三": 91, "宵重鈕四": 91, "宵重鈕三": 92,
    "侵三": 139, "侵重鈕三": 140, "緝三": 141, "緝重鈕三": 142,
    "葉三": 155, "葉重鈕三": 156, "鹽三": 153, "鹽重鈕三": 154,
    "真三": 43, "真重鈕四": 43,
    "眞三": 43, "眞重鈕四": 43,
    "質三": 48, "質重鈕四": 48
}

TONE_SYMBOL = {
    "平": "",
    "上": "X",
    "去": "H",
    "入": ""
}

FINAL_OPENNESS = {
    "真開": 44, "真合": 45,
    "眞開": 44, "眞合": 45,
    "質開": 49, "質合": 50
}

FINAL_TYPE_1 = set("微泰廢夬佳皆齊元月刪黠山鎋先屑唐鐸陽藥耕麥清昔青錫登德職")
FINAL_TYPE_2 = set("東屋宵侵緝葉鹽")
FINAL_TYPE_3 = set("支脂祭戈仙薛麻陌庚")
FINAL_TYPE_4 = set("真眞質")
FINAL_TYPE_5 = set("冬沃鍾燭江覺之魚模虞咍灰臻諄櫛術痕麧魂沒欣迄文物寒桓曷末豪肴蕭歌蒸尤侯幽談盍嚴凡業乏銜狎咸洽添怗帖覃合")

BAXTER_INITIAL = ["",
    "p", "ph", "b", "m",                # 1 2 3 4
    "t", "th", "d", "n",                # 5 6 7 8
    "tr", "trh", "dr", "nr",            # 9 10 11 12
    "ts", "tsh", "dz", "s", "z",        # 13 14 15 16 17
    "tsr", "tsrh", "dzr", "sr", "zr",   # 18 19 20 21 22
    "tsy", "tsyh", "dzy", "sy", "zy",   # 23 24 25 26 27
    "k", "kh", "g", "ng", "x", "h",     # 28 29 30 31 32 33
    "ʔ", "h", "y", "l", "ny"            # 34 35 36 37 38
]

BAXTER_FINAL = ["",
    "uwng", "juwng", "uwk", "juwk",                 # 1 2 3 4
    "owng", "owk", "jowng", "jowk",                 # 5 6 7 8
    "æwng", "æwk",                                  # 9 10
    "jie", "jwie", "je", "jwe",                     # 11 12 13 14
    "jij", "jwij", "ij", "wij",                     # 15 16 17 18
    "i", "jɨj", "jwɨj",                             # 19 20 21
    "jo", "u", "ju",                                # 22 23 24
    "aj", "waj", "joj", "jwoj",                     # 25 26 27 28
    "æj", "wæj", "ɛɨ", "wɛɨ", "ɛj", "wɛj",          # 29 30 31 32 33 34
    "jiej", "jwiej", "jej", "jwej",                 # 35 36 37 38
    "ej", "wej", "oj", "woj",                       # 39 40 41 42
    "jin", "in", "win", "in", "jwin",               # 43 44 45 46 47
    "jit", "it", "wit", "it", "jwit",               # 48 49 50 51 52
    "on", "ot", "won", "wot",                       # 53 54 55 56
    "jɨn", "jɨt", "jun", "jut",                     # 57 58 59 60
    "an", "wan", "at", "wat",                       # 61 62 63 64
    "jon", "jwon", "jot", "jwot",                   # 65 66 67 68
    "æn", "wæn", "æt", "wæt",                       # 69 70 71 72
    "ɛn", "wɛn", "ɛt", "wɛt",                       # 73 74 75 76
    "jien", "jwien", "jen", "jwen",                 # 77 78 79 80
    "jiet", "jwiet", "jet", "jwet",                 # 81 82 83 84
    "en", "wen", "et", "wet",                       # 85 86 87 88
    "aw", "æw", "jiew", "jew", "ew",                # 89 90 91 92 93
    "a", "wa", "ja", "jwa", "æ", "wæ", "jæ",        # 94 95 96 97 98 99 100
    "ang", "wang", "ak", "wak",                     # 101 102 103 104
    "jang", "jwang", "jak", "jwak",                 # 105 106 107 108
    "æng", "wæng", "jæng", "jwæng",                 # 109 110 111 112
    "æk", "wæk", "jæk", "jwæk",                     # 113 114 115 116
    "ɛng", "wɛng", "ɛk", "wɛk",                     # 117 118 119 120
    "jieng", "jwieng", "jiek", "jwiek",             # 121 122 123 124
    "eng", "weng", "ek", "wek",                     # 125 126 127 128
    "ong", "wong", "ok", "wok",                     # 129 130 131 132
    "ing", "ik", "wik",                             # 133 134 135
    "juw", "uw", "jiw",                             # 136 137 138
    "jim", "im", "jip", "ip",                       # 139 140 141 142
    "am", "ap", "jæm", "jom", "jæp", "jop",         # 143 144 145 146 147 148
    "æm", "æp", "ɛm", "ɛp",                         # 149 150 151 152
    "jiem", "jem", "jiep", "jep",                   # 153 154 155 156
    "em", "ep", "om", "op",                         # 157 158 159 160
]

def infer_categories(text):
    try:
        initial, final, deng, openness, _, tone, *_ = text
    except ValueError:
        raise ValueError(f"Malformed entry string: {text}")
    if "-" in text:
        deng = text.split("-")[1] + deng
    if tone == "入":
        try:
            final = FIN_CONV[final]
        except KeyError:
            pass
    try:
        initial_type = INIT_TYPE[initial]
    except KeyError:
        raise ValueError(f"Malformed entry string: {text}")
    try:
        tone_label = TONE_SYMBOL[tone]
    except KeyError:
        raise ValueError(f"Malformed entry string: {text}")
    if final in FINAL_TYPE_1:
        final_type = FIN_TYPE_OPEN[final + openness]
    elif final in FINAL_TYPE_2:
        final_type = FINAL_DENG[final + deng]
    elif final in FINAL_TYPE_3:
        final_type = FIN_TYPE_DENG_OPEN[final + deng + openness]
    elif final in FINAL_TYPE_4:
        if deng == "重鈕三":
            final_type = FINAL_OPENNESS[final + openness]
        else:
            final_type = FINAL_DENG[final + deng]
    elif final in FINAL_TYPE_5:
        final_type = FIN_TYPE[final]
    else:
        raise ValueError("Final not recognized.")

    return initial_type, final_type, tone_label

REMOVE_CHONGNIU = {
    "jiej": "jej",
    "jwiej": "jwej",
    "jie": "je", 
    "jwie": "jwe", 
    "jij": "ij", 
    "jwij": "wij", 
    "jiew": "jew", 
    "jin": "in", 
    "jit": "it", 
    "jwin": "win",
    "jwit": "wit",
    "jien": "jen",
    "jiet": "jet",
    "jwien": "jwen",
    "jwiet": "jwet",
    "jieng": "jeng",
    "jiek": "jek",
    "jwieng": "jweng",
    "jwiek": "jwek",
    "jim": "im",
    "jip": "ip",
    "jiem": "jem",
    "jiep": "jep",
}

REMOVE_LABIAL_ROUNDING = {
    "wan": "an",
    "wat": "at",
    "wang": "ang",
    "wak": "ak",
    "wa": "a",
    "woj": "oj",
    "jwang": "jang",
    "jwak": "jak",
    "jwoj": "joj",
    "jwon": "jon",
    "jwot": "jot",
    "jwɨj": "jɨj",
}

def wiktionary_to_baxter(text):
    initial_type, final_type, tone_label = infer_categories(text)
    initial = BAXTER_INITIAL[initial_type]
    final = BAXTER_FINAL[final_type]
    if initial not in {"p", "ph", "b", "m", "k", "kh", "g", "ng", "ʔ", "x", "h"}:
        try:
            final = REMOVE_CHONGNIU[final]
        except KeyError:
            pass
    if initial in {"p", "ph", "b", "m"}:
        try:
            final = REMOVE_LABIAL_ROUNDING[final]
        except KeyError:
            pass
    if "y" in initial and final.startswith("j"):
        final = final[1:]
    return initial + final + tone_label
