from pages.base_page import BasePage
from playwright.sync_api import expect
from utils.logger import logger

class CartPage(BasePage):
    """
    Класс, представляющий страницу корзины.
    """
    def __init__(self, page, config):
        super().__init__(page, config)
        self.checkout_button = "button[name='checkout']"
        self.termsofservice_checkbox = "#termsofservice"
        self.update_cart_button = "input[name='updatecart']"
        self.remove_checkbox = "input[name='removefromcart']"
        self.cart_content = "div.order-summary-content"
        self.cart_table = "table.cart"

    def goto_checkout(self):
        """
        Переходит на страницу оформления заказа.
        """
        try:
            self.click(self.checkout_button)
        except Exception as e:
            logger.error(f"Ошибка при переходе на страницу оформления заказа: {e}")
            raise

    def accept_term_of_service(self):
        """
        Принимает условия обслуживания.
        """
        try:
            self.page.check(self.termsofservice_checkbox)
        except Exception as e:
            logger.error(f"Ошибка при принятии условий обслуживания: {e}")
            raise

    def remove_from_cart(self, index=1):
        """
        Удаляет товар из корзины.
        """
        try:
            remove_checkbox = self.page.locator(self.remove_checkbox).nth(index - 1)
            remove_checkbox.check()
        except Exception as e:
            logger.error(f"Ошибка при удалении товара из корзины: {e}")
            raise

    def update_cart(self):
        """
        Обновляет корзину.
        """
        try:
            self.page.click(self.update_cart_button)
        except Exception as e:
            logger.error(f"Ошибка при обновлении корзины: {e}")
            raise

    def is_cart_empty(self):
        """
        Проверяет, пуста ли корзина.
        """
        try:
            expect(self.page.locator(self.cart_content)).to_be_visible(timeout=5000)
            return "Your Shopping Cart is empty!" in self.page.locator(self.cart_content).inner_text()
        except Exception as e:
            logger.error(f"Ошибка при проверке, пуста ли корзина: {e}")
            raise
