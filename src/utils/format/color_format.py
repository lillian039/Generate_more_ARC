color_map = {0: "black", 1: "blue", 2: "red", 3: "green", 4: "yellow", 5: "gray", 6: "magenta", 7: "orange", 8: "aqua", 9: "maroon"}

def transform_number_into_color(list_number):
    new_list = []
    for row in list_number:
        new_row = []
        for number in row:
            new_row.append(color_map[number])
        new_list.append(new_row)
    return new_list

def transform_color_into_number(list_color):
    new_list = []
    for row in list_color:
        new_row = []
        for color in row:
            if color not in color_map.values():
                new_row.append(-1)            
            else:
                new_row.append(list(color_map.keys())[list(color_map.values()).index(color)])
        new_list.append(new_row)
    return new_list