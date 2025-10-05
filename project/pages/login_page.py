from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import logger

class LoginPage(BasePage):
    """
    Класс, представляющий страницу входа в систему.
    """
    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.page = page
        self.config = config
        self.email_field = "#Email"
        self.password_field = "#Password"
        self.login_button = "input.button-1.login-button"
        self.error_message = "div.message-error"


    def login(self, email, password):
        """
        Выполняет вход в систему с указанным email и паролем.
        """
        try:
            self.fill(self.email_field, email, "Email field")
            self.fill(self.password_field, password, "Password field")
            self.click(self.login_button, "Login button")
        except Exception as e:
            logger.error(f"Ошибка при попытке входа в систему: {e}")
            raise

    def get_error_message_text(self):
        """
        Возвращает текст сообщения об ошибке.
        """
        try:
            return self.get_text(self.error_message, "Error message")
        except Exception as e:
            logger.error(f"Ошибка при получении текста сообщения об ошибке: {e}")
            raise

    def is_error_message_visible(self):
        """
        Проверяет, отображается ли сообщение об ошибке.
        """
        try:
            return self.is_visible(self.error_message, "Error message")
        except Exception as e:
            logger.error(f"Ошибка при проверке видимости сообщения об ошибке: {e}")
            raise
