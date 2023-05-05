#
from processor.word2vector import RecipeRecommender

recipe_ecommender = RecipeRecommender(model_path='./models/model_recipe.bin', rcp_path="./data/raw/0_2000_parsed.csv")


def get_recipes(ingredients: list, n=5):
    rst = recipe_ecommender.recommend(ingredients=ingredients, N=n)

    return rst


def get_recipes_without_allergy(ingredients: list, allergies: list, n=5):

    rst = recipe_ecommender.recommend_without_allergy(ingredients=ingredients, allergies=allergies, N=n)


    return rst