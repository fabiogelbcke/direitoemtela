from django.conf.urls import  url, include
from django.views.generic import TemplateView
import utils

urlpatterns = [
               url(r'^oi$', TemplateView.as_view(template_name='site-em-construcao.html'), name='under_construction'),
               url(r'^addtolist$', utils.add_to_list, name='add_to_mailing_list'),
]
