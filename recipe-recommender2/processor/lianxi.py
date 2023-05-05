from konlpy.tag import Okt

okt = Okt()

ingredients = ['송송 썬 파', '간마늘', '세척 당근', '대파', '생강', '아라원참치발효숙성참치액(국찌개무침용)']

lemmas = []

for ingredient in ingredients:
    pos = okt.pos(ingredient)
    for p in pos:
        if p[1] == 'Noun':
            lemma = p[0]
            lemmas.append(lemma)

print(lemmas)
# ['송송', '파', '간', '마늘', '세척', '당근', '대파', '생강', '참치', '발효', '숙성', '참치', '액', '국', '찌개']


# from konlpy.tag import Kkma
#
# kkma = Kkma()
#
# ingredients = ['송송 썬 파', '간마늘', '세척 당근', '대파', '생강', '아라원참치발효숙성참치액(국찌개무침용)']
#
# lemmas = []
#
# for ingredient in ingredients:
#     pos = kkma.pos(ingredient)
#     for p in pos:
#         if p[1] == 'NNG':
#             lemma = p[0]
#             lemmas.append(lemma)
#
# print(lemmas)
# ['파', '간', '마늘', '세척', '당근', '대파', '생강', '원', '참치', '발효', '숙성', '참치', '액', '국', '찌개', '무침']


# from konlpy.tag import Hannanum
#
# hannanum = Hannanum()
#
# ingredient = '아라원참치발효숙성참치액(국찌개무침용)'
#
# pos = hannanum.pos(ingredient)
#
# for i in range(len(pos)):
#     if pos[i][1] == 'N':
#         lemma = pos[i][0]
#         print(lemma)
#         break
#
#
