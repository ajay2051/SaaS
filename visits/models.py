from django.db import models


class PageVisit(models.Model):
    path = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'page_visit'
        verbose_name = 'Page Visit'
        verbose_name_plural = 'Page Visits'
