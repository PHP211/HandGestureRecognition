import os

output_dir = "data/pinch"
for n in range(51):
    folder_name = f'pinch_{n}'
    os.makedirs(folder_name, exist_ok=True)
