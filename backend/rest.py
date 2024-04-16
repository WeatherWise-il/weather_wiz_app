from flask_restful import Resource 
from location import get_geo_location as location
from forms import get_weather_form as geo_form
from flask import render_template
from flask_googlemaps import Map


        