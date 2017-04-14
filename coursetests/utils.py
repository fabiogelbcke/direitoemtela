from .models import Question, Alternative, UserQuestionRelationship
from django.contrib.auth.decorators import login_required
from courses.models import UserItemRelationship, UserCourseRelationship
from django.http import HttpResponse, HttpResponseBadRequest


@login_required
def answer_question(request):
    user = request.user
    question_id = request.POST.get('question_id', None)
    alternative_id = request.POST.get('alternative_id', None)
    print alternative_id
    alternative = Alternative.objects.get(id=alternative_id)
    if question_id is None or alternative_id is None:
        print 'return bad request'
    question = Question.objects.get(id=question_id)
    correct_alternative = Alternative.objects.get(
        question=question,
        correct=True
    )
    uquestion = UserQuestionRelationship.objects.get(
            question=question,
            user=user
    )
    ucourse = UserCourseRelationship.objects.get(
        course = question.test.course_item.course,
        user = user
    )
    test = question.test
    uitem = UserItemRelationship.objects.get(
        course_item = test.course_item,
        user = user
    )
    if test.questions.last() == question:
        uitem.done = True
        uitem.save()
    uquestion.answered = True
    ucourse.questions_answered += 1
    if alternative.correct:
        uquestion.answered_correctly = True
        ucourse.correct_answers += 1
    uquestion.save()
    ucourse.save()
    return HttpResponse('alternative' + str(correct_alternative.id))
    if alternative.correct:
        return HttpResponse('correct')
    else:
        return HttpResponse('incorrect')
