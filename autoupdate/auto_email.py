# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import loader

from datetime import date

import requests
import json
import shortuuid

def create_new_template(videos):
    template = loader.get_template('email-new-videos.html')
    content = template.render({'videos':videos})
    url = 'https://us16.api.mailchimp.com/3.0/templates/'
    shortuuid.set_alphabet("abcdefghijklmnopqrstuvwxyz0123456789")
    template_name = 'new-videos-' + str(date.today()) + '-' + shortuuid.uuid()[:4]
    json_data = {
        'name': template_name,
        'html': content
    }
    json_data = json.dumps(json_data)
    json_data = json_data.encode('utf8')
    r = requests.post(
        url,
        auth=(
            'ILoveBlowjobs',
            settings.MAILCHIMP_API_KEY
        ),
        data=json_data
    )
    return r
    
    
