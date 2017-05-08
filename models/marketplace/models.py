from django.db import models


class Textbook(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=70, blank=False)
    isbn = models.BigIntegerField(blank=True, null=True)
    author = models.CharField(max_length=70, blank=False)
    publicationDate = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    publisher = models.CharField(max_length=70, blank=True, null=True)


##a post for selling a textbook
class TextbookPost(models.Model):
    id = models.AutoField(primary_key=True)
    postTitle = models.CharField(max_length=70, blank=False)
    textbook = models.ForeignKey(Textbook, related_name='textbook')
    condition = models.CharField(max_length=70)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=70, null=True)
    details = models.CharField(max_length=300)
    sold = models.BooleanField(default=False)
    type = models.CharField(max_length=10)
    viewCount = models.IntegerField(default=0)
    postDate = models.DateField(auto_now=False, auto_now_add=True, blank=True, null=True)

class User(models.Model):
    username = models.CharField(max_length=20, blank=False, null=False)
    passhash = models.TextField(blank=False, null=False)
    email = models.EmailField(blank=False, null=False)

class Authenticator(models.Model):
    user_id = models.ForeignKey(User)
    authenticator = models.TextField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)

class recommendations(models.Model):
    post_id = models.IntegerField(primary_key=True)
    recommended_items = models.CharField(max_length=100)



# #each post will have one catagory.
# class Category(models.Model):
# 	id = models.AutoField(primary_key=True)
# 	name = models.CharField(max_length=25, blank=False)
