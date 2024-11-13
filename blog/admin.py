from django.contrib import admin
from .models import Post, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''
    Customizes the admin interface for the Post model.

    Displays selected fields and adds additional features such as search,
    filtering, and ordering in the admin panel.
    '''

    list_display = ['title', 'slug', 'author', 'status']  # Fields to display in the admin list view.
    list_filter = ['status','created','publish','author']  # Filters for narrowing down displayed posts.
    search_fields = ['title','body']  # Fields used for the search functionality in the admin panel.
    prepopulated_fields = {'slug': ('title',)}  # Automatically populate the slug field based on the title.
    raw_id_fields = ['author']  # Displays a lookup widget for selecting the author to enhance performance.
    date_hierarchy = 'publish'  # Adds a date-based drill-down navigation for the 'publish' field.
    ordering = ['status','publish']  # Default ordering for the Post objects.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''
    Customizes the admin interface for the Comment model.

    Provides features such as displaying selected fields, search, and filtering
    options to facilitate easier management of comments.
    '''
    list_display = ['name', 'email', 'post', 'created', 'active',]  # Fields to display in the admin list view.
    list_filter = ['active', 'created', 'updated']  # Filters for narrowing down displayed comments.
    search_fields = ['name', 'email', 'body']  # Fields used for the search functionality in the admin panel.
