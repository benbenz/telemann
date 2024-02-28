
from django.db import models
from django.db.models.signals import pre_save

class Tag(models.Model):
    id  = models.AutoField(primary_key=True) 
    tag = models.TextField(max_length=128,null=False,help_text="The tag")
    group = models.TextField(max_length=64,default=None,blank=True,null=True,help_text="The group of the tag")
    explanation = models.TextField(max_length=128,null=True,blank=True,default=None,help_text="An explanation for the tag/word")
    select = models.BooleanField(default=False)

    @staticmethod
    def clean_tag(instance):
        if instance.tag is None:
            return
        instance.tag = instance.tag.strip().lower()

    @staticmethod
    def pre_save(sender, instance, **kwargs):
        Tag.clean_tag(instance)

    class Meta:
        indexes = [
            models.Index(fields=['tag']),
        ]
        constraints = [
            models.UniqueConstraint(fields=["tag"],name="tag_unique")
        ]

pre_save.connect(Tag.pre_save, Tag)