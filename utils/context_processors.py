from dukan.models import DukanDetail
from sitaramsita import settings

def sitaram(request):
    return {
        'dukan_dtls' : DukanDetail.objects.all().first(),
        'meta_keywords' : settings.META_KEYWORDS,
        'meta_description' : settings.META_DESCRIPTION,
    }