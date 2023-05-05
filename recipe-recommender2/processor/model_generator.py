import pandas as pd
# import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt
import ast

def tokenize(train_data):
    # 형태소 분석기 OKT를 사용한 토큰화 작업 (다소 시간 소요)
    okt = Okt()

    tokenized_data = []
    for sentence in train_data['parsed']:
        tokenized_sentence = okt.morphs(sentence, stem=True)  # 토큰화
        # tokenized_sentence = sentence
        sentence = [word for word in tokenized_sentence]
        tokenized_data.append(sentence)

    return tokenized_data


def to_list(x):
    if isinstance(x, list):
        x_list = x
    else:
        x_list = ast.literal_eval(x)

    return x_list


def generate_model():
    # load in data
    train_data = pd.read_csv("./../data/raw/0_2000_parsed.csv", index_col=0, encoding='utf-8')
    train_data = train_data[['parsed']]
    train_data["token_raw"] = train_data["parsed"].apply(lambda x: to_list(x))

    # tokenized_data = tokenize(train_data)
    tokens = list(train_data.loc[:, 'token_raw'])

    model = Word2Vec(sentences=tokens, vector_size=100, window=2, min_count=2, workers=4, sg=0)

    print(model.wv.vectors.shape)

    print(model.wv.most_similar("새송이버섯"))
    print(model.wv.most_similar("새송이버섯"))
    print(model.wv.most_similar(['새송이버섯', '두유', '생크림', '청양고추', '새싹채소']))

    model.save('./../models/model_recipe.bin')
    # model.wv.save_word2vec_format('eng_w2v')  # 모델 저장
    # loaded_model = KeyedVectors.load_word2vec_format("eng_w2v")  # 모델 로드
    model2 = Word2Vec.load('./../models/model_recipe.bin')
    # model2 = Word2Vec.load("./../models/models/model_recipe.bin")


    a = 0



if __name__ == '__main__':

    # generate_model()
    model = Word2Vec.load('./../models/model_recipe.bin')
    model.init_sims(replace=True)

    print(model.wv.most_similar("새송이버섯"))
    print(model.wv.most_similar("새송이버섯"))
    print(model.wv.most_similar(['들깻가루', '레몬', '사과']))


