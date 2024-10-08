import os

folder_path = 'data/pinch'

command = 'video'

for count, filename in enumerate(os.listdir(folder_path)):
    new_name = f"{command}_{count}.avi"  # Đặt tên mới, có thể tuỳ chỉnh
    src = os.path.join(folder_path, filename)
    dst = os.path.join(folder_path, new_name)
    os.rename(src, dst)