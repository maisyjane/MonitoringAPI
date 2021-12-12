from flask import Flask, Response, request, render_template, make_response
from config import proxys
import requests
from flask_mail import Mail, Message
from io import StringIO
from flask_apscheduler import APScheduler
import csv
import random
import time
import atexit
from werkzeug.exceptions import abort  # do error handling on metrics container itself

scheduler = APScheduler()
app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_TLS'] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'qubeditoron3000@gmail.com'
app.config["MAIL_PASSWORD"] = 'editoron1'

mail = Mail(app)


@scheduler.task("interval", id="monitor", minutes=30, misfire_grace_time=900)
@app.route('/', methods=['GET'])
def monitoring():
    with scheduler.app.app_context():
        return get_request(get_random_string())


@app.route('/manual', methods=['POST'])
def manual_monitoring():
    if request.method == 'POST':
        testing_input = request.form['Test']
        return get_request(testing_input)


def get_random_string():
    random_string = ""
    for _ in range(10):
        # Considering only upper and lowercase letters
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)
        # Convert to lowercase if the flip bit is on
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        # Keep appending random characters using chr(x)
        random_string += (chr(random_integer))
    return random_string


def get_request(parameter):
    random_text_string = parameter
    comma_count_urls = []
    comma_count_responses = []
    comma_count_json = []
    comma_count_response_times = []
    comma_count_status_codes = []
    vowel_count_urls = []
    vowel_count_responses = []
    vowel_count_response_times = []
    vowel_count_json = []
    vowel_count_status_codes = []
    word_count_urls = []
    word_count_responses = []
    word_count_response_times = []
    word_count_json = []
    word_count_status_codes = []
    char_count_urls = []
    char_count_responses = []
    char_count_response_times = []
    char_count_json = []
    char_count_status_codes = []
    avg_word_urls = []
    avg_word_responses = []
    avg_word_response_times = []
    avg_word_json = []
    avg_word_status_codes = []
    and_count_urls = []
    and_count_responses = []
    and_count_response_times = []
    and_count_json = []
    and_count_status_codes = []
    danger = False;

    for i in range(len(proxys)):
        comma_count_urls.append(proxys[i] + "commacount/?x=" + random_text_string)
        vowel_count_urls.append(proxys[i] + "vowelcount/?x=" + random_text_string)
        word_count_urls.append(proxys[i] + "wordcount/?x=" + random_text_string)
        char_count_urls.append(proxys[i] + "charcount/?x=" + random_text_string)
        avg_word_urls.append(proxys[i] + "avgwordlength/?x=" + random_text_string)
        and_count_urls.append(proxys[i] + "andcount/?x=" + random_text_string)

    for i in range(len(proxys)):
        comma_count_responses.append(requests.get(comma_count_urls[i]))
        vowel_count_responses.append(requests.get(vowel_count_urls[i]))
        word_count_responses.append(requests.get(word_count_urls[i]))
        char_count_responses.append(requests.get(char_count_urls[i]))
        avg_word_responses.append(requests.get(avg_word_urls[i]))
        and_count_responses.append(requests.get(and_count_urls[i]))

    for i in range(len(proxys)):
        comma_count_response_times.append(comma_count_responses[i].elapsed.total_seconds())
        vowel_count_response_times.append(vowel_count_responses[i].elapsed.total_seconds())
        word_count_response_times.append(word_count_responses[i].elapsed.total_seconds())
        char_count_response_times.append(char_count_responses[i].elapsed.total_seconds())
        avg_word_response_times.append(avg_word_responses[i].elapsed.total_seconds())
        and_count_response_times.append(and_count_responses[i].elapsed.total_seconds())

    for i in range(len(proxys)):
        comma_count_status_codes.append(comma_count_responses[i].status_code)
        vowel_count_status_codes.append(vowel_count_responses[i].status_code)
        word_count_status_codes.append(word_count_responses[i].status_code)
        char_count_status_codes.append(char_count_responses[i].status_code)
        avg_word_status_codes.append(avg_word_responses[i].status_code)
        and_count_status_codes.append(and_count_responses[i].status_code)

    for i in range(len(proxys)):
        if comma_count_status_codes[i] == 200:
            comma_count_json.append(comma_count_responses[i].json())
        else:
            comma_count_json.append("Bad Response")
            danger = True
        if vowel_count_status_codes[i] == 200:
            vowel_count_json.append(vowel_count_responses[i].json())
        else:
            vowel_count_json.append("Bad Response")
            danger = True
        if word_count_status_codes[i] == 200:
            word_count_json.append(word_count_responses[i].json())
        else:
            word_count_json.append("Bad Response")
            danger = True
        if char_count_status_codes[i] == 200:
            char_count_json.append(char_count_responses[i].json())
        else:
            char_count_json.append("Bad Response")
            danger = True
        if avg_word_status_codes[i] == 200:
            avg_word_json.append(avg_word_responses[i].json())
        else:
            avg_word_json.append("Bad Response")
            danger = True
        if and_count_status_codes[i] == 200:
            and_count_json.append(and_count_responses[i].json())
        else:
            and_count_json.append("Bad Response")
            danger = True

    if danger:
        alert()
    print("Scheduler: New Job Starting")
    # response_times = comma_count_response_times + char_count_response_times + word_count_response_times + \
    # avg_word_response_times + and_count_response_times + vowel_count_response_times
    # write2csv(response_times)
    return render_template('frontend.html',
                           comma_count_status_codes=comma_count_status_codes,
                           vowel_count_status_codes=vowel_count_status_codes,
                           and_count_status_codes=and_count_status_codes,
                           word_count_status_codes=word_count_status_codes,
                           char_count_status_codes=char_count_status_codes,
                           avg_word_status_codes=avg_word_status_codes,
                           comma_count_json=comma_count_json,
                           vowel_count_json=vowel_count_json,
                           and_count_json=and_count_json,
                           word_count_json=word_count_json,
                           char_count_json=char_count_json,
                           avg_word_json=avg_word_json,
                           comma_count_response_times=comma_count_response_times,
                           vowel_count_response_times=vowel_count_response_times,
                           word_count_response_times=avg_word_response_times,
                           char_count_response_times=char_count_response_times,
                           and_count_response_times=and_count_response_times,
                           avg_word_response_times=avg_word_response_times
                           )


def alert():
    msg = Message('Hello', sender='yourId@gmail.com', recipients=['qubeditoron3000@gmail.com'])
    msg.body = "Connection is Down"
    mail.send(msg)


def write2csv(values):
    with open('../ResponseTimes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for value in values:
            writer.writerow(value)


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=5002)
