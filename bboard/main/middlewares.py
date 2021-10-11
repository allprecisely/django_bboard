from main import models


def bboard_context_processor(request):
    context = {}
    context['rubrics'] = models.SubRubric.objects.all()
    return context
