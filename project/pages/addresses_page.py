from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import logger

class AddressesPage(BasePage):
    """
    Класс, представляющий страницу управления адресами.
    """
    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.page = page
        self.config = config
        self.add_new_address_button = "input.button-1.add-address-button"
        self.address_list = "div.address-list"
        self.edit_address_button = "input.button-2.edit-address-button"
        self.delete_address_button = "input.button-2.delete-address-button"

    def goto_add_new_address(self):
        """
        Переходит на страницу добавления нового адреса.
        """
        try:
            self.click(self.add_new_address_button, "Add new address button")
        except Exception as e:
            logger.error(f"Ошибка при переходе на страницу добавления адреса: {e}")
            raise

    def get_address_count(self):
        """
        Возвращает количество адресов в списке.
        """
        try:
            return len(self.page.locator(self.address_list).locator("div.address-item").all())
        except Exception as e:
            logger.error(f"Ошибка при получении количества адресов: {e}")
            raise

    def click_first_edit_address_button(self):
        """
        Нажимает на кнопку редактирования адреса.
        """
        try:
            self.page.locator(self.edit_address_button).first.click()
        except Exception as e:
            logger.error(f"Ошибка при нажатии на кнопку редактирования адреса: {e}")
            raise

    def click_first_delete_address_button(self):
        """
        Нажимает на кнопку удаления первого адреса.
        """
        try:
            self.page.locator(self.delete_address_button).first.click()
        except Exception as e:
            logger.error(f"Ошибка при нажатии на кнопку удаления адреса: {e}")
            raise
