from pages.base_page import BasePage
from playwright.sync_api import expect
from utils.logger import logger

class WishlistPage(BasePage):
    """
    Класс, представляющий страницу списка желаний.
    """
    def __init__(self, page, config):
        super().__init__(page, config)
        self.remove_checkbox = "input[name='removefromcart']"
        self.update_wishlist_button = "input[name='updatecart']"
        self.wishlist_content = "div.wishlist-content"
        self.wishlist_table = "table.cart"
        self.add_to_cart_checkbox = "input[name='addtocart']"

    def remove_from_wishlist(self, index=1):
        """
        Удаляет товар из списка желаний.
        """
        try:
            remove_checkbox = self.page.locator(self.remove_checkbox).nth(index - 1)
            remove_checkbox.check()
        except Exception as e:
            logger.error(f"Ошибка при удалении товара из списка желаний: {e}")
            raise

    def update_wishlist(self):
        """
        Обновляет список желаний.
        """
        try:
            self.page.click(self.update_wishlist_button)
        except Exception as e:
            logger.error(f"Ошибка при обновлении списка желаний: {e}")
            raise

    def is_wishlist_empty(self):
        """
        Проверяет, пуст ли список желаний.
        """
        try:
            expect(self.page.locator(self.wishlist_content)).to_be_visible(timeout=5000)
            return "The wishlist is empty!" in self.page.locator(self.wishlist_content).inner_text()
        except Exception as e:
            logger.error(f"Ошибка при проверке, пуст ли список желаний: {e}")
            raise

    def add_to_cart_from_wishlist(self, index=1):
        """
        Добавляет товар из списка желаний в корзину.
        """
        try:
            add_to_cart_checkbox = self.page.locator(self.add_to_cart_checkbox).nth(index - 1)
            add_to_cart_checkbox.check()
            self.page.click("input[name='addtocartbutton']")
        except Exception as e:
            logger.error(f"Ошибка при добавлении товара из списка желаний в корзину: {e}")
            raise
