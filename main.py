from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pygame.mixer as pym
from mutagen.mp3 import MP3
import time, os

pym.init()

playlist = []
current_song = 0
playing = False
stopped = True
autoplay = True
id_ = None
muted = False

total_time = 0
converted_total_time = 0


def openfiles():
    global playlist
    new_songs = list(filedialog.askopenfilenames(title="Choose A Song", filetypes=(("mp3 Files", "*.mp3" ), )))

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
            
        elif add_to_end==False:
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


def playbtn():
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

def nextbtn():
    global current_song
    lbl_currenttime.after_cancel(id_)
    if stopped==True or len(playlist)==1:
        pass
    else:
        try:
            current_song += 1
            playsong(current_song)
        except IndexError:
            current_song = 0
            playsong(current_song)

def prevbtn():
    global current_song
    lbl_currenttime.after_cancel(id_)
    if stopped==True or len(playlist)==1:
        pass
    else:
        try:
            current_song -= 1
            playsong(current_song)
        except IndexError:
            current_song = -1
            playsong(current_song)

def stop():
    global stopped, playing, current_song
    current_song = 0
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
            return

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

def toggle_mute():
    global muted
    if muted==False:
        btn_volume['image'] = icon_mute
        pym.music.set_volume(0.0)
        muted = True
    else:
        btn_volume['image'] = icon_unmute
        pym.music.set_volume(slider_volume.get())
        muted = False

def set_volume(x=0):
    if muted==True:
        return
    pym.music.set_volume(slider_volume.get()/100)



root = Tk()
root.title("Bloom Player")
root.geometry('500x360')


icon_play = PhotoImage(file='icons/play.png')
icon_pause = PhotoImage(file='icons/pause.png')
icon_open = PhotoImage(file='icons/open.png')
icon_next = PhotoImage(file='icons/next.png')
icon_previous = PhotoImage(file='icons/previous.png')
icon_stop = PhotoImage(file='icons/stop.png')
icon_mute = PhotoImage(file='icons/mute.png')
icon_unmute = PhotoImage(file='icons/unmute.png')


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
btn_playlist = Button(frm_adcontrols, text='Show Playlist')
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


root.mainloop()
