import requests
from BeautifulSoup import BeautifulSoup

import re
import dateutil.parser

import logging
logger = logging.getLogger(__name__)

RE_PRICE = re.compile(r'\$(\d+)')
RE_EMAIL = re.compile(r'.+@.+\..+')

def parse_url(url):
    r = requests.get(url, timeout=2, headers={'User-Agent' : 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)'} )
    if r.status_code:
        soup = BeautifulSoup( r.content )

        title = soup.find('h2').text
        logger.debug('Title: %s' % title)

        price_matches = RE_PRICE.search(title)
        if price_matches:
            price = price_matches.group(1)
        else:
            price = None
        logger.debug('Price: %s' % str(price))

        description = soup.find('div',{'id': 'userbody'}).text
        logger.debug('Description: %s' % description)

        post_datetime = soup.find('span', {'class': 'postingdate'}).text.replace('Date: ','')
        post_datetime = dateutil.parser.parse(post_datetime)
        post_datetime = post_datetime.replace(tzinfo=None)
        logger.debug('Post Datetime: %s' % post_datetime)

        seller_email = None
        for small_tag in soup.find('small'):
            if RE_EMAIL.search(small_tag.text):
                seller_email = small_tag.text
        logger.debug('Seller email: %s' % str(seller_email))

        try: # Multiple images
            images = [ img['src'].replace('thumb/','') for img in soup.find('div', {'id': 'iwt'}).findAll('img') ]
        except:
            try:
                images = [ soup.find('div', {'id': 'ci'}).find('img')['src'] ]
            except:
                logger.debug('No images')
                images = []
        logger.debug('Images: %s' % str(images))

        return {
            'title' : title,
            'post_datetime' : post_datetime,
            'sell_price' : price,
            'description' : description,
            'images' : images,
            'seller_email' : seller_email,
        }
    else:
        logger.debug('Error getting %s: %s' % (url, str(r.status_code)))

    return None

if __name__ == "__main__":
    urls = ['http://newyork.craigslist.org/brk/fuo/3399953168.html',
            'http://newyork.craigslist.org/brk/fuo/3399953168.html',
            'http://newyork.craigslist.org/mnh/fuo/3399952976.html', ]

    for url in urls:
        parse_url( url )
