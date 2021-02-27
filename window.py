import ctypes, platform

def makeActive():
    if platform.system() == 'Windows':
        Active_W = ctypes.windll.user32.GetActiveWindow()
        ctypes.windll.user32.SetWindowPos(Active_W,0,0,0,0,0,0x0002|0x0001)
