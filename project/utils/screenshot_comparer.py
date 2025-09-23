import os
from PIL import Image
import imagehash
from utils.logger import logger

class ScreenshotComparer:
    """
    Класс для сравнения скриншотов.
    """

    def __init__(self, screenshot_dir, threshold):
        """
        Конструктор класса.
        :param screenshot_dir: Директория, где хранятся эталонные скриншоты.
        :param threshold: Порог различий между скриншотами (в процентах).
        """
        self.screenshot_dir = screenshot_dir
        self.threshold = threshold

    def compare_screenshots(self, screenshot_name):
        """
        Сравнивает скриншот с эталонным изображением.
        :param screenshot_name: Имя файла скриншота.
        :return: True, если скриншоты совпадают, False в противном случае.
        """
        try:
            # 1. Формируем пути к эталонному и текущему скриншотам
            expected_screenshot_path = os.path.join(self.screenshot_dir, screenshot_name)
            actual_screenshot_path = os.path.join(self.screenshot_dir, screenshot_name)

            # 2. Проверяем существование эталонного скриншота
            if not os.path.exists(expected_screenshot_path):
                logger.warning(f"Expected screenshot not found: {expected_screenshot_path}")
                return False

            # 3. Открываем изображения с помощью PIL
            expected_image = Image.open(expected_screenshot_path)
            actual_image = Image.open(actual_screenshot_path)

            # 4. Вычисляем хеши изображений
            expected_hash = imagehash.average_hash(expected_image)
            actual_hash = imagehash.average_hash(actual_image)

            # 5. Вычисляем расстояние Хэмминга между хешами
            hamming_distance = expected_hash - actual_hash

            # 6. Сравниваем расстояние Хэмминга с порогом
            if hamming_distance < self.threshold:
                logger.info(f"Screenshots are similar (Hamming distance: {hamming_distance})")
                return True
            else:
                logger.warning(f"Screenshots are different (Hamming distance: {hamming_distance})")
                return False

        except Exception as e:
            logger.error(f"Error comparing screenshots: {e}")
            return False

    def generate_hash(self, image_path):
        """
        Генерирует хеш изображения.
        :param image_path: Путь к файлу изображения.
        :return: Хеш изображения.
        """
        try:
            image = Image.open(image_path)
            hash = imagehash.average_hash(image)
            return hash
        except Exception as e:
            logger.error(f"Error generating hash: {e}")
            return None
