import os

directory_files_name = os.listdir('.')
print(directory_files_name)
for file_name in directory_files_name:
    print(file_name)
    if file_name.endswith("html"):
        with open(f"./{file_name}", "r+", encoding='utf-8') as f:
            lines = f.readlines()
            lines = [line.replace("./static/dist/", "../static/dist/") for line in lines]
            f.seek(0)
            f.writelines(lines)
            f.close()


            
