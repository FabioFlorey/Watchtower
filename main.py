#! /usr/bin/env python3
# *-* mode: python; coding: utf-8 *-*
"""
=============================================================================
Watchtower
=============================================================================
:Authors: Fabio Craig Wimmer Florey <fabioflorey@icloud.com>
:Version: 0.0.1
:License: MIT-0
"""
from __future__ import annotations

if __name__ == '__main__':

    from lib import enqueue
    from lib.load import ConfigurationManager

    config_manager = ConfigurationManager()
    websites = config_manager.get_all_website_configs()

    enqueue.items(websites)