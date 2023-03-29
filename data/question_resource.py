import random
from flask_restful import abort, Resource
from flask import jsonify, request
from . import db_session
from .countries import Country
from .api_key_tools import check_questoin_key
from .geo_tools import get_image, get_coords, get_spn, get_dist, API_KEY_GEOCODER


def abort_if_access_denied(request):
    if 'key' not in request.args or not check_questoin_key(request.args['key']):
        return abort(401, message='access denied')


class QuestionResource(Resource):
    def get(self):
        abort_if_access_denied(request)
        n_countries_name_like = 2
        n_neighbours = 1
        db_sess = db_session.create_session()
        countries = db_sess.query(Country).all()
        country = random.choice(countries)
        country_coords = (country.latitude, country.longitude)
        neighbours = sorted(
            [(i.name, get_dist((i.latitude, i.longitude), country_coords)) for i in countries], key=lambda x: x[1])[
                     1:n_neighbours + 1]
        countries.clear()
        variants = random.sample(db_sess.query(Country).filter(Country.name.like(f'{country.name[0]}%'),
                                                               Country.name.not_like(country.name)).all(),
                                 n_countries_name_like)
        coords = get_coords(country.name, API_KEY_GEOCODER)
        content = get_image(coords, type='sat,skl', point=coords[0])
        variants = [i.name for i in variants] + [i[0] for i in neighbours] + [country.name]
        return jsonify({'country': country.name, 'content': content.decode('ISO-8859-1'), 'encoding': 'ISO-8859-1',
                        'variants': variants})
