#encoding=utf-8
import sys
import logging

LOGGER = logging.getLogger(__name__)
class FactoryCreator:

	def __init__(self):
		LOGGER.info('[%s init]' % self.__class__.__name__)

	def getInstance(self, cmd):
		action_name = cmd.capitalize() + 'Action'
		LOGGER.info("[Action Name : %s]" % action_name)

		try:
			action_module = __import__(action_name.lower())
		except:
			action_module = __import__('defaultaction')
			action_name = 'DefaultAction'
			LOGGER.info("[Action Rename to %s]" % action_name)

		action = getattr(action_module, action_name)
		
		return action

if __name__ == '__main__':

	action_module = __import__("defaultaction")
	
	fc = FactoryCreator()
	action = fc.getInstance('default')
	print action