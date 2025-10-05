from pages.base_page import BasePage
from playwright.sync_api import Page
from utils.logger import logger

class HomePage(BasePage):
    """
    Класс, представляющий главную страницу.
    """
    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.page = page
        self.config = config
        self.register_link = "a.ico-register"
        self.login_link = "a.ico-login"
        self.logout_link = "a.ico-logout"
        self.account_link = "a[href='/customer/info']"
        self.search_field = "#small-searchterms"
        self.search_button = "input.button-1.search-box-button"
        self.ico_cart = "#topcartlink a.ico-cart"
        self.ico_wishlist = "a.ico-wishlist"
        self.category = "ul.top-menu > li > a[href='/{category_name}']"

    def goto(self):
        """
        Переходит на главную страницу.
        """
        try:
            super().goto()
        except Exception as e:
            logger.error(f"Ошибка при переходе на главную страницу: {e}")
            raise

    def goto_register_page(self):
        """
        Переходит на страницу регистрации.
        """
        try:
            self.click(self.register_link, "Register link")
        except Exception as e:
            logger.error(f"Ошибка при переходе на страницу регистрации: {e}")
            raise

    def goto_login_page(self):
        """
        Переходит на страницу входа.
        """
        try:
            self.click(self.login_link, "Login link")
        except Exception as e:
            logger.error(f"Ошибка при переходе на страницу входа: {e}")
            raise

    def is_logged_in(self):
        """
        Проверяет, залогинен ли пользователь.
        """
        try:
            return self.is_visible(self.logout_link)
        except Exception as e:
            logger.error(f"Ошибка при проверке, залогинен ли пользователь: {e}")
            raise

    def logout(self):
        """
        Выходит из системы.
        """
        try:
            self.click(self.logout_link, "Logout link")
        except Exception as e:
            logger.error(f"Ошибка при выходе из системы: {e}")
            raise

    def goto_account_page(self, email):
        """
        Переходит на страницу аккаунта пользователя.
        """
        try:
            account = f'{self.account_link}:text("{email}")'
            self.click(account, 'Account link with email')
        except Exception as e:
            logger.error(f"Ошибка при переходе на страницу аккаунта: {e}")
            raise

    def search(self, term):
        """
        Выполняет поиск товара.
        """
        try:
            self.fill(self.search_field, term, "Search field")
            self.click(self.search_button, "Search button")
        except Exception as e:
            logger.error(f"Ошибка при выполнении поиска: {e}")
            raise

    def goto_cart(self):
        """
        Переходит в корзину.
        """
        try:
            self.click(self.ico_cart, "Cart link")
        except Exception as e:
            logger.error(f"Ошибка при переходе в корзину: {e}")
            raise

    def goto_wishlist(self):
        """
        Переходит в список желаний.
        """
        try:
            self.click(self.ico_wishlist, "Wishlist link")
        except Exception as e:
            logger.error(f"Ошибка при переходе в список желаний: {e}")
            raise

    def click_category(self, category_name: str):
        """
        Переходит в указанную категорию.
        """
        try:
            selector = self.category.format(category_name=category_name)
            self.click(selector, f"{category_name} category link")
        except Exception as e:
            logger.error(f"Ошибка при переходе в категорию '{category_name}': {e}")
            raise
