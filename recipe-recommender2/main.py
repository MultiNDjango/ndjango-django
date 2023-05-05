from fastapi import FastAPI
import uvicorn
from service import get_recipes, get_recipes_without_allergy

app = FastAPI()


@app.get("/recipes")
async def list_recipes(ingredients: str, n: int = 5):
    ingredients_list = ingredients.split(',')
    ingredients_list.sort()

    rst = get_recipes(ingredients_list, n)
    return {'ingredients': rst, 'n': n}


@app.get("/recipes-allergy")
async def list_recipes(ingredients: str, allergies: str, n: int = 5):
    ingredients_list = ingredients.split(',')
    ingredients_list.sort()

    allergies_list = allergies.split(',')
    allergies_list.sort()

    # rst = get_recipes(ingredients_list, n)
    rst = get_recipes_without_allergy(ingredients_list, allergies_list, n)
    return {'ingredients': rst, 'n': n}


if __name__ == '__main__':

    uvicorn.run(app, host='0.0.0.0', port=5000)


