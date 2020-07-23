from typing import Callable
from functools import wraps
import pygame
event_delegates = dict()


def register_event(func, event_type, condition: Callable[[pygame.event.Event], bool] = lambda e: True):
    @wraps(func)
    def wrapper(event, *args, **kwargs):
        if condition(event):
            func(event, *args, **kwargs)
    if event_type in event_delegates:
        event_delegates[event_type].append(wrapper)
    else:
        event_delegates[event_type] = [wrapper]


def execute_events(event):
    if event.type not in event_delegates:
        return
    for delegate in event_delegates[event.type]:
        delegate(event)
