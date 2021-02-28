import json
import logging
import os
from multiprocessing import Pool

import active_plugins
import config
from crawler.modules.module import Module


class Products(Module):

    def __init__(self):
        super(Products, self).__init__()
        self.logger = logging.getLogger(f"pid={os.getpid()}")

    def bootstrap(self):
        pass

    def run(self, p: Pool = None):
        self.logger.info("Searching products")

        for plugin in active_plugins.plugins:
            self.records.extend(plugin.scrap(p))

    def finish(self):
        with open(os.path.abspath(config.products_json), "w") as f:
            json.dump(self.records, f, indent=2)