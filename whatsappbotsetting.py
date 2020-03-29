from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

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
        return self.bot.driver.find_element_by_xpath(f"//*[contains(text(), '{choice}')]")

    def press_escape(self):
        webdriver.ActionChains(self.bot.driver).send_keys(Keys.ESCAPE).perform()


class WhatsappBotGeneralSettings(WhatsappBotSettingsBase):
    def settings(self):
        self.settings = {'status' : self.bot.driver.find_element_by_xpath("//*[contains(@title, 'Status')]"),
                         'new_chat' : self.bot.driver.find_element_by_xpath("//*[contains(@title, 'New chat')]")}
        self.settings['menu'] =  self.settings['new_chat'].find_element_by_xpath("../following-sibling::div")


    def write_in_search(self, quary):
        """ Types quary to the general search box """
        self.bot.driver.find_element_by_xpath("//*[contains(text(), 'Search or start new chat')]/..").click()
        actions = ActionChains(self.bot.driver)
        actions.send_keys(quary)
        actions.perform()

    def close_search(self):
        """ Closes the search box """
        self.press_escape()

    def click_on_first_result(self):
        """ Clicks on the first conversation """
        self.bot.driver.find_element_by_xpath("//*[contains(text(), 'Chats')]").click()


class WhatsappBotConversationSettings(WhatsappBotSettingsBase):
    def settings(self):
        self.settings = {'search' : self.bot.driver.find_element_by_xpath("//*[contains(@title, 'Search')]"),
                         'attach' : self.bot.driver.find_element_by_xpath("//*[contains(@title, 'Attach')]")}
        self.settings['menu'] =  self.settings['attach'].find_element_by_xpath("../following-sibling::div")
        self.settings['title'] =  self.settings['search'].find_element_by_xpath("../../../preceding-sibling::div/following-sibling::div")


