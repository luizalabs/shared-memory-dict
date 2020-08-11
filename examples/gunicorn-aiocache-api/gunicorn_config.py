from shared_memory_dict.hooks import create_shared_memory, free_shared_memory


def on_starting(server):
    create_shared_memory(name='sm', size=1024)


def on_exit(server):
    free_shared_memory(name='sm')
