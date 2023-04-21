from django.urls import path, include
from refrigerators.individual_urls.barcode_insert import urlpatterns as barcode_urls
from refrigerators.individual_urls.base_urls import urlpatterns as base_urls
from refrigerators.individual_urls.crawling_urls import urlpatterns as crawling_urls
from refrigerators.individual_urls.icon_urls import urlpatterns as icon_urls
from refrigerators.individual_urls.photo_urls import urlpatterns as photo_urls
from refrigerators.individual_urls.table_urls import urlpatterns as table_urls


app_name = 'refrigerators'

urlpatterns = sum([barcode_urls, crawling_urls, photo_urls, table_urls], [])


urlpatterns += [
    path('base/', include(base_urls)),
    path('two-doors/', include(icon_urls)),
    # path('a', views.view_a, name="view_a"),
    # path('a', barcode_insert.view_a, name="view_a"),
    # path('b', base_crud.view_b, name="view_b"),
    # path('c', crawling_insert.view_c, name="view_c"),
    # path('d', image_display.view_d, name="view_d"),
    # path('e', photo_insert.view_e, name="view_e"),
    # path('f', table_display.view_f, name="view_f"),

]



