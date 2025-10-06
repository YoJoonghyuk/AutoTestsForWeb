import pytest
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.product_page import ProductPage
from pages.orders_page import OrdersPage
from pages.my_account_page import MyAccountPage
from playwright.sync_api import expect
from data.address import new_address
from data.product_data import product_info
from utils.logger import logger


@pytest.fixture
def home_page(page, config):
    return HomePage(page, config)


@pytest.fixture
def register_page(page, config):
    return RegisterPage(page, config)


@pytest.fixture
def cart_page(page, config):
    return CartPage(page, config)


@pytest.fixture
def checkout_page(page, config):
    return CheckoutPage(page, config)


@pytest.fixture
def product_page(page, config):
    return ProductPage(page, config)


@pytest.fixture
def orders_page(page, config):
    return OrdersPage(page, config)


@pytest.fixture
def my_account_page(page, config):
    return MyAccountPage(page, config)


@pytest.fixture
def fill_checkout_address_form(page, checkout_page):
    """
    Фикстура для заполнения адреса доставки и оплаты на странице оформления заказа.
    """
    def _fill_address(address_type):
        try:
            if address_type == "billing":
                checkout_page.fill_billing_address(
                    country=new_address["country"],
                    city=new_address["city"],
                    address1=new_address["address1"],
                    zip_code=new_address["zip_code"],
                    phone_number=new_address["phone_number"]
                )
                checkout_page.click_continue_billing()
            elif address_type == "shipping":
                page.select_option("#shipping-address-select", "New Address")
                checkout_page.fill_shipping_address(
                    country=new_address["country"],
                    city=new_address["city"],
                    address1=new_address["address1"],
                    zip_code=new_address["zip_code"],
                    phone_number=new_address["phone_number"]
                )
                checkout_page.click_continue_shipping()
            else:
                raise ValueError("Неверный тип адреса. Допустимые значения: 'billing' или 'shipping'.")
        except Exception as e:
            logger.error(f"Ошибка при заполнении формы адреса: {e}")
            raise

    return _fill_address


def test_successful_checkout_with_new_address(page, config, home_page, cart_page, checkout_page, product_page,
                                               registered_page, screenshot_comparer, fill_checkout_address_form, request):
    """ TC_CHECKOUT_001: Проверка успешного оформления заказа с новым адресом."""
    try:
        email, password, page = registered_page
        home_page.goto()
        home_page.search(product_info["product"])
        page.click("div.product-item a")
        product_page.add_to_cart()
        expect(product_page.page.locator(product_page.success_notification)).to_be_visible(timeout=5000)

        home_page.goto_cart()
        expect(cart_page.page.locator(cart_page.termsofservice_checkbox)).to_be_visible(timeout=5000)
        cart_page.accept_term_of_service()
        cart_page.goto_checkout()

        fill_checkout_address_form("billing")
        fill_checkout_address_form("shipping")

        checkout_page.click_shipping_method_next_step()
        checkout_page.click_payment_method_next_step()
        checkout_page.click_payment_info_next_step()

        expect(checkout_page.page.locator(checkout_page.confirm_order_button)).to_be_visible(timeout=5000)

        checkout_page.click_confirm_order()

        expect(page.locator("div.section.order-completed")).to_be_visible(timeout=10000)

        screenshot_name = "checkout/successful_checkout.png"
        request.node.screenshot_name = screenshot_name
        checkout_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"

    except Exception as e:
        logger.error(f"Ошибка при выполнении теста успешного оформления заказа: {e}")
        raise


def test_orders_in_profile(page, config, home_page, cart_page, checkout_page, product_page,
                           orders_page, registered_page, screenshot_comparer, fill_checkout_address_form, request):
    """ TC_CHECKOUT_001: Проверка отображения заказов в профиле пользователя после оформления заказа. """
    try:
        email, password, page = registered_page
        home_page.goto()
        home_page.search(product_info["product"])
        page.click("div.product-item a")
        product_page.add_to_cart()
        expect(product_page.page.locator(product_page.success_notification)).to_be_visible(timeout=5000)

        home_page.goto_cart()
        expect(cart_page.page.locator(cart_page.termsofservice_checkbox)).to_be_visible(timeout=5000)
        cart_page.accept_term_of_service()
        cart_page.goto_checkout()

        fill_checkout_address_form("billing")
        fill_checkout_address_form("shipping")

        checkout_page.click_shipping_method_next_step()
        checkout_page.click_payment_method_next_step()
        checkout_page.click_payment_info_next_step()

        expect(checkout_page.page.locator(checkout_page.confirm_order_button)).to_be_visible(timeout=5000)

        checkout_page.click_confirm_order()
    
        expect(page.locator("div.section.order-completed")).to_be_visible(timeout=10000)

        home_page.goto_account_page(email)
        orders_page.goto_orders()

        expect(page.locator("div.order-list")).to_be_visible(timeout=5000)
        orders_page.has_orders()

        screenshot_name = "checkout/successful_order_page.png"
        request.node.screenshot_name = screenshot_name
        orders_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"

    except Exception as e:
        logger.error(f"Ошибка при проверке отображения заказов в профиле: {e}")
        raise
