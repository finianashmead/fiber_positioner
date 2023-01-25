def displaylast(x,imagename):
    import sys
    import tkinter
    from tkinter import Frame, Label
    from PIL import Image, ImageTk
    if x == '__main__' or x == '__notmain__':
        load = Image.open(imagename)
        w, h = load.size
        print(load.size,"imagemetemp")
        wd10 = int(w/10.)
        hd10 = int(h/10.)
        if x == '__notmain__':
            win = tkinter.Toplevel()
        else:
            #win = tkinter.Tk()
            win = tkinter.Toplevel()

#        win.geometry("300x200")
        print('imageme ',imagename,x)
        win.title(str(imagename))
        frame =  Frame(win, width = wd10+5, height=hd10+5)
        frame.pack()
        load= load.resize((wd10,hd10), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(win, image=render)
        img.image = render
        img.place(x=0, y=0)
        win.mainloop()
    

if __name__ == '__main__':
    import sys
    import tkinter
    from tkinter import *
    if len(str(sys.argv[1]))>0:
        imagename = str(sys.argv[1])
        print("IMAGENAME" , imagename)   
#    print('From Main')
    x = '__main__'
    displaylast(x,imagename)


