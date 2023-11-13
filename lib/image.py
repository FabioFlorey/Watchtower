#! /usr/bin/env python3
# *-* mode: python; coding: utf-8 *-*
"""
=============================================================================
Watchtower
=============================================================================
Browser Body Image Crop Resistant Checksum.
"""
from __future__ import annotations

from  pathlib import Path

from selenium.webdriver.common.by import By
from PIL import Image
import imagehash

from lib.chrome import Chrome

def image_hash(filename):
    return imagehash.crop_resistant_hash(Image.open(filename))

def internal_checksum(first_filename, second_filename):
    return image_hash(first_filename) == image_hash(second_filename)

def screenshot_path(website:str, number:int):
    return f'./img/{website}_screenshot{number}.png'

def screenshot(driver, filename):
        driver.find_element(By.TAG_NAME, 'body').screenshot(filename)

def checksum(url, name, steps):
    with Chrome(url, steps) as chrome:
        my_path = screenshot_path(name,1)
        try:
            if not Path.exists(Path(my_path)):
                screenshot(chrome, my_path)
                return True
            else:
                my_other_path = screenshot_path(name,2)
                screenshot(chrome, my_other_path)
                check = internal_checksum(my_path, my_other_path)
                Path(my_path).unlink(True)
                Path(my_other_path).rename(my_path)
                return check
        except:
            print(f"Si è verificato un errore su {name}")
            return False
        
if __name__ == "__main__":
    pass