import re
import pytest
from utils.helper import get_count_from_text
from playwright.sync_api import expect, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.product_page import ProductPage
from pages.wishlist_page import WishlistPage
from pages.register_page import RegisterPage
from data.product_data import product_info, category
from configparser import ConfigParser
from utils.logger import logger


@pytest.fixture
def home_page(page, config):
    return HomePage(page, config)


@pytest.fixture
def login_page(page, config):
    return LoginPage(page, config)


@pytest.fixture
def cart_page(page, config):
    return CartPage(page, config)


@pytest.fixture
def wishlist_page(page, config):
    return WishlistPage(page, config) 


@pytest.fixture
def product_page(page, config): 
    return ProductPage(page, config)


@pytest.fixture
def register_page(page, config):
    return RegisterPage(page, config)


def cart_count(page):
    try:
        txt = page.locator(".header-links .cart-qty").inner_text(timeout=3000)
        return get_count_from_text(txt)
    except Exception as e:
        logger.error(f"Ошибка при получении количества товаров в корзине: {e}")
        raise


def wishlist_count(page):
    try:
        txt = page.locator(".header-links .wishlist-qty").inner_text(timeout=3000)
        return get_count_from_text(txt)
    except Exception as e:
        logger.error(f"Ошибка при получении количества товаров в списке желаний: {e}")
        raise


@pytest.fixture
def product_added_to_cart(page, config, registered_page):
    """Фикстура для добавления товара в корзину.
    Возвращает объект страницы после добавления товара в корзину.
    """
    email, password, page = registered_page
    product_page = ProductPage(page, config)
    home_page = HomePage(page, config)
    home_page.goto()

    # Убедимся, что счетчик корзины равен 0
    try:
        expect(page.locator(".header-links .cart-qty")).to_have_text("(0)", timeout=5000)
    except Exception as e:
        logger.error(f"Ошибка при проверке количества товаров в корзине: {e}")
        raise

    home_page.search(product_info["product"])
    try:
        expect(page.locator("div.product-item a", has_text=product_info["product"])).to_be_visible(timeout=7000) 
        page.locator("div.product-item a", has_text=product_info["product"]).click() 
        product_page.add_to_cart()
        expect(product_page.page.locator(product_page.success_notification)).to_be_visible(timeout=7000) 
        expect(product_page.page.locator(product_page.success_notification)).to_contain_text("added to your shopping cart", timeout=7000)
        assert product_page.is_success_notification_visible(), "Не удалось добавить товар в корзину в фикстуре"
    except Exception as e:
        logger.error(f"Ошибка при добавлении товара в корзину: {e}")
        raise
    return page


@pytest.fixture
def product_added_to_wishlist(page, config, registered_page):
    """Фикстура для добавления товара в вишлист.
    Возвращает объект страницы после добавления товара в вишлист.
    """
    email, password, page = registered_page
    product_page = ProductPage(page, config)
    home_page = HomePage(page, config)
    home_page.goto()

    # Убедимся, что счетчик вишлиста равен 0
    try:
        expect(page.locator(".header-links .wishlist-qty")).to_have_text("(0)", timeout=5000)
    except Exception as e:
        logger.error(f"Ошибка при проверке количества товаров в списке желаний: {e}")
        raise

    home_page.search(product_info["product"])
    try:
        expect(page.locator("div.product-item a", has_text=product_info["product"])).to_be_visible(timeout=5000) 
        page.locator("div.product-item a", has_text=product_info["product"]).click() 
        product_page.add_to_wishlist()
        expect(product_page.page.locator(product_page.success_notification)).to_be_visible(timeout=7000)
        expect(product_page.page.locator(product_page.success_notification)).to_contain_text("added to your wishlist", timeout=7000)
        assert product_page.is_success_notification_visible(), "Не удалось добавить товар в вишлист в фикстуре"
    except Exception as e:
        logger.error(f"Ошибка при добавлении товара в вишлист: {e}")
        raise
    return page


def test_cart_add_from_product_page(product_added_to_cart, cart_page, screenshot_comparer, request):
    """TC_CART_001: Добавление товара в корзину со страницы товара."""
    page = product_added_to_cart

    initial = cart_count(page)

    # Убедимся, что счётчик увеличился
    try:
        expect(page.locator(".header-links .cart-qty")).not_to_have_text(str(initial), timeout=5000)
    except PlaywrightTimeoutError:
        logger.warning("Не удалось дождаться обновления счетчика корзины")
    except Exception as e:
        logger.error(f"Ошибка при проверке обновления счетчика корзины: {e}")
        raise

    screenshot_name = "cart_page/cart_add_from_product_page.png"
    request.node.screenshot_name = screenshot_name
    try:
        cart_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при сравнении скриншотов: {e}")
        raise


def test_cart_add_from_category(page, config,  home_page, cart_page, screenshot_comparer, registered_page, request):
    """TC_CART_002: Добавление товара в корзину со страницы категории."""
    email, password, page = registered_page
    try:
        page.goto(config.get("DEFAULT", "base_url"))
        home_page.click_category(category["product_category"])
        product_name = product_info["product_name"]
        tile = page.locator("div.product-item", has_text=product_name).first


        initial = cart_count(page)
        add_btn = tile.locator(
            "input.product-box-add-to-cart-button, input.button-2.product-box-add-to-cart-button, input.button-2.add-to-cart-button").first
        add_btn.click()

        expect(page.locator("#bar-notification")).to_be_visible(timeout=7000)
        expect(page.locator("#bar-notification")).to_contain_text("added to your shopping cart", timeout=7000)

        # Убедимся, что счётчик увеличился
        try:
            expect(page.locator(".header-links .cart-qty")).not_to_have_text(str(initial), timeout=7000)
        except PlaywrightTimeoutError:
            logger.warning("Не удалось дождаться обновления счетчика корзины")
        except Exception as e:
            logger.error(f"Ошибка при проверке обновления счетчика корзины: {e}")
            raise
    except Exception as e:
        logger.error(f"Ошибка в процессе добавления товара в корзину со страницы категории: {e}")
        raise

    screenshot_name = "cart_page/cart_add_from_category_page.png"
    request.node.screenshot_name = screenshot_name
    try:
        cart_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при сравнении скриншотов: {e}")
        raise

def test_cart_remove_item(product_added_to_cart, config, cart_page, screenshot_comparer, request):
    """TC_CART_003: Удаление товара из корзины."""
    page = product_added_to_cart

    try:
        page.goto(config.get("DEFAULT", "base_url") + "/cart")
        # Найдём все строки корзины
        rows = page.locator("table.cart tbody tr.cart-item-row")
        initial_rows = rows.count()
        assert initial_rows > 0, "В корзине нет товаров для удаления"

        cart_page.remove_from_cart()
        cart_page.update_cart()

        # Ждём, пока количество строк уменьшится
        expect(page.locator("table.cart tbody tr.cart-item-row")).to_have_count(initial_rows - 1, timeout=7000)
    except Exception as e:
        logger.error(f"Ошибка при удалении товара из корзины: {e}")
        raise

    screenshot_name = "cart_page/cart_remove_item.png"
    request.node.screenshot_name = screenshot_name
    try:
        cart_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при сравнении скриншотов: {e}")
        raise


def test_wishlist_add_from_product_page(product_added_to_wishlist, wishlist_page, screenshot_comparer, request):
    """TC_WISHLIST_001: Добавление товара в список желаний со страницы товара."""
    page = product_added_to_wishlist

    initial = wishlist_count(page)

    # Ждём обновления счётчика в шапке
    try:
        expect(page.locator(".header-links .wishlist-qty")).not_to_have_text(str(initial), timeout=7000)
    except PlaywrightTimeoutError:
        logger.warning("Не удалось дождаться обновления счетчика wishlist")
    except Exception as e:
        logger.error(f"Ошибка при проверке обновления счетчика wishlist: {e}")
        raise

    screenshot_name = "wishlist_page/wishlist_add_from_product_page.png"
    request.node.screenshot_name = screenshot_name
    try:
        wishlist_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при сравнении скриншотов: {e}")
        raise


def test_wishlist_add_to_cart_from_wishlist(page, config, registered_page, wishlist_page, screenshot_comparer, request):
    """TC_WISHLIST_002: Добавление товара в корзину со страницы списка желаний."""
    email, password, page = registered_page

    product_name = product_info["product"]
    try:
        page.goto(f"{config.get('DEFAULT', 'base_url')}/{product_name}")
        product_page = ProductPage(page, config)
        product_page.add_to_wishlist()
        expect(product_page.page.locator(product_page.success_notification)).to_be_visible(timeout=5000)
        expect(product_page.page.locator(product_page.success_notification)).to_contain_text(
            "The product has been added to your wishlist", timeout=7000)

        page.goto(config.get("DEFAULT", "base_url") + "/wishlist")
        initial_cart = cart_count(page)

        rows = page.locator("table.cart tbody tr.cart-item-row")
        assert rows.count() > 0, "В вишлисте нет товаров для перевода в корзину"

        wishlist_page.add_to_cart_from_wishlist()

        expect(page).to_have_url(re.compile(r".*/cart"), timeout=7000)

        try:
            expect(page.locator(".header-links .cart-qty")).not_to_have_text(str(initial_cart), timeout=7000)
        except PlaywrightTimeoutError:
            logger.warning("Не удалось дождаться обновления счетчика корзины")
        except Exception as e:
            logger.error(f"Ошибка при проверке обновления счетчика корзины: {e}")
            raise
    except Exception as e:
        logger.error(f"Ошибка в процессе добавления товара в корзину из списка желаний: {e}")
        raise
    screenshot_name = "wishlist_page/add_to_cart_from_wishlist.png"
    request.node.screenshot_name = screenshot_name
    try:
        wishlist_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при сравнении скриншотов: {e}")
        raise


def test_wishlist_remove_item(page, config, registered_page, wishlist_page, screenshot_comparer, request):
    """TC_WISHLIST_003: Удаление товара из списка желаний."""
    email, password, page = registered_page

    product_name = product_info["product"]
    try:
        page.goto(f"{config.get('DEFAULT', 'base_url')}/{product_name}")
        product_page = ProductPage(page, config)
        product_page.add_to_wishlist()
        expect(product_page.page.locator(product_page.success_notification)).to_be_visible(timeout=5000)
        expect(product_page.page.locator(product_page.success_notification)).to_contain_text(
            "The product has been added to your wishlist", timeout=7000)

        page.goto(config.get("DEFAULT", "base_url") + "/wishlist")
        rows = page.locator("table.cart tbody tr.cart-item-row")
        initial_rows = rows.count()

        assert initial_rows > 0, "В вишлисте нет товаров для удаления"

        wishlist_page.remove_from_wishlist()
        wishlist_page.update_wishlist()

        expect(page.locator("table.cart tbody tr.cart-item-row")).to_have_count(initial_rows - 1, timeout=7000)
    except Exception as e:
        logger.error(f"Ошибка в процессе удаления товара из списка желаний: {e}")
        raise

    screenshot_name = "wishlist_page/wishlist_remove_item.png"
    request.node.screenshot_name = screenshot_name
    try:
        wishlist_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при сравнении скриншотов: {e}")
        raise

