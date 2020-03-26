"""
Whatsup Bot

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
PHONE_LIST_FILE = r'.\phones.txt'  # Must end with newline, Assumes phone numbers are valid
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

    def __init__(self):
        self.__connect()

    def send_whatsapp_message(self, bot_msg):
        """ Sends a single WhatsappBotMessage """
        try: 
            self.__open_chat(bot_msg.addressee.chat_link)
            self.__send_message(bot_msg.welcome_msg)
            self.__send_message(bot_msg.invitation_link)
        except exceptions.TimeoutException:
            if len(a.driver.find_elements_by_class_name('_2Vo52')):
                print(f'The message - {bot_msg.invitation_link} - contains bad number')
            else:
                print("Timed out waiting for page to load")

    def send_whatsapp_messages(self, bot_messages):
        """ Sends a collection of WhatsappBotMessage """
        for bot_msg in bot_messages:
            self.send_whatsapp_message(bot_msg)

    def create_group(self, first_contact='', group_name='Group Name'):
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
        wait.until(lambda driver: driver.find_element_by_class_name('ZP8RM')) # wait until the contact search element

    def __click_send(self):
        """Sends a message """
        send_button = self.driver.find_element_by_class_name('_3M-N-')
        send_button.click()

    def __send_message(self, content):
        """ Send's a message """
        msg_box = self.driver.find_elements_by_class_name('_3u328')[1]
        msg_box.send_keys(content)
        self.__click_send()

    def __is_invalid_link(self):
        """ Returns if a chat link what incorrect """
        return 'This link is incorrect. Close this window and try a different link.' in [e.text for e in a.driver.find_elements_by_class_name('_2yzk')]

    def __open_chat(self, chat_link):
        """ Opens a chat with unsaved number"""
        self.driver.get(chat_link)
        if self.__is_invalid_link(): 
            self.driver.execute_script("window.history.go(-1)")
            return
        
        message_button = self.driver.find_element_by_xpath('//a[@title = "Share on WhatsApp"]')
        message_button.click()
        sleep(1)
        use_web_link = self.driver.find_element_by_xpath(f'//a[text() = "use WhatsApp Web"]')
        use_web_link.click()
        wait = WebDriverWait(self.driver, timeout=15)
        wait.until(lambda driver: driver.find_element_by_class_name('_3fs0K')) 





a = None


def main():
    global a
    with open(PHONE_LIST_FILE) as phone_file:
        phones = [n.strip() for n in phone_file.readlines()]  # trim \n
    print(phones)

    group_name = 'Group Name'
    group_number = 12
    # group_to_create = group_name + str(group_number)

    #phones = []  # Enter phones here for testing
    a = WhatsappWebBot()
    bot_messages = [WhatsappBotMessage(phone) for phone in phones]
    # a.send_whatsapp_messages(bot_messages)
    #a.create_group()


if __name__ == "__main__":
    main()
