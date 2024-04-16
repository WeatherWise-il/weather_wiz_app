from main import db

class Cities(db.Model):
    __tablename__ = 'cities'
    city_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    city_name = db.Column(db.String(75), nullable=False)
    state_code = db.Column(db.String(20),nullable=False)
    country_code = db.Column(db.String(20))
    country_full = db.Column(db.String(45), nullable=False)
    city_lat = db.Column(db.Float, nullable=True)
    city_lon = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f"City: {self.city_name}, {self.state_code}, {self.country_code}, {self.country_full}, {self.city_lat}, {self.city_lon}"