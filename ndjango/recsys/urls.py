from django.urls import path, include
from recsys.individual_urls.recsys_1 import urlpatterns as rec1_urls
from recsys.individual_urls.recsys_2 import urlpatterns as rec2_urls
from recsys.individual_urls.recsys_3 import urlpatterns as rec3_urls

app_name = 'recsys'

# urlpatterns = sum([rec1_urls, rec2_urls, rec3_urls], [])

urlpatterns = [
    path('eng-recs/', include(rec1_urls)),
    path('kor-recs/', include(rec2_urls)),
    path('kor-recs2/', include(rec3_urls)),
]