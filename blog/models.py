from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    # ONLY SHOWS THE 'PUBLISHED' BLOGS ON THE VIEW
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
           
            # A QuerySet represents a collection of objects from your database. It can have zero, one or many filters. Filters narrow down the query results based on the given parameters. In SQL terms, a QuerySet equates to a SELECT statement, and a filter is a limiting clause such as WHERE or LIMIT.

    options=(
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=250)
    excerpt = models.TextField()      
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts'
    )
    status = models.CharField(max_length=10, choices=options, default="Published")

    # class Manager
    # A Manager is the interface through which database query operations are provided to Django models.
    # At least one Manager exists for every model in a Django application.
    # The Manager is the main source of QuerySets for a model. For example, Blog.objects.all() returns a
    # QuerySet that contains all Blog objects in the database.

    objects = models.Manager()#default manager
    postObjects = PostObjects()#custom manager
    

    class meta:
        ordering = ('-published',)
    
    def __str__(self):
        return self.title