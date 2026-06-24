from sqlalchemy import create_engine, String,ForeignKey, MetaData
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

with engine.begin() as conn:
    Base.metadata.create_all(conn)

with LocalSession() as session:
    product_1 = Product(
        name="Laptop",
        price=1100.1,
        in_stock=True,
        category=Category(name='Notebook/Laptop', description='Mega Notebook')

    )
    session.add(product_1)
    session.commit()

    products = session.query(Product).all()
    for p in products:
        print(f"Product: {p.name} | Price: {p.price} | In stock: {p.in_stock} | Category: {p.category.name}")

    categories = session.query(Category).all()
    for c in categories:
        print(f"Category: {c.name} | Description: {c.description}")