"""
SRP
  The Single Responsibility Principle advocates for a class or module to have only one reason to change. 
  In simpler terms, it should do one thing and do it well. By adhering to SRP, your code becomes more modular, making it easier to understand and maintain.

OCP
  The Open-Closed Principle states that software entities should be open for extension but closed for modification. 
  This means that you should be able to extend a class’s behavior without modifying it.
"""

"""
Task, assume we would like to mimic user online shopping expirience. User can add | remove an order.
As well, as user might want proceed with payment of the order with certain payment method.

Define:
  - user
  - item
  - order
  - pricing strategy
  - payment
"""

from pydantic import BaseModel
from abc import ABC, abstractmethod


class User(BaseModel):
  name: str
  age: int


class Item(BaseModel):
  title: str
  price: int


class PricingStrategy(ABC):
  @abstractmethod
  def calculate(self, items: list[Item]):
    ...
  
  @property
  @abstractmethod
  def discount(self):
    ...


class PriceWithoutDiscount(PricingStrategy):
  def calculate(self, items: list[Item]) -> int:
    return int(sum(item.price for item in items) * self.discount)
  
  @property
  def discount(self) -> int:
    return 1


class PriceWithFiftyPercentDiscount(PricingStrategy):
  def calculate(self, items: list[Item]) -> int:
    return int(sum(item.price for item in items) * self.discount)
  
  @property
  def discount(self) -> int:
    return 0.5



class Order:
  def __init__(self, user: User, pricing: PricingStrategy):
    self.user = user
    self.items: list[Item] = []
    self.pricing: PricingStrategy = pricing
  
  def add(self, item: Item) -> None:
    self.items.append(item)

  def total_price(self) -> int:
    return self.pricing.calculate(items=self.items)


class PaymentMethod(ABC):
  @abstractmethod
  def charge(self, order: Order, card: str):
    ...


class CreditCard(PaymentMethod):
  def charge(self, order: Order, card: str):
    print(f"charged {order.total_price()} from Credit card")


class DebitCard(PaymentMethod):
  def charge(self, order: Order, card: str):
    print(f"charged {order.total_price()} from Debit card")


################################################################################
items = {
    "monitor Dell": Item(title="Dell", price=100),
    "monitor Toshiba": Item(title="Toshiba", price=300),
    "iPhone 16": Item(title="Iphone 16", price=1000)
}


full_pricing = PriceWithoutDiscount()
half_pricing = PriceWithFiftyPercentDiscount()

credit_card = CreditCard()
debit_card = DebitCard()

user_bob = User(name="Bob", age=25)
bobs_order = Order(user=user_bob, pricing=half_pricing)
bobs_order.add(item=items["iPhone 16"])
bobs_order.add(item=items["monitor Dell"])
print(bobs_order.total_price())

credit_card.charge(order=bobs_order, card="1234-1234-1234-1234")