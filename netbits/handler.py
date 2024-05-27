from typing import Type, Any
from .packet import StructuredPacket

def handlesMessage(message_type: Type[StructuredPacket]):
    """
    Decorator to mark a method as a handler for a specific message type.

    :param message_type: The type of the message that the method handles.
    :type message_type: Type[StructuredPacket]
    :return: The decorator for the method.
    """
    def decorator(func):
        if not hasattr(func, '_message_type'):
            func._message_type = message_type
        return func
    return decorator

class MessageHandler:
    """
    A base class for handling messages with registered handlers.
    """

    def __init__(self):
        """
        Initialize the MessageHandler instance and register handlers.
        """
        self._handlers = {}
        self._register_handlers()

    def _register_handlers(self):
        """
        Register methods decorated with @handlesMessage as message handlers.
        """
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, '_message_type'):
                self._handlers[attr._message_type] = attr

    def handle(self, message, user_data: Any):
        """
        Handle a message by dispatching it to the appropriate handler.

        :param message: The message to handle.
        :type message: StructuredPacket
        :param user_data: Additional user data to pass to the handler.
        """
        message_type = type(message)
        if message_type in self._handlers:
            handler = self._handlers[message_type]
            handler(message, user_data)
        else:
            self.handle_unknown_message(message, user_data)

    def handle_unknown_message(self, message, user_data: Any):
        """
        Handle a message with no registered handler.

        :param message: The unknown message.
        :type message: StructuredPacket
        :param user_data: Additional user data, that was sent by the caller of the handler.
        """
        print(f"Unknown message type: {message.__class__.__name__}")
