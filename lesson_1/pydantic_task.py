
from pydantic import ValidationError

from pydantic import BaseModel, EmailStr

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
    "age": 22,
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
except ValidationError as err:
    print(err)

# user_data = {
#     "name": "John",
#     "age": 18
# }

# user1 = User(**user_data)
# user1 = User ("name" ="john", "age" = 18)
# print(user1)

