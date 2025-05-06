from marshmallow import Schema, fields, validates, ValidationError
import re


def is_valid_israeli_id(id_number: str) -> bool:
    if not id_number.isdigit() or len(id_number) > 9:
        return False
    id_number = id_number.zfill(9)
    total = 0
    for i, digit in enumerate(id_number):
        num = int(digit) * (1 if i % 2 == 0 else 2)
        total += num if num < 10 else num - 9
    return total % 10 == 0


def is_valid_phone(phone: str) -> bool:
    return bool(re.match(r"^\+\d{6,15}$", phone))


class UserSchema(Schema):
    id = fields.Str(required=True)
    phone = fields.Str(required=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)

    @validates("id")
    def validate_id(self, value, **kwargs):
        if not is_valid_israeli_id(value):
            raise ValidationError("Invalid Israeli ID")

    @validates("phone")
    def validate_phone(self, value, **kwargs):
        if not is_valid_phone(value):
            raise ValidationError("Invalid phone number format")
