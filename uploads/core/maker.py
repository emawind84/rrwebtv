#!/usr/bin/env python
import requests, logging
from threading import Thread, Event

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

class Maker():
    _maker_key = 'nmr2BnBoPJPDkNvfz3bk0'

    def send(self, event, params=None):
        '''Trigger a maker event passing the event name and parameters as json object'''
        # https://maker.ifttt.com/trigger/{event}/with/key/nmr2BnBoPJPDkNvfz3bk0
        r = requests.get("https://maker.ifttt.com/trigger/%s/with/key/%s" % (event, self._maker_key), data=params)
        _logger.info(r.text)

    def send_async(self, event, params=None):
        Thread(target=self.send, args=(event, params,)).start()