from django.contrib import admin
from .models import *
# Register your models here.
# Register your models here.
class resultPage(admin.ModelAdmin):
    list_display = ['title', 'category', 'url']

class resultPost(admin.ModelAdmin):
    list_display = ['title', 'body']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'phoneNumber', 'address', 'usertype']
    class Meta:
        model = UserProfile


class CityInfoDetailAdmin(admin.ModelAdmin):
    list_display = ('category','name', 'googlekey' , 'description', 'address', 'website', 'picture')
    list_editable = ('name', 'description', 'address', 'googlekey')

# class resultCollege(admin.ModelAdmin):
#     list_display = ['name', 'address']

# class resultHotel(admin.ModelAdmin):
#     list_display = ['name', 'address']

# class resultIndustry(admin.ModelAdmin):
#     list_display = ['name', 'address']

# class resultLibrary(admin.ModelAdmin):
#     list_display = ['name', 'address']

# class resultMall(admin.ModelAdmin):
#     list_display = ['name', 'address']

# class resultMuseum(admin.ModelAdmin):
#     list_display = ['name', 'address']

# class resultPark(admin.ModelAdmin):
#     list_display = ['name', 'address']

# class resultRestaurant(admin.ModelAdmin):
#     list_display = ['name', 'address']

# class resultZoo(admin.ModelAdmin):
#     list_display = ['name', 'address']



admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Post,resultPost)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CityInfoCategory)

admin.site.register(CityInfoDetail, CityInfoDetailAdmin)


# admin.site.register(College, resultCollege)
# admin.site.register(Library, resultLibrary)
# admin.site.register(Industry, resultIndustry)
# admin.site.register(Hotel,resultHotel)
# admin.site.register(Park, resultPark)
# admin.site.register(Zoo, resultZoo)
# admin.site.register(Museum, resultMuseum)
# admin.site.register(Restaurant, resultRestaurant)
# admin.site.register(Mall, resultMall)
