"""
icon 적재하는 python 스크립트

ref : 바코드는 workbench에서 직접 import 요망
https://pbj0812.tistory.com/301

"""

import mysql.connector
from mysql.connector import Error

import os

# pip install mysql-connector-python


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def insertBLOB(number, category, re_category, photo, db='contents'):
    print("Inserting BLOB into images table")
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             database=db,
                                             user='ndjango',
                                             password='1234')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO refrigerators_icon
                          (icon_id, category, re_category, icon_img) VALUES (%s,%s,%s,%s)"""

        Picture = convertToBinaryData(photo)

        # Convert data into tuple format
        insert_blob_tuple = (number, category, re_category, Picture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into images table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


CATEGORY_CHOICES = (
    ('processed_meat', '가공육류'),
    ('grain', '곡류'),
    ('fruit', '과일류'),
    ('snack', '과자'),
    ('oil', '기름류'),
    ('other_processed', '기타가공품'),
    ('extract', '기타추출물'),
    ('agricultural', '농산가공품'),
    ('glucose', '당류'),
    ('bean_processed', '두류가공품'),
    ('ricecake', '떡류'),
    ('noodle', '면류'),
    ('sugar_salt', '설탕소금류'),
    ('processed_marine', '수산물가공품'),
    ('seasoning', '양념'),
    ('milk', '우유'),
    ('dairy', '유제품'),
    ('meat', '육류'),
    ('drink', '음료류'),
    ('ginseng_yeast', '인삼효모류'),
    ('powder', '전분류'),
    ('pickle', '절임식품'),
    ('jelly', '젤리류'),
    ('braised', '조림류'),
    ('alcohol', '주류'),
    ('vegetable', '채소류'),
    ('chocolate', '초콜릿가공품'),
    ('spice', '향신료'),
)


if __name__ == '__main__':

    # tuple to dict
    category_dict = dict()
    for tpl in CATEGORY_CHOICES:
        category_dict[tpl[1]] = tpl[0]

    # insert icon into Icon table
    os.chdir('./../db_initializer/icon_img')

    cat_list = os.listdir()
    for idx, item in enumerate(cat_list):
        record = item.replace('.png', '')
        print(idx+1, record, item)

        # number, category, re_category, photo

        insertBLOB(idx+1, category_dict[record], record, item)
        # insertBLOB(idx+1, category_dict[record], record, item, db='contents6')


