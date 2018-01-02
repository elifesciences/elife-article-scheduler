from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime
from schedule import logic
import logging
from rest_framework import status

logger = logging.getLogger(__name__)

@api_view(['POST'])
@parser_classes((JSONParser,))
def article_schedule(rest_request, format=None):

    if rest_request is not None and rest_request.data is not None:
        articles = rest_request.data.get("articles")
        if articles is not None:
            schedules = logic.get_schedules(articles)
            return Response({"articles": schedules})
        logger.error("Request data not found, returning articles:None")
    return Response({"articles": None}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@parser_classes((JSONParser,))
def article_schedule_for_range(rest_request, start=None, end=None, format=None ):

    start = timezone.make_aware(datetime.fromtimestamp(int(start))) if start is not None else timezone.now()
    end = timezone.make_aware(datetime.fromtimestamp(int(end))) if end is not None else timezone.now()
    schedules = logic.get_schedules_range(start, end)
    return Response({"articles": schedules})


@api_view(['POST'])
@parser_classes((JSONParser,))
def schedule_article_publication(rest_request, format=None):

    if rest_request is not None and rest_request.data is not None:
        article = rest_request.data.get("article")
        if article is not None:
            article_identifier = article.get("article-identifier")
            article_scheduled = article.get("scheduled")
            if article_scheduled is None or article_scheduled is False:
                logic.cancel_schedule(article_identifier)
            else:
                scheduled_datetime = timezone.make_aware(datetime.fromtimestamp(int(article_scheduled)))
                logic.schedule_publication(article_identifier, scheduled_datetime)
            return Response({"result": "success"})

    logger.error("Request data not found, returning result:failed")
    return Response({"result": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
