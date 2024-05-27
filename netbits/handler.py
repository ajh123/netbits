def handlesMessage(message_type):
    def decorator(func):
        if not hasattr(func, '_message_type'):
            func._message_type = message_type
        return func
    return decorator

class MessageHandler:
    def __init__(self):
        self._handlers = {}
        self._register_handlers()

    def _register_handlers(self):
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, '_message_type'):
                self._handlers[attr._message_type] = attr

    def handle(self, message, user_data):
        message_type = type(message)
        if message_type in self._handlers:
            handler = self._handlers[message_type]
            handler(message, user_data)
        else:
            self.handle_unknown_message(message, user_data)

    def handle_unknown_message(self, message, user_data):
        print(f"Unknown message type: {message.__class__.__name__}")
