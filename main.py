from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pygame.mixer as pym
from mutagen.mp3 import MP3
import time, os, webbrowser

pym.init()

playlist = []
current_song = 0
current_song_name = ""
playing = False
stopped = True
autoplay = True
id_ = None
muted = False

total_time = 0
converted_total_time = 0

def openfolder():
    folder_path = str(filedialog.askdirectory(title='Choose your folder'))
    mp3_files = []
    for i in os.listdir(folder_path):
        if i.endswith('mp3'):
            mp3_files.append(f'{folder_path}/{i}')
    
    openandplay(mp3_files)

def openfiles(x=None):
    new_songs = list(filedialog.askopenfilenames(title="Choose Song(s)", filetypes=(("mp3 Files", "*.mp3" ), )))
    openandplay(new_songs)

def openandplay(new_songs):
    global playlist
    if new_songs==[]:
        pass
    elif playlist==[]:
        playlist += new_songs
        playsong(0)
    else:
        add_to_end = messagebox.askyesno('Bloom Player', 'Do you want to create a new playlist?\nIf NO, songs will be added to queue.')
        if add_to_end==True:
            playlist.clear()
            for i in new_songs:
                if i in playlist():
                    continue
                else:
                    playlist.append(i)
            playsong(0)
        else:
            playlist.extend(new_songs)
            lbl_upnexttitle['text'] = os.path.basename(playlist[current_song+1])

    print(playlist)
    
def playsong(n):
    global stopped, playing, total_time, converted_total_time
    lbl_currentlyplayingtitle['text'] = os.path.basename(playlist[n])
    try:
        lbl_upnexttitle['text'] = os.path.basename(playlist[n+1])
    except IndexError:
        lbl_upnexttitle['text'] = os.path.basename(playlist[0])
        
    playing = True
    stopped = False
    btn_playpause['image'] = icon_pause
    lbl_currenttime['text'] = "00:00"
    slider_progress['value'] = 0

    total_time = MP3(playlist[current_song]).info.length
    converted_total_time = time.strftime('%M:%S', time.gmtime(total_time))
    lbl_totaltime['text'] = converted_total_time
    slider_progress['to'] = total_time

    pym.music.load(playlist[n])
    pym.music.play(loops=0)

    play_time()

def playbtn(x=None):
    global playing
    if playlist==[] and stopped==True:
        pass
    elif playlist!=[] and stopped==True:
        playsong(current_song)
    elif playlist!=[] and stopped==False:
        if playing==False:
            btn_playpause['image'] = icon_pause
            playing = True
            pym.music.unpause()
        else:
            btn_playpause['image'] = icon_play
            playing = False
            pym.music.pause()

def nextbtn(x=None):
    global current_song
    if stopped==True or len(playlist)==1:
        pass
    else:
        lbl_currenttime.after_cancel(id_)
        try:
            current_song += 1
            playsong(current_song)
        except IndexError:
            current_song = 0
            playsong(current_song)

def prevbtn(x=None):
    global current_song
    if stopped==True or len(playlist)==1:
        pass
    else:
        lbl_currenttime.after_cancel(id_)
        try:
            current_song -= 1
            playsong(current_song)
        except IndexError:
            current_song = -1
            playsong(current_song)

def stop(x=None):
    global stopped, playing
    playing = False
    stopped = True
    btn_playpause['image'] = icon_play
    lbl_currentlyplayingtitle['text'] = ''
    lbl_upnexttitle['text'] = ''
    lbl_currenttime['text'] = '00:00'
    lbl_totaltime['text'] = '00:00'
    slider_progress['value'] = 0
    pym.music.stop()

def toggle_autoplay():
    global autoplay
    if autoplay==False:
        btn_autoplay['text'] = 'Autoplay: ON'
        autoplay = True
    else:
        btn_autoplay['text'] = 'Autoplay: OFF'
        autoplay = False

def play_time():
    global id_
    converted_current_time = time.strftime('%M:%S', time.gmtime(int(slider_progress.get())))

    if stopped:
        return
    
    if int(slider_progress.get())==int(total_time):
        if autoplay==True:
            nextbtn()
            return
        else:
            stop()
    elif playing==True:
        next_time = int(slider_progress.get()) + 1
        slider_progress['value'] = next_time
        lbl_currenttime['text'] = converted_current_time
    else:
        pass

    id_ = lbl_currenttime.after(1000, play_time)
    
def slider(x):
    if not stopped:
        pym.music.play(loops=0, start=slider_progress.get())

def toggle_mute(x=None):
    global muted
    if muted==False:
        btn_volume['image'] = icon_mute
        pym.music.set_volume(0.0)
        muted = True
    else:
        btn_volume['image'] = icon_unmute
        pym.music.set_volume(slider_volume.get()/100)
        muted = False

def set_volume(x=0):
    if muted==True:
        return
    pym.music.set_volume(slider_volume.get()/100)

def show_playlist():
    if playlist==[]:
        messagebox.showerror("Bloom Player", "Playlist is empty. Add some songs first")
    else:
        playlist_window = Toplevel()
        playlist_window.title("Bloom Player - Playlist")
        playlist_window.configure(height=200, width=650)

        lst_playlist = Listbox(playlist_window,activestyle="underline",background="black", fg='pink', width=80)
        lst_playlist.grid(column=0, padx=10, pady=10, row=0)

        for i in playlist:
            lst_playlist.insert(END, os.path.basename(i))

def show_shortcuts():

    help_window = Toplevel()
    help_window.resizable(False, False)
    help_window.title("Bloom Player - Shortcuts")

    frm_heading = Frame(help_window)
    frm_heading.grid(column=0, padx=5, pady=5, row=0)
    lbl_heading = Label(frm_heading, font="{consolas} 24 {}", justify="center", text='Shortcut Keys')
    lbl_heading.grid(column=0, row=0)

    frm_shortcuts = Frame(help_window)
    frm_shortcuts.grid(column=0, row=1)
    lbl_funcheading = LabelFrame(frm_shortcuts, height=200, text='FUNCTION', width=200)
    lbl_funcheading.grid(column=1, ipadx=10, padx=10, pady=10, row=0)
    lbl_functions = Label(lbl_funcheading, font="{consolas} 12", justify="left", text='Open Files\nPlay/Pause\nNext\nPrevious\nStop\nMute/Unmute')
    lbl_functions.grid(column=0, padx=10, pady=10, row=0)

    lbl_keysheading = LabelFrame(frm_shortcuts)
    lbl_keysheading.grid(column=0, padx=10, pady=10, row=0)
    lbl_keysheading.configure(height=200, text='KEY', width=200)
    lbl_keys = Label(lbl_keysheading, font="{consolas} 12 {}", justify="center", text='O\nSpace\nN\nP\nX\nM')
    lbl_keys.grid(column=0, padx=10, pady=10, row=0)

    help_window.mainloop()


root = Tk()
root.title("Bloom Player")
root.geometry('500x380')
root.resizable(0, 0)


icon_play = PhotoImage(file='icons/play.png')
icon_pause = PhotoImage(file='icons/pause.png')
icon_open = PhotoImage(file='icons/open.png')
icon_next = PhotoImage(file='icons/next.png')
icon_previous = PhotoImage(file='icons/previous.png')
icon_stop = PhotoImage(file='icons/stop.png')
icon_mute = PhotoImage(file='icons/mute.png')
icon_unmute = PhotoImage(file='icons/unmute.png')

menubar = Menu(root)
root.config(menu=menubar)

menu_file = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=menu_file)
menu_file.add_command(label="Open File(s)", command=openfiles)
menu_file.add_command(label="Open Folder", command=openfolder)

menu_help = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=menu_help)
menu_help.add_command(label="Shortcut Keys", command=show_shortcuts)
menu_help.add_command(label="About")
menu_help.add_command(label="Contact Developer", command=lambda:webbrowser.open('https://github.com/bitan005')  )


lbl_currentlyplaying = LabelFrame(root, text="CURRENTLY PLAYING", font=('consolas', 11, 'bold'), relief=RIDGE)
lbl_currentlyplaying.grid(row=0, column=0, padx=3)
lbl_currentlyplayingtitle = Label(lbl_currentlyplaying, text='WELCOME TO BLOOM PLAYER\n ',font=('consolas', 10), width=60, wraplength=480)
lbl_currentlyplayingtitle.grid(row=0, column=0)

frm_controls = Frame(root)
frm_controls.grid(row=1, column=0, pady=10)
btn_previous = Button(frm_controls, image=icon_previous, borderwidth=0, command=prevbtn)
btn_previous.grid(row=0, column=0, padx=10, pady=2)
btn_playpause = Button(frm_controls, image=icon_play, borderwidth=0, command=playbtn)
btn_playpause.grid(row=0, column=1, padx=10, pady=2)
btn_next = Button(frm_controls, image=icon_next, borderwidth=0, command=nextbtn)
btn_next.grid(row=0, column=2, padx=10, pady=2)
btn_stop = Button(frm_controls, image=icon_stop, borderwidth=0, command=stop)
btn_stop.grid(row=0, column=3, padx=10, pady=2)
btn_open = Button(frm_controls, image=icon_open, borderwidth=0, command=openfiles)
btn_open.grid(row=0, column=4, padx=10, pady=2)

frm_adcontrols = Frame(root)
frm_adcontrols.grid(row=2, column=0)
btn_autoplay = Button(frm_adcontrols, text="Autoplay: ON", command=toggle_autoplay)
btn_autoplay.grid(row=0, column=0, pady=10, padx=5)
btn_playlist = Button(frm_adcontrols, text='Show Playlist', command=show_playlist)
btn_playlist.grid(row=0, column=1, pady=10, padx=5)

lbl_volume = LabelFrame(frm_adcontrols, text='VOLUME', font=('consolas', 11, 'bold'), relief=RIDGE)
lbl_volume.grid(row=0, column=2, pady=10)
btn_volume = Button(lbl_volume, text='Volume', image=icon_unmute, borderwidth=0, command=toggle_mute)
btn_volume.grid(row=0, column=0, padx=5, pady=3)
slider_volume = ttk.Scale(lbl_volume, from_=0, to=100, orient=HORIZONTAL, length=150, value=100, command=set_volume)
slider_volume.grid(row=0, column=1, padx=5, pady=3)

frm_progress = LabelFrame(root)
frm_progress.grid(row=3, column=0)
lbl_currenttime = Label(frm_progress, text="00:00")
lbl_currenttime.grid(row=0, column=0, padx=10)
slider_progress = ttk.Scale(frm_progress, from_=0, to=100, orient=HORIZONTAL, length=365, value=0, command=slider)
slider_progress.grid(row=0, column=1, pady=20)
lbl_totaltime = Label(frm_progress, text="00:00")
lbl_totaltime.grid(row=0, column=2, padx=10)

lbl_upnext = LabelFrame(root, text="UP NEXT", font=('consolas', 11, 'bold'), relief=RIDGE)
lbl_upnext.grid(row=4, column=0, padx=3, pady=10)
lbl_upnexttitle = Label(lbl_upnext, text='\n', font=('consolas', 10), width=60, wraplength=480)
lbl_upnexttitle.grid(row=0, column=0)

root.bind('<space>', playbtn)
root.bind('m', toggle_mute)
root.bind('n', nextbtn)
root.bind('p', prevbtn)
root.bind('o', openfiles)
root.bind('x', stop)

root.mainloop()
