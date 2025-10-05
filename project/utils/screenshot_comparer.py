import os
from PIL import Image
import imagehash
import logging


class ScreenshotComparer:
    """
    Класс для сравнения скриншотов на основе алгоритма хеширования изображений.
    """
    def __init__(self, screenshot_dir, actual_screenshot_dir, threshold, update_snapshots=False):
        self.screenshot_dir = screenshot_dir
        self.actual_screenshot_dir = actual_screenshot_dir
        self.threshold = threshold
        self.update_snapshots = update_snapshots
        self.logger = logging.getLogger(__name__)

    def compare_screenshots(self, screenshot_name):
        """
        Сравнивает два скриншота (эталонный и актуальный).
        """
        expected_screenshot_path = os.path.join(self.screenshot_dir, screenshot_name)
        actual_screenshot_path = os.path.join(self.actual_screenshot_dir, screenshot_name)

        try:
            if not os.path.exists(expected_screenshot_path):
                self.logger.warning(f"Ожидаемый скриншот не найден: {expected_screenshot_path}")
                if self.update_snapshots:
                  os.makedirs(os.path.dirname(expected_screenshot_path), exist_ok=True)
                  actual_image = Image.open(actual_screenshot_path)
                  actual_image.save(expected_screenshot_path)
                  self.logger.info(f"Эталонный скриншот создан: {expected_screenshot_path}")
                  return True
                else:
                    return False 

            expected_image = Image.open(expected_screenshot_path)
            actual_image = Image.open(actual_screenshot_path)

            expected_hash = imagehash.average_hash(expected_image)
            actual_hash = imagehash.average_hash(actual_image)

            hamming_distance = expected_hash - actual_hash

            if self.update_snapshots:
                actual_image.save(expected_screenshot_path) 
                self.logger.info(f"Эталонный скриншот обновлен: {expected_screenshot_path}")
                return True 

            if hamming_distance < self.threshold:
                self.logger.info(f"Скриншоты похожи (расстояние Хэмминга: {hamming_distance})")
                return True
            else:
                self.logger.warning(f"Скриншоты отличаются (расстояние Хэмминга: {hamming_distance})")
                return False
        except Exception as e:
            self.logger.error(f"Ошибка при сравнении скриншотов: {e}")
            return False

