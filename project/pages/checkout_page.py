from pages.base_page import BasePage
from playwright.sync_api import expect
from utils.logger import logger

class CheckoutPage(BasePage):
    """
    Класс, представляющий страницу оформления заказа.
    """
    def __init__(self, page, config):
        super().__init__(page, config)
        self.billing_country_dropdown = "#BillingNewAddress_CountryId"
        self.billing_city_field = "#BillingNewAddress_City"
        self.billing_address1_field = "#BillingNewAddress_Address1"
        self.billing_zip_code_field = "#BillingNewAddress_ZipPostalCode"
        self.billing_phone_number_field = "#BillingNewAddress_PhoneNumber"

        self.shipping_country_dropdown = "#ShippingNewAddress_CountryId"
        self.shipping_city_field = "#ShippingNewAddress_City"
        self.shipping_address1_field = "#ShippingNewAddress_Address1"
        self.shipping_zip_code_field = "#ShippingNewAddress_ZipPostalCode"
        self.shipping_phone_number_field = "#ShippingNewAddress_PhoneNumber"

        self.continue_billing_button = "#billing-buttons-container input[value='Continue']"
        self.continue_shipping_button = "#shipping-buttons-container input[value='Continue']"
        self.shipping_method_next_step = "input.button-1.shipping-method-next-step-button"
        self.payment_method_next_step = "input.button-1.payment-method-next-step-button"
        self.payment_info_next_step = "input.button-1.payment-info-next-step-button"
        self.confirm_order_button = "input.button-1.confirm-order-next-step-button"
        self.order_success_message = "div.section.order-completed div.title strong"

    def fill_billing_address(self, country, city, address1, zip_code, phone_number):
        """
        Заполняет форму адреса для выставления счета.
        """
        try:
            self.page.select_option(self.billing_country_dropdown, country)
            self.page.fill(self.billing_city_field, city)
            self.page.fill(self.billing_address1_field, address1)
            self.page.fill(self.billing_zip_code_field, zip_code)
            self.page.fill(self.billing_phone_number_field, phone_number)
        except Exception as e:
            logger.error(f"Ошибка при заполнении адреса для выставления счета: {e}")
            raise

    def fill_shipping_address(self, country, city, address1, zip_code, phone_number):
        """
        Заполняет форму адреса доставки.
        """
        try:
            self.page.select_option(self.shipping_country_dropdown, country)
            self.page.fill(self.shipping_city_field, city)
            self.page.fill(self.shipping_address1_field, address1)
            self.page.fill(self.shipping_zip_code_field, zip_code)
            self.page.fill(self.shipping_phone_number_field, phone_number)
        except Exception as e:
            logger.error(f"Ошибка при заполнении адреса доставки: {e}")
            raise

    def click_continue_billing(self):
        """
        Нажимает кнопку следующего шага на шаге выставления счета.
        """
        try:
            self.page.click(self.continue_billing_button)
            expect(self.page.locator("#opc-shipping")).to_be_visible(timeout=5000)
        except Exception as e:
            logger.error(f"Ошибка при нажатии кнопки следующего шага на шаге выставления счета: {e}")
            raise

    def click_continue_shipping(self):
        """
        Нажимает кнопку следующего шага на шаге доставки.
        """
        try:
            self.page.click(self.continue_shipping_button)
            expect(self.page.locator("#opc-shipping_method")).to_be_visible(timeout=5000)
        except Exception as e:
            logger.error(f"Ошибка при нажатии кнопки следующего шага на шаге доставки: {e}")
            raise

    def click_shipping_method_next_step(self):
        """
        Нажимает кнопку следующего шага на шаге выбора способа доставки.
        """
        try:
            self.page.click(self.shipping_method_next_step)
            expect(self.page.locator("#opc-payment_method")).to_be_visible(timeout=5000)
        except Exception as e:
            logger.error(f"Ошибка при нажатии кнопки следующего шага на шаге выбора способа доставки: {e}")
            raise

    def click_payment_method_next_step(self):
        """
        Нажимает кнопку следующего шага на шаге выбора способа оплаты.
        """
        try:
            self.page.click(self.payment_method_next_step)
            expect(self.page.locator("#opc-payment_info")).to_be_visible(timeout=5000)
        except Exception as e:
            logger.error(f"Ошибка при нажатии кнопки следующего шага на шаге выбора способа оплаты: {e}")
            raise

    def click_payment_info_next_step(self):
        """
        Нажимает кнопку следующего шага на шаге ввода информации об оплате.
        """
        try:
            self.page.click(self.payment_info_next_step)
            expect(self.page.locator("#opc-confirm_order")).to_be_visible(timeout=5000)
        except Exception as e:
            logger.error(f"Ошибка при нажатии кнопки следующего шага на шаге ввода информации об оплате: {e}")
            raise

    def click_confirm_order(self):
        """
        Подтверждает заказ.
        """
        try:
            self.page.click(self.confirm_order_button)
        except Exception as e:
            logger.error(f"Ошибка при подтверждении заказа: {e}")
            raise

    def get_order_success_message(self):
        """
        Возвращает сообщение об успешном оформлении заказа.
        """
        try:
            return self.page.locator(self.order_success_message).inner_text()
        except Exception as e:
            logger.error(f"Ошибка при получении сообщения об успешном оформлении заказа: {e}")
            raise
