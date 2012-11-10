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
        pages = [ 'http://newyork.craigslist.org/fuo/',
                  'http://newyork.craigslist.org/fuo/index100.html',
                  'http://newyork.craigslist.org/fuo/index200.html',
                ]

        cnt = 0
        for url in pages:
            logger.debug('Loading url %s' % url)
            page = requests.get(url)
            soup = BeautifulSoup(page.content)

            toc = soup.find(id='toc_rows')

            rows = toc.findAll('p',{'class':'row'})
            listing_ids = []
            for row in rows:
                listing_url = row.find('a')['href']
                logger.info(listing_url)

                item = Item.objects.create_item(listing_url)
                logger.info(item)

                cnt += 1

                time.sleep(2)

                # m = RE_ITEM_ID.search(listing_link)
                # if m:
                #     listing_id = m.groups(0)[0]
                #     logger.info(listing_id)
                #     listing_ids.append(listing_id)

        logger.debug('Processed %d items' % cnt)