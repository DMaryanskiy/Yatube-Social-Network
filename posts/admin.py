""" импорт функции admin и модулей Post, Group """
from django.contrib import admin

from .models import Post, Group

class PostAdmin(admin.ModelAdmin):
    """ создаем класс, в котором создаем интерфейс для создания и просмотра постов """
    list_display = ('pk', 'text', 'pub_date', 'author', )
    search_fields = ('text', )
    list_filter = ('pub_date', )
    empty_value_display = '-пусто-'

class GroupAdmin(admin.ModelAdmin):
    """ создаем класс, в котором создаем интерфейс для создания и просмотра групп """
    list_display = ('title', 'slug', 'description')
    search_fields = ('title', )
    empty_value_display = '-пусто-'

admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
