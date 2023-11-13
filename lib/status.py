#! /usr/bin/env python3
# *-* mode: python; coding: utf-8 *-*
"""
=============================================================================
Watchtower
=============================================================================
Get website status code and status code description.
"""
from __future__ import annotations

import requests

def get(url: str) -> tuple(str, str):
    try:
        response = requests.get(url)
        response.raise_for_status()

        status_code = response.status_code
        status_message = requests.status_codes._codes[status_code][0]

        return status_code, str(status_message).upper()

    except requests.exceptions.RequestException as e:
        return '000','KO'

if __name__ == "__main__":
    pass