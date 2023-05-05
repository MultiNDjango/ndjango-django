import pandas as pd
import string
import ast
import re
import unidecode
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter

import re


def has_number(val):
    re_numbers = re.compile(r"\d")
    return True if re_numbers.search(val) else False


def raw_ingredients(val: str) -> list:
    val = val.replace("\"", "")
    # val = val.replace("[소스소개]", "\n")
    val = re.sub("\\[소스소개\\]+[ ]?", ", ", val)

    # 1. 소제목 \n 재료 -> 재료만 남기기
    lines = val.split('\n')
    raw_list = [x for x in lines if has_number(x)]

    # 2. •필수 재료 :, ○ 필수재료 :, ●방울토마토 소박이 :, ●떡꼬치: , - 주재료:,  주재료 : 등
    # (반죽재료), (속재료), [ 2인분 ], 재료
    # .. -> regex로 제거


    re_base = re.compile(r"●[ㄱ-ㅣ가-힣\s]+ : ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in raw_list]

    re_base = re.compile(r"●[ㄱ-ㅣ가-힣\s]+:")
    rebase_raw_list = [re.sub(re_base, '', item) for item in raw_list]

    re_base = re.compile(r"•[ㄱ-ㅣ가-힣\s]+ : ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"- [ㄱ-ㅣ가-힣\s]+ : ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣\s]+ : ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"\([ㄱ-ㅣ가-힣\s]+\)+[ ]?")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"\[[ㄱ-ㅣ가-힣0-9\s]+\] ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"\[[ㄱ-ㅣ가-힣0-9\s]+\]")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]?재료 ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]?반죽 ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]+양념+[: ]?")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]?양념 ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]?육수 ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]?밑간 ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]?드레싱 ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]+드레싱+[: ]?")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]+소스+[: ]?")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]?소스+[: ]?")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]+장:")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣0-9\s]?무침 ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"[ㄱ-ㅣ가-힣\s]+:")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]

    re_base = re.compile(r"단촛물 ")
    rebase_raw_list = [re.sub(re_base, '', item) for item in rebase_raw_list]




    # 3. raw ingredients list 만들기
    raw_str = ', '.join(rebase_raw_list)
    raw_str = raw_str.strip()
    # raw_str = raw_str.replace("\\", "").replace("\'","")
    raw_list = raw_str.split(',')
    raw_list = [x.lstrip() for x in raw_list]

    return raw_list


def ingredient_parser(ingreds):
    measures = ['조금', '약간', '한 줌', '적당량', '갠것', '믹서에', '갈아줌']
    condiments = ['후추', '후춧가루', '소금', '설탕', '식용유', '올리브유', '쌀뜨물', '물']
    to_remove = ['저염재래된장', '주먹밥', '두부강된장', '홍초물', '채', '어슷', '얇게', '송송', '잘게', '썬', '다진']
    adjectives = ['저염', '삶은', '갈은', '다진것', '불린', '채썬것', '토막', '낸', '어슷',
                  '무게', '얼린', '으깬', '무가당', '손질된', '적당량', '굵은', '면발', '고기(', '다시마국물(',
                  '물(', '콩(', '데친', '부순', '김치주머니', '마른', '(x'
                  ]
    ingred_list = []

    if isinstance(ingreds, list):
        ingredients = ingreds
    else:
        ingredients = ast.literal_eval(ingreds)

    # lemmatizer = WordNetLemmatizer()
    # 한글 추출
    re_base = re.compile(r"[ㄱ-ㅣ가-힣\s]")

    for i in ingredients:
        items_raw = re.split(" |-", i)

        # 1. 한글만 추출 (ex: (100g) 등 제거)
        items1 = [word for word in items_raw if re_base.match(word)]
        items1 = [re.sub(r'\([^)]*\)', '', item) for item in items1]
        items1 = [re.sub(r'([0-9])\w+', '', item) for item in items1]
        items1 = [re.sub(r'([0-9])', '', item) for item in items1]
        items1 = [re.sub(r'([0-9].[0-9])', '', item) for item in items1]
        items1 = [re.sub(r'\(×', '', item) for item in items1]
        # items1 = [re.sub(r'[가-힣]+ +썬 ', '', item) for item in items1]

        # 2. 형용사 제거 (ex: 저염)
        items2 = []
        for item in items1:
            tmp = item
            for to_del in adjectives:
                tmp = tmp.replace(to_del, "")

            items2.append(tmp)

        if len(items2) == 0:
            continue

        # 3. 불필요 단어 제거
        items3 = [word for word in items2 if word not in measures]
        items4 = [word for word in items3 if word not in condiments]
        items5 = [word for word in items4 if word not in to_remove]

        if len(items5) == 0:
            continue

        # 4. 연결
        items6 = [itm for itm in items5 if len(itm) > 0]
        ingred_list.append(" ".join(items6))

    ingred_list = list(filter(len, ingred_list))
    return ingred_list


if __name__ == '__main__':

    # recipe_df = pd.read_csv('./../data/raw/0_2000.csv', index_col=0, encoding='utf-8')
    # recipe_df.dropna(subset=['RCP_PARTS_DTLS'], inplace=True)
    # recipe_df = recipe_df[recipe_df.RCP_PARTS_DTLS != '.']
    #
    # # b = recipe_df.iloc[678]['RCP_PARTS_DTLS']
    # # c = raw_ingredients(b)
    # #
    # # b = recipe_df['RCP_PARTS_DTLS']
    #
    # recipe_df['RAW'] = recipe_df['RCP_PARTS_DTLS'].apply(lambda x: raw_ingredients(x))
    # recipe_df = recipe_df.reset_index(drop=True)
    #
    # recipe_df.to_csv('./../data/raw/0_2000_raw.csv')

    raw_df = pd.read_csv('./../data/raw/0_2000_raw.csv', index_col=0, encoding='utf-8')
    # b = raw_df.iloc[1098]['RAW']
    # ingredient_parser(b)

    raw_df["parsed"] = raw_df["RAW"].apply(lambda x: ingredient_parser(x))

    raw_df.to_csv('./../data/raw/0_2000_parsed.csv')


    a = 0
