# Import everything needed to edit video clips  
import subprocess
import sys
import os

try:  # Checks if ytdl is installed- installs if unavailable
    import youtube_dl
except ImportError as e:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'youtube-dl'])
    import youtube_dl

try:  # Checks if moviepy is installed- installs if unavailable
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
except ImportError as e:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'moviepy'])
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from moviepy.editor import *  
links = None

def convert_list_to_string(org_list, seperator=' '):
    """ Convert list to string, by joining all item in list with given separator.
        Returns the concatenated string """
    return seperator.join(org_list)


try:
    links = open("links.txt", "r")
except FileNotFoundError as e:
    input(
        "Unable to start! Make sure you create a file called: 'links.txt' in this SAME folder as this program!\nPress "
        "any key to exit")
    sys.exit(-1)

for idx, line in enumerate(links.readlines()):
    info = line.split(" ")
    link = info[0]
    print(link)


    ydl_opts = {"outtmpl": f"{link[-5:]}.mp4"}  # Fix file extension not being appended

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except youtube_dl.utils.DownloadError as ex:
            print("\nThis link does not work: " + f"{link}")

    video = None
    print(info[1:2])
    start_time = 0
    end_time = 0
    for timestamp in info[1:2]:
        try:
            time_info = timestamp.split(":")
            start_time = timestamp.split(":")
            time_m = int(time_info[0])

            time_s = int(time_info[1])
            time = time_m * 60 + time_s

            print(f"{time} - {time_m} - {time_s}")
        except:
            input("\nCould not read the given timestamps\nbe sure to write them correctly in the links.txt file\n")
        # Measured in seconds
        try:
          time_info = info[2].split(':')
          end_time = info[2].split(':')
          time_m = int(time_info[0])

          time_s = int(time_info[1])
          time_d = time_m * 60 + time_s
        except:
          time_d = 4.25  # Time delta (time between timestamp and end of clip)
        time_b = 0  # Time buffer (time between beginning of clip and timestamp)
        print(time_d)
        try:
            txt = convert_list_to_string(info[3:])
        except:
            txt = ''
        try:
            i = 0
            for vid in os.listdir():
                if vid.endswith(f"{link[-5:]}.mp4"):
                    while f"00{link[-8:]}{i}.mp4" in os.listdir():
                        i += 1
                    ffmpeg_extract_subclip(f"{vid}", time + 1 - time_b,
                                            time_d, targetname=f"00{link[-8:]}{i}.mp4")
                    vid_ = f"00{link[-8:]}{i}.mp4"
                    video = vid
                elif vid.endswith(f"{link[-5:]}.mkv"):
                    while f"00{link[-8:]}{i}.mkv" in os.listdir():
                        i += 1
                    ffmpeg_extract_subclip(f"{vid}",  time + 1 - time_b,
                                           time_d, targetname=f"00{link[-8:]}{i}.mkv")
                    vid_ = f"00{link[-8:]}{i}.mkv"
                    video = vid
        except IOError as ex:
            print("\nCould not run! There was a video with the same filename '" + f"{link[-5:]}.mp4" + "' inside this "
                                                                                                       "folder\nPress "
                                                                                                       "any key to "
                                                                                                       "exit")
        except:
            input("\nSomething went wrong\nCould not cut video")
            sys.exit(-1)
    try:
        os.remove(f"{video}")
        print("Done")
    except:
        print("Fail")
        pass
    print(video)

    # loading video dsa gfg intro video  
    clip = VideoFileClip(vid_)  
        
    # # clipping of the video   
        
    # # Reduce the audio volume (volume x 0.8)  
    clip = clip.volumex(0.8)  
    w,h = moviesize = clip.size    
        
    # # Generate a text clip  
    tss = '  ' + "\n" + '   ' + txt
    txt_clip = TextClip(f"{tss}", bg_color="black", align="center", kerning=5, fontsize = 26, color = 'white')  
        
    # setting position of text in the center and duration will be 10 seconds  
    # txt_clip = txt_clip.set_pos('center').set_duration(5)  
    txt_clip = txt_clip.margin(right=30).set_pos(lambda t: (min(w/30,int(w-0.5*w*t)),max(5*h/6,int(100*t)))).fadein(2.0).set_duration(4)  
        
    # # Overlay the text clip on the first video clip  
    video_ = CompositeVideoClip([clip, txt_clip])  
        
    # # showing video  
    video_.write_videofile(f"output_{idx}.mp4",fps=24,codec='libx264') 
    print(vid_)
    try:
        os.remove(vid_)
    except:
        print('Fail')
        pass
    try:
        try:
            os.remove("__temp__.mp4")
        except:
            os.remove("__temp__.mkv")
    except:
        pass

    vid_ = ''
links.close()
print("\nDone!")


