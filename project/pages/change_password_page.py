from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from utils.logger import logger

class ChangePasswordPage(BasePage):
    """
    Класс, представляющий страницу изменения пароля.
    """
    def __init__(self, page: Page, config):
        super().__init__(page, config)
        self.page = page
        self.config = config
        self.old_password_field = "#OldPassword"
        self.new_password_field = "#NewPassword"
        self.confirm_new_password_field = "#ConfirmNewPassword"
        self.change_password_button = "input.button-1.change-password-button"
        self.success_message_locator = ".result"
        self.old_password_error_locator = ".validation-summary-errors li"
        self.new_password_mismatch_locator = "span.field-validation-error span"

    def change_password(self, old_password, new_password, confirm_new_password):
        """
        Заполняет поля для изменения пароля.
        """
        try:
            self.page.fill(self.old_password_field, old_password)
            self.page.fill(self.new_password_field, new_password)
            self.page.fill(self.confirm_new_password_field, confirm_new_password)
        except Exception as e:
            logger.error(f"Ошибка при заполнении полей изменения пароля: {e}")
            raise

    def save_password_changes(self):
        """
        Сохраняет изменения пароля.
        """
        try:
            self.click(self.change_password_button, "Change password button")
        except Exception as e:
            logger.error(f"Ошибка при сохранении изменений пароля: {e}")
            raise

    def verify_success_message(self, expected_message="Password was changed"):
        """
        Проверяет отображение сообщения об успешном изменении пароля.
        """
        try:
            expect(self.page.locator(self.success_message_locator).first).to_have_text(expected_message)
        except Exception as e:
            logger.error(f"Ошибка при проверке сообщения об успехе: {e}")
            raise

    def verify_old_password_error(self, expected_error="Old password doesn't match"):
        """
        Проверяет отображение сообщения об ошибке при вводе неверного пароля.
        """
        try:
            expect(self.page.locator(self.old_password_error_locator).first).to_have_text(expected_error)
        except Exception as e:
            logger.error(f"Ошибка при проверке сообщения об ошибке для старого пароля: {e}")
            raise

    def verify_new_password_mismatch_error(self, expected_error="The new password and confirmation password do not match."):
        """
        Проверяет отображение сообщения об ошибке при неудачном подтверждении пароля.
        """
        try:
            expect(self.page.locator(self.new_password_mismatch_locator).first).to_have_text(expected_error)
        except Exception as e:
            logger.error(f"Ошибка при проверке сообщения о неудачном подтверждении пароля: {e}")
            raise
