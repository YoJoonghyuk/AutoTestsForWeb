import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.addresses_page import AddressesPage
from pages.add_address_page import AddAddressPage
from pages.register_page import RegisterPage
from pages.change_password_page import ChangePasswordPage
from utils.helper import generate_random_string
from playwright.sync_api import Page, expect
from data.user import user_data
from utils.logger import logger
from data.address import new_address  


@pytest.fixture
def home_page(page, config):
    return HomePage(page, config)


@pytest.fixture
def login_page(page, config):
    return LoginPage(page, config)


@pytest.fixture
def my_account_page(page, config):
    return MyAccountPage(page, config)


@pytest.fixture
def change_password_page(page, config):
    return ChangePasswordPage(page, config)


@pytest.fixture
def addresses_page(page, config):
    return AddressesPage(page, config)


@pytest.fixture
def add_address_page(page, config):
    return AddAddressPage(page, config)


@pytest.fixture
def register_page(page, config):
    return RegisterPage(page, config)


@pytest.fixture
def filled_address_form(page, config, registered_page, my_account_page, addresses_page, add_address_page):
    """
    Фикстура для заполнения полей адреса 
    """
    email, password, page = registered_page 
    home_page = HomePage(page, config)

    try:
        home_page.goto_account_page(email)
        expect(my_account_page.page.locator(my_account_page.addresses_link)).to_be_visible(timeout=5000)
        my_account_page.goto_addresses()
        expect(addresses_page.page.locator(addresses_page.add_new_address_button)).to_be_visible(
            timeout=5000)  
        addresses_page.goto_add_new_address()

        first_name = generate_random_string(8)
        last_name = generate_random_string(8)

        add_address_page.fill_address_form(
            first_name=first_name,
            last_name=last_name,
            email=email,
            country=new_address["country"],
            city=new_address["city"],
            address1=new_address["address1"],
            zip_code=new_address["zip_code"],
            phone_number=new_address["phone_number"]
        )
        add_address_page.save_address()

        expect(page.locator(my_account_page.addresses_list)).to_be_visible(timeout=5000)  
        expect(page.locator(my_account_page.addresses_list)).to_contain_text(first_name,
                                                                  timeout=5000) 

        return page, email
    except Exception as e:
        logger.error(f"Ошибка при заполнении формы адреса: {e}")
        raise


def test_edit_profile_information_success(page, config, logged_in_page, home_page, my_account_page, screenshot_comparer, request):
    """TC_PROFILE_001: Проверка успешного изменения информации профиля."""
    try:
        page = logged_in_page
        home_page.goto_account_page(user_data["valid"]["email"])

        new_first_name = generate_random_string(8)
        new_last_name = generate_random_string(8)

        my_account_page.fill_profile_information(first_name=new_first_name, last_name=new_last_name)

        my_account_page.save_profile_changes()

        my_account_page.verify_profile_information(expected_first_name=new_first_name,
                                                    expected_last_name=new_last_name)

        screenshot_name = "profile_management/edit_profile_success.png"
        request.node.screenshot_name = screenshot_name
        my_account_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при изменении информации профиля: {e}")
        raise

def test_edit_profile_information_empty_fields(page, config, logged_in_page, home_page, my_account_page, screenshot_comparer, request):
    """TC_PROFILE_002: Проверка ошибки при изменении информации профиля с пустыми полями."""
    try:
        page = logged_in_page
        home_page.goto_account_page(user_data["valid"]["email"])

        page.fill("#FirstName", "")
        page.fill("#LastName", "")
        page.fill("#Email", "")

        my_account_page.save_profile_changes()

        expect(page.locator("span[data-valmsg-for='FirstName']")).to_be_visible()
        expect(page.locator("span[data-valmsg-for='LastName']")).to_be_visible()
        expect(page.locator("span[data-valmsg-for='Email']")).to_be_visible()

        screenshot_name = "profile_management/edit_profile_empty.png"
        request.node.screenshot_name = screenshot_name
        my_account_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при попытке изменить информацию профиля с пустыми полями: {e}")
        raise


def test_edit_profile_information_invalid_email(page, config, logged_in_page, home_page, my_account_page, screenshot_comparer, request):
    """TC_PROFILE_003: Проверка изменения информации профиля с некорректным email."""
    try:
        page = logged_in_page
        home_page.goto_account_page(user_data["valid"]["email"])

        my_account_page.fill_profile_information(email="invalid-email")
        my_account_page.save_profile_changes()
        expect(page.locator("span[data-valmsg-for='Email']")).to_be_visible()

        screenshot_name = "profile_management/edit_invalid_email.png"
        request.node.screenshot_name = screenshot_name
        my_account_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при попытке изменить информацию профиля с некорректным email: {e}")
        raise


def test_add_new_address(page, config, registered_page, addresses_page,
                       filled_address_form, screenshot_comparer, request):
    """TC_ADDRESS_001: Проверка добавления нового адреса."""
    try:
        email, password, page = registered_page
        page, email = filled_address_form

        screenshot_name = "profile_management/add_new_address.png"
        request.node.screenshot_name = screenshot_name
        addresses_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при добавлении нового адреса: {e}")
        raise


def test_edit_existing_address(page, config, registered_page, home_page, my_account_page, addresses_page,
                              add_address_page, screenshot_comparer, filled_address_form, request):
    """TC_ADDRESS_002: Проверка редактирования существующего адреса."""
    try:
        email, password, page = registered_page

        page, email = filled_address_form
        home_page.goto_account_page(email)
        my_account_page.goto_addresses()

        addresses_page.click_first_edit_address_button()

        new_city = generate_random_string(5)
        new_address1 = generate_random_string(10)
        page.fill("#Address_City", new_city)  
        page.fill("#Address_Address1", new_address1) 

        add_address_page.save_address()  
        my_account_page.goto_addresses()

        add_address_page.verify_address_displayed(new_city)

        screenshot_name = "profile_management/edit_existing_address.png"
        request.node.screenshot_name = screenshot_name
        addresses_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при редактировании существующего адреса: {e}")
        raise


def test_delete_existing_address(page, config, registered_page, addresses_page, screenshot_comparer, filled_address_form, request):
    """TC_ADDRESS_003: Проверка удаления существующего адреса."""
    try:
        email, password, page = registered_page
        page, email = filled_address_form

        addresses_page.click_first_delete_address_button()

        expect(page.locator("div.address-list")).not_to_be_empty()

        screenshot_name = "profile_management/delete_existing_address.png"
        request.node.screenshot_name = screenshot_name
        addresses_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при удалении существующего адреса: {e}")
        raise


def test_change_password_success(page, config, logged_in_page, home_page, my_account_page, screenshot_comparer,
                                change_password_page, request):
    """TC_PASSWORD_001: Проверка успешного изменения пароля."""
    try:
        page = logged_in_page

        home_page.goto_account_page(user_data["valid"]["email"])
        my_account_page.goto_change_password()

        change_password_page.change_password(user_data["valid"]["password"], user_data["valid"]["password"],
                                            user_data["valid"]["password"])

        change_password_page.save_password_changes()
        change_password_page.verify_success_message()

        screenshot_name = "profile_management/change_password.png"
        request.node.screenshot_name = screenshot_name
        my_account_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при изменении пароля: {e}")
        raise


def test_change_password_invalid_old_password(page, config, logged_in_page, home_page, my_account_page, screenshot_comparer, change_password_page, request):
    """TC_PASSWORD_002: Проверка ошибки при изменении пароля с неверным старым паролем."""
    try:
        page = logged_in_page
        home_page.goto_account_page(user_data["valid"]["email"])
        my_account_page.goto_change_password()

        change_password_page.change_password("wrong_password", "new_password", "new_password")
        change_password_page.save_password_changes()

        change_password_page.verify_old_password_error()

        screenshot_name = "profile_management/change_password_invalid.png"
        request.node.screenshot_name = screenshot_name
        my_account_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при попытке изменить пароль с неверным старым паролем: {e}")
        raise

def test_change_password_mismatched_new_password(page, config, logged_in_page, home_page, my_account_page, screenshot_comparer, change_password_page, request):
    """TC_PASSWORD_003: Проверка ошибки при изменении пароля в случае неуспешного подтверждения."""
    try:
        page = logged_in_page
        home_page.goto_account_page(user_data["valid"]["email"])
        my_account_page.goto_change_password()

        change_password_page.change_password(user_data["valid"]["password"], "new_password", "different_password")
        change_password_page.save_password_changes()
        change_password_page.verify_new_password_mismatch_error()

        screenshot_name = "profile_management/change_password_mismatched.png"
        request.node.screenshot_name = screenshot_name
        my_account_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при попытке изменить пароль при неуспешном подтверждении: {e}")
        raise
