"""
한글 레시피 DB 구축 스크립트

ref
1. 0_2000_parsed.csv : 한글 레시피 파싱 파일 (for DB Init)
2. kor_recipe.py : 한글 레시피 파싱 파일을 DB에 insert하는 파이썬 스크립트
3. contents_recsys_koreanrecipe.sql: DB에 바로 insert하는 sql 파일
    db insert 방법
    a) workbench에서 use contents; 실행
    b)윗줄은 무시하고,
    -> INSERT INTO `recsys_koreanrecipe` VALUES (1,18,'버섯 두유 소스
    여기부터 맨 마지막줄 까지 선택하고 실행
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import numpy as np


USER = 'ndjango'
HOST = 'localhost'
PASSWD = '1234'
PORT = 3306
DB = 'contents'
TABLE = 'recsys_koreanrecipe'

# pymysql 세팅
db = pymysql.connect(user=USER, host=HOST, passwd=PASSWD, port=PORT, db=DB)
cursor = db.cursor()

# csv파일 불러오기
data_type = {
    'INFO_WGT': float,
    'INFO_ENG': float,
    'INFO_CAR': float,
    'INFO_PRO': float,
    'INFO_FAT': float,
    'INFO_NA': float,
}
df = pd.read_csv('0_2000_parsed.csv', encoding='utf-8',
                 dtype=data_type, index_col=0)
# df.index = np.arange(1, len(df) + 1)
df.reset_index(inplace=False)
# print(df.columns)

df.columns = ['rcp_seq', 'rcp_nm', 'rcp_way2', 'rcp_pat2', 'info_wgt', 'info_eng', 'info_car', 'info_pro', 'info_fat', 'info_na', 'hash_tag', 'att_file_no_main', 'att_file_no_mk', 'rcp_parts_dtls', 'manual01', 'manual_img01', 'manual02', 'manual_img02', 'manual03', 'manual_img03', 'manual04', 'manual_img04', 'manual05', 'manual_img05', 'manual06', 'manual_img06', 'raw', 'parsed']
df = df.replace({np.nan: None})
a = 0


# sqlalchemy를 사용해 원하는 database에 csv파일 저장
engine = create_engine(f"mysql+pymysql://{USER}:"+f"{PASSWD}"+f"@{HOST}:{PORT}/{DB}?charset=utf8")
conn = engine.connect()
dbname = TABLE
df.to_sql(dbname, con=engine, if_exists='append', index=False)
conn.close()

# 저장 확인
sql = f"select * from {TABLE} limit 5"
print(pd.read_sql(sql, db))

