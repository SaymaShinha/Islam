import re
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_migrate import Migrate
import requests
import json
import unicodedata

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://sayma:123@localhost:5432/islam"
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


class Quran_ayah_info(db.Model):
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
    sajda_obligatory = db.Column(db.Boolean, nullable=True)
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
        exist_quran_ed = Quran_ayah_info.query.filter_by(identifier=item_ed).first()
        if not exist_quran_ed:
            response = requests.get("http://api.alquran.cloud/v1/quran/" + item_ed.identifier)
            data = json.loads(response.content)["data"]
        for item in data["surahs"]:
            for ayah in item['ayahs']:
                print(type(ayah['sajda']))
                if type(ayah['sajda']) is dict:
                    surah_ayah = Quran_ayah_info(identifier=data["edition"]["identifier"],
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
                    surah_ayah = Quran_ayah_info(identifier=data["edition"]["identifier"],
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
        exist_quran_ed = Quran_ayah_info.query.filter_by(identifier=item_ed.identifier).first()
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

    return "data hase been saved";


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/quran')
def get_sample_quran():
    sample_quran = Quran_Info.query.all()
    return render_template('quran.html', sample_quran=sample_quran)


@app.route('/surah/<int:surah_number>')
def get_sample_surah(surah_number):
    bismillah_auzubillah = Quran_ayah_info.query.filter_by(surah_number=0).order_by(Quran_ayah_info.id).all()
    sample_surah = Quran_ayah_info.query.filter_by(surah_number=surah_number, name="Uthamani").order_by(
    Quran_ayah_info.id).all()
    return render_template('surah.html', sample_surah=sample_surah, bismillah_auzubillah=bismillah_auzubillah)

@app.route('/surah/<int:surah_number>/<string:name>', methods=['GET',])
def get_sample_surah_with_transelator(surah_number, name):
    surah_translation = Quran_ayah_info.query.filter_by(surah_number=surah_number, name=name).with_entities(Quran_ayah_info.text).order_by(
    Quran_ayah_info.id).all()
    return jsonify(surah_translation)

@app.route('/get_lang_ed', methods=['GET'])
def get_lang_ed():
    lang = request.args.get("lang")
    quran_ed = Quran_Editions.query.filter_by(format="text", language=lang).with_entities(Quran_Editions.name).all()
    return jsonify(quran_ed)

@app.route('/get_default_lang_and_ed', methods=['POST'])
def get_default_lang_and_ed():
    quran_lang_and_ed = Quran_Editions.query.filter_by(format="text").with_entities(Quran_Editions.language,
                                                                                    Quran_Editions.name).all()
    data = {}
    for item in quran_lang_and_ed:
        if data.get(item.language):
            data[item.language].append(item.name)
        else:
            data[item.language] = [item.name]

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
