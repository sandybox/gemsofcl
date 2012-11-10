# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from craigslist.models import Item

import requests
from BeautifulSoup import BeautifulSoup

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        base_url = 'http://newyork.craigslist.org/fua/'

        page = requests.get(base_url)
        soup = BeautifulSoup(page.content)

        print soup

        cnt = 0

        logger.debug('Processed %d items' % cnt)