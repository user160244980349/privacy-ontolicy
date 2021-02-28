import logging
import os
import re
from time import sleep

from crawler.plugins.plugin import Plugin


class Walmart(Plugin):

    def __init__(self, keywords, pages, cooldown=3.):
        super().__init__(keywords, pages)
        self.cooldown = cooldown

    def gen_search_urls(self, keyword, pages):
        return [f"https://www.walmart.com/search/?page={p}&query={keyword}"
                for p in range(1, pages + 1)]

    def scrap_products(self, url):
        sleep(self.cooldown)
        return self.scrap_products_base(url, self.product_template)

    def get_product(self, product):
        sleep(self.cooldown)
        return self.get_product_base(
            product,
            (self.template1, self.template2),
            captcha=self.captcha
        )

    @classmethod
    def captcha(cls, markup):
        logger = logging.getLogger(f"pid={os.getpid()}")
        if re.search("Help us keep your account safe by clicking on the checkbox below.", markup):
            logger.error("Sorry, we just need to make sure you're not a robot.")
            return True
        return False

    @classmethod
    def product_template(cls, soup):
        return [f"https://www.walmart.com{item.get('href')}"
                for item in soup.findAll("a", {"class": "product-title-link"})]

    @classmethod
    def template1(cls, body):
        div = body.find("table", {"class": "product-specification-table"})
        if div is not None:
            for tr in div.tbody.findChildren("tr"):
                tds = tr.findChildren("td")
                if re.search("^Manufacturer$", re.sub(r"[\n\s]", "", tds[0].text)):
                    return re.sub(r"[\"\',\n]", "", tds[1].text).lower()
        return None

    @classmethod
    def template2(cls, body):
        div = body.find("table", {"class": "product-specification-table"})
        if div is not None:
            for tr in div.tbody.findChildren("tr"):
                tds = tr.findChildren("td")
                if re.search("^Brand$", re.sub(r"[\n\s]", "", tds[0].text)):
                    return re.sub(r"[\"\',\n]", "", tds[1].text).lower()
        return None