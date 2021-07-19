import json
from datetime import datetime
from .paths import *

def update_channels(provider,channels):
    with open(BOUQUETS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["name"] == provider:
            channel['channels'] = sorted([ch for ch in list(dict.fromkeys(channels))])
    with open(BOUQUETS_ROOT, 'w') as f:
        json.dump(data, f)

def get_channels(provider):
    with open(BOUQUETS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["name"] == provider:
            return channel['channels']

def update_status(provider):
    with open(PROVIDERS_ROOT, 'r') as f:
        data = json.load(f)
    for channel in data['bouquets']:
        if channel["bouquet"] == provider:
            channel['date'] = datetime.today().strftime('%A %d %B %Y at %I:%M %p')
    with open(PROVIDERS_ROOT, 'w') as f:
        json.dump(data, f)
