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
