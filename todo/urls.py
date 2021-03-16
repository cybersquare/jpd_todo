from . import views
from django.urls import path, include

urlpatterns = [
    path('',views.home),
    path('login/',views.login),
    path('register/',views.register),
    path('todo/',views.todo),
    path('save/',views.save),
    path('delete',views.delete),
    path('logout',views.logout),
]
