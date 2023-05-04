# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 14:17:21 2023

@author: PC
"""
#사용한 모듈
import pandas as pd
import re
import ast
import pickle
from collections import Counter, defaultdict

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import SpectralClustering
from nltk.stem import PorterStemmer


#함수 정의
## 레시피 데이터 전처리 함수

def clean_ingredients_list(ingredients_list):
    cleaned_list = []
    for ingredient in ingredients_list:
        ingredient = re.sub(r'\d+x|\d+x\d+|\dx', '', ingredient)
        cleaned_list.append(ingredient.lower())
    return cleaned_list


def clean_recipe(recipe):
    clean_recipe = []
    for r in recipe:
        # 괄호와 내용물 제거
        r = re.sub(r'\(.*?\)', '', r)
        # 숫자와 분수 제거
        r = re.sub(r'\d+[\d\/]*', '', r)
        # 하이픈 제거
        r = re.sub(r'-', '', r)
        # 특수문자 제거
        r = re.sub(r'[^\w\s]', '', r)
        r = re.sub(r'\b[-\d⅓⅔¼¾½⅛⅜]+|\.\s|\s?(tsp|tbsp|teaspoon|tablespoon|ounce|oz|cup|pound|lb)s?\b', '', r)

        clean_recipe.append(r.strip())
    return clean_recipe

def split_ingredients(ingredients):
    new_list = []
    for item in ingredients:
        string_item = str(item)
        split_items = re.split(r'\band\b|\bsuch as\b|\bof\b|\bthen\b|\bthrough\b|\balso as\b|\badd\b|\bplus\b|\bafter\b|\bbut\b|\bfor\b|\binto\b|\bto\b|\bwith\b|\bcut into\b|\babout\b|\bor\b', string_item)
        new_list.extend(split_items)
    
    add_list = []
    for item in new_list:   
        string_item = str(item)
        split_items = re.split(r'(^|\b\s+)(g|t|sc|pinch of|strip|tbs|ounce|amount|brick|bar|barrel|bottle|bowl|loaf|loaves|dozen|sheet|cube|accompaniment|ball|block|bag|gram|pound|lb|package|slice|quart|can|piece|or)?s(\s+\b|$)', string_item)
        add_list.extend(split_items)
    
    es_list = []
    for item in add_list:   
        string_item = str(item)
        split_items = re.split(r'(^|\b\s+)(inch|box|bunch|pinch of|pinch|you|batch|dish|pinch|clove)?es(\s+\b|$)', string_item)
        es_list.extend(split_items)
    
    add_list = []
    for item in es_list:   
        string_item = str(item)
        split_items = re.split(r'(^|\b\s+)(g|t|sc|pinch of|tbs|ounce|amount|brick|bar|barrel|bottle|bowl|loaf|loaves|dozen|sheet|cube|accompaniment|ball|block|bag|gram|pound|lb|package|slice|quart|can|piece|or)?s(\s+\b|$)', string_item)
        add_list.extend(split_items)
    
    es_list = []
    for item in add_list:   
        string_item = str(item)
        split_items = re.split(r'(^|\b\s+)(inch|box|bunch|pinch of|pinch|you|batch|dish|pinch|clove)?es(\s+\b|$)', string_item)
        es_list.extend(split_items)
    
    return es_list
def clean_ingredients(ingredients):
    cleaned_ingredients = []
    for ingredient in ingredients:
        # 관사 제거
        ingredient = ' '.join([word for word in ingredient.split() if word.lower() not in ['a', 'the', 'an']])
        # 마침표 제거
        ingredient = re.sub(r'\.', '', ingredient)
        ingredient = re.sub(r'^(t|teaspooon|teasoon|milliliter|teardrop|teapoon|sticks|stick|tablespons|tablesepoon|tablepoon|tablepsoon|sc|tbs|bag|tbspg|tbspml|piece|bar|pinch of|package|bottle|batch|g|bunch|sheet|can|dozen|box|clove|ml|inch|cm)s?(\b\s+|$)', ' ', ingredient)

        #수식하는 동사 변형형제거
        ingredient = re.sub(r'(^|\b\s+)(warmed|pciked over|stemmed|steamed|vineripened|halved|fresh|using|use|untrimmed|purchased|drained|bleanched|diced|baked|countrystyle|welltrimmed|welltoasted|wellstirred|wellseasd|cured|cubed|decorative|cutup|boiled|cheap|buttered|breifly|brinecured|brined|boiling|bless|blanched|blended|needed|cooled|beaten|called|known|additive|kneading|serving|spraying|unfiltered|brushing|activated|shaved|torn|crushed|chilled|quartered|skinned|mixed|granulated|toasted|peeled|sliced|frozen|thawed|seeded|grated|roasted|seperated|minced|cored|sifted|chopped|trimmed|bottled|assorted|bruised|drained|rinsed|softened|cleaned|divided)s?(\b\s+|$)', ' ', ingredient)
        ingredient = re.sub(r'(^|\b\s+)(halved|fresh|using|packed|closed|tied|use|untrimmed|purchased|drained|bleanched|diced|baked|countrystyle|welltrimmed|welltoasted|wellstirred|wellseasd|cured|cubed|decorative|cutup|boiled|cheap|buttered|breifly|brinecured|brined|boiling|bless|blanched|blended|needed|cooled|beaten|called|known|additive|kneading|serving|spraying|unfiltered|brushing|activated|shaved|torn|crushed|chilled|quartered|skinned|mixed|granulated|toasted|peeled|sliced|frozen|thawed|seeded|grated|roasted|seperated|minced|cored|sifted|chopped|trimmed|bottled|assorted|bruised|drained|rinsed|softened|cleaned|divided)s?(\b\s+|$)', ' ', ingredient)

        #수식하는 형용/부사 제거(^|\b) -맨 앞 또는 단어 경계+공백(\b\s+|$) 맨 뒤 또는 단어 경계+공백
        ingredient = re.sub(r'(^|\b\s+)(sushigrade|substitute|mediumsize|strong|strained|storebought|wellwashed|thinsliced|topquality|unbleached|ultrafresh|ultrathin|uncle bens|wellshaken|whatever|wellsifted|wellrinsed|wellseasoned|wellchilled|wide|wild|warm|homemade|thin|very|young|thickcut|thick|coarsely|good|freshly|roughly|approximately|unpeeled|cooked|finely)s?(\b\s+|$)', ' ', ingredient)
        ingredient = re.sub(r'(^|\b\s+)(accompaniment|thinly|thickly)s?(\b\s+|$)', ' ', ingredient)
        ingredient = re.sub(r'(^|\b\s+|)(additional|tightly|finequality|bestquality|medium|small|large)(\b\s+|$)', ' ', ingredient)

        # 항목에 있다면 항목제거
        ingredient = re.sub(r'\b\s+(metal|pan|dish|knife)\s+\b|\W', ' ', ingredient)
        ingredient = re.sub(r'\b\s+(slicer|pan|available|shop|your|cloth|market|youll|markets|shops|minutes|disposable|discarding|minute|cool|you|ovenproof|pot|info|steamer|combine|choose|straws|shaker|castiron|ingredient|amys|blender|pan|pans|supermarkets|bundt|brushed||tweezers|metal|acrylic|are)(\s+|$)|\W', ' ', ingredient)
        ##맨 앞에 있을때
        ingredient = re.sub(r'^(if|of|thinly|tightly|from|at|available|are|as|also as)\b\s+|\W', ' ', ingredient)
        ingredient = re.sub(r'^(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|ninetine|twnety|t|x|sc|tbs|ingredient|bag|piece|bar|bottle|batch|g|bunch|sheet|can|dozen|box|clove|ml|inch|cm)s?(\b\s+|$)', ' ', ingredient)
        #단어를 포함하고있으면 제거
        ingredient = re.sub(r'\b\w*spoon\w*\b|\W', ' ', ingredient)
        ingredient = re.sub(r'\b\w*proof\w*\b|\W', ' ', ingredient)
        ingredient = re.sub(r'^.*thermo.*$', ' ', ingredient)
        # 공백 제거
        ingredient = ' '.join(ingredient.split())
        #is가 있으면 is 뒤 모두 제거
        ingredient = re.sub(r'\b(is|can be|will be)\b.*', '', ingredient).strip()
        #공백 사이에 해당 단어 있으면 뒤를 전부 제거
        ingredient = re.sub(r'\b\s+(cut|on diagonal|layers|at|soaked|scrubbed|lengthwise|in|crosswise|widthwise|if|at room temperature|room temperature)\s+\b.*', '', ingredient).strip()
        #맨 앞에서부터 시작해서 단어+공백이면 모두 제거
        ingredient = re.sub(r'^(stems removed|grill|patted dry|as|at|be|by|until|cut|wooden|lengthwise|will|crosswise|your|you|youre|youll)\s+\b.*', '', ingredient).strip()
        #단어가 맨 뒤에 있으면 제거 
        ingredient = re.sub(r'\b\s+(lengthwise|of|from|widthwise|split|soaked|picked over|on bias|on holes|on diagonal|scrubbed|patted dry|on mandoline|mandoline|if|at room temperature|room temperature)$.*', '', ingredient).strip()

        ingredient = re.sub(r'\b(dish|sheet|spatula|grill|electric|processor|peeler|equipment|temperature|mixer|tops|knife|cutter|cutters|dishes|online|sheets|skewer|blender|skewers|scraper)\b.*', '', ingredient).strip()
        ingredient = re.sub(r'^(as|at|be|by|cut|thislengthwise|crosswise)\s+\b.*', '', ingredient).strip()
        ingredient = re.sub(r'\sbaking\b$', '', ingredient)
        ingredient = ingredient.replace(' bu ', ' bulb ')
        cleaned_ingredients.append(ingredient)
    return cleaned_ingredients

def separate_plural_units(ingredients):
    new_list = []
    for item in ingredients:
        string_item = str(item)
        split_items = re.split(r'\band\b|\bsuch as\b|\binch\b|\balso as\b|\badd\b|\bplus\b|\bafter\b|\bbut\b|\bfor\b|\binto\b|\bto\b|\bwith\b|\bcut into\b|\babout\b|\bor\b', string_item)
        new_list.extend(split_items)
    # 복수형이 s인 단위들 분리
    add_list=[]
    for item in new_list:   
        string_item = str(item)
        split_items = re.split(r'(^|\b\s+)(g|t|stalk|sprig|square|wedge|tube|drop|sc|pinch of|tbs|ounce|amount|brick|bar|barrel|bottle|bowl|loaf|loaves|dozen|sheet|cube|accompaniment|ball|block|bag|gram|pound|lb|package|slice|quart|can|piece|or)?s(\s+\b|$)', string_item)
        add_list.extend(split_items)
    # 복수형이 es인 단위들 분리
    es_list=[]
    for item in add_list:   
        string_item = str(item)
        split_items = re.split(r'(^|\b\s+)(inch|tube|box|bunch|pinch of|pinch|you|batch|dish|pinch|clove)?es(\s+\b|$)', string_item)
        es_list.extend(split_items)
    return es_list


def clean_recipe_dataframe(df):
    for i in range(len(df)):
        listed_df=ast.literal_eval(df['Ingredients'][i])
        cleaned_df = clean_ingredients(separate_plural_units(clean_ingredients(split_ingredients(clean_recipe(clean_ingredients_list(listed_df))))))
        df.loc[i, 'Ingredients']=str(list(filter(lambda x: len(x) > 0, cleaned_df)))
    return df

# 카테고리화를 위한 tokenizer함수

# tokenizer 함수 정의 (PorterStemmer를 사용)
def tokenize(text):
    return [stemmer.stem(word) for word in text.split()]

### 실행 코드

uniqin=pd.read_csv('F:\\Ndjango\\branch_test\\uniqingred.csv',header=None)
uniqin_list=uniqin[0].values.tolist()

#### 카테고리 추출 과정 코드

enrecipe=pd.read_csv('F:\\Ndjango\\branch_test\\archive\\recipeenglish.csv')
enrecipe.columns
Instructions=enrecipe['Instructions'].astype(str)
Instructionslist=Instructions.apply(lambda x: x.split('\n'))
list_lengths = Instructionslist.apply(lambda x: len(x))
enrecipe = pd.concat([enrecipe, list_lengths.rename('Instructions_length')], axis=1)
#ingredient=enrecipe[['Ingredients','Cleaned_Ingredients']]
#print(ingredient)
#min(list_lengths)
enrecipe.columns
enrecipe=enrecipe.drop('Unnamed: 0',axis=1)

##### 데이터프레임에서 식재료 추출

ingredients = enrecipe['Cleaned_Ingredients']

all_ingredients = []
for ingredients in enrecipe['Cleaned_Ingredients']:
    list_ingredients = ast.literal_eval(ingredients)
    all_ingredients.append(list_ingredients)

ingredients_list2 = [item for sublist in all_ingredients for item in sublist]
merged_ingre_list = list(set(ingredients_list2))
ingredients_lower = [ingredient.lower() for ingredient in ingredients_list2]
ingredients4=clean_ingredients_list(ingredients_lower)
ingredients4= clean_recipe(ingredients4)
ingredients4=split_ingredients(ingredients4)
ingredients4= clean_ingredients(ingredients4)
ingredients4=separate_plural_units(ingredients4)
ingredients4=clean_ingredients(ingredients4)
ingredients4 = list(filter(lambda x: len(x) > 0, ingredients4))
uniqlist=list(set(ingredients4))

#####특정 문자열이 있는지, 있다면 몇개인지 확인

notuniq=[]
for items in ing_categories2.values():
    for item in items:
        if 'grill' in item:
            notuniq.append(item)
    if items.endswith('of'):
        notuniq.append(items)
    if items.starswith('one '):
        notuniq.append(items)

uniqlistpd=pd.DataFrame(uniqlist)
uniqlistpd.to_csv('F:\\Ndjango\\branch_test\\uniqlist.csv',index=None,header=None)

uniqlist=pd.read_csv('F:\\Ndjango\\branch_test\\uniqlist.csv',header=None)
uniqlist=uniqlist[0].values.tolist()

#!pip install nltk  

##### 카테고리화 모델

# PorterStemmer 객체 생성
stemmer = PorterStemmer()

# CountVectorizer 객체 생성 (n-gram 범위: 1~8)
vectorizer = CountVectorizer(ngram_range=(1, 8), tokenizer=tokenize)
#vectorizer = CountVectorizer(ngram_range=(1, 8))
X = vectorizer.fit_transform(uniqlist)

model = SpectralClustering(n_clusters=250, affinity='nearest_neighbors', assign_labels='discretize')
model.fit(X)

labels = model.labels_


# 각 클러스터에 속한 데이터 개수를 카운트
cluster_counts = Counter(labels)

# 클러스터별 가장 많이 등장한 단어 추출
most_common_words = []
for i in range(len(set(labels))):
    cluster_data = [uniqlist[j] for j in range(len(uniqlist)) if labels[j] == i]
    cluster_words = " ".join(cluster_data).split()
    most_common_word = Counter(cluster_words).most_common(1)[0][0]
    most_common_words.append(most_common_word)
    
# 카테고리 이름과 해당하는 데이터의 리스트로 딕셔너리 생성
categories3 = defaultdict(list)
for i, label in enumerate(labels):
    category_name = most_common_words[label]
    categories3[category_name].append(uniqlist[i])

print(dict(categories3))


# 원본 데이터에 동일한 처리를 한 리스트 생성 
enrecipe_cleaned=clean_recipe_dataframe(enrecipe)


# 카테고리 및 한글화를 위한 저장

a=categories3
with open('spectralingre23.pickle', 'wb') as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

t1_keys=pd.DataFrame(list(ing_categories1.keys()))
with open('spectralingre21.pickle', 'rb') as handle:
    ing_categories1 = pickle.load(handle)
    
t1_keys=pd.DataFrame(list(ing_categories1.keys()))
t1_keys.to_csv('t3_categories.csv',index=None)
#한글 카테고리는 따로 작성
enrecipe_cleaned.to_csv('enrecipe_cleaned.csv',index=None)
en=pd.read_csv('enrecipe_cleaned.csv')
