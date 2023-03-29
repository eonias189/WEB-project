from pprint import pprint
from data import db_session
from data.countries import Country

db_session.global_init('db/country_guesser.db')
db_sess = db_session.create_session()
country = Country(name='Бразилия', latitude=-15.802118, longitude=-47.889062)
db_sess.add(country)
db_sess.commit()
print(country)
