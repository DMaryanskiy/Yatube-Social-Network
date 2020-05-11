""" импорт функции path"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("group/<slug:slug>/", views.group_posts, name="group_posts"),
    path("new/", views.new_post, name="new_post"),
    path("follow/", views.follow_index, name="follow_index"),
    path("<username>/", views.profile, name="profile"),
    path("<username>/follow/", views.profile_follow, name="profile_follow"), 
    path("<username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
    path("<username>/<post_id>/", views.post_view, name="post"),
    path("<username>/<post_id>/edit/", views.post_edit, name="post_edit"),
    path("<username>/<post_id>/comment/", views.add_comment, name="add_comment"),
]
