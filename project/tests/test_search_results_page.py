import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from playwright.sync_api import expect
from data.search_data import search_terms
from utils.logger import logger


@pytest.fixture
def home_page(page, config):
    return HomePage(page, config)


@pytest.fixture
def search_results_page(page, config):
    return SearchResultsPage(page, config)


def test_search_existing_product(page, config, home_page, search_results_page, screenshot_comparer):
    """TC_SEARCH_001: Проверка поиска существующего товара."""
    try:
        search_term = search_terms["existing_product"]
        home_page.goto()
        home_page.search(search_term)

        expect(search_results_page.page.locator(search_results_page.search_results)).to_be_visible(timeout=5000)
        assert search_results_page.has_results()

        screenshot_name = "search_page/search_existing_product.png"
        search_results_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при поиске существующего товара: {e}")
        raise


def test_search_nonexistent_product(page, config, home_page, search_results_page, screenshot_comparer):
    """TC_SEARCH_002: Проверка поиска несуществующего товара."""
    try:
        search_term = search_terms["nonexistent_product"]
        home_page.goto()
        home_page.search(search_term)

        expect(search_results_page.page.locator(search_results_page.no_results_message)).to_be_visible(timeout=5000)
        assert search_results_page.get_no_results_message() == "No products were found that matched your criteria."

        screenshot_name = "search_page/search_nonexistent_product.png"
        search_results_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при поиске несуществующего товара: {e}")
        raise


def test_search_empty_query(page, config, home_page, search_results_page, screenshot_comparer):
    """TC_SEARCH_003:  Проверка поиска с пустым запросом."""
    try:
        home_page.goto()
        search_term = search_terms["empty_query"]
        home_page.search(search_term)

        expect(search_results_page.page.locator(search_results_page.search_results)).to_be_visible(timeout=5000)
        
        screenshot_name = "search_page/search_empty_query.png"
        search_results_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при поиске с пустым запросом: {e}")
        raise
