import urllib2
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import shortuuid

def generate_filename():
    shortuuid.set_alphabet("aaaaabcdefgh1230123")
    return shortuuid.uuid()

def get_avatar(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        #url = "http://graph.facebook.com/%s/picture?type=large"%response['id']
        # if you need a square picture from fb, this line help you
        url = "http://graph.facebook.com/%s/picture?width=150&height=150"%response['id']
    #if backend.name == 'twitter':
    #    url = response.get('profile_image_url', '').replace('_normal','')
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        url = url.split('?')[0]
        url += '?sz=150'
    if backend.name == 'linkedin-oauth2':
        url = response['pictureUrl']
        print url
    if url is not None and user is not None:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urllib2.urlopen(url).read())
        img_temp.flush()
        user.profile_image.save(generate_filename(), File(img_temp))


def generate_username(strategy, details, backend, user=None, *args, **kwargs):
    if details.get('email'):
        return {'username': details['email']}
    return get_username(strategy, details, backend, user, args, kwargs)
