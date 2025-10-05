from pages.base_page import BasePage
from playwright.sync_api import expect
from utils.logger import logger

class ProductPage(BasePage):
    """
    Класс, представляющий страницу товара.
    """
    def __init__(self, page, config):
        super().__init__(page, config)
        self.add_to_cart_button = "input.button-1.add-to-cart-button"
        self.add_to_wishlist_button = "input.button-2.add-to-wishlist-button"
        self.success_notification = "#bar-notification"
        self.product_name_locator = "div.product-name h1"
        self.product_price_locator = "div.product-price span"

    def add_to_cart(self):
        """
        Добавляет товар в корзину.
        """
        try:
            self.page.click(self.add_to_cart_button)
        except Exception as e:
            logger.error(f"Ошибка при добавлении товара в корзину: {e}")
            raise

    def add_to_wishlist(self):
        """
        Добавляет товар в список желаний.
        """
        try:
            self.page.click(self.add_to_wishlist_button)
        except Exception as e:
            logger.error(f"Ошибка при добавлении товара в список желаний: {e}")
            raise

    def is_success_notification_visible(self):
        """
        Проверяет, отображается ли уведомление об успехе.
        """
        try:
            return self.page.locator(self.success_notification).is_visible()
        except Exception as e:
            logger.error(f"Ошибка при проверке видимости уведомления об успехе: {e}")
            raise

    def get_success_notification_text(self):
        """
        Возвращает текст уведомления об успехе.
        """
        try:
            return self.page.locator(self.success_notification).inner_text()
        except Exception as e:
            logger.error(f"Ошибка при получении текста уведомления об успехе: {e}")
            raise

    def get_product_name(self):
        """
        Возвращает имя товара.
        """
        try:
            return self.page.locator(self.product_name_locator).inner_text()
        except Exception as e:
            logger.error(f"Ошибка при получении имени товара: {e}")
            raise

    def get_product_price(self):
        """
        Возвращает цену товара.
        """
        try:
            return self.page.locator(self.product_price_locator).inner_text()
        except Exception as e:
            logger.error(f"Ошибка при получении цены товара: {e}")
            raise
