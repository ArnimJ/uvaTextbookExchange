from django.db import models


##a post for selling a textbook
class TextbookPost(models.Model):
	id = models.AutoField(primary_key=True)
	title =  models.CharField(max_length=70, blank=False)
	isbn = ISBNField()
	price = models.DecimalField(max_digits=6, decimal_places=2)
	category = models.ForeignKey(Category)

#each post will have one catagory.
class Category(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=25, blank=False)
	


		