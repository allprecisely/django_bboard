import os
import glob

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Renames the Project'

    def add_arguments(self, parser):
        parser.add_argument('old', nargs='+', type=str, help="current project name")
        parser.add_argument('new', nargs='+', type=str, help="new project name")

    def handle(self, *args, **options):
        old = options["old"][0]
        new = options["new"][0]

        base = settings.BASE_DIR
        project_files = base.glob("**/*.py")
        for python_file in project_files:
            with open(python_file) as file:
                old_data = file.read()

            new_data = old_data.replace(old, new)

            if new_data != old_data:
                with open(python_file, 'w') as file:
                    file.write(new_data)
                print(python_file)
        os.rename(base / old, base / new)
