import requests
from sqlalchemy.orm import Session
import models
from main import session_local

APIs = [
    

]

def func(db: Session):
    for api in APIs:
        response = requests.get(api)
        if response.status_code == 200:
            products = response.json()
            for product in products:
                db_product = models.Product(
                    name=product['name'],
                    price=product['price'],
                    category=product['category'],
                    company=product['company'],
                    rating=product.get('rating', 0)
                )
                db.add(db_product)
            db.commit()

if __name__ == "__main__":
    db = session_local()
    func(db)
    db.close()