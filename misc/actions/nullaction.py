#encoding=utf-8
from models import Actions

import logging

LOGGER = logging.getLogger(__name__)

class NullAction(Actions):

	def __init__(self):
		Actions.__init__(self);
	
	def doAction(self):
		pass
