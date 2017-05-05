from django.utils.functional import wraps
from django.http import HttpResponseNotFound
from .models import UserCourseRelationship

def is_registered_to_course(view):
    @wraps(view)
    def inner(request, *args, **kwargs):
        if (not 'course_id' in kwargs or
            not request.user.is_authenticated()
            or UserCourseRelationship.objects.filter(
                user=request.user,
                course__id=int(kwargs['course_id'])
            ).exists() is False):
            return HttpResponseNotFound()
        return view(request, *args, **kwargs)
    return inner
