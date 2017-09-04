# encoding: utf-8
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from django.contrib.staticfiles.templatetags.staticfiles import static
from reportlab.lib.units import inch
from django.conf import settings
from reportlab.lib.utils import ImageReader
from xhtml2pdf import pisa
from cStringIO import StringIO
from django.core.mail import EmailMessage
from django.shortcuts import render
from .models import Certificate
import datetime
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.content), pdf)
    return pdf

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL
    sRoot = '/Users/dietbacon/Library/Mobile Documents/com~apple~CloudDocs/Development/direitoemtela_project/direitoemtela/devstatic'
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT
    # Typically /static/
    # Typically /home/userX/project_static/
    # Typically /static/media/
    # Typically /home/userX/project_static/media/
    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri # handle absolute uri (ie: http://some.tld/foo.png)
    # make sure that file exists
    if not os.path.isfile(path): raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl) )
    print path
    return path

def send_pdf_email(request):
    certificate = Certificate.objects.get(identifier='3dti849cnyhpciuzsy1hrd7c9')
    template = get_template('attempt-certificate.djhtml')
    html = template.render({'certificate': certificate})
    # Write PDF to file
    f = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=f, link_callback=link_callback)
    # Return PDF document through a Django HTTP response
    f.seek(0)
    pdf = f.read()
    f.close() # Don't forget to close the file handle return
    return HttpResponse(pdf, content_type='application/pdf')


