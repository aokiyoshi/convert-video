Ffmpeg ui wrapper written in Python Customtkinter for personal purposes and kind of education. 

Usage:

1. Create and activate virtual env
2. pip install -r requirements.txt
3. python run.py


This program requires ffmpeg installed on your OS. "ffmpeg" command should be available.

Parameters:

1. width 
2. heigth 
3. frame rate
4. use gpu

Width and height parameters are not linked to aspect ratio. Maybe in future versions. Frame rate can not be 0. If check box "use gpu" libx264 codec will be used, otherwise h264.

Attention: converting parameters are not checked at all, be careful.
