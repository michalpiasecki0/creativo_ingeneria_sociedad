def remove_unnecessary_lines(path):
    f = open(file=path, mode="r")
    new_path = f"{path[:-3]}_corrected.csv"
    while(True):
        line = f.readline()
        if line[0] != "," :
            break
    new_f = open(new_path, "w")
    while(True):
        new_f.write(line)
        line = f.readline()
        if line == None:
            break
    f.close()
    new_f.close()



