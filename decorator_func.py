"""
Module for demonstrating decorator functionality with timing.
This module contains a decorator that measures execution time of functions.
"""

import time

def decorator(func):
    """
    Decorator function that measures the execution time of the decorated function.
    
    Args:
        func: The function to be decorated
        
    Returns:
        wrapper: The wrapped function with timing functionality
    """
    def wrapper(number):
        start = time.time()
        result = func(number)
        end = time.time()
        print("time : ", end - start)
        return result
    return wrapper

@decorator
def my_list_objects(number):
    """
    Creates a list of numbers from 1 to the given number.
    
    Args:
        number: The upper limit for the list
        
    Returns:
        list: A list containing numbers from 1 to number
    """
    my_list = []
    i = 1
    while i <= number:
        my_list.append(i)
        i += 1
    print(my_list)
    return my_list

n = int(input("please enter a number : "))
my_list_objects(n)
