from django.conf.urls import url
from .utils import answer_question

urlpatterns = [
    url(r'^answerquestion',
        answer_question,
        name='answer_question'),
    ]
