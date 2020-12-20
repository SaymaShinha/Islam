import re
from datetime import date
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
import json
import csv
from sqlalchemy import or_, func

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Quran_Editions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(120), nullable=False)
    language = db.Column(db.String(80), nullable=False)
    en_name = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)
    format = db.Column(db.String(120), nullable=False)
    direction = db.Column(db.String(10))


class Quran_Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surah_number = db.Column(db.Integer, nullable=False)
    surah_ar_name = db.Column(db.String(500), nullable=False)
    surah_en_name = db.Column(db.String(120), nullable=False)
    surah_en_name_translation = db.Column(db.String(300), nullable=False)
    revelation_type = db.Column(db.String(120), nullable=False)
    total_ayah = db.Column(db.Integer, nullable=False)


class Quran_text_ayah_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(120), nullable=False)
    surah_number = db.Column(db.Integer, nullable=False)
    surah_ar_name = db.Column(db.String(500), nullable=False)
    surah_en_name = db.Column(db.String(120), nullable=False)
    surah_en_name_translation = db.Column(db.String(50000), nullable=False)
    revelation_type = db.Column(db.String(120), nullable=False)
    ayah_number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(), nullable=False)
    juz = db.Column(db.Integer, nullable=False)
    manzil = db.Column(db.Integer, nullable=False)
    page = db.Column(db.Integer, nullable=False)
    ruku = db.Column(db.Integer, nullable=False)
    hizb_quarter = db.Column(db.Integer, nullable=False)
    sajda = db.Column(db.Boolean, nullable=False)
    sajda_id = db.Column(db.Integer, nullable=True)
    sajda_recommended = db.Column(db.Boolean, nullable=True)
    sajda_obligatory = db.Column(db.Boolean)
    language = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    transelator_en_name = db.Column(db.String(120), nullable=False)
    format = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)


class Quran_audio_ayah_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(120), nullable=False)
    surah_number = db.Column(db.Integer, nullable=False)
    surah_ar_name = db.Column(db.String(500), nullable=False)
    surah_en_name = db.Column(db.String(120), nullable=False)
    surah_en_name_translation = db.Column(db.String(50000), nullable=False)
    revelation_type = db.Column(db.String(120), nullable=False)
    ayah_number = db.Column(db.Integer, nullable=False)
    audio = db.Column(db.String(), nullable=False)
    audio_secondary = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), nullable=False)
    juz = db.Column(db.Integer, nullable=False)
    manzil = db.Column(db.Integer, nullable=False)
    page = db.Column(db.Integer, nullable=False)
    ruku = db.Column(db.Integer, nullable=False)
    hizb_quarter = db.Column(db.Integer, nullable=False)
    sajda = db.Column(db.Boolean, nullable=False)
    sajda_id = db.Column(db.Integer, nullable=True)
    sajda_recommended = db.Column(db.Boolean, nullable=True)
    sajda_obligatory = db.Column(db.Boolean, nullable=True)
    language = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    transelator_en_name = db.Column(db.String(120), nullable=False)
    format = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(120), nullable=False)


class Quran_exist_in_database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)


class World_cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    subcountry = db.Column(db.String, nullable=False)


@app.route('/save_world_cities')
def save_world_cities():
    with open('world-cities.csv', encoding="utf8") as f:
        reader = csv.reader(f)
        save_world_cities_list = list(reader)

        for item in save_world_cities_list:
            cities = World_cities(city=item[0], country=item[1], subcountry=item[2])
            db.session.add(cities)
        db.session.commit()
    return "data has been saved"


@app.route('/save_all_edition')
def save_all_edition():
    response = requests.get("http://api.alquran.cloud/v1/edition")
    data = json.loads(response.content)["data"]
    for item in data:
        exist_quran_ed = Quran_Editions.query.filter_by(identifier=item['identifier'], name=item['name'],
                                                        language=item['language'], en_name=item['englishName'],
                                                        type=item['type'],
                                                        format=item['format'], direction=item['direction']).first()
        if not exist_quran_ed:
            print(f"adding following edition: '{item['identifier']}'")
            quran = Quran_Editions(identifier=item['identifier'], name=item['name'],
                                   language=item['language'], en_name=item['englishName'], type=item['type'],
                                   format=item['format'], direction=item['direction'])
            db.session.add(quran)
        db.session.commit()

    return "data has been saved"


@app.route('/save_quran_surah_info')
def save_quran_surah_info():
    response = requests.get("http://api.alquran.cloud/v1/quran")
    data = json.loads(response.content)["data"]

    for item in data["surahs"]:
        exist_quran_surah = Quran_Info.query.filter_by(surah_number=item['number']).first()
        if not exist_quran_surah:
            print(f"adding following edition: '{item['number']}'")

            quran = Quran_Info(surah_number=item['number'], surah_ar_name=item['name'],
                               surah_en_name=item['englishName'],
                               surah_en_name_translation=item['englishNameTranslation'],
                               revelation_type=item['revelationType'], total_ayah=item['ayahs'].__len__())
            db.session.add(quran)

    db.session.commit()

    return "data has been saved"


@app.route('/save_text_quran')
def save_text_quran():
    quran_ed = Quran_Editions.query.filter_by(format="text").with_entities(Quran_Editions.identifier).all()

    for item_ed in quran_ed:
        exist_quran_ed = Quran_text_ayah_info.query.filter_by(identifier=item_ed).first()
        if not exist_quran_ed:
            response = requests.get("http://api.alquran.cloud/v1/quran/" + item_ed.identifier)
            data = json.loads(response.content)["data"]
        for item in data["surahs"]:
            for ayah in item['ayahs']:
                print(type(ayah['sajda']))
                if type(ayah['sajda']) is dict:
                    surah_ayah = Quran_text_ayah_info(identifier=data["edition"]["identifier"],
                                                      surah_number=item["number"],
                                                      surah_ar_name=item['name'], surah_en_name=item['englishName'],
                                                      surah_en_name_translation=item['englishNameTranslation'],
                                                      revelation_type=item['revelationType'], juz=ayah['juz'],
                                                      manzil=ayah['manzil'],
                                                      page=ayah['page'], ruku=ayah['ruku'],
                                                      hizb_quarter=ayah['hizbQuarter'],
                                                      sajda=True, sajda_id=ayah['sajda']['id'],
                                                      sajda_obligatory=ayah['sajda']['obligatory'],
                                                      sajda_recommended=ayah['sajda']['recommended'],
                                                      language=data['edition']['language'],
                                                      name=data['edition']['name'],
                                                      transelator_en_name=data['edition']['englishName'],
                                                      format=data['edition']['format'],
                                                      type=data['edition']['type'], ayah_number=ayah['number'],
                                                      text=ayah['text']
                                                      )
                else:
                    surah_ayah = Quran_text_ayah_info(identifier=data["edition"]["identifier"],
                                                      surah_number=item["number"],
                                                      surah_ar_name=item['name'], surah_en_name=item['englishName'],
                                                      surah_en_name_translation=item['englishNameTranslation'],
                                                      revelation_type=item['revelationType'], juz=ayah['juz'],
                                                      manzil=ayah['manzil'],
                                                      page=ayah['page'], ruku=ayah['ruku'],
                                                      hizb_quarter=ayah['hizbQuarter'],
                                                      sajda=ayah['sajda'], language=data['edition']['language'],
                                                      name=data['edition']['name'],
                                                      transelator_en_name=data['edition']['englishName'],
                                                      format=data['edition']['format'],
                                                      type=data['edition']['type'], ayah_number=ayah['number'],
                                                      text=ayah['text']
                                                      )

                db.session.add(surah_ayah)
                db.session.commit()

    return "data has been saved"


@app.route("/save_audio_quran")
def save_audio_quran():
    quran_ed = Quran_Editions.query.filter_by(format="audio").with_entities(Quran_Editions.identifier).all()

    for item_ed in quran_ed:
        exist_quran_ed = Quran_text_ayah_info.query.filter_by(identifier=item_ed.identifier).first()
        if not exist_quran_ed:
            response = requests.get("http://api.alquran.cloud/v1/quran/" + item_ed.identifier)
            data = json.loads(response.content)["data"]
            for item in data["surahs"]:
                for ayah in item['ayahs']:
                    print(type(ayah['sajda']))
                    if ayah['audioSecondary'].__len__() > 0:
                        for audio_sec in ayah['audioSecondary']:
                            if type(ayah['sajda']) is dict:
                                surah_ayah = Quran_audio_ayah_info(identifier=data["edition"]["identifier"],
                                                                   surah_number=item["number"],
                                                                   surah_ar_name=item['name'],
                                                                   surah_en_name=item['englishName'],
                                                                   surah_en_name_translation=item[
                                                                       'englishNameTranslation'],
                                                                   revelation_type=item['revelationType'],
                                                                   juz=ayah['juz'],
                                                                   manzil=ayah['manzil'],
                                                                   page=ayah['page'], ruku=ayah['ruku'],
                                                                   hizb_quarter=ayah['hizbQuarter'],
                                                                   sajda=True, sajda_id=ayah['sajda']['id'],
                                                                   sajda_obligatory=ayah['sajda']['obligatory'],
                                                                   sajda_recommended=ayah['sajda']['recommended'],
                                                                   language=data['edition']['language'],
                                                                   name=data['edition']['name'],
                                                                   transelator_en_name=data['edition']['englishName'],
                                                                   format=data['edition']['format'],
                                                                   type=data['edition']['type'],
                                                                   ayah_number=ayah['number'],
                                                                   text=ayah['text'], audio=ayah['audio'],
                                                                   audio_secondary=audio_sec
                                                                   )
                            else:
                                surah_ayah = Quran_audio_ayah_info(identifier=data["edition"]["identifier"],
                                                                   surah_number=item["number"],
                                                                   surah_ar_name=item['name'],
                                                                   surah_en_name=item['englishName'],
                                                                   surah_en_name_translation=item[
                                                                       'englishNameTranslation'],
                                                                   revelation_type=item['revelationType'],
                                                                   juz=ayah['juz'],
                                                                   manzil=ayah['manzil'],
                                                                   page=ayah['page'], ruku=ayah['ruku'],
                                                                   hizb_quarter=ayah['hizbQuarter'],
                                                                   sajda=ayah['sajda'],
                                                                   language=data['edition']['language'],
                                                                   name=data['edition']['name'],
                                                                   transelator_en_name=data['edition']['englishName'],
                                                                   format=data['edition']['format'],
                                                                   type=data['edition']['type'],
                                                                   ayah_number=ayah['number'],
                                                                   text=ayah['text'], audio=ayah['audio'],
                                                                   audio_secondary=audio_sec
                                                                   )
                            db.session.add(surah_ayah)
                            db.session.commit()

    return "data hase been saved"


@app.route("/save_exist_name_language_in_db")
def save_exist_name_language_in_db():
    quran_lang_and_ed = Quran_text_ayah_info.query.with_entities(Quran_text_ayah_info.language,
                                                                 Quran_text_ayah_info.name).all()
    data = {}
    for item in quran_lang_and_ed:
        if data.get(item.language):
            if item.name not in data[item.language]:
                data[item.language].append(item.name)
        else:
            data[item.language] = [item.name]

    for item_lang in data:
        for item_name in data[item_lang]:
            exist_quran_ed = Quran_exist_in_database.query.filter_by(name=item_name, language=item_lang).first()
            if not exist_quran_ed:
                quran_ed = Quran_exist_in_database(name=item_name, language=item_name)
                db.session.add(quran_ed)
                db.session.commit()
                print(type(item_name, item_name))
            else:
                print(type("no new edition"))
                return "no new edition"

    return "data hase been saved"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/quran')
def quran():
    sample_quran = Quran_Info.query.all()
    return render_template('quran.html', sample_quran=sample_quran)


@app.route('/get_quran')
def get_quran():
    sample_quran = Quran_Info.query.with_entities(Quran_Info.surah_number, Quran_Info.surah_en_name,
                                                  Quran_Info.total_ayah).all()
    data = {}
    for item in sample_quran:
        data[str(item[0]) + '.' + item[1]] = [item[2]]
    return jsonify(data)


@app.route('/surah/<int:surah_number>')
def surah(surah_number):
    bismillah_auzubillah = Quran_text_ayah_info.query.filter_by(surah_number=0).order_by(Quran_text_ayah_info.id).all()
    sample_surah = Quran_text_ayah_info.query.filter_by(surah_number=surah_number, name="Uthamani").order_by(
        Quran_text_ayah_info.id).all()
    if sample_surah.__len__() != 0:
        return render_template("surah.html", sample_surah=sample_surah, bismillah_auzubillah=bismillah_auzubillah)


@app.route('/surah/<surah_number>/<ar_name>')
def get_sample_surah_with_transelator_ar(surah_number, ar_name):
    bismillah_auzubillah = Quran_text_ayah_info.query.filter_by(surah_number=0).order_by(Quran_text_ayah_info.id).all()
    sample_surah = Quran_text_ayah_info.query.filter_by(surah_number=surah_number, name=ar_name).order_by(
        Quran_text_ayah_info.id).all()
    if sample_surah.__len__() != 0:
        return render_template("surah.html", sample_surah=sample_surah, bismillah_auzubillah=bismillah_auzubillah)


@app.route('/audio/<surah_number>/<audio_name>')
def get_sample_surah_with_audio_ar(surah_number, audio_name):
    sample_surah = Quran_audio_ayah_info.query.filter_by(surah_number=surah_number, name=audio_name).with_entities(
        Quran_audio_ayah_info.identifier, Quran_audio_ayah_info.ayah_number, Quran_audio_ayah_info.audio_secondary). \
        order_by(Quran_audio_ayah_info.id).all()

    data = {}
    for item in sample_surah:
        if data.get(item.identifier):
            if item.ayah_number not in data[item.identifier]:
                data[item.identifier].append(item.ayah_number)
        else:
            data[item.identifier] = [item.ayah_number]

    return jsonify(data)


@app.route('/surah/<surah_number>/<ar_name>/<name>')
def get_sample_surah_with_transelator(surah_number, ar_name, name):
    surah_translation = Quran_text_ayah_info.query.filter_by(surah_number=surah_number, name=name).with_entities(
        Quran_text_ayah_info.text).order_by(
        Quran_text_ayah_info.id).all()
    return jsonify(surah_translation)


@app.route('/get_translator', methods=['GET', 'POST'])
def get_translator():
    lang = request.args.get("lang")
    quran = Quran_exist_in_database.query.filter_by(language=lang).with_entities(Quran_exist_in_database.name).all()
    return jsonify(quran)


@app.route('/get_surah_text_lang', methods=['POST'])
def get_surah_text_lang():
    quran_lang_and_ed = Quran_exist_in_database.query.all()
    data = {}
    for item in quran_lang_and_ed:
        if data.get(item.language):
            if item.name not in data[item.language]:
                data[item.language].append(item.name)
        else:
            data[item.language] = [item.name]

    return jsonify(data)


@app.route('/get_surah_audio', methods=['POST'])
def get_surah_audio():
    data = Quran_audio_ayah_info.query.with_entities(Quran_audio_ayah_info.transelator_en_name).distinct().all()
    return jsonify(data)


@app.route('/get_namaz_time_by_device_latitude_longitude', methods=['GET'])
def get_namaz_time_by_device_latitude_longitude():
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    method = request.args.get("method")
    today = re.split("-", str(date.today()))

    response = requests.get('http://api.aladhan.com/v1/timings/' + today[2] + '-' + today[1] + '-' + today[
        0] + '?latitude=' + latitude + '&longitude=' + longitude + '&method=' + method)
    return jsonify(json.loads(response.content)["data"]['timings'])


@app.route('/get_namaz_time_by_address', methods=['GET'])
def get_namaz_time_by_address():
    address = request.args.get("address")
    method = request.args.get("method")
    today = re.split("-", str(date.today()))
    response = requests.get(
        'https://api.aladhan.com/timingsByAddress/' + today[2] + '-' + today[1] + '-' + today[
            0] + '?address=' + address + '&method=' + method)

    return jsonify(json.loads(response.content)["data"]['timings'])


@app.route('/get_addresses_from_db')
def get_addresses_from_db():
    term = request.args['term']
    search = "{}%".format(term.lower())
    data = World_cities.query.filter(
        or_((func.lower(World_cities.city).like(search)), (func.lower(World_cities.country).like(search)))).all()
    results = []
    for item in data:
        address = ','.join((item.city, item.country))
        results.append({"id": address, "text": address})
    return {"results": results}


if __name__ == '__main__':
    app.run(debug=True)
