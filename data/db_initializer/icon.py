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

def insertBLOB(number, name, photo, db='contents'):
    print("Inserting BLOB into images table")
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             database=db,
                                             user='ndjango',
                                             password='1234')

        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO refrigerators_icon
                          (icon_id, re_category, icon_img) VALUES (%s,%s,%s)"""

        Picture = convertToBinaryData(photo)

        # Convert data into tuple format
        insert_blob_tuple = (number, name, Picture)
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



if __name__ == '__main__':

    os.chdir('./../db_initializer/icon_img')

    cat_list = os.listdir()
    for idx, item in enumerate(cat_list):
        record = item.replace('.png', '')
        print(idx+1, record, item)
        insertBLOB(idx+1, record, item)
        # insertBLOB(idx+1, record, item, db='ndjango_master')

        b = 0

    a = 0


# insertBLOB(25, "육류", "육류.png")