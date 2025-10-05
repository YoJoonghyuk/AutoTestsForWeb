from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from utils.logger import logger

class RegisterPage(BasePage):
    """
    Класс, представляющий страницу регистрации пользователя.
    """
    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.page = page
        self.config = config
        self.gender_male_radio = "#gender-male"
        self.gender_female_radio = "#gender-female"
        self.first_name_field = "#FirstName"
        self.last_name_field = "#LastName"
        self.email_field = "#Email"
        self.password_field = "#Password"
        self.confirm_password_field = "#ConfirmPassword"
        self.register_button = "input.button-1.register-next-step-button"
        self.success_message = "div.result"
        self.error_message_container = "div.validation-summary-errors"
        self.error_message ="span.field-validation-error"

    def register(self, gender, first_name, last_name, email, password, confirm_password):
        """
        Регистрирует нового пользователя.
        """
        try:
            if gender == "male":
                self.click(self.gender_male_radio, "Male radio")
            elif gender == "female":
                self.click(self.gender_female_radio, "Female radio")
            self.fill(self.first_name_field, first_name, "First Name field")
            self.fill(self.last_name_field, last_name, "Last Name field")
            self.fill(self.email_field, email, "Email field")
            self.fill(self.password_field, password, "Password field")
            self.fill(self.confirm_password_field, confirm_password, "Confirm Password field")
            self.click(self.register_button, "Register button")
        except Exception as e:
            logger.error(f"Ошибка при регистрации пользователя: {e}")
            raise

    def get_success_message_text(self):
        """
        Возвращает текст сообщения об успешной регистрации.
        """
        try:
            return self.get_text(self.success_message, "Success message")
        except Exception as e:
            logger.error(f"Ошибка при получении текста сообщения об успехе: {e}")
            raise

    def is_success_message_visible(self):
        """
        Проверяет, отображается ли сообщение об успешной регистрации.
        """
        try:
            return self.is_visible(self.success_message)
        except Exception as e:
            logger.error(f"Ошибка при проверке видимости сообщения об успехе: {e}")
            raise

    def get_error_message_text(self, field):
        """
        Возвращает текст сообщения об ошибке для указанного поля.
        """
        try:
            locator = f"span.field-validation-error[data-valmsg-for='{field}']"
            expect(self.page.locator(locator)).to_be_visible(timeout=5000)
            if self.page.locator(locator).count() > 0:
                return self.get_text(locator, f"Error message for {field}")
            else:
                return ""
        except Exception as e:
            logger.error(f"Ошибка при получении текста сообщения об ошибке для поля '{field}': {e}")
            raise

    def is_error_message_visible(self):
        """
        Проверяет, отображается ли контейнер с общими сообщениями об ошибках.
        """
        try:
            return self.is_visible("self.error_message_container")
        except Exception as e:
            logger.error(f"Ошибка при проверке видимости контейнера с сообщениями об ошибках: {e}")
            raise

    def get_specific_error_text(self):
        """
        Получает текст из общего контейнера с ошибками.
        """
        try:
            return self.get_text("div.validation-summary-errors ul li", "Specific error message")
        except Exception as e:
            logger.error(f"Ошибка при получении текста из общего контейнера с ошибками: {e}")
            raise
