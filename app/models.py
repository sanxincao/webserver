
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer)

    def __init__(self, name, email, username, access=ACCESS['guest']):
        self.id = ''
        self.name = name
        self.email = email
        self.username = username
        self.password_hash = ''
        self.access = access

    def is_admin(self):
        return self.access == ACCESS['admin']

    def is_user(self):
        return self.access == ACCESS['user']

    def allowed(self, access_level):
        return self.access >= access_level

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {0}>'.format(self.username)