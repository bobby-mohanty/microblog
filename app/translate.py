import json
import requests
from flask_babel import _
from app import app


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in app.config or \
            not app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']}
    # r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
    #                  '/Translate?text={}&from={}&to={}'.format(
    #                      text, source_language, dest_language),
    #                  headers=auth)
    header = {}
    header.update({"Content-Type": "application/json; charset=UTF-8"})
    header.update(auth)
    body = [{'Text': text}]
    params = (
        ('api-version', '3.0'),
        ('from', source_language),
        ('to', dest_language),
    )
    r = requests.post("https://api.cognitive.microsofttranslator.com/translate",
                      headers=header, params=params, data=str(json.dumps(body)))
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    response_json = json.loads(r.content.decode('utf-8-sig'))
    return response_json[0]['translations'][0]['text']
