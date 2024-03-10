from config import db, app


class Product(db.Model):
    id = db.Column('prod_id', db.Integer, primary_key=True)
    name = db.Column('prod_name', db.String(30))
    vendor = db.Column('prod_vendor', db.String(30))
    category = db.Column('prod_category', db.String(30))
    price = db.Column('prod_price', db.Float())
    qyt = db.Column('prod_qyt', db.Integer)


print('Table Is Created...')
with app.app_context():
    db.create_all()
