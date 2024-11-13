from django.urls import path
from . import views

# Namespace for the blog app to avoid name conflicts with other apps.
app_name = 'blog'

# URL patterns for the blog application.
urlpatterns = [
    path('',views.post_list, name='post_list'),  # URL for the main page displaying the list of posts.
    path('tag/<slug:tag_slug>/',
         views.post_list, name='post_list_by_tag'),  # URL for filtering posts by a specific tag.

    # The commented-out path below could be used for a class-based view version of post_list.
    # path('', views.PostListView.as_view(), name='post_list'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>',  # URL for displaying a specific post based
         views.post_detail,                               # on its date and slug.
         name='post_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),  # URL for sharing a specific post by its ID.
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),  # URL for adding a comment to a specific post by its ID.
]

