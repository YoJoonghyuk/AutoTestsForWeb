from pages.base_page import BasePage
from playwright.sync_api import expect
from utils.logger import logger

class OrdersPage(BasePage):
    """
    Класс, представляющий страницу заказов пользователя.
    """
    def __init__(self, page, config):
        super().__init__(page, config)
        self.order_list = "div.order-list"
        self.order_details_button = "input.button-2.order-details-button"
        self.orders_link = "a.inactive[href='/customer/orders']"

    def has_orders(self):
        """
        Проверяет, есть ли у пользователя заказы.
        """
        try:
            return "No orders" not in self.page.locator(self.order_list).inner_text()
        except Exception as e:
            logger.error(f"Ошибка при проверке наличия заказов: {e}")
            raise

    def view_order_details(self):
        """
        Переходит к просмотру деталей первого заказа.
        """
        try:
            self.page.click(self.order_details_button)
        except Exception as e:
            logger.error(f"Ошибка при переходе к деталям заказа: {e}")
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
