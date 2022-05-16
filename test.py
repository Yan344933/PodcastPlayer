#from pygame import mixer
from tkinter import *
import tkinter.font as font
from tkinter import messagebox
import requests
from xml.etree import ElementTree
from datetime import datetime
from os import path
import vlc

def Play():
    song=songs_list.get(ACTIVE)
    result = [d for d in playlist if d['title'] == song]
    mixer.set_media(vlc.Media(result[0]['guid']))
    mixer.play()
#to pause the song 
def Pause():
    mixer.pause()
#to stop the  song 
def Stop():
    mixer.stop()
    songs_list.selection_clear(ACTIVE)
#to resume the song
def Resume():
    mixer.pause()
#Function to navigate from the current song
def Previous():
    #to get the selected song index
    previous_one=songs_list.curselection()
    #to get the previous song index
    previous_one=previous_one[0]-1
    #to get the previous song
    temp2=songs_list.get(previous_one)
    result = [d for d in playlist if d['title'] == temp2]
    mixer.pause()
    mixer.set_media(vlc.Media(result[0]['guid']))   
    mixer.play()
    songs_list.selection_clear(0,END)
    #activate new song
    songs_list.activate(previous_one)
    #set the next song
    songs_list.selection_set(previous_one)
def Next():
    #to get the selected song index
    next_one=songs_list.curselection()
    #to get the next song index
    next_one=next_one[0]+1
    #to get the next song 
    temp=songs_list.get(next_one)
    result = [d for d in playlist if d['title'] == temp]
    mixer.pause()
    mixer.set_media(vlc.Media(result[0]['guid']))   
    mixer.play()
    songs_list.selection_clear(0,END)
    #activate newsong
    songs_list.activate(next_one)
     #set the next song
    songs_list.selection_set(next_one)

def Load():
    rss=RSS_input.get()
    global playlist 
    playlist = GetSongs()
    #print(playlist[0])
    for item in playlist:
        songs_list.insert(END, item['title'])
    print('Finish Loading')

def GetSongs(): 

    if not path.exists('podcast.xml'):
        messagebox.showinfo(message="Download XML first")
        return

    root = ElementTree.fromstring(open('podcast.xml', 'r', encoding="utf8").read())

    data = []
    root = root.find('channel')

    for item in root.findall('item'):
        title = item.find('title').text
        mp3 = item.find('guid').text
        pubDate_str = item.find('pubDate').text
        pubDate = datetime.strptime(pubDate_str, '%a, %d %b %Y %H:%M:%S %z')
        data.append({"title": title, "guid": mp3, "pubDate": pubDate})
    print('Finish process XML')

    newlist = sorted(data, key=lambda d: d['pubDate'])
    return newlist

def downloadFile():
    print('Start download File')
    link = RSS_input.get()
    response = requests.get(link)
    open("podcast.xml", "wb").write(response.content)
    print('Finish getting rss!')

playlist =[]
#creating the root window 
root=Tk()
root.title('Podcast Player')
#initialize mixer 
#mixer.init()
mixer = vlc.MediaPlayer()
#create the listbox to contain songs
songs_list=Listbox(root,selectmode=SINGLE,bg="black",fg="white",font=('arial',15),height=12,width=47,selectbackground="gray",selectforeground="black")
songs_list.grid(columnspan=9)

#font is defined which is to be used for the button font 
defined_font = font.Font(family='Helvetica')
#play button
play_button=Button(root,text="Play",width =7,command=Play)
play_button['font']=defined_font
play_button.grid(row=1,column=0)
#pause button 
pause_button=Button(root,text="Pause",width =7,command=Pause)
pause_button['font']=defined_font
pause_button.grid(row=1,column=1)
#stop button
stop_button=Button(root,text="Stop",width =7,command=Stop)
stop_button['font']=defined_font
stop_button.grid(row=1,column=2)
#resume button
Resume_button=Button(root,text="Resume",width =7,command=Resume)
Resume_button['font']=defined_font
Resume_button.grid(row=1,column=3)
#previous button
previous_button=Button(root,text="Prev",width =7,command=Previous)
previous_button['font']=defined_font
previous_button.grid(row=1,column=4)
#nextbutton
next_button=Button(root,text="Next",width =7,command=Next)
next_button['font']=defined_font
next_button.grid(row=1,column=5)
#create input box for RSS link
RSS_input = Entry(root, width=40)
RSS_input.grid(row=2, column=0, columnspan=4)
#Load button
load_button=Button(root,text="Load",width =7,command=Load)
load_button['font']=defined_font
load_button.grid(row=2,column=4)
#Download button
download_button=Button(root,text="Download",width =7,command=downloadFile)
download_button['font']=defined_font
download_button.grid(row=2,column=5)

mainloop()