def grab_info(file_name, string_find):
    file = open(file_name, "r")
    for line in file:
        processed = line.strip("\n").split(":")
        key = processed[0]
        value = processed[1].strip("\"")
        if key == string_find:
            return value
    return "Value Not Found"