from database import Base, SessionLocal, engine
from models import Product

# Test

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.query(Product).delete()

db.add_all([
    Product(name="Laptop", price=999.99),
    Product(name="Keyboard", price=49.99),
    Product(name="Mouse", price=29.99),
    Product(name="Monitor", price=349.99),
    Product(name="Headphones", price=79.99),
])

db.commit()
db.close()
print("Database seeded")
