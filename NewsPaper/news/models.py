from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(post_rating=Sum('rating'))
        post_rating = post_rating.get('post_rating', 0)
        if not isinstance(post_rating, int):
            post_rating = 0

        comment_rating = self.author.comment_set.aggregate(comment_rating=Sum('rating'))
        comment_rating = comment_rating.get('comment_rating', 0)
        if not isinstance(comment_rating, int):
            comment_rating = 0

        self.rating = post_rating * 3 + comment_rating
        self.save()

    def __str__(self):
        return f'{self.author} - {self.rating}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, through='SubscribedUsersCategory')

    def __str__(self):
        return self.name


class SubscribedUsersCategory(models.Model):
    subscribed_users = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=64)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.author} - {self.datetime} - {self.title}'


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    datetime = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.datetime} - {self.user} - {self.rating} - {self.text[0:100]}...'
