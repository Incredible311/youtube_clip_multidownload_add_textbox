# Import everything needed to edit video clips  
# !apt install ffmpeg
import subprocess
import sys
import os
import shutil
import os, urllib.request
try:
  HOME = os.path.expanduser("~")
  from IPython.display import clear_output
  pathDoneCMD = f'{HOME}/doneCMD.sh'
  if not os.path.exists(f"{HOME}/.ipython/ttmg.py"):
      hCode = "https://raw.githubusercontent.com/yunooooo/gcct/master/res/ttmg.py"
      urllib.request.urlretrieve(hCode, f"{HOME}/.ipython/ttmg.py")

  from ttmg import (
      loadingAn,
      textAn,
  )

  loadingAn(name="lds")
  textAn("Installing Dependencies...", ty='twg')
  os.system('pip install git+git://github.com/AWConant/jikanpy.git')
  os.system('add-apt-repository -y ppa:jonathonf/ffmpeg-4')
  os.system('apt-get update')
  os.system('apt install mediainfo')
  os.system('apt-get install ffmpeg')
  clear_output()
  print('Installation finished.')
except:
  pass


try:
    from PIL import Image, ImageDraw, ImageFont
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'Pillow'])
    from PIL import Image, ImageDraw, ImageFont

try:  # Checks if ytdl is installed- installs if unavailable
    import youtube_dl
except ImportError as e:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'youtube-dl'])
    import youtube_dl
from time import sleep
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
    if os.path.exists('TEMP'):
      shutil.rmtree('TEMP')

    if os.path.exists('Cut'):
      shutil.rmtree('Cut')
    info = line.split(" ")
    link = info[0]
    print(link)

    #Download Youtube and Cut Video
    SAVE_PATH = '/'.join(os.getcwd().split('/')[:3]) + '/TEMP'
    ydl_opts = {"outtmpl": f"{SAVE_PATH}/{link[-5:]}.mp4"}  # Fix file extension not being appended

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
        except youtube_dl.utils.DownloadError as ex:
            print("\nThis link does not work, So Video Passed : " + f"{link}")
            print(f"Check Line Number {idx}")
            continue
    video = None
    print(info[1:2])
    
    for timestamp in info[1:2]:
        try:
            time_info = timestamp.split(":")
            time_m_ = int(time_info[0])

            time_s_ = int(time_info[1])
            time = time_m_ * 60 + time_s_

            
        except:
            print("\nCould not read the given timestamps\nbe sure to write them correctly in the links.txt file\n")
            print(f"Check Line Number {idx}")
            print("Correct First Time Should Look Like '0:20' something")
            continue
        # Measured in seconds
        try:
          time_info = info[2].split(':')
          time_m = int(time_info[0])

          time_s = int(time_info[1])
          time_d = time_m * 60 + time_s
        except:
          time_d = 4.25  # Time delta (time between timestamp and end of clip)
        time_b = 0  # Time buffer (time between beginning of clip and timestamp)
        
        try:
            txt = convert_list_to_string(info[3:])
        except:
            txt = ''
        
        try:
          vid = os.listdir('TEMP')[0]
          if not os.path.exists('Cut'):
            os.mkdir('Cut')
            print('Created Cut Folder')
          if vid.endswith('.mp4'):
            print('Condition-1')
            new = VideoFileClip(f"TEMP/{vid}")
            sub = new.subclip(time, time_d)
            sub.write_videofile(f"Cut/cutVideo_{idx}.mp4", codec='libx264') 
            sub.close()
            # ffmpeg_extract_subclip(f"TEMP/{vid}", time, time_d,
            #                      targetname=f"Cut/cutVideo_{idx}.mp4")
          else:
            print('Condition-2')
            new = VideoFileClip(f"TEMP/{vid}")
            sub = new.subclip(time, time_d)
            sub.write_videofile(f"Cut/cutVideo_{idx}.mkv", codec='libx264') 
            sub.close()
            # ffmpeg_extract_subclip(f"TEMP/{vid}", time, time_d,
            #                      targetname=f"Cut/cutVideo_{idx}.mkv")
          print(f"Video Extracted._")
          
          shutil.rmtree('TEMP')
          print('Removed TEMP')
        except:
          print("Some Error Occured While Cutting Video!!")
          continue
          
        
          
    
    
    # loading video
    vid_link = os.listdir('Cut')[0]
        
    
      
    try:
      clip = VideoFileClip(f"Cut/{vid_link}")    
    except:
      print("Some Unknown error Occurred")
      continue  
    # # clipping of the video   
        
    # # Reduce the audio volume (volume x 0.8)  
    clip = clip.volumex(0.8)  
    w,h = moviesize = clip.size
    start_time = info[1]
    end_time = info[2]
     
    # # Generate a text clip  
    # Add Rounded Borders
    def add_corners(im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im
    # fnt = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", 28)
    fnt = ImageFont.truetype("arial", 28)
    # fnt = ImageFont.load_default()
    # Add Text To Image
    def image_with_text(size, pos, text):

        img = Image.new("RGB", pos, "black")
        draw = ImageDraw.Draw(img)
        draw.text((size[0], size[1]), text, font = fnt, fill="white")
    
        return img 

    # Add Text To Video Using PIL  
    txt_ = txt
    pos_1 = fnt.getsize(txt_)
    p = image_with_text((34, pos_1[1]/2 + 8), (pos_1[0] + 75, 75), txt)
    p.save('set.png')
    i = Image.open('set.png')
    img = add_corners(i, 21)
    img.save('cor.png')
    os.remove('set.png')  
        
    # # Overlay the text clip on the first video clip
    txt_clip = ImageClip('cor.png')
    txt_clip_ = txt_clip.set_position(lambda t: (min(w/30,int(w-0.5*w*t)),max(5*h/6.3,0))).set_duration(5)  
    video_ = CompositeVideoClip([clip, txt_clip_])  
        
    # # Saving video
    if not os.path.exists("Result"):
      os.mkdir('Result')
    out = f"Result/output_{idx}_{link[-8:]}.avi"
    if os.path.exists(out):
      output = f"Result/output_{idx}_{link[-8:]}_d.avi"
    else:
      output = f"Result/output_{idx}_{link[-8:]}.avi"
    video_.write_videofile(output,fps=22,codec='libx264') 
    # video_.write_videofile(output) 
    print(vid_link)

    os.remove('cor.png')
    
    try:
        try:
            os.remove("__temp__.mp4")
        except:
            os.remove("__temp__.mkv")
    except:
        pass
    video_.close()
    clip.close()
    shutil.rmtree('Cut')
    vid_ = ''
links.close()
print("\nDone!")


