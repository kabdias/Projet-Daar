#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from elasticsearch import Elasticsearch

elastic=Elasticsearch(hosts=["127.0.0.1"])
if elastic.indices.exists(index='books3'):
    print('index already exists')
    
else:
    print("indexing data ...")
    import Indexation


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elastic.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':

    main()
