from whatsappbotsetting import WhatsappBotGeneralSettings, WhatsappBotConversationSettings, WhatsappBotSettingsBase
import win32clipboard
from selenium.webdriver import ActionChains
from selenium.common import exceptions
from time import sleep


class WhatsappBotGroup:
    def __init__(self, bot):
        self.bot = bot

    def __write_text_on_cursor(self, text):
        actions = ActionChains(self.bot.driver)
        actions.send_keys(text)
        actions.perform()

    def create_group(self, first_contact, group_name):
        """ Creates a new group with the bot and a single contact """
        WhatsappBotGeneralSettings(self.bot).sub_menue('New group').click()
        sleep(1)
        self.__write_text_on_cursor(first_contact)  # look for user
        sleep(1)
        self.bot.driver.find_elements_by_xpath(f"//*[contains(text(), '{first_contact}')]")[1].click()  # choose user
        sleep(1)
        self.bot.driver.find_element_by_xpath("//*[span[@data-icon='forward-light']]").click()  # click next
        sleep(1)
        self.__write_text_on_cursor(group_name)  # insert group name
        sleep(1)
        self.bot.driver.find_element_by_xpath("//*[span[@data-icon='checkmark-light']]").click()  # click finish
        sleep(1)

    def make_admin(self, user_name):
        """ Makes user_name a group admin - within that group context  """
        self.__open_group_settings()
        sleep(1)
        user = self.__get_user(user_name)
        actions = ActionChains(self.bot.driver)
        actions.context_click(user).perform()  # right click
        sleep(1)
        self.bot.driver.find_element_by_xpath("//*[contains(text(), 'Make group admin')]").click()  # choose
        sleep(1)
        self.bot.driver.find_element_by_xpath("//*[contains(text(), 'Make group admin')]").click()  # accept
        sleep(1)
        self.__close_group_settings()
        sleep(1)

    def get_joining_link(self):
        """ Returns a group's joining link - within that group context """
        self.__open_group_settings()
        sleep(1)
        self.__invite_to_group_via_link_element().click()
        sleep(1)
        self.bot.driver.find_element_by_xpath(
            "//*[contains(text(), 'Copy link')]").click()  # 'Send link via WhatsApp', 'Copy link','Revoke link'
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
        """ Returns whether group_name exists , if it does it enters """
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
        sleep(1)
        # Check if it is the real name
        return WhatsappBotConversationSettings(self.bot).settings['title'].text.startswith(group_name)

    def get_group_size(self):
        self.__open_group_settings()
        sleep(1)
        try:
            size = int(self.__get_group_info_segment('participants').text.split()[0])
        except exceptions.NoSuchElementException:
            size = 1
        sleep(1)
        self.__close_group_settings()  # the entire group settings
        sleep(1)
        return size

    def __open_group_settings(self):
        WhatsappBotConversationSettings(self.bot).settings['title'].click()

    def __close_group_settings(self):
        WhatsappBotSettingsBase(self.bot).press_escape()

    def __get_group_info_segment(self, query):
        """ Returns the segments of an open group settings """
        group_info = self.bot.driver.find_element_by_xpath(
            "//*[contains(text(), 'Group info')]/../../following-sibling::div")
        return group_info.find_element_by_xpath(f"//*[contains(text(), '{query}')]")

    def __invite_to_group_via_link_element(self):
        """ Returns the element of the open group menue for inviting via link """
        return self.__get_group_info_segment('Invite to group via link')

    def __get_user(self, user_name):
        """ Returns the user element after the group options open """
        return self.__get_group_info_segment(user_name)  # get users
