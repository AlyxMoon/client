"""
MapVault Documentation

I don't know what's going on here yet, I'm just trying to redo the map vault page
- Alyxdelunar

"""

from logging import getLogger
from PyQt5 import QtCore, QtWidgets, QtGui
from tornado import httpclient, httputil
import json
import util

from ui.busy_widget import BusyWidget

logger = getLogger(__name__)
FormClass, BaseClass = util.THEME.loadUiType("mapvault/mapvault.ui")

class MapVault(FormClass, BaseClass, BusyWidget):
    def __init__(self, client, *args, **kwargs):
        logger.debug("Map Vault tab instantiating")

        QtCore.QObject.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.client = client

        self.loaded = False

        self.http_client = httpclient.HTTPClient()
        self.pagination_limit = 10
        self.pagination_offset = 0

    @QtCore.pyqtSlot()
    def busy_entered(self):
        url = httputil.url_concat(
            "https://api.faforever.com/data/mapVersion",
            dict([
                ("page[limit]", self.pagination_limit),
                ("page[offset]", self.pagination_offset),
                ("page[totals]", "1")
            ])
        )
        response = self.http_client.fetch(url)
        self.http_client.close()
