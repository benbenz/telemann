from django.db import models

from tags.models import Tag

class SoundGenerator(models.Model):
    id          = models.AutoField(primary_key=True) 
    name        = models.CharField(max_length=64,null=False,help_text="The name of the sound generator")
    description = models.TextField(max_length=256,null=True,default=None)
    filenames   = models.TextField(max_length=256,null=False,help_text="The list of possible file names for the plugin")

    class Meta:
        indexes = [
#            models.Index(fields=['name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"],name="generator_name_unique")
        ]


class Sound(models.Model):
    id            = models.AutoField(primary_key=True) 
    generator     = models.ForeignKey(SoundGenerator,on_delete=models.CASCADE)
    file_path     = models.FilePathField(max_length=512,null=False,help_text="File path of this entry")
    last_modified = models.DateTimeField(default=None,null=True,help_text="the date/time the file was modified")
    record_date   = models.DateTimeField(auto_now_add=True,help_text="the date/time the file was entered in the database")
    # relations
    tags          = models.ManyToManyField(Tag,related_name="sounds")

    class Meta:
        ordering = ['record_date']
        indexes = [
            models.Index(fields=['record_date']),
            models.Index(fields=['file_path']),
#            models.Index(fields=['status']),
            models.Index(fields=['application'])
        ]
        constraints = [
#            models.UniqueConstraint(fields=["doc_id", "vector_store"],name="doc_id_vector_store_unique")
            models.UniqueConstraint(fields=["application","file_path"],name="application_file_path_unique")
        ]