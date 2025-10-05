from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from utils.logger import logger

class AddAddressPage(BasePage):
    """
    Класс, представляющий страницу добавления адреса.
    """
    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.page = page
        self.config = config
        self.first_name_field = "#Address_FirstName"
        self.last_name_field = "#Address_LastName"
        self.email_field = "#Address_Email"
        self.country_dropdown = "#Address_CountryId"
        self.city_field = "#Address_City"
        self.address1_field = "#Address_Address1"
        self.zip_code_field = "#Address_ZipPostalCode"
        self.phone_number_field = "#Address_PhoneNumber"
        self.save_button = "input.button-1.save-address-button"
        self.address_list = "div.address-list"

    def fill_address_form(self, first_name, last_name, email, country, city, address1, zip_code, phone_number):
        """
        Заполняет форму добавления адреса.
        """
        try:
            self.page.fill(self.first_name_field, first_name)
            self.page.fill(self.last_name_field, last_name)
            self.page.fill(self.email_field, email)
            self.page.select_option(self.country_dropdown, country)
            self.page.fill(self.city_field, city)
            self.page.fill(self.address1_field, address1)
            self.page.fill(self.zip_code_field, zip_code)
            self.page.fill(self.phone_number_field, phone_number)
        except Exception as e:
            logger.error(f"Ошибка при заполнении формы адреса: {e}")
            raise

    def save_address(self):
        """
        Сохраняет адрес.
        """
        try:
            self.click(self.save_button)
        except Exception as e:
            logger.error(f"Ошибка при сохранении адреса: {e}")
            raise

    def verify_address_displayed(self, expected_city):
        """
        Проверяет, что адрес отображается на странице.
        """
        try:
            expect(self.page.locator(self.address_list)).to_contain_text(expected_city)
        except Exception as e:
            logger.error(f"Ошибка при проверке отображения адреса: {e}")
            raise
