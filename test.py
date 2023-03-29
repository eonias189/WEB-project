from pprint import pprint
from data import db_session
from data.countries import Country
from geo_tools import get_coords, API_KEY_GEOCODER

db_session.global_init('db/country_guesser.db')
db_sess = db_session.create_session()
countries = db_sess.query(Country).all()
for i in range(len(countries)):
    response = get_coords(countries[i].name, API_KEY_GEOCODER)
    longitude, latitude = response[1][-1]
    countries[i].longitude = longitude
    countries[i].latitude = latitude
    if i % 10 == 0:
        print((i + 1) / 216 * 100)

db_sess.commit()
