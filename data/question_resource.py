import random
from flask_restful import abort, Resource
from flask import jsonify, request
from . import db_session
from .countries import Country
from .api_key_tools import check_questoin_key
from .geo_tools import get_image, get_spn, get_dist, get_bbox


def abort_if_access_denied(request):
    if 'key' not in request.args or not check_questoin_key(request.args['key']):
        return abort(401, message='access denied')


class QuestionResource(Resource):
    def get(self):
        abort_if_access_denied(request)
        complexity_dict = {'easy': (0, 0, 3), 'normal': (1, 1, 1), 'hard': (0, 3, 0)}
        db_sess = db_session.create_session()
        if 'complexity' in request.args and request.args['complexity'] in ['easy', 'normal', 'hard']:
            countries = db_sess.query(Country).filter(Country.complexity == request.args['complexity'][0]).all()
            n_countries_name_like, n_neighbours, n_randoms = complexity_dict[request.args['complexity']]
        else:
            countries = db_sess.query(Country).all()
            n_countries_name_like = 1
            n_neighbours = 1
            n_randoms = 1
        if 'country' not in request.args or not db_sess.query(Country).filter(
                Country.name == request.args['country']).first():
            country = random.choice(countries)
        else:
            country = db_sess.query(Country).filter(Country.name == request.args['country']).first()
        country_coords = (country.latitude, country.longitude)
        neighbours = sorted(
            [(i.name, get_dist((i.latitude, i.longitude), country_coords)) for i in countries], key=lambda x: x[1])[
                     1:n_neighbours + 1]
        neighbours = [i[0] for i in neighbours]
        variants_1 = db_sess.query(Country).filter(Country.name.like(f'{country.name[0]}%'),
                                                   Country.name.not_like(country.name),
                                                   Country.name.notin_(neighbours)).all()
        if len(variants_1) < n_countries_name_like:
            n_randoms += 1
            variants = []
        else:
            variants = random.sample(variants_1, n_countries_name_like)
        variants = [i.name for i in variants]
        randoms = random.sample([i.name for i in countries if i not in neighbours and i not in variants], n_randoms)
        group_1 = ['Австралия', 'Алжир', 'Ангола', 'Аргентина', 'Афганистан', 'Боливия', 'Бразилия', 'Великобритания',
                   'Венесуэла', 'Вьетнам', 'Германия', 'Гонконг', 'Египет', 'Замбия', 'Индия', 'Индонезия', 'Иран',
                   'Исландия', 'Испания', 'Италия', 'Кабо-Верде', 'Казахстан', 'Камерун', 'Канада', 'Кипр', 'Китай',
                   'Колумбия',
                   'Острова Кука', 'Ливия', 'Мавритания', 'Мали', 'Мексика', 'Мозамбик', 'Монако', 'Монголия', 'Мьянма',
                   'Намибия', 'Нигер', 'Нигерия', 'Норвегия', 'Оман', 'Пакистан', 'Папуа Новая Гвинея', 'Перу',
                   'Португалия',
                   'Сан-Томе и Принсипи', 'Саудовская Аравия', 'Остров Святой Елены', 'Сейшеллы', 'Сомали', 'Судан',
                   'Таиланд',
                   'Тайвань', 'Танзания', 'Токелау', 'Тонга', 'Тувалу', 'Туркменистан', 'Туркс и Кейкос', 'Турция',
                   'Узбекистан', 'Украина', 'Фарерские о-ва', 'Филиппины', 'Финляндия', 'Франция',
                   'Французская Полинезия', 'Чад', 'Чили', 'Швеция', 'Эквадор', 'Эфиопия', 'ЮАР', 'Кирибати',
                   'Новая Зеландия', 'Россия', 'США', 'Фиджи']
        need_another_spn = {'Аргентина': 8, 'Острова Кука': 0.01, 'Норвегия': 6, 'Папуа Новая Гвинея': 4, 'Россия': 6,
                            'США': 8, 'Чили': 6}
        ll = f'{country.longitude},{country.latitude}'
        geo = (country.r, country.l, country.u, country.d)
        bbox = get_bbox(geo)
        if country.name in need_another_spn:
            spn = get_spn(geo, n=need_another_spn[country.name])
        else:
            spn = get_spn(geo)
        if country.name not in group_1:
            content = get_image(bbox=bbox, type='sat,skl', point=ll, z=5)
        else:
            content = get_image(ll=ll, spn=spn, type='sat,skl', point=ll)
        variants = variants + neighbours + [country.name] + randoms
        random.shuffle(variants)
        return jsonify({'country': country.name, 'content': content.decode('ISO-8859-1'), 'encoding': 'ISO-8859-1',
                        'variants': variants})
