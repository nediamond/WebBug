from django.db import models

from django.contrib.auth.models import User


class Bug(models.Model):
    # Uses django id for url gen
    owner = models.ForeignKey(User, unique=False, on_delete=models.CASCADE,)

    def _get_num_hits(self):
        return Hit.objects.filter(bug=self).count()
    num_hits = property(_get_num_hits)

    def _get_hits(self):
        return Hit.objects.filter(bug=self)
    hits = property(_get_hits)

    def _get_num_unique_users(self):
        return self.hits.values("uuid").distinct().count()
    num_unique_users = property(_get_num_unique_users)

    def __unicode__(self):
        return unicode("Bug "+str(self.id))


class Hit(models.Model):
    bug = models.ForeignKey(Bug, unique=False, on_delete=models.CASCADE,)
    date = models.DateTimeField(auto_now_add=True)
    http_headers_json = models.TextField(blank=False)
    cookies_json = models.TextField(blank=False)
    http_referer = models.TextField(blank=True)
    remote_addr = models.TextField(blank=True)
    remote_port = models.TextField(blank=True)
    real_ip = models.TextField(blank=True)
    uuid = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.date)

