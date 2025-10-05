import os
import pytest
import base64
from playwright.sync_api import sync_playwright, Page
from configparser import ConfigParser
from utils.screenshot_comparer import ScreenshotComparer
from utils.logger import logger
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from playwright.sync_api import expect
import logging

from data.user import user_data, registration_data
from utils.helper import generate_random_email, generate_random_string

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ Хук pytest для добавления информации о тесте в отчет HTML """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, "extras", [])

    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            config = item.funcargs['config']  
            actual_screenshot_dir = config.get("DEFAULT", "actual_screenshot_dir")
            file_name = report.nodeid.replace("::", "_") + ".png"
            screenshot_path = os.path.join(actual_screenshot_dir, file_name)

            if os.path.exists(screenshot_path):
                logger.info(f"Найден скриншот для отчета: {screenshot_path}")
                try:
                    with open(screenshot_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

                    extra.append(pytest_html.extras.html(
                        f'<div><img src="data:image/png;base64,{encoded_string}" alt="screenshot" style="width:300px;height:200px;" onclick="window.open(this.src)" align="right"/></div>'
                    ))
                except Exception as e:
                    logger.error(f"Ошибка при чтении файла скриншота: {e}")
            else:
                logger.warning(f"Скриншот не найден: {screenshot_path}")
        report.extras = extra


def pytest_html_results_table_header(cells):
    """  Хук pytest для настройки отображения HTML """
    cells.insert(2, "Description")
    cells.pop()


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f'<td>{report.description}</td>') 
    cells.pop()


@pytest.hookimpl(optionalhook=True) 
def pytest_html_results_summary(prefix):
    prefix.extend(["Optional Summary sentence"])


def pytest_configure(config):
    log_level_str = config.getini('log_level') or 'INFO'
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    logger.setLevel(log_level) 


@pytest.fixture(scope="session")
def config():
    """  Фикстура для чтения конфигурации """
    config = ConfigParser()
    config.read("config/config.ini")
    return config


@pytest.fixture(scope="session")
def playwright(config):
    """  Фикстура для инициализации Playwright """
    with sync_playwright() as p:
        browser_type = config.get("DEFAULT", "browser")
        headless = config.getboolean("DEFAULT", "headless")
        if browser_type == "chromium":
            browser = p.chromium.launch(headless=headless)
        elif browser_type == "firefox":
            browser = p.firefox.launch(headless=headless)
        elif browser_type == "webkit":
            browser = p.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")
        yield browser
        browser.close()


@pytest.fixture
def page(playwright, config, request):
    """ Фикстура для создания страницы """
    browser = playwright
    page = browser.new_page()
    page.set_default_timeout(float(config.get("DEFAULT", "timeout", fallback="10"))) 
    yield page
    page.close()

@pytest.fixture
def screenshot_comparer(config, pytestconfig):  
    """ Фикстура для ScreenshotComparer """
    screenshot_dir = config.get("DEFAULT", "screenshot_dir")
    actual_screenshot_dir = config.get("DEFAULT", "actual_screenshot_dir") 
    threshold = int(config.get("DEFAULT", "threshold"))
    update_snapshots = pytestconfig.getoption("--update-snapshots") 

    return ScreenshotComparer(screenshot_dir, actual_screenshot_dir, threshold, update_snapshots)

def pytest_addoption(parser):
    parser.addoption(
        "--update-snapshots", action="store_true", help="Update baseline screenshots."
    )

@pytest.fixture
def logged_in_page(page: Page, config: ConfigParser):
    """
    Фикстура для автоматического логина пользователя.
    """
    home_page = HomePage(page, config)
    login_page = LoginPage(page, config)

    logger.info("Начало процесса авторизации")
    home_page.goto()
    home_page.goto_login_page()
    login_page.login(user_data["valid"]["email"], user_data["valid"]["password"])
    expect(home_page.page.locator(home_page.logout_link)).to_be_visible(timeout=5000) 
    assert home_page.is_logged_in(), "Ошибка входа"
    logger.info("Успешный вход")
    return page


@pytest.fixture
def registered_page(page: Page, config: ConfigParser):
    """
    Фикстура для автоматической регистрации пользователя.
    """
    home_page = HomePage(page, config)
    register_page = RegisterPage(page, config)

    logger.info("Начало процесса регистрации")
    home_page.goto()
    home_page.goto_register_page()
    email = generate_random_email()
    password = generate_random_string(10)
    register_page.register(
        gender=registration_data["gender"],
        first_name=registration_data["first_name"],
        last_name=registration_data["last_name"],
        email=email,
        password=password,
        confirm_password=password
    )
    try:
        expect(register_page.page.locator(register_page.success_message)).to_be_visible(timeout=5000) 
        assert register_page.is_success_message_visible(), "Ошибка регистрации"
        logger.info("Успешная регистрация")
    except AssertionError as e:
        logger.error(f"Registration failed: {e}") 
        raise  

    yield email, password, page  
