from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def db_init(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    guardian_name = db.Column(db.String(100))
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.DATE)
    occupation = db.Column(db.String(20))
    address = db.Column(db.String(200))
    prof_img_path = db.Column(db.Text, unique=True, nullable=False)

    # prof_filename = db.Column(db.Text, nullable=False)
    # prof_mimetype = db.Column(db.Text, nullable=False)

    def __init__(self, user_name, password, name, guardian_name, email, phone, dob, occupation, address, prof_img_path):
        self.user_name = user_name
        self.password = password
        self.name = name
        self.guardian_name = guardian_name
        self.email = email
        self.phone = phone
        self.dob = dob
        self.occupation = occupation
        self.address = address
        self.prof_img_path = prof_img_path
        # self.prof_filename = prof_filename
        # self.prof_mimetype = prof_mimetype
