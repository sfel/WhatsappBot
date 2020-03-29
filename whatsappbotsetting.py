from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import whatsapp_web_classnames

GROUP_SETTINGS_XPATH = '//header//div[@role="button"]/parent::div'


class WhatsappBotSettingsBase:
    def __init__(self, bot):
        self.bot = bot
        self.settings()

    def settings(self):
        pass

    def sub_menue(self, choice):
        """ Returns th chosen element from the sub menue - This function must be called after settings is called
            choice is in ['New group', 'Profile', 'Archived', 'Starred', 'Settings', 'Log out'] """
        self.settings['menu'].click()
        return self.bot.driver.find_element_by_xpath(f'//*[contains(text(), "{choice}")]')

    def press_escape(self):
        webdriver.ActionChains(self.bot.driver).send_keys(Keys.ESCAPE).perform()


class WhatsappBotGeneralSettings(WhatsappBotSettingsBase):
    def settings(self):
        settings = dict(zip(['status', 'new_chat', 'general_menu', 'search', 'attach', 'conversation_menu'],
                            self.bot.driver.find_elements_by_xpath(GROUP_SETTINGS_XPATH)))
        self.settings = dict((k, settings[k]) for k in ('status', 'new_chat', 'general_menu'))
        self.settings['menu'] = self.settings.pop('general_menu')

    def write_in_search(self, query):
        """ Types query to the general search box """
        chat_search_bar = self.bot.driver.find_elements_by_xpath(
            '//div[text() = "Search or start new chat"]/following-sibling::label/child::div')[0]
        chat_search_bar.send_keys(query)

    def close_search(self):
        """ Closes the search box """
        webdriver.ActionChains(self.bot.driver).send_keys(Keys.ESCAPE).perform()  # press escape

    def click_on_first_result(self):
        """ Clicks on the first conversation """
        self.bot.driver.find_element_by_class_name(whatsapp_web_classnames.CONVERSATION).click()  # for more options use find_elements... method

    def _get_groups_menu(self):
        """ Returns the groups menu html node """
        return self.driver.find_element_by_xpath('//div[@role="button" and @title="Menu"]/parent::div')[1]


class WhatsappBotConversationSettings(WhatsappBotSettingsBase):
    def settings(self):
        settings = dict(zip(['status', 'new_chat', 'general_menu', 'search', 'attach', 'conversation_menu'],
                            GROUP_SETTINGS_XPATH))
        self.settings = dict((k, settings[k]) for k in ('search', 'attach', 'conversation_menu'))
        self.settings['menu'] = self.settings.pop('conversation_menu')