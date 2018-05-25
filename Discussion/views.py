from django.conf import settings
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views import generic

from .models import Discuss


# Create your views here.

class DiscussView(generic.ListView):
    model = Discuss
    context_object_name = 'Discussions'
    template_name = 'Discussion/discussions.html'
    # TODO 分页数量
    paginate_by = getattr(settings, 'PER_PAGE_SHOW', 20)
    paginate_orphans = getattr(settings, 'ORPHANS_PAGE_SHOW', 5)

    def get_ordering(self):
        sort = self.kwargs.get('sort', '-pub_date')
        return (str(sort), '-pub_date', '-id')


def all_hot_dicussions(request):
    discussions = Discuss.objects.annotate(reply_num=Count('replys')).all()[:10]
    discussions = sorted(discussions, key=lambda x: x.reply_num, reverse=True)

    context = {
        'discussions': discussions,
    }
    return render(request, 'Discussion/hot_discussions.html', context=context)
