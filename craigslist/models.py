from django.db import models
from tools import parser

class ItemManager(models.Manager):
    def create_item(self, url):
        try:
            data = parser.parse_url(url)
        except Exception, e:
            print 'Could not get url %s: %s' % (url, str(e))
            return None

        if data:
            try:
                item = Item.objects.get(url=url)
                item.title = data['title']
                item.description = data['description']
                item.post_datetime = data['post_datetime']
                item.price = data['sell_price']
                item.save()
                ItemImage.objects.filter(item=item).delete()
            except Item.DoesNotExist:
                item = Item(url=url,
                            title=data['title'],
                            description=data['description'],
                            post_datetime=data['post_datetime'],
                            price=data['sell_price'],
                            )
                item.save()

            for idx, img in enumerate(data['images']):
                item_image = ItemImage(item=item,
                                       url=img,
                                       order=idx,
                                    )
                item_image.save()

            return item
        return None

class Item(models.Model):
    objects = ItemManager()

    url = models.URLField(unique=True,max_length=200,null=False)
    title = models.CharField(max_length=200,null=False)
    description = models.TextField(null=False)
    post_datetime = models.DateTimeField(null=False)
    price = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)

    def __unicode__(self):
        return u"Item %s" % self.title

class ItemImage(models.Model):
    item = models.ForeignKey(Item)
    url = models.URLField(max_length=200,null=False)
    order = models.IntegerField()

    def __unicode__(self):
        return u"%s" % self.url