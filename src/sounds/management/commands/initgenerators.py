import os
import logging
import argparse
from django.core.management import BaseCommand, call_command , CommandError
from django.core.management.base import CommandParser

from sounds.models import SoundGenerator

class Command(BaseCommand):
    help = "DEV COMMAND: Fill databasse with handled sound generators"

    def add_arguments(self, parser: CommandParser) -> None:
        super().add_arguments(parser)
        #parser.add_argument('--use_default', action=argparse.BooleanOptionalAction, default=False)        

    def handle(self, *args, **options):
        # add the sound generators
        try:
            call_command('loaddata','generators.json')
        except CommandError:
            logging.error("Error while loading generators")