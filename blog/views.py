from django.db.models import Count
from taggit.models import Tag
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm


# Create your views here.



def post_detail(request, year, month, day, post):
    '''
    Display a single post's details, including active comments and similar posts.

    Args:
        request (HttpRequest): The HTTP request object.
        year (int): The year of the post's publication date.
        month (int): The month of the post's publication date.
        day (int): The day of the post's publication date.
        post (str): The slug of the post.

    Returns:
        HttpResponse: Rendered detail page for a post.
    '''
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)

    form = CommentForm()  # Empty comment form for user submissions.

    #List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                   .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                  .order_by('-same_tags','-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


def post_list(request, tag_slug=None):
    '''
    Display a list of published posts, optionally filtered by tag.

    Args:
        request (HttpRequest): The HTTP request object.
        tag_slug (str, optional): The slug of a tag to filter posts by.

    Returns:
        HttpResponse: Rendered list page of posts.
    '''
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)  # Get the tag object or return a 404 error.
        post_list = post_list.filter(tags__in=[tag])  # Filter posts by the tag.

    paginator = Paginator(post_list, 3)  # Paginate the posts with 3 per page.

    page_number = request.GET.get('page',1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)  # If the page number is not an integer, show the first page.
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # If the page number is out of range, show the last page.
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})


class PostListView(ListView):
    """
    Alternative view for displaying a list of posts using Django's generic ListView.
    """
    queryset = Post.published.all()
    context_object_name = 'posts'  # Context variable name to use in the template.
    paginate_by = 3  # Number of posts per page.
    template_name = 'blog/post/list.html'



def post_share(request, post_id):
    '''
    Handle the sharing of a post via email.

    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the post to be shared.

    Returns:
        HttpResponse: Rendered sharing form page.
    '''
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(  # Build the absolute URL for the post.
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()  # Instantiate an empty form for GET requests.
    return render(request, 'blog/post/share.html', {'post': post,
                                                                        'form': form,
                                                                         'sent': sent})



@require_POST
def post_comment(request, post_id):
    '''
    Handle the submission of a comment for a specific post.

    Args:
        request (HttpRequest): The HTTP request object.
        post_id (int): The ID of the post being commented on.

    Returns:
        HttpResponse: Rendered comment form page with status and form data.
    '''
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)  # Create the comment object but do not save to the database yet.
        comment.post = post  # Associate the comment with the post.
        comment.save()  # Save the comment to the database.
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})