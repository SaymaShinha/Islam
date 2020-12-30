import datetime
import errno
import os
import re
import geocoder as geocoder
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
import json
import csv
from sqlalchemy import or_, func
from sqlalchemy.dialects.mysql import TEXT

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://sayma:Depasse1!@localhost:3306/Islam"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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


class Rev_Quran_Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chronological_order = db.Column(db.Integer, nullable=False)
    traditional_order = db.Column(db.Integer, nullable=False)
    surah_ar_name = db.Column(db.String(50), nullable=False)
    surah_en_name = db.Column(db.String(50), nullable=False)
    surah_en_name_translation = db.Column(db.String(50), nullable=False)
    location_of_revelation = db.Column(db.String(50), nullable=False)
    total_ayah = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(100), nullable=False)


class Quran_exist_in_database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(300), nullable=False)
    name = db.Column(db.String(300), nullable=False)


class World_cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(300), nullable=False)
    country = db.Column(db.String(300), nullable=False)
    subcountry = db.Column(db.String(300), nullable=False)


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False, default="")
    identifier = db.Column(db.String(100), nullable=False)
    transelator_en_name = db.Column(db.String(150), nullable=False)
    language = db.Column(db.String(150), nullable=False)


class Quran_text_ayah_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(120), nullable=False)
    surah_number = db.Column(db.Integer, nullable=False)
    surah_ar_name = db.Column(db.String(500), nullable=False)
    surah_en_name = db.Column(db.String(120), nullable=False)
    surah_en_name_translation = db.Column(db.String(200), nullable=False)
    revelation_type = db.Column(db.String(120), nullable=False)
    ayah_number = db.Column(db.Integer, nullable=False)
    text = db.Column(TEXT, nullable=False)
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


class Allah_Names(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Ar_name = db.Column(db.String(300), nullable=False)
    Ar_transliteration = db.Column(db.String(300), nullable=False)
    Pronunciation = db.Column(db.String(300), nullable=False)
    Meaning_En = db.Column(db.String(300), nullable=False)


class Quran_audio_ayah_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(120), nullable=False)
    surah_number = db.Column(db.Integer, nullable=False)
    surah_ar_name = db.Column(db.String(500), nullable=False)
    surah_en_name = db.Column(db.String(120), nullable=False)
    surah_en_name_translation = db.Column(db.String(200), nullable=False)
    revelation_type = db.Column(db.String(120), nullable=False)
    ayah_number = db.Column(db.Integer, nullable=False)
    audio = db.Column(db.String(300), nullable=False)
    audio_secondary = db.Column(db.String(300), nullable=False)
    text = db.Column(TEXT, nullable=False)
    juz = db.Column(db.Integer, nullable=False)
    manzil = db.Column(db.Integer, nullable=False)
    surah_page = db.Column(db.Integer, nullable=False)
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


@app.route('/save_language')
def save_language():
    data = Quran_text_ayah_info.query.with_entities(Quran_text_ayah_info.identifier,
                                                    Quran_text_ayah_info.transelator_en_name,
                                                    Quran_text_ayah_info.language).distinct(
        Quran_text_ayah_info.identifier).all()

    for item in data:
        lang = Language(identifier=item[0], transelator_en_name=item[1], language=item[2])

        db.session.add(lang)

    db.session.commit()

    data_file = {}
    quran_lang_and_ed = Language.query.all()

    for item in quran_lang_and_ed:
        if data_file.get(item.language):
            if item.transelator_en_name not in data_file[item.language]:
                data_file[item.language].append({'identifier': item.identifier,
                                                 'transelator_en_name': item.transelator_en_name,
                                                 'file_name': item.file_name})
        else:
            data_file[item.language] = [{'identifier': item.identifier,
                                         'transelator_en_name': item.transelator_en_name, 'file_name': item.file_name}]

    with open('language.json', 'w') as f:
        f.write(json.dumps([data_file]))
        print("saved")

    return "data has been saved"


@app.route('/save_allah_names_from_saved_file')
def save_allah_names_from_saved_file():
    with open('Allah_Names.csv', encoding="utf8") as f:
        reader = csv.reader(f)
        save_name_list = list(reader)

        for item in save_name_list:
            names = Allah_Names(Ar_name=item[1], Ar_transliteration=item[2],
                                Pronunciation=re.split(":", item[3])[re.split(":", item[3]).__len__() - 1],
                                Meaning_En=item[4])
            db.session.add(names)
        db.session.commit()
    return "data has been saved"


@app.route('/save_world_cities_from_saved_file')
def save_world_cities_from_saved_file():
    response = requests.get(
        "https://raw.githubusercontent.com/SaymaShinha/islamDB/master/islam_public_world_cities.json")

    data = json.loads(response.content)

    for item in data:
        cities = World_cities(city=item['city'], country=item['country'], subcountry=item['subcountry'])
        db.session.add(cities)
    db.session.commit()

    return "data has been saved"


@app.route('/save_quran_surah_info')
def save_quran_surah_info():
    response = requests.get(
        "https://raw.githubusercontent.com/SaymaShinha/islamDB/master/islam_public_quran__info.json")

    data = json.loads(response.content)

    for item in data:
        quran = Quran_Info(surah_number=item['surah_number'], surah_ar_name=item['surah_ar_name'],
                           surah_en_name=item['surah_en_name'],
                           surah_en_name_translation=item['surah_en_name_translation'],
                           revelation_type=item['revelation_type'], total_ayah=item['total_ayah'])
        db.session.add(quran)

    db.session.commit()

    return "data has been saved"


############################################################################
@app.route('/save_text_quran')
def save_text_quran():
    language = Language.query.all()

    for lang_item in language:
        response = requests.get(
            "https://raw.githubusercontent.com/SaymaShinha/islamDB/master/islam_public_"+ lang_item.file_name +".json")

        data = json.loads(response.content)
        for item in data:
            surah_ayah = Quran_text_ayah_info(identifier=item['identifier'],
                                              surah_number=item['surah_number'],
                                              surah_ar_name=item['surah_ar_name'], surah_en_name=item['surah_en_name'],
                                              surah_en_name_translation=item['surah_en_name_translation'],
                                              revelation_type=item['revelation_type'], juz=item['juz'],
                                              manzil=item['manzil'],
                                              page=item['page'], ruku=item['ruku'],
                                              hizb_quarter=item['hizb_quarter'],
                                              sajda=item['sajda'], sajda_id=item['sajda_id'],
                                              sajda_obligatory=item['sajda_obligatory'],
                                              sajda_recommended=item['sajda_recommended'],
                                              language=item['language'],
                                              name=item['name'],
                                              transelator_en_name=item['transelator_en_name'],
                                              format=item['format'],
                                              type=item['type'], ayah_number=item['ayah_number'],
                                              text=item['text'])
            db.session.add(surah_ayah)
        db.session.commit()


@app.route('/save_text_quran_in_file')
def save_text_quran_in_file():
    language = Language.query.all()

    for lang_item in language:
        try:
            os.makedirs(lang_item.file_name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        for x in range(114):
            surah = Quran_text_ayah_info.query.filter_by(surah_number=x + 1, identifier=lang_item.identifier).order_by(
                Quran_text_ayah_info.ayah_number).all()

            results = []
            for item in surah:
                results.append({"id": item.id, "identifier": item.identifier,
                                "surah_number": item.surah_number, "surah_ar_name": item.surah_ar_name,
                                "surah_en_name": item.surah_en_name,
                                "surah_en_name_translation": item.surah_en_name_translation,
                                "revelation_type": item.revelation_type, "juz": item.juz,
                                "manzil": item.manzil,
                                "page": item.page, "ruku": item.ruku,
                                "hizb_quarter": item.hizb_quarter,
                                "sajda": item.sajda, "sajda_id": item.sajda_id,
                                "sajda_obligatory": item.sajda_obligatory,
                                "sajda_recommended": item.sajda_recommended,
                                "language": item.language,
                                "name": item.name,
                                "transelator_en_name": item.transelator_en_name,
                                "format": item.format,
                                "type": item.type, "ayah_number": item.ayah_number,
                                "text": item.text})

            with open(str(x + 1) + '.json', 'w') as f:
                f.write(json.dumps(results))
                print("saved: " + str(x + 1))

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


############################################################################


@app.route('/')
def home():
    names = get_allah_names()

    return render_template('index.html', names=names)


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


@app.route('/get_namaztime_by_device_location', methods=['GET'])
def get_namaztime_by_device_location():
    myloc = geocoder.ip('me')
    device_location = json.loads(myloc.response.content)

    return get_namaz_time_by_address(device_location['city'] + ',' + device_location['country'])


@app.route('/get_namaz_time_by_address/<address>', methods=['GET'])
def get_namaz_time_by_address(address):
    response = requests.get(
        'http://api.aladhan.com/v1/timingsByAddress?address=' + address + '&method=2')

    return jsonify(json.loads(response.content)["data"]['timings'], {'address': address})


#####

@app.route('/get_arabic_calender', methods=['GET'])
def get_arabic_calender():
    current_date = datetime.datetime.now()

    response = requests.get('http://api.aladhan.com/v1/gToH?date='
                            + str(current_date.day) + '-' + str(current_date.month) + '-' + str(current_date.year))

    return jsonify(json.loads(response.content)["data"])


#####


@app.route('/get_allah_names')
def get_allah_names():
    response = requests.get('https://raw.githubusercontent.com/SaymaShinha/islamDB/master/AAllah_99_names.json')
    data = json.loads(response.content)

    return data


#######################################
@app.route('/quran')
def quran():
    return render_template('quran.html')


@app.route('/get_quran_by_sort', methods=['GET'])
def get_quran_by_sort():
    sort_by = request.args.get("sort_by")

    if sort_by == None:
        sample_quran = Quran_Info.query.order_by(Quran_Info.id).all()

    elif sort_by == "Traditional Order":
        sample_quran = Quran_Info.query.order_by(Quran_Info.id).all()

    elif sort_by == "According To Revelation":
        response = requests.get('https://raw.githubusercontent.com/SaymaShinha/islamDB/master/Allah_99_names.json')
        data = json.loads(response.content)

        return data

    elif sort_by == "Desc Surah Name":
        sample_quran = Quran_Info.query.order_by(Quran_Info.surah_en_name.desc()).all()

    elif sort_by == "Desc Surah Total Ayah":
        sample_quran = Quran_Info.query.order_by(Quran_Info.total_ayah.desc()).all()

    elif sort_by == "Asc Surah Total Ayah":
        sample_quran = Quran_Info.query.order_by(Quran_Info.total_ayah.asc()).all()

    elif sort_by == "Meccan Surah":
        sample_quran = Quran_Info.query.filter_by(revelation_type="Meccan").all()

    elif sort_by == "Medinan Surah":
        sample_quran = Quran_Info.query.filter_by(revelation_type="Medinan").all()

    results = []
    for item in sample_quran:
        results.append({"surah_number": item.surah_number, "surah_ar_name": item.surah_ar_name,
                        "surah_en_name": item.surah_en_name,
                        "surah_en_name_translation": item.surah_en_name_translation,
                        "revelation_type": item.revelation_type, "total_ayah": item.total_ayah, "note": ""})

    return jsonify(results)


#########################################


@app.route('/fill_surah')
def fill_surah():
    surah = Quran_Info.query.with_entities(Quran_Info.surah_number, Quran_Info.surah_en_name,
                                           Quran_Info.total_ayah).order_by(
        Quran_Info.id).all()
    results = []
    for item in surah:
        results.append(
            {"surah_number": item.surah_number, "surah_en_name": item.surah_en_name, "total_ayah": item.total_ayah})

    return jsonify(results)


@app.route('/surah/<int:surah_number>')
def surah(surah_number):
    response = requests.get(
        'https://raw.githubusercontent.com/SaymaShinha/islamDB/master/ar__uthmani/' + str(surah_number) + '.json')
    sample_surah = json.loads(response.content)

    return render_template('surah.html', sample_surah=sample_surah)


@app.route('/get_surah_ar')
def get_surah_ar():
    surah_number = request.args.get('surah_number')

    response = requests.get(
        'https://raw.githubusercontent.com/SaymaShinha/islamDB/master/ar__uthmani/' + str(surah_number) + '.json')

    data = json.loads(response.content)
    return json.dumps(data, indent=2, sort_keys=True)


@app.route('/fill_trans_language')
def fill_trans_language():
    response = requests.get('https://raw.githubusercontent.com/SaymaShinha/islamDB/master/language.json')
    data = json.loads(response.content)

    return jsonify(data)


@app.route('/get_surah_trans', methods=['GET'])
def get_surah_trans():
    surah_number = request.args.get('surah_number')
    file_name = request.args.get('file_name')

    response = requests.get(
        'https://raw.githubusercontent.com/SaymaShinha/islamDB/master/'+ file_name +'/' + str(surah_number) + '.json')

    data = json.loads(response.content)
    return json.dumps(data, indent=2, sort_keys=True)




if __name__ == '__main__':
    app.run(debug=True)
