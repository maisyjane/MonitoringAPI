from flask import Flask, Response, request, render_template
from config import proxys
import requests
import json
from werkzeug.exceptions import abort

app = Flask(__name__)


def get_request(testing_input):
    random_text_string = testing_input
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
        if vowel_count_status_codes[i] == 200:
            vowel_count_json.append(vowel_count_responses[i].json())
        else:
            vowel_count_json.append("Bad Response")
        if word_count_status_codes[i] == 200:
            word_count_json.append(word_count_responses[i].json())
        else:
            word_count_json.append("Bad Response")
        if char_count_status_codes[i] == 200:
            char_count_json.append(char_count_responses[i].json())
        else:
            char_count_json.append("Bad Response")
        if avg_word_status_codes[i] == 200:
            avg_word_json.append(avg_word_responses[i].json())
        else:
            avg_word_json.append("Bad Response")
        if and_count_status_codes[i] == 200:
            and_count_json.append(and_count_responses[i].json())
        else:
            and_count_json.append("Bad Response")

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
                           )


@app.route('/', methods=['GET', 'POST'])
def monitoring():
    if request.method == 'GET':
        return get_request("test")
    if request.method == 'POST':
        testing_input = request.form['Test']
        return get_request(testing_input)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
