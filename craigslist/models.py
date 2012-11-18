from django.db import models
from tools import parser

import logging
logger = logging.getLogger(__name__)

class ItemManager(models.Manager):
    def create_item(self, url):
        try:
            data = parser.parse_url(url)
        except Exception, e:
            logger.error('Could not get url %s: %s' % (url, str(e)))
            return None

        # Only store items with price & image
        if data and data['sell_price'] and data['images'] and len(data['images']):
            try:
                item = Item.objects.get(url=url)
                item.title = data['title']
                item.description = data['description']
                item.post_datetime = data['post_datetime']
                item.price = data['sell_price']
                item.seller_email = data['seller_email']
                item.location = data['location']
                item.save()
                ItemImage.objects.filter(item=item).delete()
            except Item.DoesNotExist:
                item = Item(url=url,
                            title=data['title'],
                            description=data['description'],
                            post_datetime=data['post_datetime'],
                            price=data['sell_price'],
                            seller_email=data['seller_email'],
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

    url = models.URLField(unique=True,max_length=200,null=False,db_index=True)
    title = models.CharField(max_length=200,null=False)
    description = models.TextField(null=False)
    post_datetime = models.DateTimeField(null=False,db_index=True)
    price = models.DecimalField(null=True,blank=True,decimal_places=2,max_digits=10)
    active = models.BooleanField(null=False,default=True)
    num_views = models.IntegerField(null=False,default=0)
    num_likes = models.IntegerField(null=False,default=0)
    num_dislikes = models.IntegerField(null=False,default=0)
    seller_email = models.EmailField(null=True,max_length=75)
    location = models.CharField(null=False, default='', max_length=100)

    def first_image(self):
        return self.itemimage_set.all()[0]

    def rating(self):
        if self.num_views > 0:
            return float(self.num_likes) / float(self.num_views)
        else:
            return None

    def __unicode__(self):
        return u"Item %s" % self.title

class ItemImage(models.Model):
    item = models.ForeignKey(Item)
    url = models.URLField(max_length=200,null=False)
    order = models.IntegerField()

    def __unicode__(self):
        return u"%s" % self.url

class Subscriber(models.Model):
    email = models.EmailField(null=False,max_length=75)

    def __unicode__(self):
        return u'%s' % self.email