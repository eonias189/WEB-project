from pprint import pprint
import requests
from data import db_session
from data.countries import Country
from data.geo_tools import get_bbox, get_image, get_spn


def test_db():
    # 69 99 48
    db_session.global_init('db/country_guesser.db')
    db_sess = db_session.create_session()
    countries = db_sess.query(Country).all()
    group_1 = ['Австралия', 'Алжир', 'Ангола', 'Аргентина', 'Афганистан', 'Боливия', 'Бразилия', 'Великобритания',
               'Венесуэла', 'Вьетнам', 'Германия', 'Гонконг', 'Египет', 'Замбия', 'Индия', 'Индонезия', 'Иран',
               'Исландия', 'Испания', 'Италия', 'Кабо-Верде', 'Казахстан', 'Камерун', 'Канада', 'Кипр', 'Китай',
               'Колумбия',
               'Кука о-ва', 'Ливия', 'Мавритания', 'Мали', 'Мексика', 'Мозамбик', 'Монако', 'Монголия', 'Мьянма',
               'Намибия', 'Нигер', 'Нигерия', 'Норвегия', 'Оман', 'Пакистан', 'Папуа Новая Гвинея', 'Перу',
               'Португалия',
               'Сан-Томе и Принсипи', 'Саудовская Аравия', 'Святой Елены о-в', 'Сейшеллы', 'Сомали', 'Судан', 'Таиланд',
               'Тайвань', 'Танзания', 'Токелау о-ва', 'Тонга', 'Тувалу', 'Туркменистан', 'Туркс и Кейкос', 'Турция',
               'Узбекистан', 'Украина', 'Фарерские о-ва', 'Филиппины', 'Финляндия', 'Франция',
               'Французская Полинезия', 'Чад', 'Чили', 'Швеция', 'Эквадор', 'Эфиопия', 'ЮАР', 'Кирибати',
               'Новая Зеландия', 'Россия', 'США', 'Фиджи']

    country = db_sess.query(Country).filter(Country.name == 'Канада').first()
    ll = f'{country.longitude},{country.latitude}'
    geo = (country.r, country.l, country.u, country.d)
    bbox = get_bbox(geo)
    spn = get_spn(geo)
    if country.name not in group_1:
        print(country.name)
        content = get_image(bbox=bbox, type='sat,skl', point=ll, z=5)
    else:
        content = get_image(ll=ll, spn=spn, type='sat,skl', point=ll)


def test_question_api():
    url = 'http://127.0.0.1:5000/api/question'
    params = {'key': "ER*los]NtTW:G14SH@", 'country': '', 'complexity': 'easy'}
    response = requests.get(url, params=params).json()
    varinats, content, encoding, country = response['variants'], response['content'], response['encoding'], response[
        'country']
    content = bytes(content, encoding)
    with open('static/img/image.png', 'wb') as f:
        f.write(content)
    print(varinats)
    print(country)


if __name__ == '__main__':
    test_question_api()
