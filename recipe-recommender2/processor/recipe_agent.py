import json
import pandas as pd


def json_to_csv(path):
    with open(path, encoding='utf-8') as f:
        re = f.read()
        contents = json.loads(re)

        recipes = contents['COOKRCP01']['row']
        # a = len(app)

    df = pd.DataFrame(recipes)
    seq = ['RCP_SEQ', 'RCP_NM', 'RCP_WAY2', 'RCP_PAT2', 'INFO_WGT', 'INFO_ENG', 'INFO_CAR',
           'INFO_PRO', 'INFO_FAT', 'INFO_NA', 'HASH_TAG', 'ATT_FILE_NO_MAIN', 'ATT_FILE_NO_MK',
           'RCP_PARTS_DTLS', 'MANUAL01', 'MANUAL_IMG01', 'MANUAL02', 'MANUAL_IMG02',
           'MANUAL03', 'MANUAL_IMG03', 'MANUAL04', 'MANUAL_IMG04', 'MANUAL05', 'MANUAL_IMG05',
           'MANUAL06', 'MANUAL_IMG06'
           ]

    # seq = ['RCP_SEQ', 'RCP_NM', 'RCP_WAY2', 'RCP_PAT2', 'INFO_WGT', 'INFO_ENG', 'INFO_CAR',
    #        'INFO_PRO', 'INFO_FAT', 'INFO_NA', 'HASH_TAG', 'ATT_FILE_NO_MAIN', 'ATT_FILE_NO_MK',
    #        'RCP_PARTS_DTLS', 'MANUAL01', 'MANUAL_IMG01', 'MANUAL02', 'MANUAL_IMG02',
    #        'MANUAL03', 'MANUAL_IMG03', 'MANUAL04', 'MANUAL_IMG04', 'MANUAL05', 'MANUAL_IMG05',
    #        'MANUAL06', 'MANUAL_IMG06', 'MANUAL07', 'MANUAL_IMG07', 'MANUAL08', 'MANUAL_IMG08',
    #        'MANUAL09', 'MANUAL_IMG09', 'MANUAL10', 'MANUAL_IMG10', 'MANUAL11', 'MANUAL_IMG11',
    #        'MANUAL12', 'MANUAL_IMG12', 'MANUAL13', 'MANUAL_IMG13', 'MANUAL14', 'MANUAL_IMG14',
    #        'MANUAL15', 'MANUAL_IMG15', 'MANUAL16', 'MANUAL_IMG16', 'MANUAL17', 'MANUAL_IMG17',
    #        'MANUAL18', 'MANUAL_IMG18', 'MANUAL19', 'MANUAL_IMG19', 'MANUAL20', 'MANUAL_IMG20'
    #        ]

    df = df[seq]

    df["RCP_SEQ"] = df['RCP_SEQ'].astype('int')
    # print(df.dtypes)
    df = df.sort_values(by='RCP_SEQ')
    df = df.reset_index(drop=True)
    df.to_csv('./../data/raw/0_2000.csv')


if __name__ == '__main__':
    json_to_csv('./../data/raw/0_2000.json')






