from . import views
from django.urls import path

app_name = 'analyzer'
urlpatterns = [

    path('', views.index, name='index'),
    path('features/', views.features, name='features'),
    path('engine/', views.upload, name='upload-data'),
    path('graph/', views.graph, name='graph'),


]
