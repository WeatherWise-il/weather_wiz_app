from logging.config import dictConfig

import prometheus_client
from flask import Flask, render_template, request
from flask_swagger_ui import get_swaggerui_blueprint
import os
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_restful import Api
from forms import get_weather_form as weather_form
from flask_sqlalchemy import SQLAlchemy
import json
from flask_htmx import HTMX
import requests
import datetime
import pytz
from datetime import datetime
import pytz
from typing import Dict
from prometheus_client import Counter, Gauge, Histogram, Summary, generate_latest, CONTENT_TYPE_LATEST
import time

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "app.log",
                "maxBytes": 60 * 1024 * 1024,  # 60 MB
                "backupCount": 10,
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["file"]},
    }
)

with open("/run/secrets/app_api_key", "r") as f:
    app_api_key = f.read().strip()

app = Flask(__name__)
api = Api(app)
htmx = HTMX(app)
app.logger.setLevel("DEBUG")
app.logger.info("Getting the environment variables")
FLASK_PORT = os.getenv("FLASK_PORT")
FLASK_HOST = os.getenv("FLASK_HOST")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CSRF_KEY = os.getenv("CSRF_SECRET_KEY")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

# Define metrics
REQUEST_COUNT = Counter('request_counter', 'full requests counter', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'request latency', ['method', 'endpoint'])
REQUEST_DURATION = Summary('request_duration_seconds', 'request duration', ['method', 'endpoint'])


app.logger.debug("List of environment variables:")
app.logger.debug("*" * 50)
app.logger.debug(f"FLASK_PORT:{FLASK_PORT}")
app.logger.debug(f"FLASK_HOST:{FLASK_HOST}")
app.logger.debug("*" * 50)

Bootstrap5(app)
app.secret_key = CSRF_KEY
csrf = CSRFProtect(app)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

app.cities = None
app.cities_only = None
SWAGGER_URL = "/api/docs"
API_URL = "/static/docs/swagger.yaml"
SWAGGER_BLUEPRINT_URL = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Weather app"}
)

app.register_blueprint(SWAGGER_BLUEPRINT_URL, url_prefix=SWAGGER_URL)


class Cities(db.Model):
    __tablename__ = "cities"
    city_id = db.Column(
        db.Integer, primary_key=True, index=True, autoincrement=True, nullable=False
    )
    city_name = db.Column(db.String(75), nullable=False)
    state_code = db.Column(db.String(20), nullable=False)
    country_code = db.Column(db.String(20))
    country_full = db.Column(db.String(45), nullable=False)
    city_lat = db.Column(db.Float, nullable=True)
    city_lon = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"City: {self.city_name}, {self.state_code}, {self.country_code}, {self.country_full}, {self.city_lat}, {self.city_lon}"


@app.errorhandler(404)
def page_not_found(e):
    REQUEST_COUNT.labels(method='GET', endpoint='/404', http_status=404).inc()
    temp_title = "404"
    app.logger.error(f"Page not found: {e} request: {request.path}")
    return render_template("404.html", title=temp_title), 404


# @app.get("/weather")
# def get_weather_backend():
#     REQUEST_COUNT.labels(method='GET', endpoint='/weather', http_status=200).inc()
#     return json.dumps({"results": "contries_res"}), 200


def convert_epoch_to_time(epoch):
    """
    Convert an epoch time to a human-readable time.
    """
    jerusalem_tz = pytz.timezone("Asia/Jerusalem")  # Specify Jerusalem time zone
    dt = datetime.fromtimestamp(epoch, jerusalem_tz)
    return dt.strftime("%I:%M:%S %p").lower()


def convert_date_to_weekday(date: str):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    day_of_week = date_obj.strftime("%A")
    return day_of_week


def convert_date_format(date: str):
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    new_format = date_obj.strftime("%d/%m/%Y")
    return new_format


def get_city_forcast(city_data: list[dict]):
    """
    Get the weather forecast for a city.
    """
    app.logger.info(f"Getting the weather forcast for city: {city_data}")

    app.logger.info(f"### cityy_data = {city_data}### ")
    city_lat: str = city_data.get("city_lat")
    city_lon: str = city_data.get("city_lon")
    rest_endpoint_url: str = f"https://api.weatherbit.io/v2.0/forecast/daily?lat={city_lat}&lon={city_lon}&units=M&key={app_api_key}&days=5"
    app.logger.info(f"REST_ENDPOINT_URL = {rest_endpoint_url}")
    response = requests.get(rest_endpoint_url)
    print(f"response = {response.encoding}")
    city_forcast: list = []
    for item in response.json().get("data"):
        if city_data is not None:  # Add null check
            city_forcast.append(
                {
                    "valid_date": convert_date_format(item.get("valid_date")),
                    "weekday": convert_date_to_weekday(item.get("valid_date")),
                    "temp": item.get("temp"),
                    "min_temp": item.get("min_temp"),
                    "max_temp": item.get("max_temp"),
                    "sunrise_ts": convert_epoch_to_time(item.get("sunrise_ts")),
                    "sunset_ts": convert_epoch_to_time(item.get("sunset_ts")),
                    "weather_desc": item.get("weather").get("description"),
                    "weather_icon": item.get("weather").get("icon"),
                }
            )
    app.logger.debug(f"city_forcast results: {city_forcast}")
    return city_forcast


@app.before_first_request
def before_first_request():
    print("Running before any request")
    """
    Executes a database query and stores results in global_data before first request.
    """
    try:
        app.cities = [u.__dict__ for u in Cities.query.all()]
        list_of_contries = [item.get("country_full") for item in app.cities]
        app.contries = list(dict.fromkeys(list_of_contries))
        app.contries.sort()
        app.cities_only = [item.get("city_name") for item in app.cities]
        app.cities_only.sort()
        app.logger.info("Database query executed successfully")
    except Exception as e:
        print(f"Error querying database: {e}")


@app.route("/get_cities", methods=["GET"])
def get_cities_by_country():
    try:
        print("Called to get cities by country")
        selected_country = request.args.get("countries")
        app.logger.debug(f"selected_country = {selected_country}")
        cities_list_of_choices = [
            item.get("city_name")
            for item in app.cities
            if item.get("country_full") == selected_country
        ]
        cities_list_of_choices.sort()
        app.logger.debug(f"### cities_list_of_choices = {cities_list_of_choices}")
        REQUEST_COUNT.labels(method='GET', endpoint='/get_cities', http_status=200).inc()
        return render_template("cities_options.html", cities=cities_list_of_choices)
    except Exception as e:
        app.logger.error(f"Error querying database: {e}")
        REQUEST_COUNT.labels(method='GET', endpoint='/get_cities', http_status=500).inc()


@app.route("/search", methods=["GET"])
def search():
    search_term = request.args.get("search_term")
    print(f"q = {search_term}")
    if not search_term:
        filtered_data = [{}]
        return render_template("search_results.html", results=filtered_data)
    else:
        query_res = (
            Cities.query.filter(Cities.city_name.like(f"%{search_term}%"))
            .limit(10)
            .all()
        )
        print(f"query_res = {query_res}")
        filtered_data = [
            {"city_id": item.city_id, "city_name": item.city_name} for item in query_res
        ]
        if not filtered_data:
            filtered_data = [{}]
    return render_template("search_results.html", results=filtered_data)


@app.route("/get_weather", methods=["POST"])
def get_weather():
    try:
        city_id = request.form.get("select_field")
        print(f"request.form = {request.form}")
        city = Cities.query.filter_by(city_id=city_id).first()
        city_obj = {
            "city_id": city_id,
            "city_name": city.city_name,
            "state_code": city.state_code,
            "country_code": str(city.country_code),
            "country_full": city.country_full,
            "city_lat": city.city_lat,
            "city_lon": city.city_lon,
        }
        print(f"city_obj = {city_obj}")
        results = get_city_forcast(city_obj)
        REQUEST_COUNT.labels(method='POST', endpoint='/get_weather', http_status=200).inc()
        return render_template("weather_results.html", results=results)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        REQUEST_COUNT.labels(method='POST', endpoint='/get_weather', http_status=500).inc()
        return render_template("500.html", title="500 Error page"), 500


@app.route("/", methods=["GET"])
def home():
    try:
        temp_title = "Weather App"
        form = weather_form()
        # if form.validate_on_submit():
        #     print(f"search = {form.search_term.data}")
        #     print(f"city = {form.select_field.data}")
        REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=200).inc()
        return render_template(
                "index.html",
                title=temp_title,
                form=form), 200
    except Exception as e:
        app.logger.error(f"Error: {e}")
        REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=500).inc()
        return render_template("500.html", title="500 Error page"), 500



@app.errorhandler(500)
def internal_error(error):
    temp_title = "500 Error page"
    return render_template("500.html", title=temp_title), 500


@app.route('/metrics', methods=['GET'])
def metrics():
    return prometheus_client.generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(port=FLASK_PORT, host=FLASK_HOST)
