# from django.conf.individual_urls import
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from refrigerators.views import base_crud
from refrigerators.individual_urls.barcode_urls import urlpatterns as barcode_urls
from refrigerators.individual_urls.base_urls import urlpatterns as base_urls
from refrigerators.individual_urls.icon_urls import urlpatterns as icon_urls
# from refrigerators.individual_urls.photo_urls import urlpatterns as photo_urls
# from refrigerators.individual_urls.table_urls import urlpatterns as table_urls
# from refrigerators.individual_urls.crawling_urls import urlpatterns as crawling_urls


app_name = 'refrigerators'

urlpatterns = [
    path('base/', include(base_urls)),
    path('media/<int:pk>/', base_crud.serve_grocery_image, name='image'),
    path('two-doors/', include(icon_urls)),
    path('barcodes/', include(barcode_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


