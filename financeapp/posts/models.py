from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField('Title', max_length=100)
    content = models.TextField('Content')
    read_time = models.IntegerField('Read Time (minutes)')
    created_at = models.DateField('Created At', auto_now_add=True)
    image_path = models.ImageField('Main Photo', upload_to='photos/%Y/%m/%d/')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='posts'
    )
    is_published = models.BooleanField('Is Published', default=True)
    views_counter = models.IntegerField('Views Counter', default=0)
    favorites_counter = models.IntegerField('Favorites Counter', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class PostLike(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post_id', 'user_id')
