from whatsappbotsetting import WhatsappBotGeneralSettings
import win32clipboard
from selenium.webdriver import ActionChains
from selenium.common import exceptions
from time import sleep


class WhatsappBotGroup:
    def __init__(self, bot):
        self.bot = bot

    def click_next(self):
        self.bot.driver.find_element_by_xpath('//span[@data-icon = "forward-light"]/parent::div').click()

    def click_finish(self):
        self.bot.driver.find_element_by_xpath('//span[@data-icon = "checkmark-light"]/parent::div').click()

    def create_group(self, first_contact, group_name):
        """ Creates a new group with the bot and a single contact """
        WhatsappBotGeneralSettings(self.bot).sub_menue()['new_group'].click()
        self.bot.driver.find_element_by_xpath('//input[@placeholder = "Type contact name"]').send_keys(
            first_contact)  # write name
        self.bot.driver.find_element_by_class_name('_2wP_Y').click()  # choose user
        self.click_next()  # click next
        self.bot.driver.find_element_by_class_name('_3F6QL ').send_keys(group_name)  # insert group name
        self.click_finish()  # click finish

    def make_admin(self, user_name):
        """ Makes user_name a group admin - within that group context  """
        self.__open_group_settings()
        sleep(1)
        user = self.__get_user(user_name)
        actions = ActionChains(self.bot.driver)
        actions.context_click(user).perform()  # right click
        sleep(1)
        self.bot.driver.find_element_by_xpath('//div[@role = "button" and @title = "Make group admin"]').click()  # choose
        sleep(1)
        self.bot.driver.find_element_by_xpath('//div[@role = "button" and text() = "Make group admin"]').click()  # accept
        sleep(1)
        self.__close_group_settings()
        sleep(1)

    def get_joining_link(self):
        """ Returns a group's joining link - within that group context """
        self.__open_group_settings()
        sleep(1)
        self.__invite_to_group_via_link_element().click()
        sleep(1)
        {e.text: e for e in self.bot.driver.find_element_by_class_name('rK2ei').find_elements_by_class_name('_26JG5')}[
            'Copy link'].click()  # 'Send link via WhatsApp', 'Copy link','Revoke link'
        sleep(2)
        win32clipboard.OpenClipboard()
        link = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        self.__close_group_settings()  # the copying link settings
        sleep(1)
        self.__close_group_settings()  # the entire group settings
        sleep(1)
        return link

    def enter_group_if_exists(self, group_name):
        """ Returns wether group_name exists , if it does it enters """
        settings = WhatsappBotGeneralSettings(self.bot)
        # Enter group name
        settings.write_in_search(group_name)
        sleep(2)
        try:
            settings.click_on_first_result()
        except exceptions.NoSuchElementException:
            settings.close_search()
            return False
        settings.close_search()
        # Check if it is the real name
        return self.__get_conversation_title_element().text.startswith(group_name)

    def get_group_size(self):
        self.__open_group_settings()
        sleep(1)
        size = len(self.__get_users_in_group())
        sleep(1)
        self.__close_group_settings()  # the entire group settings
        sleep(1)
        return size

    def __get_conversation_title_element(self):
        return self.bot.driver.find_element_by_xpath('//div[@id = "main"]/child::header')

    def __open_group_settings(self):
        self.__get_conversation_title_element().click()

    def __close_group_settings(self):
        self.bot.driver.find_element_by_class_name('qfKkX').click()

    def __get_group_segments(self):
        """ Returns the segments of an open group settings """
        return dict(zip(['header', 'description', 'shared_media', 'options', 'participants', 'exit', 'report'],
                        self.bot.driver.find_elements_by_class_name('_1CRb5')))

    def __invite_to_group_via_link_element(self):
        """ Returns the element of the opeened group menue for inviting via link """
        return {e.text: e for e in self.__get_group_segments()['participants'].find_elements_by_class_name('_2UaNq')}[
            'Invite to group via link']

    def __get_users_in_group(self):
        """ Returns the users from an oppened group settings """
        return self.__get_group_segments()['participants'].find_elements_by_class_name('_2wP_Y')

    def __get_user(self, user_name):
        """ Returns the user element after the group options openned """
        users = self.__get_users_in_group()  # get users
        return [u for u in users if u.text.encode('UTF-8').decode('utf-8').startswith(user_name)][0]
