from playwright.sync_api import Page
from utils.logger import logger
import os

class BasePage:
    """
    Базовый класс для всех страниц.
    """
    def __init__(self, page: Page, config):
        self.page = page
        self.config = config
        self.base_url = config.get("DEFAULT", "base_url")
        self.screenshot_dir = config.get("DEFAULT", "screenshot_dir")

    def goto(self, path=""):
        """
        Переходит по указанному пути
        """
        try:
            url = f"{self.base_url}/{path}"
            logger.info(f"Переход по: {url}")
            self.page.goto(url)
        except Exception as e:
            logger.error(f"Ошибка при переходе на страницу: {e}")
            raise

    def click(self, locator, description=None):
        """
        Кликает на элемент.
        """
        try:
            logger.info(f"Клик на элемент: {description or locator}")
            self.page.locator(locator).click()
        except Exception as e:
            logger.error(f"Ошибка при нажатии на элемент '{description or locator}': {e}")
            raise

    def fill(self, locator, text, description=None):
        """
        Заполняет текстовое поле.
        """
        try:
            logger.info(f"Заполнить '{description or locator}' текстом: {text}")
            self.page.locator(locator).fill(text)
        except Exception as e:
            logger.error(f"Ошибка при заполнении поля '{description or locator}': {e}")
            raise

    def get_text(self, locator, description=None):
        """
        Возвращает текст элемента.
        """
        try:
            text = self.page.locator(locator).inner_text()
            logger.info(f"Получить текст '{description or locator}': {text}")
            return text
        except Exception as e:
            logger.error(f"Ошибка при получении текста из '{description or locator}': {e}")
            raise

    def is_visible(self, locator, description=None):
        """
        Проверяет видимость элемента.
        """
        try:
            logger.info(f"Проверка видимости элемента: {description or locator}")
            return self.page.locator(locator).is_visible()
        except Exception as e:
            logger.error(f"Ошибка при проверке видимости элемента '{description or locator}': {e}")
            raise

    def take_screenshot(self, screenshot_name):
        """
        Делает скриншот страницы и сохраняет его в указанную директорию.
        """
        try:
            actual_screenshot_dir = self.config.get("DEFAULT", "actual_screenshot_dir")
            screenshot_path = os.path.join(actual_screenshot_dir, screenshot_name)
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)  

            logger.info(f"Получен скриншот: {screenshot_path}")
            self.page.screenshot(path=screenshot_path)
            return screenshot_path
        except Exception as e:
            logger.error(f"Ошибка при создании скриншота: {e}")
            raise
