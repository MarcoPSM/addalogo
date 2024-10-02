from tkinter import filedialog
from tkinter import *
import os
import string

abc = list(string.ascii_uppercase)


def order(number):
    if number <= len(abc):
        return abc[number % len(abc) - 1]
    return abc[len(abc) - 1] + order(number - len(abc))


root = Tk()
files = filedialog.askopenfilenames()

counter = 1
for f in files:
    dir_name = os.path.dirname(f)
    basename = os.path.basename(f)
    file_name, file_ext = os.path.splitext(basename)
    if file_name.isnumeric():
        new_name = os.path.join(dir_name, order(int(file_name))) + file_ext
    else:
        print(dir_name)
        print(counter, order(counter))
        new_name = os.path.join(dir_name, order(counter)) + file_ext
    counter += 1
    os.rename(f, new_name)
	

