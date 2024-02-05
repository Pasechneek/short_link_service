from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_new_link/', views.add_new_link, name='add_new_link'),
    path('add_new_link/result/<str:short_link>', views.show_result, name='result'),
    path("<str:short_link>/", views.shot_link_redirect, name='short_link_redirect'),
]
