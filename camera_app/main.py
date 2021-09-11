import camera_app.AppWindow as a
import tkinter as tk

def main():
    win = tk.Tk()#윈도우창
    app = a.AppWin(win, '700x600+100+100')
    win.mainloop()

main()
