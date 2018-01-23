# -*- coding: utf-8 -*-
from django.conf import settings
from django.core import files
from django.core.mail import mail_admins
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from apiclient.discovery import build
from videos.models import Video, Tag
from categories.models import Category, VideoCategory, Professor
from datetime import datetime
from django.utils import timezone
import requests
import tempfile
import re
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

def get_new_video_ids():
    youtube = build(
        settings.YOUTUBE_API_SERVICE_NAME,
        settings.YOUTUBE_API_VERSION,
        developerKey=settings.YT_KEY)
    video_ids = []
    page_token = None
    no_results = 0
    while True:
        search_response = youtube.search().list(
            type="video",
            channelId='UCOEfipXIvMmAHgg8XPcBtag',
            pageToken=page_token,
            part='id, snippet',
            order='date',
            maxResults=50,
        ).execute()
        for search_result in search_response.get('items', []):
            result_id = search_result['id']['videoId']
            if Video.objects.filter(yt_id=result_id).exists():
                return video_ids
            video_ids.append(search_result['id']['videoId'])
        page_token = search_response.get('nextPageToken', None)
        no_results += len(search_response.get('items', []))
        if page_token is None or len(search_response.get('items', [])) < 1:
            break
    return video_ids

def get_sorting_factor(video_info):
    if not 'Aula' in video_info['title']:
        return 1000
    else:
        index_list = re.findall('Aula (\d+)', video_info['title'])
        if index_list:
            return int(index_list[0])
        else:
            return 1000

def get_videos_info(video_ids):
    youtube = build(
        settings.YOUTUBE_API_SERVICE_NAME,
        settings.YOUTUBE_API_VERSION,
        developerKey=settings.YT_KEY)
    page_token = None
    videos = []
    for i in range(int(len(video_ids)/50) + 1):
        ids_str = ','.join(video_ids[i*50 : (i + 1)*50])
        response = youtube.videos().list(
            id=ids_str,
            maxResults=50,
            pageToken=page_token,
            part='snippet',
        ).execute()
        page_token = response.get('nextPageToken', None)
        for item in response['items']:
            video_info = {}
            video = item['snippet']
            video_info['title'] = video['title']
            video_info['description'] = video['description']
            if 'tags' in video:
                video_info['tags'] = video['tags']
            video_info['id'] = item['id']
            if 'maxres' in video['thumbnails']:
                video_info['thumbnail_url'] = video['thumbnails']['maxres']['url']
            elif 'standard' in video['thumbnails']:
                video_info['thumbnail_url'] = video['thumbnails']['standard']['url']
            else:
                video_info['thumbnail_url'] = video['thumbnails']['high']['url']
            video_info['published_at'] = timezone.make_aware(datetime.strptime(video['publishedAt'], '%Y-%m-%dT%H:%M:%S.000Z'))
            videos.append(video_info)
    videos = sorted(videos, key=get_sorting_factor)
    return videos

def get_category_ids():
    youtube = build(
        settings.YOUTUBE_API_SERVICE_NAME,
        settings.YOUTUBE_API_VERSION,
        developerKey=settings.YT_KEY)
    response = youtube.playlists().list(
        part='snippet',
        channelId=settings.YT_CHANNEL_ID,
        maxResults=50
    ).execute()
    category_ids = [[item['id'], item['snippet']['title']] for item  in response['items']]
    category_ids.reverse()
    return category_ids

def clean_video_title(yt_title):
    if not 'aula' in yt_title.lower():
        return yt_title
    title_list = [x.strip() for x in yt_title.split('-')]
    del title_list[:2]
    if len(title_list) > 1 and title_list[0][:3].lower() == 'art':
        title_list[0], title_list[1] = title_list[1], title_list[0]
    title = ' - '.join(title_list)
    title.replace(u'Código Civil', 'CC')
    return title

def clean_video_description(yt_description):
    if not 'Para mais' in yt_description:
        return yt_description
    description = yt_description.split('Para mais')[0]
    description = description.strip()
    return description

def create_new_videos(videos_info):
    for video_info in videos_info:
        video = Video(
            yt_id=video_info['id'],
            yt_title=video_info['title'],
            published_at_yt=video_info['published_at'])
        video.title = clean_video_title(video_info['title'])
        video.description = clean_video_description(video_info['description'])
        video.save()
        request = requests.get(video_info['thumbnail_url'], stream=True)
        if request.status_code == requests.codes.ok:
            tempimg = tempfile.NamedTemporaryFile()
            for block in request.iter_content(1024 * 8):
                if not block:
                    break
                tempimg.write(block)
            video.thumbnail = files.File(tempimg)
            video.save()
            # make thumbnail be "cut" in the right ratio for the video thumbnails
            ratio = 275.0/154.0
            t_width = int(min(video.thumbnail.width, video.thumbnail.height * ratio))
            t_height = int(min(video.thumbnail.width / ratio, video.thumbnail.height))
            #center the cut
            y_origin = video.thumbnail.height/2 - t_height/2
            y_end = y_origin + t_height
            t_ratio = '0,' + str(y_origin) + str(t_width) + ',' + str(y_end)
            video.thumbnail_ratio = t_ratio
            video.save()
        if 'tags' in video_info:
            for video_tag in video_info['tags']:
                tag = Tag.objects.create(video=video,
                                         name=video_tag)

def add_videos_to_category(pl_id, video_ids, youtube):
    page_token = None
    while True:
        if Category.objects.filter(yt_id=pl_id[0]).exists() is False:
            Category.objects.create(title=pl_id[1],
                                    yt_id=pl_id[0])
        category = Category.objects.get(yt_id=pl_id[0])
        response = youtube.playlistItems().list(
            part='snippet',
            playlistId=pl_id[0],
            maxResults=50,
            pageToken=page_token
        ).execute()
        ids_to_add = [x['snippet']['resourceId']['videoId'] for x in response['items']
                      if x['snippet']['resourceId']['videoId'] in video_ids]
        videos_to_add = Video.objects.filter(yt_id__in=ids_to_add).reverse()
        #had to reverse cause newer videos were coming first and hence would
        #be added to category before the older videos i.e. in reverse order
        for video in videos_to_add:
            VideoCategory.objects.create_object(video=video,
                                                category=category)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
                
def add_videos_to_categories(category_info, video_ids):
    youtube = build(
        settings.YOUTUBE_API_SERVICE_NAME,
        settings.YOUTUBE_API_VERSION,
        developerKey=settings.YT_KEY)
    for pl_id in category_info:
        add_videos_to_category(pl_id, video_ids, youtube)
    

def get_new_videos():
    video_ids = get_new_video_ids()
    if video_ids:
        videos_info = get_videos_info(video_ids)
        create_new_videos(videos_info)
        category_ids = get_category_ids()
        add_videos_to_categories(category_ids, video_ids)
    return len(video_ids)

@staff_member_required
def get_video_by_id(request):
    video_id = request.POST.get('video_id', None)
    if video_id is None:
        video_id = request.GET.get('video_id', None)
    if video_id:
        try:
            video_ids=[video_id]
            videos_info = get_videos_info(video_ids)
            create_new_videos(videos_info)
            category_ids = get_category_ids()
            add_videos_to_categories(category_ids, video_ids)
            return HttpResponse('Video adicionado')
        except Exception as e:
            print e
            mail_admins(
                subject='error',
                message=e
            )
            return HttpResponse('Deu ruim')
    else:
        return HttpResponse('Deu ruim')    
        
