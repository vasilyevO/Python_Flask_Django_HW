from pydantic import BaseModel, EmailStr, ValidationError
import json


class Address(BaseModel):
    city: str
    street: str
    house_number: str


class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    address: Address


json_string = """{
    "name": "John Doe",
    "age": "22",
    "email": "john.doe@example.com",
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": "123"
    }
}"""

try:
    user1 = User.model_validate_json(json_string)
    print(user1)
    with open('user1.json', 'w') as outfile:
        outfile.write(user1.model_dump_json())

except ValidationError as e:
    print(e)