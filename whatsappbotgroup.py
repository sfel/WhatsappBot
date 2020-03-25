from whatsappbotsetting import WhatsappBotGeneralSettings
import win32clipboard
from selenium.webdriver import ActionChains
from time import sleep


class WhatsappBotGroup:
	def __init__(self, bot):
		self.bot = bot

	def click_next(self):
		self.bot.driver.find_element_by_class_name('_1g8sv').click() 

	def __open_group_settings(self):
		self.bot.driver.find_element_by_class_name('_3V5x5').click()

	def __close_group_settings(self):
		self.bot.driver.find_element_by_class_name('qfKkX').click() 

	def __get_group_segments(self):
		""" Returns the segments of an oppened group settings """
		return dict(zip(['header', 'description', 'shared_media','options', 'participants', 'exit', 'report'],
				    self.bot.driver.find_elements_by_class_name('_2LSbZ')))

	def __invite_to_group_via_link_element(self):
		""" Returns the element of the opeened group menue for inviting via link """
		return {e.text:e for e in self.__get_group_segments()['participants'].find_elements_by_class_name('_2UaNq')}['Invite to group via link']

	def __get_user(self, user_name):
		""" Returns the user element after the group options openned """
		users = self.__get_group_segments()['participants'].find_elements_by_class_name('X7YrQ')  # get users
		return [u for u in users if u.text.encode('UTF-8').decode('utf-8').startswith(user_name)][0]

	def create_group(self,  first_contact, group_name):
		""" Creates a new group with the bot and a single contact """
		WhatsappBotGeneralSettings(self.bot).sub_menue()['new_group'].click()
		self.bot.driver.find_element_by_class_name('_44uDJ').send_keys(first_contact)  # write name
		self.bot.driver.find_element_by_class_name('_2UaNq').click()  # choose user 
		self.click_next()  # click next
		self.bot.driver.find_element_by_class_name('_7w-84').send_keys(group_name)  # insert group name
		self.click_next()  # click finish
		
	def make_admin(self, user_name):
		""" Makes user_name a group admin - within that group context  """
		self.__open_group_settings()
		sleep(1)
		user = self.__get_user(user_name)
		actions = ActionChains(self.bot.driver)
		actions.context_click(user).perform()  # right click
		sleep(1)
		{e.text:e for e in  self.bot.driver.find_elements_by_class_name('_3cfBY')}['Make group admin'].click()  # choose
		sleep(1)
		{e.text:e for e in  self.bot.driver.find_elements_by_class_name('_2eK7W')}['MAKE GROUP ADMIN'].click()  # accept
		sleep(1)
		self.__close_group_settings()
		sleep(1)

	def get_joining_link(self):
		""" Returns a group's joining link - within that group context """
		self.__open_group_settings()
		sleep(1)
		self.__invite_to_group_via_link_element().click()
		sleep(1)
		{e.text:e for e in self.bot.driver.find_element_by_class_name('rK2ei').find_elements_by_class_name('_26JG5')}['Copy link'].click() # 'Send link via WhatsApp', 'Copy link','Revoke link'
		sleep(3)
		win32clipboard.OpenClipboard()
		link = win32clipboard.GetClipboardData()
		win32clipboard.CloseClipboard()
		self.__close_group_settings()  # the copying link settings
		self.__close_group_settings()  # the entire group settings
		return link