import os, keyboard, mutagen.mp3
from time import sleep
from pygame import mixer

option = 'N'

def change_option(choice):
    global option
    option = choice

keyboard.add_hotkey('end+p', lambda: change_option('P'))
keyboard.add_hotkey('end+r', lambda: change_option('R'))
keyboard.add_hotkey('end+n', lambda: change_option('N'))
keyboard.add_hotkey('end+s', lambda: change_option('S'))
keyboard.add_hotkey('end+q', lambda: change_option('Q'))
keyboard.add_hotkey('end+up', lambda: change_option('VU'))
keyboard.add_hotkey('end+down', lambda: change_option('VD'))
keyboard.add_hotkey('end+b', lambda: change_option('B'))

path = 'C://Users/%s/Music/' % os.getlogin()

option = input("The default location of the songs is: %s do you want to change it? (Y/N) " % path)

if(option.upper() == "Y"):
    valid = False
    while(not valid):
        path = input("Enter the full path where the songs are located: ")
        if(os.path.isdir(path)):
            valid = True
        else:
            print("Invalid path!\n")

files = os.listdir(path)
mp3files = list(filter(lambda f: f.endswith('.mp3') ,files))

i=0
for song in mp3files:
    print('Index: '+str(i)+' | '+song)
    i+=1

print('#'*100)
print('Write the indexes of the songs you want to play separated by space. Ex: 4 2 15 7')
print('If you want to play all the songs, just type the index of the song you want to start to play')
playlist = input("Indexes: ")

playlist = playlist.split(' ')
if(len(playlist)>1):
    songs = []
    for index in playlist:
        if(index.isdigit() and int(index)<i and int(index)>=0):
            songs.append(mp3files[int(index)])
    mp3files = songs
    i=0
    total=len(mp3files)
else:
    total=i
    i=int(playlist[0])
    if(i>total):
        i=total-1
    else:
        if(i<0):
            i=0

stopped = False
mixer.init()

current_volume = mixer.music.get_volume()

print('#'*100)
print('End + n - Next song')
print('End + b - Go back to the previous song')
print('End + s - Stop song')
print('End + up - Volume up')
print('End + down - Volume down')
print('End + p - Pause the song')
print('End + r - Resume the song')
print('End + q - Quit player')
print('#'*100)

while(True):
    sleep(0.3)
    if(not mixer.music.get_busy() and not stopped):
        option='N'
    if(option):
        if(option == 'Q'):
            break
        elif(option == 'S'):
                mixer.music.stop()
                print('#'*100)
                print('The song has stopped')
                print('#'*100)
                stopped=True
                option=False
        elif(option == 'P'):
                mixer.music.pause()
                print('#'*100)
                print('The song was paused...')
                print('#'*100)
                option=False
        elif(option == 'R'):
                mixer.music.unpause()
                print('#'*100)
                print('The song is playing again!')
                print('#'*100)
                option=False
        elif(option == 'N' or option == 'B'):
                if(option == 'B'):
                    if(i==0):
                        i=total-2
                    else:
                        i-=2
                        if(i<0):
                            i=total-1
                print('#'*100)
                print('Currently playing '+mp3files[i])
                print('#'*100)
                freq = mutagen.mp3.MP3(path+"\/"+mp3files[i]).info.sample_rate
                mixer.quit()
                mixer.init(frequency=freq)
                mixer.music.set_volume(current_volume)
                mixer.music.load(path+"\/"+mp3files[i])
                mixer.music.play()
                i+=1
                if(i == total):
                    i=0
                stopped=False
                option=False
        elif(option == 'VU'):
                current = current_volume
                current+= 0.05
                if(current <= 1):
                    current_volume=current
                    mixer.music.set_volume(current)
                option=False
        elif(option == 'VD'):
                current = current_volume
                current-= 0.05
                if(current >= 0):
                    current_volume=current
                    mixer.music.set_volume(current)
                option=False