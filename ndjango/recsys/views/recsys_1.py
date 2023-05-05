from django.shortcuts import render
from django.templatetags.static import static
from django.shortcuts import redirect

from recsys.utils.recsys_1.get_recipe import *
'''
추천시스템 1 모듈
'''

def eng_search(request):
    return render(request,'recsys_1/eng_search.html')

def get_recipe_info(request):
    message = request.GET.get('message')
    messagelist = message.split(',')
    threshold= 1/(len(messagelist)+1)

    if messagelist == ['']:
        recipe_html = f"""
                <div>
                    <h2>재료를 입력하지 않았습니다</h2>
                    재료를 입력해주세요
                 <ul>
            """
        searchmessage= '재료를 입력하지 않았습니다'
    else:
        recinfo = enrecipe_cleaned.loc[get_index(search_recipes(messagelist,threshold)),['Title','Instructions','Image_Name','Cleaned_Ingredients']][1:10]
        
        recipe_list = []
        if len(recinfo) > 0:
            for index, row in recinfo.iterrows():
                cooktitle = row['Title']
                cookInst = row['Instructions'].split('\n')
                cookimglink = row['Image_Name']
                cookingr = eval(row['Cleaned_Ingredients'])
        
                img_path = f"/recsys/recsys_1/img/{cookimglink}.jpg"
                img_url = static(img_path)
                img_html = '<img src="{}" alt="">'.format(img_url)
        
                recipe_html = f"""
                    <div>
                        <h2>{cooktitle}</h2>
                        {img_html}
                    <ul>
                """
                for ingredient in cookingr:
                    recipe_html += f"<li>{ingredient}</li>"
                recipe_html += "</ul><ol>"
                for step in cookInst:
                    recipe_html += f"<li>{step}</li>"
                recipe_html += "</ol></div>"
        
                recipe_list.append(recipe_html)
        
            recipe_html = "\n".join(recipe_list)
        else:
            recipe_html = f"""
                <div>
                    <h2>레시피를 찾을 수 없었습니다.</h2>
                    다른 재료로 다시 검색해 볼까요?
                 <ul>
            """
        searchmessage= message +'(으)로 검색한 결과입니다.'
        

    return render(request, 'recsys_1/eng_result.html', {'search':searchmessage,'message':recipe_html})


