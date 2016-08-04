from django.core.management.base import BaseCommand
from schedule import models
from django.utils import timezone
from django.conf import settings
import requests
import requests.auth
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        scheduled = models.ScheduledPublication.objects.filter(scheduled__lt=timezone.now(), published=False)
        for schedule in scheduled:
            self.publish_article(schedule)

    @staticmethod
    def publish_article(schedule):
        try:

            message = {
                "articles":  [{
                     "id": schedule.article_identifier
                }]
            }

            service = settings.DASHBOARD_PUBLISHING_SERVICE
            auth = requests.auth.HTTPBasicAuth(settings.PUBLISHING_SERVICE_USER,
                                               settings.PUBLISHING_SERVICE_PASSWORD)
            response = requests.post(service, json=message, auth=auth)
            if response.status_code is 200:
                schedule.published = True
                schedule.save()
            else:
                logger.error("response returned %s", response.status_code)
        except Exception as e:
            logger.error("An error has occurred. Exception: %s", e.message)




