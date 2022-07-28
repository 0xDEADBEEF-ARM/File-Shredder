import subprocess as sp
import os
import glob

def shred():
    name = "./000000"
    file_path = "./"
    file_type = input('Enter file type to shred: ')
    speed = input('Faster or more Secure? f/s : ')
    gen = glob.iglob(f'{file_path}/**/*.{file_type}', recursive=True)
    
    if speed == "f" or speed == "F":
        speed = "urandom"
    elif speed == "s" or speed == "S":
        speed = "random"
    else:
        speed = "urandom"

#check total blocks size occupied by file

    for file in gen:
        print(f'\nshredding {file}\n')
        v=sp.check_output(f"stat -c '%b' {file} ", shell = True)
             
        v=int(v.decode("utf-8"))
        v=v*512 #total allocated bytes in blocks

#overwrite file

        for overwrite in range(3):
            print(f"\noverwrite with {speed}")
            sp.call(f'dd bs={v} if=/dev/{speed} iflag=fullblock  of={file} count=1 oflag=sync status=progress', shell=True)
        
        print("\noverwrite with zero")
        sp.call(f'dd bs={v} if=/dev/zero iflag=fullblock  of={file} count=1 oflag=sync status=progress', shell=True)

#rename file

        x = 8
        print(f"\nrenaming {file} to {name[:x]}")
        sp.call(f'mv {file} {name[:x]}', shell=True)
        sp.call(f'sync  {name[:x]}', shell=True)
        
        while x > 3:
            print(f"renaming {name[:x]} to {name[:x-1]}")
            sp.call(f'mv {name[:x]} {name[:x-1]}', shell=True)
            sp.call(f'sync {name[:x-1]}', shell=True)
            x -= 1

#remove file

        print("\nremoving ./0\n")
        sp.call(f'rm ./0', shell=True)

        print(f'done shredding {file}, moving to the next file\n')

    print('All files shredded!')

shred()
