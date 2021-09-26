# import os
#
# old_path = r"letters/latters"
# new_path = r"letters/lattters"
# file_list_names = []

# for root, dirs, files in os.walk(old_path):
#     for file in files:
#         # append the file name to the list
#         name = str(os.path.join(root, file)).replace(f"{old_path}\\", "").replace(".png", "").replace("symbol_", "")
#         if name in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:
#             file_list_names.append(name)
#             file_list.append(f'{new_path}/symbol_{name[0]}.png')
#         else:
#             print(name)

# for root, dirs, files in os.walk(old_path):
#     for file in files:
#         name = str(os.path.join(root, file)).replace(f"{old_path}\\", "").replace(".png", "").replace("letter_", "").replace("symbol_", "").replace('number_', '').replace("upper_", "")
#         file_list_names.append(name)
#
# for name in file_list_names:
#     with open(f'{old_path}/symbol_{name}.png', 'rb') as f, open(f'{new_path}/characters_lower_{name}.png', 'wb') as f1:
#         f1.write(f.read())

import os

path = r"characterts"
# we shall store all the file names in this list
file_list = []

for root, dirs, files in os.walk(path):
    for file in files:
        file_list.append(os.path.join(root, file).replace("characterts\\characters_", "").replace(".png", ""))
for index, value in enumerate(file_list):
    if value[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z'] and len(value) == 2 and value[0] == value[1]:
        value = value[0]
        file_list[index] = value
for index, value in enumerate(file_list):
    if len(value) > 1:
        value = input(f'{value}: ')
        file_list[index] = value

# ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'a', '&', '@', 'B', '`', '\\', 'b', 'C', 'c', ')', ']', ':', ',', '©', 'D', '-', 'd', '$', '.', 'E', 'e', '=', '€', '!', 'F', 'f', 'G', 'g', 'H', '#', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', '*', 'N', 'n', 'O', 'o', '(', '[', 'P', '%', '+', 'p', 'Q', 'q', '?', '"', 'R', '®', 'r', 'S', "'", '/', 's', 'T', '~', 't', 'U', '_', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z']
print(file_list)
