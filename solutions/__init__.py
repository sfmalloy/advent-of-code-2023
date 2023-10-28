# auto import all days
import pathlib
import os
import importlib

days = [f[:-3] for f in os.listdir(pathlib.Path(__file__).resolve().parent) if f.endswith('.py') and f not in {'__init__.py', 'advent.py'}]
for d in days:
    importlib.import_module(f'.{d}', package='solutions')
