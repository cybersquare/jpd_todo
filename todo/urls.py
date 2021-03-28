from . import views
from . import views_api
from django.urls import path

urlpatterns = [
    path('',views.home),
    path('login/',views.login),
    path('register/',views.register),
    path('todo/',views.todo),
    path('save/',views.save),
    path('delete',views.delete),
    path('logout',views.logout),

    path('api_home/', views_api.home),
    path('api_login/', views_api.login),
    path('api_register/',views_api.register),
    path('api_todo/',views_api.todo),
    path('api_save/',views_api.save),
    path('api_delete/',views_api.delete),

]
