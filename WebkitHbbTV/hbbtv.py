from Screens.Screen import Screen

from enigma import eTimer

import os, struct

from . import vbcfg
from .__init__ import _
from .vbipc import VBController

class HbbTVWindow(Screen):
	skin = """
		<screen name="HbbTVWindow" position="0,0" size="1280,720" backgroundColor="transparent" flags="wfNoBorder" title="HbbTV Plugin">
		</screen>
		"""
	def __init__(self, session, url=None, app_info=None):
		vbcfg.g_position = vbcfg.getPosition()
		vbcfg.osd_lock()

		Screen.__init__(self, session)

		self._url = url
		self._info = app_info

		self.onLayoutFinish.append(self.start_hbbtv_application)

		self._close_timer = eTimer()
		self._close_timer.callback.append(self.stop_hbbtv_application)

		try:
			if self._cb_set_title not in vbcfg.g_main.vbhandler.onSetTitleCB:
				vbcfg.g_main.vbhandler.onSetTitleCB.append(self._cb_set_title)
		except Exception:
			pass

		try:
			if self._cb_close_window not in vbcfg.g_main.vbhandler.onCloseCB:
				vbcfg.g_main.vbhandler.onCloseCB.append(self._cb_close_window)
		except Exception:
			pass

	def _cb_set_title(self, title=None):
		vbcfg.LOG("pate title: %s" % title)
		if title is None:
			return
		self.setTitle(title)

	def _cb_close_window(self):
		self._close_timer.start(1000)

	def start_hbbtv_application(self):
		vbcfg.g_main.vbhandler.soft_volume = -1
		self.setTitle(_('HbbTV Plugin'))
		vbcfg.LOG("Starting HbbTV")

		vbcfg.DEBUG("url : %s" % self._url and self._url)
		vbcfg.DEBUG("info: %s" % self._info and self._info)

		if self._info and self._info["control"] == 1 and vbcfg.g_channel_info is not None:
			os.system("run-webkit.sh restart %s" % (self._info["url"]))
		else:
			if self._url is not None:
				os.system("run-webkit.sh restart %s" % (self._url))
			else:
				os.system("run-webkit.sh restart %s" % (self._info["url"]))


	def stop_hbbtv_application(self):
		self._close_timer.stop()
		self._close_timer = None

		try:
			if self._cb_set_title in vbcfg.g_main.vbhandler.onSetTitleCB:
				vbcfg.g_main.vbhandler.onSetTitleCB.remove(self._cb_set_title)
		except Exception:
			pass

		try:
			if self._cb_close_window in vbcfg.g_main.vbhandler.onCloseCB:
				vbcfg.g_main.vbhandler.onCloseCB.remove(self._cb_close_window)
		except Exception:
			pass

		from enigma import getDesktop, gMainDC
		dsk = getDesktop(0)
		desktop_size = dsk.size()
		gMainDC.getInstance().setResolution(desktop_size.width(), desktop_size.height())

		vbcfg.setPosition(vbcfg.g_position)
		vbcfg.osd_unlock()
		dsk.paint()

		vbcfg.set_bgcolor("0")
		vbcfg.LOG("Stop HbbTV")
		self.close()

