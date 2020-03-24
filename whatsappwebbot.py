"""
Whatsup Bot
For dependencies:
- pipenv install selenium
- I used webdriver for chrome version 80 (you can install yours by googling for it)
For debugging use: python -i whatsappwebbot.py
And then debug the driver by using a.driver object
"""
from selenium import webdriver
from time import sleep

DRIVER_PATH = r'.\chromedriver_win32\chromedriver.exe'
PHONE_LIST_FILE=r'.\phones.txt'   # Assumes they are all valid
MSG_TO_SEND = 'בלה בלה בלה'

class WhatsappBotUser:
	def __init__(self, phone_number, country_prefix='972'):
		self.phone_number = phone_number
		self.chat_link = f'https://api.whatsapp.com/send?phone={country_prefix}{phone_number[1:]}&text='

	def __str__(self):
		return f'WhatsappBotUser({self.phone_number})'
	def __repr__(self):
		return f'WhatsappBotUser(phone={self.phone_number},chat_link={self.chat_link})'

class WhatsappBotMessage:
	def __init__(self, addressee_phone, welcome_msg=MSG_TO_SEND, invitation_link='TESTING123 www.google.com'):
		self.addressee = WhatsappBotUser(addressee_phone)
		self.welcome_msg = welcome_msg.encode('UTF-8').decode('UTF-8')
		self.invitation_link = invitation_link

	def __str__(self):
		return f'WhatsappBotMessage(addressee={str(self.addressee)}, welcome_msg={self.welcome_msg}, invitation_link={self.invitation_link})'
	def __repr__(self):
		return f'WhatsappBotMessage(addressee={repr(self.addressee)}, welcome_msg={self.welcome_msg}, invitation_link={self.invitation_link})'

class WhatsappWebBot:
	""" Automation class for whatsup """
	
	def __init__(self, group_name='LinkSendingBot'):
		self.__connect()
		self.group_name = group_name

	def __connect(self):
		self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
		self.driver.get('https://web.whatsapp.com/')
		input('Scan QR code and then enter anything')  # The connection to whatsupweb is the only manual thing you need to do

	def __click_send(self):
	  """Sends a message """
	  send_button = self.driver.find_element_by_class_name('_3M-N-')
	  send_button.click()

	def __enter_spamming_group(self):
		""" Enters the spamming group of the bot """
		user = self.driver.find_element_by_xpath(f'//span[@title = "{self.group_name}"]')
		user.click()

	def __send_welcome_message(self, bot_msg):
		""" Sends the utf8 encoded welcome message """
		send_message_js =  'var event = new InputEvent("input", {bubbles: true});'
		send_message_js += 'var textbox = document.getElementsByClassName("_3u328")[1];'
		send_message_js += f'textbox.textContent = "{bot_msg.welcome_msg}";'
		send_message_js += 'textbox.dispatchEvent(event);'
		send_message_js += 'document.querySelector("button._3M-N-").click()'
		self.driver.execute_script(send_message_js)  # Sends the welcome message (encoded to utf-8)
		

	def __send_link(self, link):
		""" Send's a message """
		msg_box = self.driver.find_elements_by_class_name('_3u328')[1]
		msg_box.send_keys(link)
		self.__click_send()

	def __click_on_last_sent_message(self):
		""" Clicks on the last message that the bot sent """
		self.driver.find_elements_by_class_name('message-out')[-1].click()
		sleep(3)

	def __is_valid_number(self):
		""" Checks for popup window with the text 'Phone number shared via url is invalid.' """
		return len(self.driver.find_elements_by_xpath("//*[contains(text(), 'Phone number shared via url is invalid.')]")) == 0

	def send_whatsapp_message(self, bot_msg):
		""" Sends a single WhatsappBotMessage """
		self.__enter_spamming_group()
		self.__send_link(bot_msg.addressee.chat_link)
		self.__click_on_last_sent_message()
		if self.__is_valid_number():
			self.__send_welcome_message(bot_msg)
			self.__send_link(bot_msg.invitation_link)
		else:
			self.driver.find_element_by_class_name('_2eK7W').click()
			print(f'The message - {bot_msg.invitation_link} - contains bad number')

	def send_whatsapp_messages(self, bot_messages):
		""" Sends a collection of WhatsappBotMessage """
		for bot_msg in bot_messages:
			self.send_whatsapp_message(bot_msg)

a = None
def main():
	global a
	with open(PHONE_LIST_FILE) as phone_file:
		phones = [f'{COUNTRY_PREFIX}{n[1:-1]}' for n in phone_file.readlines()]  # trim \n and first 0 of the number

	print(phones)

	phones = ['']  # Enter phones here for testing
	a = WhatsappWebBot()
	bot_messages = [WhatsappBotMessage(phone) for phone in phones]
	a.send_whatsapp_messages(bot_messages)

if __name__ == "__main__":
	main()
