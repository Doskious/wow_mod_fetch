__all__ = ['Item', 'Bookmarks']


from datetime import datetime, timezone, timedelta
import json
import os
import sys

from .classes import Item, Bookmarks
from .main import main

instance = main()
folders = [] if not instance else instance.folders
urls = [] if not instance else instance.urls
