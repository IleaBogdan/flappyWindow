import ctypes
import os

def load_libs():
    libs_path=list(os.listdir("./libs"))

    libs={}
    for lib in libs_path:
        if '/' not in str(lib):
            libs[str(lib).split('.')[0]]=ctypes.CDLL('./libs/'+str(lib))
    return libs