from django.core.exceptions import ObjectDoesNotExist
import models
import logging

logger = logging.getLogger(__name__)


def get_schedules(articles):

    logger.info("getting schedules")
    schedules = []
    for article in articles:
        try:
            scheduled_publication = models.ScheduledPublication.objects.get(article_identifier=article)
            scheduled = int(scheduled_publication.scheduled.strftime("%s"))
            published = scheduled_publication.published
        except ObjectDoesNotExist:
            scheduled = None
            published = False
        schedules.append({
            "article-identifier": article,
            "scheduled": scheduled,
            "published": published
        })
    return schedules


def get_schedules_range(start, end, include_published=False):

    scheduled_publications = []
    schedules = models.ScheduledPublication.objects.filter(scheduled__gt=start, scheduled__lt=end)
    if not include_published:
        schedules = schedules.filter(published=False)
    for schedule in schedules:
        scheduled_publications.append({
            "article-identifier": schedule.article_identifier,
            "scheduled": int(schedule.scheduled.strftime("%s")),
            "published": schedule.published
        })
    return scheduled_publications


def schedule_publication(article_identifier, article_schedule):

    try:
        existing = models.ScheduledPublication.objects.get(article_identifier=article_identifier)
        logger.debug("Updating scheduling record for article %s at %s", article_identifier, article_schedule)
        existing.scheduled = article_schedule
        existing.published = False
        existing.save()

    except ObjectDoesNotExist:
        logger.debug("Creating scheduling record for article %s at %s", article_identifier, article_schedule)
        schedule = models.ScheduledPublication(
                article_identifier=article_identifier,
                scheduled=article_schedule,
                published=False
            )
        schedule.save()


def cancel_schedule(article_identifier):

    try:
        logger.debug("Cancelling scheduled publication for article %s", article_identifier)
        existing = models.ScheduledPublication.objects.get(article_identifier=article_identifier)
        existing.delete()
    except ObjectDoesNotExist:
        logger.info("Article %s not found", article_identifier)


