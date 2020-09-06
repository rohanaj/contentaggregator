from .views import *
from django.urls import path,include,re_path

urlpatterns = [
    path("index",index,name="index"),
    path('scrapenews',scrape_news,name="scrapenews"),
path('indexpagescrape',indexpageforscrape,name="indexpagescrape"),
    path('results/<str:source>',results,name="results")
]