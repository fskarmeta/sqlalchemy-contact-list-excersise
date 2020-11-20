from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    agenda_slug = db.Column(db.String(150))
    address = db.Column(db.String(150), nullable=True, default="")
    phone = db.Column(db.String(100), nullable=True)


    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "agenda_slug": self.agenda_slug,
            "address": self.address,
            "phone": self.phone
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()