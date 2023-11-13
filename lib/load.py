#! /usr/bin/env python3
# *-* mode: python; coding: utf-8 *-*
"""
=============================================================================
Watchtower
=============================================================================
Configuration Manager for YAML file.
"""
from yaml import safe_load, safe_dump

class ConfigurationManager:
    def __init__(self) -> None:
        self.PATH = './conf/websites.yaml'
        with open(self.PATH, 'r', encoding='latin-1') as cfg:
            self.config = safe_load(cfg.read())

    def get_website_config(self, website_name):
        return self.config.get(website_name, {})

    def get_all_website_configs(self):
        all_websites = [{website_name: self.get_website_config(website_name)} for website_name in self.config]
        return [(key, value) for item in all_websites for key, value in item.items()]
    
    def update_website_fields(self, website_name, **kwargs):
        website_config = self.get_website_config(website_name)

        for field, value in kwargs.items():
            if value is not None:
                website_config[field] = value

        self.set_website_config(website_name, {**website_config, **kwargs})
        self.save_config()

    def set_website_config(self, website_name, new_config):
        self.config[website_name] = new_config

    def save_config(self):
        with open(self.PATH, 'w', encoding='latin-1') as cfg:
            safe_dump(self.config, cfg, default_flow_style=False)

if __name__ == "__main__":
    pass