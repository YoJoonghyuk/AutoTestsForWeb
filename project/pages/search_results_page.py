from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import logger

class SearchResultsPage(BasePage):
    """
    Класс, представляющий страницу результатов поиска.
    """
    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.page = page
        self.config = config
        self.search_results = "div.product-grid"
        self.no_results_message = "strong.result"

    def has_results(self):
        """
        Проверяет, есть ли результаты поиска.
        """
        try:
            return self.is_visible(self.search_results)
        except Exception as e:
            logger.error(f"Ошибка при проверке наличия результатов поиска: {e}")
            raise

    def get_no_results_message(self):
        """
        Возвращает сообщение об отсутствии результатов поиска.
        """
        try:
            return self.get_text(self.no_results_message, "No results message")
        except Exception as e:
            logger.error(f"Ошибка при получении сообщения об отсутствии результатов: {e}")
            raise

    def is_no_results_message_visible(self):
        """
        Проверяет, отображается ли сообщение об отсутствии результатов поиска.
        """
        try:
            return self.is_visible(self.no_results_message)
        except Exception as e:
            logger.error(f"Ошибка при проверке видимости сообщения об отсутствии результатов: {e}")
            raise
