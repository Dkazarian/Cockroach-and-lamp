import inspect
import sys


class EventManager:

    def __init__ (self):
        self.HANDLERS = dict()

    def add(self, eventType, action, handler=None):
        if handler is None:
            stack = inspect.stack()
            frame = stack[1][0]
            caller_name = frame.f_locals.get("__name__")
            handler = sys.modules[caller_name]

        handlerList = self.HANDLERS.get(eventType, None)

        if handlerList is None:
            handlerList = list()
            self.HANDLERS[eventType] = handlerList

        handlerList.append((handler, action))

    def remove(self, eventType, action, handler=None):

        if handler is None:
            stack = inspect.stack()
            frame = stack[1][0]
            caller_name = frame.f_locals.get("__name__")
            handler = sys.modules[caller_name]

        handlerList = self.HANDLERS.get(eventType, None)

        if handlerList is None:
            return False

        if (handler, action) in handlerList:
            handlerList.remove((handler, action))
            return True
        else:
            return False

    def handle(self, events):

        for event in events:
            if event.type in self.HANDLERS:
                for handler, action in self.HANDLERS[event.type]:
                    getattr(handler, action)(event)
