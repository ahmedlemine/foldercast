import uuid
from django.db import models
from django.urls import reverse


class Feed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    url = models.URLField()
    artwork = models.URLField()
    qr_code = models.URLField()
    items_count = models.PositiveBigIntegerField(default=0)
    last_generated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("feeds:feed_details", kwargs={"feed_uuid": self.id})