from time import perf_counter
from functools import wraps

from asgiref.sync import sync_to_async, async_to_sync

from django.core.cache import cache
from django.db.models.base import ModelBase
from django.shortcuts import get_object_or_404
from django.db import connection, reset_queries

def destructuring(dict: dict, *args: str):
    """
    ex) foo, blah = pluck(things, 'foo', 'blah')
    https://stackoverflow.com/a/17074606/15126990
    lambda dict, *args: (dict[arg] for arg in args)
    """
    return (dict[arg] for arg in args)


def query_debugger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        number_of_end_queries = len(connection.queries)
        print("-------------------------------------------------------------------")
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {number_of_end_queries-number_of_start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        print("-------------------------------------------------------------------")
        return result

    return wrapper


