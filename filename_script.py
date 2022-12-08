import os
def change_filename(way):
    entries = os.listdir(way)
    #entries = sorted(os.listdir(way))
    for i in range(len(entries)):
        entries[i] = int(entries[i].replace(".png", ""))

    entries = sorted(entries)

    for i in range(len(entries)):
        entries[i] = f'{entries[i]}.png'
        old_file = os.path.join(way, f'{entries[i]}')
        new_File = os.path.join(way, f'{entries[i]}')
        os.rename(old_file, new_File)

    return entries
    
if __name__ == '__main__':
    way = f'{os.getcwd()}/data/'
    change_filename(way)