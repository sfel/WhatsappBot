from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class WhatsappBotSettingsBase:
    def __init__(self, bot):
        self.bot = bot
        self.settings()

    def settings(self):
        pass


class WhatsappBotGeneralSettings(WhatsappBotSettingsBase):
    def settings(self):
        settings = dict(zip(['status', 'new_chat', 'general_menu', 'search', 'attach', 'conversation_menu'],
                            self.bot.driver.find_elements_by_class_name('_3j8Pd')))
        self.settings = dict((k, settings[k]) for k in ('status', 'new_chat', 'general_menu'))
        self.settings['menu'] = self.settings.pop('general_menu')

    def sub_menue(self):
        """ Returns dictionary of sub menue - This function must be called after settings is called """
        self.settings['menu'].click()
        return dict(zip(['new_group', 'profile', 'archieved', 'starred', 'settings', 'log_out'],
                        self.bot.driver.find_elements_by_class_name('_3cfBY')))

    def write_in_search(self, quary):
        """ Types quary to the general search box """
        self.bot.driver.find_element_by_class_name('eiCXe').find_element_by_class_name('_3u328').send_keys(quary)

    def close_search(self):
        """ Closes the search box """
        webdriver.ActionChains(self.bot.driver).send_keys(Keys.ESCAPE).perform()  #  press escape

    def click_on_first_result(self):
        """ Clicks on the first conversation """
        self.bot.driver.find_element_by_class_name('_3vpWv').click()  # for more options use find_elements... method


class WhatsappBotConversationSettings(WhatsappBotSettingsBase):
    def settings(self):
        settings = dict(zip(['status', 'new_chat', 'general_menu', 'search', 'attach', 'conversation_menu'],
                            self.bot.driver.find_elements_by_class_name('_3j8Pd')))
        self.settings = dict((k, settings[k]) for k in ('search', 'attach', 'conversation_menu'))
        self.settings['menu'] = self.settings.pop('conversation_menu')

    def sub_menue(self):
        """ Returns dictionary of sub menue - This function must be called after settings is called """
        self.settings['menu'].click()
        return dict(zip(['new_group', 'profile', 'archieved', 'starred', 'settings', 'log_out'],
                        self.bot.driver.find_elements_by_class_name('_3cfBY')))
