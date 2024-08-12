from django.contrib import admin
from .models import Category, Announcement, Comment, AnnouncementCategory, Author

admin.site.register(Category)
admin.site.register(Announcement)
admin.site.register(Comment)
admin.site.register(AnnouncementCategory)
admin.site.register(Author)


