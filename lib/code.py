#! /usr/bin/env python3
# *-* mode: python; coding: utf-8 *-*
"""
=============================================================================
Watchtower
=============================================================================
HTML Checksum.
"""
from __future__ import annotations

import requests
import hashlib
import random
import string

from bs4 import BeautifulSoup

def generate_random_characters(length=15):
    characters = string.ascii_letters + string.digits
    random_chars = ''.join(random.choice(characters) for _ in range(length))
    return random_chars

def get_html(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        html_content = response.content
        
        soup = BeautifulSoup(html_content, 'lxml')
        
        for tag in soup.find_all(True):
            attrs = ['href', 'value']
            [tag.attrs.pop(_, None) for _ in attrs]
        
        for script_tag in soup.find_all('script'):
            script_tag.decompose()
        
        modified_html = str(soup)
        
        return hashlib.sha256(modified_html.encode()).hexdigest()
    else:
        return f'Error > {generate_random_characters()}'