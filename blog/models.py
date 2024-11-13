from taggit.managers import TaggableManager
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# Custom model manager for filtering published posts.
class PublishedManager(models.Manager):
    '''
    Manager to retrieve only published posts.
    '''
    def get_queryset(self):
        return super().get_queryset()\
                    .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    '''Model representing a blog post.

    Attributes:
        title (str): The title of the blog post.
        slug (str): A unique slug for use in URLs, based on the publish date.
        author (User): The user who authored the post.
        body (str): The main content of the post.
        publish (datetime): The date and time the post was published.
        created (datetime): The date and time the post was created.
        updated (datetime): The date and time the post was last updated.
        status (str): The status of the post (draft or published).
        tags (TaggableManager): Tags associated with the post for categorization.
    '''
    class Status(models.TextChoices):
        '''
        Enumeration for post status options.
        '''
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB','Published'

    title = models.CharField(max_length=250,
                             unique_for_date='publish')
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    #Managers
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()  # Adds tagging functionality to the model.

    class Meta:
        ordering = ['-publish']  # Orders posts by publish date in descending order.
        indexes = [
            models.Index(fields=['-publish']),   # Index for optimizing queries by publish date.
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        '''
        Returns the canonical URL for the post.

        The URL includes the year, month, day, and slug for the post.
        :return:
        '''
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])




class Comment(models.Model):
    '''
    Model representing a comment on a blog post.

    Attributes:
        post (Post): The post the comment is related to.
        name (str): The name of the person who made the comment.
        email (str): The email address of the person who made the comment.
        body (str): The content of the comment.
        created (datetime): The date and time the comment was created.
        updated (datetime): The date and time the comment was last updated.
        active (bool): Indicates whether the comment is visible or hidden.
    '''
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'