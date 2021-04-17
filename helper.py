import requests
from tkinter import *
from bs4 import BeautifulSoup as bs
import os
import time



def timer(func):
    """ for personal use"""
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        value = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f'This is the time {func.__name__} took:{t2 - t1} second(s)')
        return value
    return wrapper




