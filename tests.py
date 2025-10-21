from functions.run_python_file import *

print('------------------------------------------------------------\n\n\n')
print(run_python_file("calculator", "main.py"))

print('------------------------------------------------------------\n\n\n')
print(run_python_file("calculator", "main.py", ["3 + 5"]))

print('------------------------------------------------------------\n\n\n')
print(run_python_file("calculator", "tests.py"))

print('------------------------------------------------------------\n\n\n')
print(run_python_file("calculator", "../main.py"))

print('------------------------------------------------------------\n\n\n')
print(run_python_file("calculator", "nonexistent.py"))

print('------------------------------------------------------------\n\n\n')
print(run_python_file("calculator", "lorem.txt"))