import os

number = 290

for filename in os.listdir("."):
    if filename == "change_name_files.py":
        continue
    os.rename(filename, "sol_ida_problem_"+str(number)+"_.txt")
    number += 1
