from django.db import models
from django.forms import ModelForm

class Translation_length (models.Model):
    translation_id = models.AutoField(
      primary_key=True,
      max_length=10,
    )
    year_month = models.CharField(
      verbose_name='年月',
      max_length=6,
      unique=True
    )
    translation_length = models.IntegerField(
      verbose_name='翻訳文字数'
    )
    insert_date = models.DateTimeField(
      'date published',
      auto_now_add=True,
    )
    update_date = models.DateTimeField(
      'date published',
      auto_now=True,
    )
