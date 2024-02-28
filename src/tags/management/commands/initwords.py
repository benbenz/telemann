import os
import logging
import argparse
from django.core.management import BaseCommand, call_command , CommandError
from django.core.management.base import CommandParser
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with handled sound sources"

    def add_arguments(self, parser: CommandParser) -> None:
        super().add_arguments(parser)
        #parser.add_argument('--use_default', action=argparse.BooleanOptionalAction, default=False)        

    def handle(self, *args, **options):
        # add the sound sources
        try:
            call_command('loaddata','words.json')
        except IntegrityError as e:
            logging.error("Error while loading words")
        except CommandError:
            logging.error("Error while loading words")