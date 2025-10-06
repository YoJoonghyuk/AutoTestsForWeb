import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from data.user import user_data
from utils.logger import logger


@pytest.fixture
def home_page(page, config):
    return HomePage(page, config)


@pytest.fixture
def login_page(page, config):
    return LoginPage(page, config)


def test_successful_login(page, config, home_page, login_page, screenshot_comparer, request):
    """ LOGIN_001: Успешный логин"""
    try:
        home_page.goto()
        home_page.goto_login_page()

        login_page.login(user_data["valid"]["email"], user_data["valid"]["password"])

        assert home_page.is_logged_in(), "Ошибка входа"

        screenshot_name = "login_page/login_page_success.png"
        request.node.screenshot_name = screenshot_name
        home_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при выполнении успешного логина: {e}")
        raise


def test_login_with_incorrect_password(page, config, home_page, login_page, screenshot_comparer, request):
    """ LOGIN_002: Логин с некорректным паролем"""
    try:
        home_page.goto()
        home_page.goto_login_page()

        login_page.login(user_data["valid"]["email"], user_data["invalid"]["password"])
        assert login_page.is_error_message_visible(), "Сообщение об ошибке не найдено"
        assert "Login was unsuccessful" in login_page.get_error_message_text(), "Сообщение об ошибке не найдено"
        
        screenshot_name = "login_page/login_page_incorrect_password.png"
        request.node.screenshot_name = screenshot_name
        home_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"

    except Exception as e:
        logger.error(f"Ошибка при выполнении логина с некорректным паролем: {e}")
        raise


def test_login_with_empty_fields(page, config, home_page, login_page, screenshot_comparer, request):
    """ LOGIN_003:Логин с пустыми полями"""
    try:
        home_page.goto()
        home_page.goto_login_page()

        login_page.login(user_data["invalid"]["empty"], user_data["invalid"]["empty"])
        assert login_page.is_error_message_visible(), "Сообщение об ошибке не найдено"

        screenshot_name = "login_page/login_page_empty_fields.png"
        request.node.screenshot_name = screenshot_name

        home_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при выполнении логина с пустыми полями: {e}")
        raise


def test_login_with_nonexistent_email(page, config, home_page, login_page, screenshot_comparer, request):
    """ LOGIN_004: Логин с несуществующим email"""
    try:
        home_page.goto()
        home_page.goto_login_page()

        login_page.login(user_data["invalid"]["email"], user_data["valid"]["password"])
        assert login_page.is_error_message_visible(), "Сообщение об ошибке не найдено"
        assert "Login was unsuccessful" in login_page.get_error_message_text(), "Сообщение об ошибке не найдено"

        screenshot_name = "login_page/login_page_nonexistent_email.png"
        request.node.screenshot_name = screenshot_name
        home_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при выполнении логина с несуществующим email: {e}")
        raise



def test_logout(page, config, home_page, screenshot_comparer, request):
    """ LOGIN_005: Выход из системы"""
    try:
        home_page.goto()
        home_page.goto_login_page()
        login_page = LoginPage(page, config)  
        login_page.login(user_data["valid"]["email"], user_data["valid"]["password"])
        assert home_page.is_logged_in(), "Ошибка входа"

        home_page.logout()

        assert not home_page.is_logged_in(), "Ошибка выхода"

        screenshot_name = "login_page/logout_page_success.png"
        request.node.screenshot_name = screenshot_name

        home_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при выполнении выхода из системы: {e}")
        raise

