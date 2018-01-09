from django.conf.urls import url
from schedule import views

urlpatterns_v1 = [
    url(r'^v1/article_scheduled_status/$', views.article_schedule, name='article-schedule'),
    url(r'^v1/article_schedule_for_range/from/(?P<start>.*?)/to/(?P<end>.*?)/$', views.article_schedule_for_range,
        name='article-schedule-for-range'),
    url(r'^v1/schedule_article_publication/$', views.schedule_article_publication, name='schedule-article-publication')
]

urlpatterns = urlpatterns_v1
