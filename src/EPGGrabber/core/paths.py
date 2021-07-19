import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_PATH = os.path.join(BASE_DIR, 'api')

PROVIDERS_PATH = os.path.join(BASE_DIR, 'providers')

PROVIDERS_ROOT = os.path.join(BASE_DIR, 'api/providers.json')

BOUQUETS_ROOT = os.path.join(BASE_DIR, 'api/bouquets.json')

EPG_ROOT = '/etc/epgimport/ziko_epg'
