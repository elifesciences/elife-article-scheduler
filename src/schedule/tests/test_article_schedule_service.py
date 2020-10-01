from .base import BaseCase
from schedule.models import ScheduledPublication
from django.utils import timezone
from django.test import Client
from django.urls import reverse
import json

class Ping(BaseCase):
    def test_ping(self):
        c = Client()
        resp = c.get(reverse('ping'))
        self.assertEqual('pong', resp.content.decode('utf-8'))

class ArticleScheduleServiceCase(BaseCase):

    fixtures = ['test-schedules.yaml']

    def setUp(self):
        self.c = Client()
        self.article_one = ScheduledPublication.objects.get(pk="1")
        one_hour = timezone.timedelta(hours=1)
        self.window_start = int((self.article_one.scheduled - one_hour).strftime("%s"))
        self.window_end = int((self.article_one.scheduled + one_hour).strftime("%s"))

    def tearDown(self):

        pass

    def test_article_schedule_service(self):

        request_url = reverse('article-schedule')
        json_data = json.dumps({"articles": ["00123"]})
        response = self.c.post(request_url, json_data, content_type="application/json")
        self.assertEquals(self.article_one.article_identifier, response.data['articles'][0]['article-identifier'])
        self.assertEquals(int(self.article_one.scheduled.strftime("%s")), response.data['articles'][0]['scheduled'])
        self.assertEquals(self.article_one.published, False)

    def test_article_schedule_for_range_service(self):

        request_url = reverse('article-schedule-for-range', args=(self.window_start, self.window_end))
        response = self.c.get(request_url)
        self.assertEquals(len(response.data['articles']), 2)
        self.assertEquals(response.data['articles'][0]['article-identifier'], '00123')
        self.assertEquals(response.data['articles'][1]['article-identifier'], '00124')
        # (00125 should not be present as outside range, 00999 is already published)

    def test_schedule_article_service(self):

        test_id = "00111"
        test_schedule = 1456854838
        request_url = reverse('schedule-article-publication')
        json_data = json.dumps({
            "article": {
                    "article-identifier": test_id,
                    "scheduled": test_schedule
            }
        })
        response = self.c.post(request_url, json_data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        article = ScheduledPublication.objects.get(article_identifier=test_id)
        self.assertEquals(article.article_identifier, test_id)
        self.assertEquals(int(article.scheduled.strftime("%s")), test_schedule)
        self.assertEquals(article.published, False)

