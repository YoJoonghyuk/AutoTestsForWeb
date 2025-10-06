from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from utils.logger import logger

class MyAccountPage(BasePage):
    """
    Класс, представляющий страницу аккаунта пользователя.
    """
    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.page = page
        self.config = config
        self.change_password_link = "a[href='/customer/changepassword']"
        self.orders_link = "a[href='/customer/orders']"
        self.addresses_link = "div.block.block-account-navigation a[href='/customer/addresses']"
        self.addresses_list = "div.address-list"
        self.save_button = "input[value=Save]"
        self.first_name_field = "#FirstName"
        self.last_name_field = "#LastName"
        self.email_field = "#Email"
        self.first_name_error_message = "span[data-valmsg-for='FirstName']"
        self.last_name_error_message = "span[data-valmsg-for='LastName']"
        self.email_error_message = "span[data-valmsg-for='Email']"

    def goto_change_password(self):
        """
        Переходит на страницу изменения пароля.
        """
        try:
            self.click(self.change_password_link, "Change password link")
        except Exception as e:
            logger.error(f"Ошибка при переходе на страницу изменения пароля: {e}")
            raise

    def goto_orders(self):
        """
        Переходит на страницу заказов.
        """
        try:
            self.click(self.orders_link, "Orders link")
        except Exception as e:
            logger.error(f"Ошибка при переходе на страницу заказов: {e}")
            raise

    def goto_addresses(self):
        """
        Переходит на страницу адресов.
        """
        try:
            self.click(self.addresses_link, "Addresses link")
        except Exception as e:
            logger.error(f"Ошибка при переходе на страницу адресов: {e}")
            raise

    def save_profile_changes(self):
        """
        Сохраняет изменения профиля.
        """
        try:
            self.click(self.save_button, "Save profile button")
        except Exception as e:
            logger.error(f"Ошибка при сохранении изменений профиля: {e}")
            raise

    def fill_profile_information(self, first_name="", last_name="", email=""):
        """
        Заполняет информацию профиля.
        """
        try:
            if first_name:
                self.page.fill(self.first_name_field, first_name)
            if last_name:
                self.page.fill(self.last_name_field, last_name)
            if email:
                self.page.fill(self.email_field, email)
        except Exception as e:
            logger.error(f"Ошибка при заполнении информации профиля: {e}")
            raise

    def verify_profile_information(self, expected_first_name, expected_last_name):
        """
        Проверяет, что информация профиля соответствует ожидаемой.
        """
        try:
            expect(self.page.locator(self.first_name_field)).to_have_value(expected_first_name)
            expect(self.page.locator(self.last_name_field)).to_have_value(expected_last_name)
        except Exception as e:
            logger.error(f"Ошибка при проверке информации профиля: {e}")
            raise

    def verify_error_messages_visibility(self):
        """
        Проверяет видимость сообщений об ошибках для обязательных полей.
        """
        try:
            expect(self.page.locator(self.first_name_error_message)).to_be_visible()
            expect(self.page.locator(self.last_name_error_message)).to_be_visible()
            expect(self.page.locator(self.email_error_message)).to_be_visible()
        except Exception as e:
            logger.error(f"Ошибка при проверке видимости сообщений об ошибках: {e}")
            raise
