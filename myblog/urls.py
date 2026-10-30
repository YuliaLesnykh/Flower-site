from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('add-post/', views.add_post, name='add_post'),
    path('add-category/', views.add_category, name='add_category'),
    path('logout/', views.logout_view, name='logout'),
    path('thanks/', views.thanks, name='thanks'),
    path('tag/<slug:slug>/', views.tag_view, name='tag'), # <-- НОВЫЙ ПУТЬ
]