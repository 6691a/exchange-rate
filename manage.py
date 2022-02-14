#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import uvicorn


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def run():
    if sys.argv[1] == "run":
        uvicorn.run("config.asgi:application", port=8080, reload=True)
    else:
        main()


if __name__ == "__main__":
    run()
