from django.db import models

# Create your models here.
from django.db import models

class TestCase(models.Model):
    title = models.CharField(max_length=255)
    xml_content = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):  
        return self.title

