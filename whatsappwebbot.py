"""
WhatsApp Bot

For debugging use: python -i whatsappwebbot.py
And then debug the driver by using a.driver object
"""
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from whatsappbotgroup import WhatsappBotGroup

DRIVER_PATH = r'.\chromedriver_win32\chromedriver.exe'


class WhatsappBotUser:
    def __init__(self, phone_number, country_prefix='972'):
        self.phone_number = phone_number
        self.chat_link = f'https://api.whatsapp.com/send?phone={country_prefix}{phone_number[1:]}&text='

    def __str__(self):
        return f'WhatsappBotUser({self.phone_number})'

    def __repr__(self):
        return f'WhatsappBotUser(phone={self.phone_number},chat_link={self.chat_link})'


class WhatsappBotMessage:
    def __init__(self, addressee_phone, welcome_msg, invitation_link):
        self.addressee = WhatsappBotUser(addressee_phone)
        self.welcome_msg = welcome_msg.encode('UTF-8').decode('UTF-8')
        self.invitation_link = invitation_link

    def __str__(self):
        return f'WhatsappBotMessage(addressee={str(self.addressee)}, welcome_msg={self.welcome_msg}, ' \
               f'invitation_link={self.invitation_link})'

    def __repr__(self):
        return f'WhatsappBotMessage(addressee={repr(self.addressee)}, welcome_msg={self.welcome_msg}, ' \
               f'invitation_link={self.invitation_link})'


class BadLinkException(Exception):
    pass


class WhatsappWebBot:
    """ Automation class for WhatsApp"""

    def __init__(self):
        self.__connect()

    def send_whatsapp_message(self, bot_msg):
        """ Sends a single WhatsappBotMessage """
        try:
            self.__open_chat(bot_msg.addressee.chat_link)
            self.__send_message(bot_msg.welcome_msg)
            self.__send_message(bot_msg.invitation_link)
        except exceptions.TimeoutException:
            print(f"Timed out waiting for page to load - {bot_msg}")
        except BadLinkException:
            print(f'Bad link for {bot_msg}')

    def send_whatsapp_messages(self, bot_messages):
        """ Sends a collection of WhatsappBotMessage """
        for bot_msg in bot_messages:
            self.send_whatsapp_message(bot_msg)

    def create_group(self, first_contact, group_name):
        """ Creates a group, adds first_contact as admin and returns a link to join the group """
        first_contact = first_contact.encode('UTF-8').decode('UTF-8')
        group_name = group_name.encode('UTF-8').decode('UTF-8')
        group_manager = WhatsappBotGroup(self)
        group_manager.create_group(first_contact=first_contact, group_name=group_name)
        sleep(2)
        group_manager.make_admin(first_contact)
        sleep(2)
        link = group_manager.get_joining_link()
        self.__send_message(link)
        return link

    def __connect(self):
        """ Connects to the browser's driver, Opens whatsapp web and waits for the user to scann the QR code """
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.get('https://web.whatsapp.com/')
        wait = WebDriverWait(self.driver, timeout=60)
        wait.until(lambda driver: driver.find_element_by_xpath(
            "//*[contains(text(), 'Search or start new chat')]"))  # wait until the contact search element

    def __click_send(self):
        """Sends a message """
        send_button = self.driver.find_element_by_xpath("//*[span[@data-icon='send']]")
        send_button.click()

    def __send_message(self, content):
        """ Sends a message """
        msg_box = self.driver.find_element_by_xpath("//*[contains(text(), 'Type a message')]").find_element_by_xpath(
            '../..')
        msg_box.send_keys(content)
        self.__click_send()

    def __is_invalid_link(self):
        """ Returns if a chat link what incorrect """
        return len(self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'This link is incorrect. Close this window and try a different link.')]")) > 0

    def __open_chat(self, chat_link):
        """ Opens a chat with unsaved number"""
        self.driver.get(chat_link)
        if self.__is_invalid_link():
            self.driver.execute_script("window.history.go(-1)")
            raise BadLinkException()
        else:
            message_button = self.driver.find_element_by_xpath('//a[@title = "Share on WhatsApp"]')
            message_button.click()
            sleep(1)
            use_web_link = self.driver.find_element_by_xpath(f'//a[text() = "use WhatsApp Web"]')
            use_web_link.click()

        wait = WebDriverWait(self.driver, timeout=25)
        wait.until(lambda driver: driver.find_element_by_xpath("//*[contains(text(), 'Type a message')]"))
