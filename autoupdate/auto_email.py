# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import loader
from django.core.mail import mail_admins

from datetime import date

import requests
import json
import shortuuid


def create_new_videos_template(videos):
    template = loader.get_template('email-new-videos.html')
    content = template.render({
        'videos':videos,
        'WEBSITE_URL': settings.WEBSITE_URL[:-1]
    })
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
    if r.status_code / 100 != 2:
        mail_admins(
            subject='problem creating template for auto email',
            message=str(r)
        )
        return None
    r_content =  json.loads(r.content)
    return r_content['id']


def create_new_videos_campaign(template_id):
    url = 'https://us16.api.mailchimp.com/3.0/campaigns/'
    subject = 'Novos vídeos no site Direito em Tela!'
    preview = 'Tem vídeo fresquinho no Direito em Tela'
    title = 'new-videos-campaign-' + str(date.today()) + '-' + shortuuid.uuid()[:4]
    json_data = {
        'type': 'regular',
        'recipients': {
            'list_id': settings.MAILCHIMP_USER_LIST_ID,
        },
        'settings': {
            'subject_line': subject,
            'preview_text': preview,
            'title': title,
            'from_name': 'Equipe Direito em Tela',
            'reply_to': settings.DEFAULT_REPLY_TO_EMAIL,
            'template_id': template_id,
        },
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
    if r.status_code / 100 != 2:
        mail_admins(
            subject='problem creating campaign for auto email',
            message=str(r)
        )
        return None
    r_content =  json.loads(r.content)
    return r_content['id']


def send_campaign(campaign_id):
    url = 'https://us16.api.mailchimp.com/3.0/campaigns/'
    url += campaign_id
    url += '/actions/send'
    r = requests.post(
        url,
        auth=(
            'ILoveBlowjobs',
            settings.MAILCHIMP_API_KEY
        ),
    )
    if r.status_code / 100 != 2:
        mail_admins(
            subject='problem sending campaign for auto email',
            message=str(r)
        )
        return False
    return True

def send_new_videos_campaign(videos):
    template_id = create_new_videos_template(videos)
    if template_id is None:
        return False
    campaign_id = create_new_videos_campaign(template_id)
    if campaign_id is None:
        return False
    return send_campaign(campaign_id)
