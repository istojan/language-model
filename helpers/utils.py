import time


def get_elapsed_time(start_time):
    return format(time.time() - start_time, ".2f")
