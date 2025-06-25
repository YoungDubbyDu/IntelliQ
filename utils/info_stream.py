from queue import Queue

info_queue = Queue()


def push_info(message: str) -> None:
    """Add a message to the info queue."""
    info_queue.put(message)


def get_next_info() -> str:
    """Block until the next info message is available and return it."""
    return info_queue.get()
