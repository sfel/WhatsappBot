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
COUNTRY_PREFIX = '972'

class WhatsupWebBot:
	""" Automation class for whatsup """
	group_name = 'LinkSendingBot'
	link_to_send = 'TESTING123 www.google.com' # Dont forget to update it to whatever you want to send
	welcome_msg = 'בלה בלה בלה'.encode('UTF-8').decode('UTF-8')

	def __init__(self, phone_numbers):
		self.__connect()
		self.links_to_chats = [f'https://api.whatsapp.com/send?phone={number}&text=' for number in phone_numbers]

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
		user = self.driver.find_element_by_xpath(f'//span[@title = "{WhatsupWebBot.group_name}"]')
		user.click()

	def send_message_with_link(self, link):
		send_message_js =  'var event = new InputEvent("input", {bubbles: true});'
		send_message_js += 'var textbox = document.getElementsByClassName("_3u328")[1];'
		send_message_js += f'textbox.textContent = "{WhatsupWebBot.welcome_msg}";'
		send_message_js += 'textbox.dispatchEvent(event);'
		send_message_js += 'document.querySelector("button._3M-N-").click()'
		self.driver.execute_script(send_message_js)  # Sends the welcome message (encoded to utf-8)
		self.__send_link(link)

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

	def run(self):
		for link in self.links_to_chats:
			self.__enter_spamming_group()
			self.__send_link(link)
			self.__click_on_last_sent_message()
			if self.__is_valid_number():
				self.send_message_with_link(WhatsupWebBot.link_to_send)
			else:
				self.driver.find_element_by_class_name('_2eK7W').click()
				print(f'The message - {link} - contains bad number')
a = None
def main():
	global a
	with open(PHONE_LIST_FILE) as phone_file:
		phones = [f'{COUNTRY_PREFIX}{n[1:-1]}' for n in phone_file.readlines()]  # trim \n and first 0 of the number

	print(phones)

	phones = ['']  # Enter phones here for testing
	a = WhatsupWebBot(phones)
	#WhatsupWebBot.link_to_send = MSG_TO_SEND
	a.run()

if __name__ == "__main__":
	main()
