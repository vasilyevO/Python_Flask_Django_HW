from sqlalchemy import create_engine, String, ForeignKey, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from decimal import Decimal

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column()
    in_stock: Mapped[bool] = mapped_column()
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'))
    category: Mapped["Category"] = relationship(back_populates="products")


class Category(Base):
    __tablename__ = 'category'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    products: Mapped[list["Product"]] = relationship(back_populates="category")

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
LocalSession = sessionmaker(bind=engine)

with LocalSession() as session:

    # Задача 1 — добавление данных
    categories = [
        Category(name="Электроника", description="Гаджеты и устройства."),
        Category(name="Книги", description="Печатные книги и электронные книги."),
        Category(name="Одежда", description="Одежда для мужчин и женщин.")
    ]
    session.add_all(categories)
    session.commit()

    products = [
        Product(name="Смартфон", price=299.99, in_stock=True, category=categories[0]),
        Product(name="Ноутбук", price=499.99, in_stock=True, category=categories[0]),
        Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category=categories[1]),
        Product(name="Джинсы", price=40.50, in_stock=True, category=categories[2]),
        Product(name="Футболка", price=20.00, in_stock=True, category=categories[2]),
    ]
    session.add_all(products)
    session.commit()

    # Задача 2 — чтение данных
    print("\n--- Задача 2: Категории и продукты ---")
    all_categories = session.query(Category).all()
    for cat in all_categories:
        print(f"\nКатегория: {cat.name}")
        for p in cat.products:
            print(f"  - {p.name} | {p.price}")

    # Задача 3 — обновление цены
    print("\n--- Задача 3: Обновление цены ---")
    smartphone = session.query(Product).filter(Product.name == "Смартфон").first()
    smartphone.price = 349.99
    session.commit()
    print(f"Новая цена смартфона: {smartphone.price}")

    # Задача 4 — количество продуктов в каждой категории
    print("\n--- Задача 4: Количество продуктов ---")
    result = session.query(
        Category.name,
        func.count(Product.id)
    ).join(Product).group_by(Category.name).all()

    for category_name, count in result:
        print(f"{category_name}: {count} продуктов")

    # Задача 5 — категории с более чем одним продуктом
    print("\n--- Задача 5: Категории с более чем 1 продуктом ---")
    result = session.query(
        Category.name,
        func.count(Product.id)
    ).join(Product).group_by(Category.name).having(func.count(Product.id) > 1).all()

    for category_name, count in result:
        print(f"{category_name}: {count} продуктов")