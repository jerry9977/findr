from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self): # For Python 2, use __unicode__ too
        return self.name

class Post(models.Model):
    """
    The model for a post in the timeline
    """
    title = models.CharField(max_length=140)
    body = models.CharField(max_length=500)

    def __str__(self):
        return self.title,self.body
    #"Post(Title: " + self.title + ", Body: " + self.body + ")"

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    
    def __str__(self): # For Python 2, use __unicode__ too
        return self.title

class College(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    department = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

    def _str_(self):
        return self.name

class Library(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phonenumber = models.IntegerField(default='NULL')
    email = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Libraries'

    def _str_(self):
        return self.name

class Industry(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    iType = models.CharField(max_length=128)
    email = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Industries'
    
    def _str_(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phonenumber = models.IntegerField(default='NULL')
    email = models.CharField(max_length=128)

    def _str_(self):
        return self.name

class Park(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phonenumber = models.IntegerField(default='NULL')
    email = models.CharField(max_length=128)

    def _str_(self):
        return self.name

class Zoo(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phonenumber = models.IntegerField(default='NULL')
    email = models.CharField(max_length=128)

    def _str_(self):
        return self.name

class Museum(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phonenumber = models.IntegerField(default='NULL')
    email = models.CharField(max_length=128)

    def _str_(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phonenumber = models.IntegerField(default='NULL')
    email = models.CharField(max_length=128)

    def _str_(self):
        return self.name

class Mall(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    phonenumber = models.IntegerField(default='NULL')
    email = models.CharField(max_length=128)

    def _str_(self):
        return self.name
