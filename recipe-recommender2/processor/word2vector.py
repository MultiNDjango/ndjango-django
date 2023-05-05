import ast
import numpy as np
import pandas as pd

# from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

import gensim

from processor.ingredient_parser import ingredient_parser
from konlpy.tag import Okt


class MeanEmbeddingVectorizer(object):
    def __init__(self, word_model):
        self.word_model = word_model
        self.vector_size = word_model.wv.vector_size

    def fit(self):  # comply with scikit-learn transformer requirement
        return self

    def transform(self, docs):  # comply with scikit-learn transformer requirement
        doc_word_vector = self.word_average_list(docs)
        return doc_word_vector

    def word_average(self, sent):
        """
        Compute average word vector for a single doc/sentence.
        :param sent: list of sentence tokens
        :return: mean: float of averaging word vectors
        """

        mean = []
        for word in sent:
            if word in self.word_model.wv.index_to_key:
                mean.append(self.word_model.wv.get_vector(word))

        if not mean:  # empty words
            # If a text is empty, return a vector of zeros.
            # logging.warning(
            #     "cannot compute average owing to no vector for {}".format(sent)
            # )
            return np.zeros(self.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean

    def word_average_list(self, docs):
        """
        Compute average word vector for multiple docs, where docs had been tokenized.
        :param docs: list of sentence in list of separated tokens
        :return: array of average word vector in shape (len(docs),)
        """

        return np.vstack([self.word_average(sent) for sent in docs])


class TfidfEmbeddingVectorizer(object):
    def __init__(self, word_model):

        self.word_model = word_model
        self.word_idf_weight = None
        self.vector_size = word_model.wv.vector_size

    def fit(self, docs):  # comply with scikit-learn transformer requirement
        """
        Fit in a list of docs, which had been preprocessed and tokenized,
        such as word bi-grammed, stop-words removed, lemmatized, part of speech filtered.
        Then build up a tfidf model to compute each word's idf as its weight.
        Noted that tf weight is already involved when constructing average word vectors, and thus omitted.
        :param docs: pre_processed_docs: list of docs, which are tokenized
        :return: self
        """

        text_docs = []
        for doc in docs:
            text_docs.append(" ".join(doc))

        tfidf = TfidfVectorizer()
        tfidf.fit(text_docs)  # must be list of text string

        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)  # used as default value for defaultdict
        self.word_idf_weight = defaultdict(
            lambda: max_idf,
            [(word, tfidf.idf_[i]) for word, i in tfidf.vocabulary_.items()],
        )
        return self

    def transform(self, docs):  # comply with scikit-learn transformer requirement
        doc_word_vector = self.word_average_list(docs)
        return doc_word_vector

    def word_average(self, sent):
        """
        Compute average word vector for a single doc/sentence.
        :param sent: list of sentence tokens
        :return: mean: float of averaging word vectors
        """

        mean = []
        for word in sent:
            if word in self.word_model.wv.index_to_key:
                mean.append(
                    self.word_model.wv.get_vector(word) * self.word_idf_weight[word]
                )  # idf weighted

        if not mean:  # empty words
            # If a text is empty, return a vector of zeros.
            # logging.warning(
            #     "cannot compute average owing to no vector for {}".format(sent)
            # )
            return np.zeros(self.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean

    def word_average_list(self, docs):
        """
        Compute average word vector for multiple docs, where docs had been tokenized.
        :param docs: list of sentence in list of separated tokens
        :return: array of average word vector in shape (len(docs),)
        """

        return np.vstack([self.word_average(sent) for sent in docs])


class RecipeRecommender:
    def __init__(self, model_path='./../models/model_recipe.bin', rcp_path="./../data/raw/0_2000_parsed.csv"):

        model = gensim.models.Word2Vec.load(model_path)
        model.init_sims(replace=True)
        if model:
            print("Successfully loaded model")

        # load in data
        self.df_recipes = pd.read_csv(rcp_path)

        # create corpus
        corpus = self.get_and_sort_corpus(self.df_recipes)

        # use TF-IDF as weights for each word embedding
        self.tfidf_vec_tr = TfidfEmbeddingVectorizer(model)
        self.tfidf_vec_tr.fit(corpus)
        self.doc_vec = self.tfidf_vec_tr.transform(corpus)
        self.doc_vec = [doc.reshape(1, -1) for doc in self.doc_vec]
        assert len(self.doc_vec) == len(corpus)


    def get_and_sort_corpus(self, data):
        """
        Get corpus with the documents sorted in korean alphabetical order
        """
        corpus_sorted = []
        for doc in data.parsed.values:
            if isinstance(doc, list):
                ingredients = doc
            else:
                ingredients = ast.literal_eval(doc)
            ingredients.sort()
            corpus_sorted.append(ingredients)
        return corpus_sorted

    def get_recommendations(self, N, scores, allergies: list = []):
        """
        Top-N recomendations order by score
        """
        # order the scores with and filter to get the highest N scores
        # top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
        descending = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        # create dataframe to load in recommendations
        recommendation = pd.DataFrame(columns=["recipe", "score"])
        count = 0
        for i in descending:
            if isinstance(self.df_recipes["parsed"][i], list):
                ingredients = self.df_recipes["parsed"][i]
            else:
                ingredients = ast.literal_eval(self.df_recipes["parsed"][i])

            intersection = list(set(allergies).intersection(ingredients))
            if len(intersection) >= 1:
                continue

            recommendation.at[count, "recipe"] = self.df_recipes["RCP_NM"][i]
            recommendation.at[count, "ingredients"] = self.df_recipes["parsed"][i]
            recommendation.at[count, "score"] = f"{scores[i]}"
            count += 1
            if count >= N:
                break

        return recommendation

    def recommend(self, ingredients: list, N=5, mean=False):
        # model = gensim.models.Word2Vec.load('./../models/model_cbow.bin')

        # create embedding for input text

        input = ingredient_parser(ingredients)

        # get embeddings for ingredient doc
        input_embedding = self.tfidf_vec_tr.transform([input])[0].reshape(1, -1)

        # get cosine similarity between input embedding and all the document embeddings
        cos_sim = map(lambda x: cosine_similarity(input_embedding, x)[0][0], self.doc_vec)
        scores = list(cos_sim)
        # Filter top N recommendations
        recommendations = self.get_recommendations(N, scores)
        return recommendations

    def recommend_without_allergy(self, ingredients: list, allergies: list, N=5):

        input = ingredient_parser(ingredients)

        # get embeddings for ingredient doc
        input_embedding = self.tfidf_vec_tr.transform([input])[0].reshape(1, -1)

        # get cosine similarity between input embedding and all the document embeddings
        cos_sim = map(lambda x: cosine_similarity(input_embedding, x)[0][0], self.doc_vec)
        scores = list(cos_sim)
        # Filter top N recommendations
        recommendations = self.get_recommendations(N, scores, allergies)

        return recommendations




if __name__ == '__main__':
    input_val = ['달걀', '큐민']

    recipe_recommender = RecipeRecommender()

    app = recipe_recommender.recommend(input_val)

    # input_val = ['새송이버섯', '두유', '생크림', '청양고추', '새싹채소']
    # app = recommend(input_val)
    print(app)


    # input_val = ['감자', '달걀']
    # input_val = ['달걀', '콩나물', '오뎅', '자동차', '된장']
    # input_val = ['고구마', '단호박', '우유']

    okt = Okt()
    # input_val = ['오케이쿡 사천풍 중화볶음밥','키요 단백질 웨하스 카카오','삼립호빵 발효미종 단팥','돈트리 수제소스 고추장돼지불고기','밀크씨슬 간건강 플러스+','라포맨','연근차','오늘 더 가벼움','손질문어','맛있는 카레소스','돈도담한우국거리(설도,앞다리,목심)냉동','곡물식빵믹스','구절초사랑','자연만을 해풍담은 흑마늘','삼희 영양순대','푸른밤','꿀유자차','생강미인','5령3일첫누에환','젬무브생생디앤알']
    # input_val = ['고구마전분맛', '수제소스 콩나물', '밀크씨슬 오뎅', '앞다리 자동차', '맛있는 된장']
    input_val = ['고구마전분맛', '맛있는 된장', '간마늘', '아라원참치발효숙성참치액(국찌개무침용)']

    # ingredients = ['송송 썬 파', '간마늘', '세척 당근', '대파', '생강', '아라원참치발효숙성참치액(국찌개무침용)']


    lemmas = []
    for vi in input_val:
        pos = okt.pos(vi)
        for p in pos:
            if p[1] == 'Noun':
                lemmas.append(p[0])

    recipes = recipe_recommender.recommend(lemmas)
    print(recipes)
