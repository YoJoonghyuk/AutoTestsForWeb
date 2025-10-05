import pytest
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from utils.helper import generate_random_email, generate_random_string
from playwright.sync_api import expect
from data.user import user_data, registration_data
from utils.logger import logger


@pytest.fixture
def home_page(page, config):
    return HomePage(page, config)


@pytest.fixture
def register_page(page, config):
    return RegisterPage(page, config)


def test_successful_registration(page, config, home_page, register_page, screenshot_comparer):
    """TC_REGISTER_001: Успешная регистрация пользователя."""
    try:
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

        expect(register_page.page.locator(register_page.success_message)).to_be_visible(timeout=5000)
        assert "Your registration completed" in register_page.get_success_message_text()

        screenshot_name = "register_page/register_page_success.png"
        register_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"

    except Exception as e:
        logger.error(f"Ошибка при выполнении регистрации: {e}")
        raise


def test_registration_with_existing_email(page, config, home_page, register_page, screenshot_comparer):
    """TC_REGISTER_002: Регистрация пользователя с уже существующим email."""
    try:
        home_page.goto()
        home_page.goto_register_page()

        existing_email = user_data["valid"]["email"]
        password = generate_random_string(10)

        register_page.register(
            gender=registration_data["gender"],
            first_name=registration_data["first_name"],
            last_name=registration_data["last_name"],
            email=existing_email,
            password=password,
            confirm_password=password
        )

        expect(register_page.page.locator(register_page.error_message_container)).to_be_visible(timeout=5000)
        assert "The specified email already exists" in register_page.get_specific_error_text()

        screenshot_name = "register_page/register_page_existing_email.png"
        register_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"

    except Exception as e:
        logger.error(f"Ошибка при регистрации с существующим email: {e}")
        raise


def test_registration_with_invalid_email_format(page, config, home_page, register_page, screenshot_comparer):
    """TC_REGISTER_003: Регистрация пользователя с неверным форматом email."""
    try:
        home_page.goto()
        home_page.goto_register_page()

        invalid_email = user_data["invalid"]["invalid_email"]
        password = generate_random_string(10)

        register_page.register(
            gender=registration_data["gender"],
            first_name=registration_data["first_name"],
            last_name=registration_data["last_name"],
            email=invalid_email,
            password=password,
            confirm_password=password
        )

        expect(register_page.page.locator(register_page.error_message)).to_be_visible(timeout=5000)
        assert "Wrong email" in register_page.get_error_message_text('Email')

        screenshot_name = "register_page/register_page_invalid_email.png"
        register_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"

    except Exception as e:
        logger.error(f"Ошибка при регистрации с неверным форматом email: {e}")
        raise


def test_registration_with_empty_required_fields(page, config, home_page, register_page, screenshot_comparer):
    """TC_REGISTER_004: Регистрация пользователя с незаполненными обязательными полями."""
    try:
        home_page.goto()
        home_page.goto_register_page()

        register_page.register(
            gender=user_data["invalid"]["empty"],  
            first_name=user_data["invalid"]["empty"],
            last_name=user_data["invalid"]["empty"],
            email=user_data["invalid"]["empty"],
            password=user_data["invalid"]["empty"],
            confirm_password=user_data["invalid"]["empty"]
        )

        assert "First name is required." in register_page.get_error_message_text('FirstName')
        assert "Last name is required." in register_page.get_error_message_text('LastName')
        assert "Email is required." in register_page.get_error_message_text('Email')
        assert "Password is required." in register_page.get_error_message_text('Password')
        assert "Password is required." in register_page.get_error_message_text('ConfirmPassword')

        screenshot_name = "register_page/register_page_empty_fields.png"
        register_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"

    except Exception as e:
        logger.error(f"Ошибка при регистрации с незаполненными обязательными полями: {e}")
        raise


def test_registration_with_mismatched_passwords(page, config, home_page, register_page, screenshot_comparer):
    """TC_REGISTER_005: Регистрация пользователя в случае неуспешного подтверждения пароля."""
    try:
        home_page.goto()
        home_page.goto_register_page()

        email = generate_random_email()
        password = generate_random_string(10)
        mismatched_password = generate_random_string(11)

        register_page.register(
            gender=registration_data["gender"],
            first_name=registration_data["first_name"],
            last_name=registration_data["last_name"],
            email=email,
            password=password,
            confirm_password=mismatched_password
        )

        expect(register_page.page.locator(register_page.error_message)).to_be_visible(timeout=5000)
        assert "The password and confirmation password do not match." in register_page.get_error_message_text(
            'ConfirmPassword')

        screenshot_name = "register_page/register_page_mismatched_passwords.png"
        register_page.take_screenshot(screenshot_name)
        assert screenshot_comparer.compare_screenshots(screenshot_name), "Скриншоты не совпадают"
    except Exception as e:
        logger.error(f"Ошибка при регистрации с неуспешным подтвержденикм пароля: {e}")
        raise
