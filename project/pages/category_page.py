from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import logger

class CategoryPage(BasePage):
    """
    Класс, представляющий страницу категории товаров.
    """
    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.page = page
        self.config = config
        self.product_grid = "div.product-grid"
        self.product_items = "div.item-box"

    def get_product_count(self):
        """
        Возвращает количество товаров в категории.
        """
        try:
            return self.page.locator(self.product_items).count()
        except Exception as e:
            logger.error(f"Ошибка при получении количества товаров в категории: {e}")
            raise
    
    def get_product_name(self, index):
        """
        Возвращает имя товара по указанному индексу.
        """
        try:
            locator = f"{self.product_items}:nth-child({index + 1}) h2.product-title a"
            return self.get_text(locator, f"Product Name at index {index}")
        except Exception as e:
            logger.error(f"Ошибка при получении имени товара по индексу {index}: {e}")
            raise

    def goto(self, path):
        """
        Переходит по указанному пути.
        """
        try:
            super().goto(path)
        except Exception as e:
            logger.error(f"Ошибка при переходе по пути '{path}': {e}")
            raise
