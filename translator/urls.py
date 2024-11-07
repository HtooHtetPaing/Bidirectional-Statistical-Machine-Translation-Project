from django.urls import path
from . import views
urlpatterns =[
    path('translator/',views.translator,name='translator'),
    path('saveinfo/',views.saveinfo,name='saveinfo')
]