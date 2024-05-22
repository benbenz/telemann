import os
import json
from django.core.management import BaseCommand
from django.core.management.base import CommandParser

class Command(BaseCommand):
    help = "creates words.json fixture from words.raw"

    def add_arguments(self, parser: CommandParser) -> None:
        super().add_arguments(parser)

    def handle(self, *args, **options):

        raw_file_path  = os.path.join(os.path.dirname(__file__), '..', '..','fixtures','raw','words.raw')
        json_file_path = os.path.join(os.path.dirname(__file__), '..', '..','fixtures','words.json')
        entries = []
        with open(raw_file_path,'r') as raw_file:
            c = 1
            while line := raw_file.readline():
                bits = line[:-1].split('|')
                entry = {
                        "fields" : {
                            "tag" : bits[0],
                            "group" : bits[1],
                            "explanation" : bits[2],
                            "select" : True
                        } ,
                        "model": "tags.Tag" ,
                        "pk" : c ,
                }
                entries.append(entry)
                c+=1
        with open(json_file_path,'w') as json_file:
            json.dump(entries,json_file,indent=4)
