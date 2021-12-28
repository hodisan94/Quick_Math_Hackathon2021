'''
in this file we build functions to call particular color named functions to execute the relevant ANSI Escape Sequence.
You can use these functions instead of the "print" function
these functions will print the message on the screen when the rest of the writing is in the color you selected
'''
def print_Red(skk): print("\033[91m {}\033[00m" .format(skk))
def print_Green(skk): print("\033[92m {}\033[00m" .format(skk))
def print_Yellow(skk): print("\033[93m {}\033[00m" .format(skk))
def print_LightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def print_Purple(skk): print("\033[95m {}\033[00m" .format(skk))
def print_Cyan(skk): print("\033[96m {}\033[00m" .format(skk))
def print_LightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def print_Black(skk): print("\033[98m {}\033[00m" .format(skk))