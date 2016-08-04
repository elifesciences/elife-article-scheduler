from base import BaseCase
from schedule.models import ScheduledPublication
from django.utils import timezone


class ScheduledPublicationModelCase(BaseCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_store_scheduledpublication(self):

        # this test doesn't use fixtures as it tests adding a new record of ScheduledPublication
        publication = ScheduledPublication(
            article_identifier="00123",
            scheduled=timezone.now(),
            published=True
        )
        publication.save()

        retrieved_publication = ScheduledPublication.objects.get(article_identifier=publication.article_identifier)
        self.assertEquals(retrieved_publication.article_identifier, publication.article_identifier)
        self.assertEquals(retrieved_publication.scheduled, publication.scheduled)
        self.assertEquals(retrieved_publication.published, publication.published)
