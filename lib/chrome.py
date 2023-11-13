#! /usr/bin/env python3
# *-* mode: python; coding: utf-8 *-*
"""
=============================================================================
Watchtower
=============================================================================
Generic context manager made with Selenium.
It assumes the Chrome WebDriver is installed and up to date.
"""
from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.common.by import By

class Chrome:
    def __init__(self, url, xpaths):
        self.url = url
        self.xpaths = xpaths

    def __enter__(self, url=None):
        ARGUMENTS = ['--headless=new','--hide-scrollbars','--log-level=3']
        options = webdriver.ChromeOptions()
        [options.add_argument(_) for _ in ARGUMENTS]
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        try:
            self.driver.get(self.url)
            for xpath in self.xpaths:
                self.driver.implicitly_wait(12)
                self.driver.find_element(By.XPATH, xpath).click()
                self.driver.implicitly_wait(2)
            return self.driver
        except Exception as e:
            print(e)
            return self.driver
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()