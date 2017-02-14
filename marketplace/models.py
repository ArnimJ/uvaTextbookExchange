from django.db import models


class Textbook(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=70, blank=False)
    isbn = models.BigIntegerField(blank=False) 	
    author = models.CharField(max_length=70)
    publicationDate = models.DateField(auto_now=False, auto_now_add=False)
    publisher = models.CharField(max_length=70)


##a post for selling a textbook
class TextbookPost(models.Model):
    id = models.AutoField(primary_key=True)
    postTitle = models.CharField(max_length=70, blank=False)
    textbook = models.ForeignKey(Textbook)
    condition = models.CharField(max_length=70)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=70)
    sold = models.BooleanField(default=False)

# #each post will have one catagory.
# class Category(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	name = models.CharField(max_length=25, blank=False)
