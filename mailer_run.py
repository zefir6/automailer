# coding=UTF-8
from flask import Flask, render_template, flash, redirect, url_for, make_response, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import os
import time
import atexit
from itsdangerous import URLSafeTimedSerializer
from get_template import pobierz_wzor_maila
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gmail import gmail_message
from flask_httpauth import HTTPBasicAuth
import threading
import random
from time import sleep

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == app.config['CNP_API_ACCESS_USER']:
        return app.config['CNP_API_ACCESS_KEY']
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


def confirmation_link(email):
    token = generate_confirmation_token(email=email)
    print("Token: {} for {}".format(token, email))
    with app.app_context():
        confirm_url = url_for('confirm_email', token=token, _external=True)
    # print("We generated confrimation link {} for email {}".format(confirm_url, email))
    return confirm_url

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=86400):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

def otworz_arkusz():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(app.config['MAILLIST_JSON_KEYFILE'], app.config['SCOPE'])
    gc = gspread.authorize(credentials)
    arkusz = gc.open_by_key(app.config['MAILLIST_GDOCS_ID'])
    return arkusz

def update_user_status(arkusz, email, status):
    odbiorcy = arkusz.get_all_records()
    for rekord_odbiorcy in odbiorcy:
        if rekord_odbiorcy['Email Odbiorcy'] == email:
            status_column = arkusz.find("Status").col
            wiersz = odbiorcy.index(rekord_odbiorcy) + 2
            arkusz.update_cell(wiersz, status_column, status)

def run_mailing(mail_template_credentials_json, json_keyfile, lista_odbiorcow, scope):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    gc = gspread.authorize(credentials)
    arkusz = gc.open_by_key(lista_odbiorcow)
    arkusz_sesji = arkusz.get_worksheet(0)
    arkusz_informacje_ogolne = arkusz.get_worksheet(1)
    czy_procesowac = arkusz_informacje_ogolne.acell('C2').value
    informacje_ogolne = dict()
    informacje_ogolne['mail_dw'] = arkusz_informacje_ogolne.acell('A2').value
    informacje_ogolne['nadawca'] = arkusz_informacje_ogolne.acell('B2').value
    # informacje_ogolne['subject'] = arkusz_informacje_ogolne.acell('A6').value

    print(czy_procesowac)
    if czy_procesowac == 'TAK':
        ### TESTY START

        statuses = {'sent': 'Mail Wysłany', 'confirmed': 'Gracz Potwierdził'}
        wyslane = [ 'Mail Wysłany', 'Gracz Potwierdził']

        odbiorcy = arkusz_sesji.get_all_records()

        status_column = arkusz_sesji.find("Status").col
        print(status_column)

        for rekord_odbiorcy in odbiorcy:
            waittime = random.randrange(1, 5, 1)
            sleep(waittime)
            # print(rekord_odbiorcy)

            pola = {
                "email": rekord_odbiorcy['Email Odbiorcy'],
                "Pole 1": rekord_odbiorcy['Pole 1'],
                "Pole 2": rekord_odbiorcy['Pole 2'],
                "Pole 3": rekord_odbiorcy['Pole 3'],
                "Pole 4": rekord_odbiorcy['Pole 4'],
                "Pole 5": rekord_odbiorcy['Pole 5'],
                "Pole 6": rekord_odbiorcy['Pole 6'],
                "Pole 7": rekord_odbiorcy['Pole 7']
            }

            wiersz = odbiorcy.index(rekord_odbiorcy) + 2
            # print("Wiersz w arkuszu: {}".format(wiersz))
            # val = arkusz_sesji.cell(wiersz, 1).value

            status = rekord_odbiorcy['Status']

            if status not in statuses.values():
                print("Procesujemy rekord")
                pola['link'] = confirmation_link(rekord_odbiorcy['Email Odbiorcy'])
                print("Próbujemy uzyć formatki maila z: {}".format(rekord_odbiorcy['Formatka']))
                wzor_maila = pobierz_wzor_maila(credentials_json=mail_template_credentials_json,
                                                DOCUMENT_ID=rekord_odbiorcy['Formatka'])
                print(wzor_maila.format(**pola))
                gmail_message(sender=informacje_ogolne['nadawca'], gmail_json=app.config['GMAIL_JSON'], subject=rekord_odbiorcy['Temat maila'], to=pola['email'], cc=informacje_ogolne['mail_dw'], contents=wzor_maila.format(**pola), auth_hostname=app.config['GMAIL_AUTH_HOSTNAME'], auth_port=app.config['GMAIL_AUTH_PORT'])
                arkusz_sesji.update_cell(wiersz, status_column, statuses['sent'])
            else:
                print("Wiersz {} już przetworzony".format(wiersz))

        # print(arkusz_sesji.col_values(1))
        # print(arkusz_sesji.col_values(2))

        arkusz_informacje_ogolne.update_acell('C2', 'NIE')
        print("""Zmieniam "Czy wysyłać" z powrotem na NIE""")
    else:
        print("Ustawione na nie, nic nie robimy!")



def mailing():
    # print(app.config['MAIL_TEMPLATE_CREDENTIALS'])
    # run_mailing(mail_template_credentials_json=app.config['MAIL_TEMPLATE_CREDENTIALS'], json_keyfile=app.config['MAILLIST_JSON_KEYFILE'], lista_odbiorcow=app.config['MAILLIST_GDOCS_ID'], scope=app.config['SCOPE'])
    run_mailing(mail_template_credentials_json=app.config['MAILLIST_JSON_KEYFILE'],
                json_keyfile=app.config['MAILLIST_JSON_KEYFILE'], lista_odbiorcow=app.config['MAILLIST_GDOCS_ID'],
                scope=app.config['SCOPE'])




import threading
class AsyncMailing(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Starting background task - init")
    def run(self):
        print("Running mailing method")
        mailing()
        # try:
        #     mailing()
        # except:
        #     print("Cos poszlo nie tak przy probie mailingu, sprawdz czy masz pliki kluczy w katalogu: {}\n{}\n{}\n".format(app.config['MAILLIST_JSON_KEYFILE'],app.config['MAILLIST_JSON_CREDENTIALS_FILE'],app.config['GMAIL_JSON']))


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=mailing, trigger="interval", seconds=10)
# scheduler.start()
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    print("Back to main")
    return render_template('index.html')

@app.route('/api/mailrun')
# @auth.login_required
def mailrun():
    print("Running mailing")
    # try:
        # mailing()
    asyncmailing = AsyncMailing()
    asyncmailing.start()
    # return render_template('mailing_started.html')
    return make_response(jsonify({'status':'Mailing started'}))
    # except:
    #     print("Something went wrong, when running mailing")
    #     return make_response(jsonify({'error': 'Something went wrong when starting mailing'}), 500)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token=token)
        print("{} confirmed his token".format(email))
        arkusz = otworz_arkusz()
        arkusz_odbiorcy = arkusz.get_worksheet(0)
        update_user_status(arkusz_odbiorcy, email, 'Gracz Potwierdził')
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        print('The confirmation link is invalid or has expired.', 'danger')
    # user = User.query.filter_by(email=email).first_or_404()
    # if user.confirmed:
    #     flash('Account already confirmed. Please login.', 'success')
    # else:
    #     # user.confirmed = True
    #     # user.confirmed_on = datetime.datetime.now()
    #     # # db.session.add(user)
    #     # db.session.commit()
    #     flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    listen = app.config['LISTEN']
    listenport = app.config['LISTEN_PORT']
    app.run(host=listen, port=listenport)
