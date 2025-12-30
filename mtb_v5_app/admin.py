from django.contrib import admin
from .models import Page, Media, History

class MediaInline( admin.TabularInline ):
 model = Media
 extra = 0

class HistoryInline( admin.TabularInline ):
 model = History
 extra = 0

class PageAdmin( admin.ModelAdmin ):
 inlines = [ MediaInline, HistoryInline ]

admin.site.register( Page, PageAdmin )
admin.site.register( Media )
admin.site.register( History )
