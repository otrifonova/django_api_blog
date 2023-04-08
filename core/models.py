from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    following = models.ManyToManyField('self',
                                       symmetrical=False,
                                       through='Follow',
                                       blank=True)


class Follow(models.Model):
    from_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='followers')
    start_date = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    title = models.CharField(max_length=80)
    text = models.TextField()
    author = models.ForeignKey(User,
                               related_name='posts',
                               on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True)
    read_by_user = models.ManyToManyField(User,
                                          related_name='read_posts')

    class Meta:
        ordering = ['-pub_date']
