from django.urls import path
from . import views

urlpatterns = [
    path('metadata/<uuid:token_id>/', views.token_metadata_json, name='token-metadata-json'),
    path('api/tokens/metadata/<uuid:order_id>/', views.token_metadata_json, name='token-metadata-json'),
]



