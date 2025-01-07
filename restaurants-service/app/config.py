class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@restaurants-db:5432/restaurants_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "supersecretkey"
