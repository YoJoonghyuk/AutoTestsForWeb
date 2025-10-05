import pytest
from pages.home_page import HomePage
from pages.category_page import CategoryPage
from playwright.sync_api import expect
from data.product_data import category
from utils.logger import logger


@pytest.fixture
def home_page(page, config):
    return HomePage(page, config)


@pytest.fixture
def category_page(page, config):
    return CategoryPage(page, config)


def test_display_list_of_products_in_category(page, config, home_page, category_page, screenshot_comparer):
    """TC_CATEGORY_001: Отображение списка товаров в категории"""
    try:
        home_page.goto()
        home_page.click_category(category["product_category"])

        expect(category_page.page.locator(category_page.product_grid)).to_be_visible(timeout=5000)
        assert category_page.get_product_count() > 0, "В категории не найдено товаров"
    except Exception as e:
        logger.error(f"Ошибка при отображении списка товаров в категории: {e}")
        raise

    screenshot_name = "category_page/category_page_products_list.png"
    try:
        category_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при сравнении скриншотов: {e}")
        raise
