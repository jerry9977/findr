from django.db import models
from django.contrib.auth.models import User

USERTYPES = (
    ('1', 'Student'),
    ('2', 'Tourist'),
    ('3', 'Businessman'),
)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    objects = models.Manager()
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
    objects = models.Manager()
    def __str__(self):
        return self.title,self.body
    #"Post(Title: " + self.title + ", Body: " + self.body + ")"

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    objects = models.Manager()
    def __str__(self): # For Python 2, use __unicode__ too
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    # website = models.URLField(blank=True)
    name = models.CharField(max_length=128)
    phoneNumber = models.IntegerField(default=0)
    address = models.CharField(max_length=128)
    usertype = models.CharField(max_length=128,choices = USERTYPES, default = '')
    objects = models.Manager()
    class Meta:
        verbose_name_plural = 'User Profiles'
    
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username, self.user.usertype


class CityInfoCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    objects = models.Manager()
    def __str__(self):
        return self.name  

class CityInfoDetail(models.Model):
    category = models.ForeignKey(CityInfoCategory)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128, default='  ')
    address = models.CharField(max_length=128)
    department = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    website = models.URLField(blank=True)
    googlekey = models.URLField(blank=True)
    picture = models.ImageField(upload_to='thumbnail_images', blank=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
        

