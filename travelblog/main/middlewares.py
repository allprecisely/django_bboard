from main import models


def travelblog_context_processor(request):
    context = {'cities': models.City.objects.all(), 'keyword': '', 'all': ''}
    if keyword := request.GET.get('keyword'):
        context['keyword'] = f'?keyword={keyword}'
        context['all'] = context['keyword']
    if page := request.GET.get('page'):
        if page != 1:
            context['all'] += '&' if context['all'] else '?'
            context['all'] += f'page={page}'

    return context
