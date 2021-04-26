import time

url_main = "https://www.iroads.co.il/"
filter = 'מידע-לספקים'



def timer(func):
    """ for personal use"""
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        value = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f'This is the time {func.__name__} took:{t2 - t1} second(s)')
        return value
    return wrapper




