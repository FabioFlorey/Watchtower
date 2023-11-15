#! /usr/bin/env python3
# *-* mode: python; coding: utf-8 *-*
"""
=============================================================================
Watchtower
=============================================================================
Queue websites in order to process them in a multi-threaded fashion.
"""
from __future__ import annotations

from time import sleep
import queue
import threading
from enum import Enum
from datetime import datetime

from colorama import Fore, Style

class Message:
    def __init__(self, check, text) -> None:
        self.check = check
        self.text = text

    def __str__(self) -> str:
        if self.check:
            return ''.join([Fore.LIGHTGREEN_EX,self.text,Fore.RESET])
        return ''.join([Fore.RED,self.text,Fore.RESET])

from lib.status import get
from lib.code import get_html
from lib.image import checksum
from lib.load import ConfigurationManager

cfg = ConfigurationManager()

class State(Enum):
    INITIAL = 1
    CHECK_STATUS = 2
    IMAGE_CHECKSUM = 3
    CODE_CHECKSUM = 4
    FINAL = 5

def initial_state(item):
    print(Style.BRIGHT, f'Procedo al controllo di {item[0]}', Style.RESET_ALL)

def check_status(item):
    status = get(item[1]['url'])
    verify = status[0]==200
    print(Message(verify, f'Il sito {item[0]} risulta {"" if verify else "non"} attivo.'))
    cfg.update_website_fields(item[0], status_code=status)

def image_checksum(item):
    image_check = checksum(item[1]['url'], item[0], item[1]['steps'])
    print(Message(image_check, f'Il sito {item[0]} {"non" if image_check else ""} è cambiato graficamente.'))
    cfg.update_website_fields(item[0], image_checksum=image_check)

def code_checksum(item):
    code_checksum = get_html(item[1]['url'])
    comparison = item[1]['html'] == code_checksum 
    print(Message(comparison, f'Il sito {item[0]} risulta{" non " if comparison else " "}cambiato a livello HTML.'))
    cfg.update_website_fields(item[0], html_checksum=comparison, html=code_checksum)

def update_date(item):
    cfg.update_website_fields(item[0], last_check=datetime.now().strftime('%Y-%m-%d'))

def process_item(item: str, state_queue: queue):
    state_functions = {
        State.INITIAL: initial_state,
        State.CHECK_STATUS: check_status,
        State.IMAGE_CHECKSUM: image_checksum,
        State.CODE_CHECKSUM: code_checksum,
        State.FINAL: update_date
    }

    while True:
        sleep(0.1)
        current_state = state_queue.get()
        state_function = state_functions.get(current_state, None)

        if state_function:
            state_function(item)

        if current_state == State.FINAL:
            state_queue.task_done()
            break

        next_state = State.INITIAL if current_state == State.FINAL else State(current_state.value + 1)
        state_queue.put(next_state)

    state_queue.task_done()

def items(items):
    item_queue = queue.Queue()
    state_queue = queue.Queue()
    
    [item_queue.put(item) for item in items]

    threads = []
    for _ in range(len(items)):
        item = item_queue.get()
        state_queue.put(State.INITIAL)
        
        # Create a thread for each item and start it
        thread = threading.Thread(target=process_item, args=(item, state_queue))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    pass
