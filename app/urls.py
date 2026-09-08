from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,re_path
from . import views

app_name = "app"

slug_pattern = r"[-\w\u0980-\u09FF]+" 

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/new/", views.post_create, name="post_create"),
    re_path(rf"^post/(?P<slug>{slug_pattern})/$", views.post_detail, name="post_detail"),
    re_path(rf"^post/(?P<slug>{slug_pattern})/edit/$", views.post_edit, name="post_edit"),
    re_path(rf"^post/(?P<slug>{slug_pattern})/delete/$", views.post_delete, name="post_delete"),
    
    path("category/<slug:slug>/", views.post_by_category, name="posts_by_category"),
    path("tag/<slug:tag_slug>/", views.post_by_tag, name="posts_by_tag"),
    path("search/", views.search_posts, name="search_posts"),
    
    path("accounts/profile/<str:username>/", views.profile_detail, name="profile_detail"),
    path("accounts/login-redirect/",views.custom_login_redirect,name="custom_login_redirect",),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    path("about/", views.about, name="about"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # not