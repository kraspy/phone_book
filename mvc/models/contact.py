import re
from mvc.errors import ContactError


class Contact:
    def __init__(self, name: str, phone: str, comment: str | None = None):
        self.name = self.validate_name(name)
        self.phone = self.validate_phone(phone)
        self.comment = comment

    @staticmethod
    def validate_name(name: str) -> str:
        if not name or len(name.strip()) == 0:
            raise ContactError("Имя не может быть пустым")
        return name.strip()

    @staticmethod
    def validate_phone(phone: str) -> str:
        if not re.match(r'^\+?\d{9,12}$', phone):
            raise ContactError("Неверный формат номера телефона")
        return phone

    def model_dump_tuple(self) -> tuple[str, str, str]:
        return self.name, self.phone, self.comment or ""
