from multiprocessing.shared_memory import SharedMemory

from .templates import MEMORY_NAME


def create_shared_memory(name: str, size: int) -> None:
    SharedMemory(MEMORY_NAME.format(name=name), create=True, size=size)


def free_shared_memory(name: str) -> None:
    shared_memory = SharedMemory(MEMORY_NAME.format(name=name))
    shared_memory.unlink()
