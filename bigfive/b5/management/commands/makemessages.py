from django.core.management.commands import makemessages


class Command(makemessages.Command):
    def handle(self, *args, **options):
        # Django treats .txt files as templates and writes a temporary .py file
        # next to them, which fails in the container where /code is not writable.
        options["ignore_patterns"] = [*options["ignore_patterns"], "requirements.txt"]
        # Keep the .po files in the format they are committed in.
        options["no_location"] = True
        options["no_wrap"] = True
        return super().handle(*args, **options)
