import os

number = 499

for filename in os.listdir("."):
    if filename == "change_name_files.py" or filename == "1.1":
        continue
    os.rename(filename, "sol_ida_problem_"+str(number)+"_.txt")
    number += 1
