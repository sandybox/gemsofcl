from django.contrib import admin
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from craigslist.models import Item, ItemImage

class ItemImageInline(admin.TabularInline):
    template = "admin/edit_inline/tabular_imageitem.html"

    model = ItemImage
    extra = 3

class ItemAdmin(admin.ModelAdmin):
    list_display = ('post_datetime', 'title', 'img', 'click_to_url')

    def img(self, obj):
        images = obj.itemimage_set.all()
        if len(images) > 0:
            return ''.join('<img src="%s" style="height:160px; padding-right:10px;" />' % img for img in images)
        else:
            return ''
    img.short_description = 'Images'
    img.allow_tags = True

    inlines = [ ItemImageInline, ]

    def click_to_url(self, obj):
        return "<a target='_blank' href='%s'>link</a>" % (obj.url)

    click_to_url.short_description = 'Link'
    click_to_url.allow_tags = True

# class ItemImageAdmin(admin.ModelAdmin):
#     list_display = ('item', 'url', 'order', 'img')

#     def img(self, obj):
#         return "<img src='%s'/>" % (obj.url)
#     img.short_description = 'Image'
#     img.allow_tags = True

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImage)