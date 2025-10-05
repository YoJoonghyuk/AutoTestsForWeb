import re
import random
import string

def get_count_from_text(text):
    """
    Извлекает число из текста, содержащего число в скобках, например, "(2)".
    """
    match = re.search(r"\((\d+)\)", text)
    if match:
        return int(match.group(1))
    return 0

def generate_random_email(length=10):
    """
    Генерирует рандомный email
    """
    username = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    domain = "random.com"  
    return f"{username}@{domain}"

def generate_random_string(length=10):
    """
    Генерирует рандомную строку заданной длины
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
