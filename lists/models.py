#------------------------------
# lists.models
#------------------------------
# Author: TangJianwei
# Create: 2019-03-10
#------------------------------
from django.db import models
from django.urls import reverse
from django.conf import settings


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id', )


    @property
    def name(self):
        return self.item_set.first().text
    
    def get_absolute_url(self):
        return reverse('view_list', args=[self.id, ])


class Item(models.Model):
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
    text = models.TextField(default='')

    class Meta:
        ordering = ('id', )
        unique_together = ('list', 'text', )


    def __str__(self):
        return self.text
