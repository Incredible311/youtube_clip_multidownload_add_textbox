ownload multiple Youtube videos and cut them around certain timestamps automatically

How it works:

Preparation:

If you haven’t installed python already, do that. As soon as you did that, you have to pip-install the python packages “YouTube_dl” and “moviepy”. For that just type “pip install YouTube_dl” and “pip install moviepy” in your terminal.

Install ImageMagic As Well 
and in the root that python installed ..Lib/site-packages/moivepy/config_defult.py, change  IMAGEMAGICK_BINARY = os.getenv('IMAGEMAGICK_BINARY', 'auto-detect') to 
IMAGEMAGICK_BINARY = r"C:\\Program Files\\ImageMagick-7.0.11-Q16\\magick.exe"

Create a folder anywhere you like and place the .py file in it and and create a text file with the name “links.txt” in the same folder.

Execution:

Paste multiple links together with timestamps (separated by a space) in the links.txt file. Place every single new video in a new line like this:

Youtube Link, Start Time, End Time, Text

https://youtube.com/… 3:40 3:50 Text

…

Now execute the .py file and it will download the videos and cut out everything, so you end with a clip around the given timestamp. It will save these clips with the last characters from the link and the file extension (this is sometimes .mp4 and sometimes .mkv but both are very supported file types), with two “0” at the beginning, so it lists them at the top of the folder.

Tweaking:

In the code are two variables which represents a time-delta (which is the time between the given timestamp and the end of the clip within the video) and a time-buffer (which represents the time between the beginning of the clip and the timestamp within the video). These are given in seconds and the standard values are 2 seconds for the buffer and 4.25 seconds for the delta, which are just based on experience and trial/error. You can change these in the .py file to your needs of course.