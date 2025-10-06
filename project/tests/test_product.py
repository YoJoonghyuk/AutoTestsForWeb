import pytest
from pages.home_page import HomePage
from pages.category_page import CategoryPage
from pages.product_page import ProductPage
from data.product_data import product_info, category
from utils.logger import logger


@pytest.fixture
def home_page(page, config):
    return HomePage(page, config)


@pytest.fixture
def category_page(page, config):
    return CategoryPage(page, config)


@pytest.fixture
def product_page(page, config):
    return ProductPage(page, config)


def test_display_product_page(page, config, home_page, product_page, screenshot_comparer, request):
    """ PRODUCT_PAGE_001: Проверка отображения страницы товара."""
    try:
        home_page.goto()
        home_page.click_category(category["product_category"])
        product = product_info["product_link"]
        product_page.goto(f"/{product}")

        assert product_page.get_product_name() == product_info["product_name"]
        assert product_page.get_product_price() == product_info["product_price"]

        screenshot_name = "product_page/product_page_display.png"
        request.node.screenshot_name = screenshot_name
        product_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают" 

    except Exception as e:
        logger.error(f"Ошибка при проверке отображения страницы товара: {e}")
        raise
