from poll.models import Question


def polls_count(request):
    # pylint: disable=E1101
    count = Question.objects.count()
    return {"polls_count": count}
