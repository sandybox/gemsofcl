# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from craigslist.models import Item

import time
import re
import requests
from BeautifulSoup import BeautifulSoup

import logging
logger = logging.getLogger(__name__)

RE_ITEM_ID = re.compile(r'(\d+)\.html')

class Command(BaseCommand):
    def handle(self, *args, **options):
        base_url = 'http://newyork.craigslist.org/fua/'

        page = requests.get(base_url)
        soup = BeautifulSoup(page.content)

        toc = soup.find(id='toc_rows')

        rows = toc.findAll('p',{'class':'row'})
        listing_ids = []
        for row in rows:
            listing_url = row.find('a')['href']
            print listing_url

            item = Item.objects.create_item(listing_url)
            print item

            time.sleep(2)

            # m = RE_ITEM_ID.search(listing_link)
            # if m:
            #     listing_id = m.groups(0)[0]
            #     print listing_id
            #     listing_ids.append(listing_id)

        cnt = 0

        logger.debug('Processed %d items' % cnt)