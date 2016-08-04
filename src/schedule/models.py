from __future__ import unicode_literals

from django.db import models


class ScheduledPublication(models.Model):
    article_identifier = models.CharField(max_length=512)
    scheduled = models.DateTimeField('scheduled datetime')
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.article_identifier + '--' + str(self.scheduled) + '--' + str(self.published)