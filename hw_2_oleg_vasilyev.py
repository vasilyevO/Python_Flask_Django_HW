import json
from pydantic import BaseModel, Field, EmailStr, model_validator, ValidationError


class Address(BaseModel):
    """Модель адреса пользователя."""
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)


class User(BaseModel):
    """Модель пользователя с валидацией."""
    name: str = Field(min_length=2, pattern=r"^[a-zA-Z\s]+$")
    age: int = Field(ge=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode='after')
    def check_employment_age(self) -> 'User':
        """Проверяет что занятый пользователь имеет возраст от 18 до 65."""
        if self.is_employed and not 18 <= self.age <= 65:
            raise ValueError("Employed user must be between 18 and 65.")
        return self


def register_user(json_input: str) -> str:
    """
    Валидирует и регистрирует пользователя.

    Args:
        json_input: JSON строка с данными пользователя.

    Returns:
        JSON строка с валидными данными или сообщение об ошибке.
    """
    try:
        data = json.loads(json_input)
        user = User(**data)
        return user.model_dump_json()
    except ValidationError as e:
        return f"Validation error: {e}"


json1 = """{
    "name": "John",
    "age": 30,
    "email": "john@example.com",
    "is_employed": true,
    "address": {"city": "Berlin", "street": "Main Street", "house_number": 5}
}"""

json2 = """{
    "name": "Bill",
    "age": 70,
    "email": "bill@example.com",
    "is_employed": true,
    "address": {"city": "Hamburg", "street": "Oak Avenue", "house_number": 12}
}"""

json3 = """{
    "name": "Bob",
    "age": 25,
    "email": "not-an-email",
    "is_employed": false,
    "address": {"city": "Munich", "street": "Park Lane", "house_number": 3}
}"""

print(register_user(json1))
print(register_user(json2))
print(register_user(json3))