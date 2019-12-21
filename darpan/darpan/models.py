from django.db import models



class LinkAccess(models.Model):
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.url
