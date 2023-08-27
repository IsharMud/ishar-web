from django.db import models

from .account import Account


class News(models.Model):
    """
    News post.
    """
    news_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, models.CASCADE)
    created_at = models.DateTimeField()
    subject = models.CharField(max_length=64)
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'news'
