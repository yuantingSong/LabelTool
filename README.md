# faceLabel

## The process 
1. downvideo download vedio.
2. ffmpeg -i [filename] %7d.jpg  // get pictures from vedio.
3. use deeplearning faceDetection to detect face in pictures （syt-main, test）
    input path
        format ---videos
            -video1(file)
                -%7d.jpg
            -video2(file)
                -%7d.jpg
    output [videoName].json
4.  use json2txt.py convert .json to .txt
    use Mywriter.py convert .txt to .xml
5. labelTool



## labelTool
This label tool redevelop basing on [tzutalin/labelImg](https://github.com/tzutalin/labelImg)

### installation
1. After the installation on Windows, replace the labelImg.py file

2. install openCV and opencv contrib : 
    pip install opencv-python
    pip install opencv-contrib-python
3. start labelImg.py

### Hotkeys (Modified)
    Ctrl + u    Load all of the images from a directory
    Ctrl + r    Change the default annotation target dir
    Ctrl + s    Manually Save
    Ctrl + d    Copy the current label and rect box 
    Space   Delete the selected rect box
    w   Create a rect box
    e   Edit the box
    d   Next image (autosave)
    a   Previous image
    t   Convert mode :Track(default),inherit
    s   Work under inherit mode (load the former)
    r   Reload image and box
    v   Flag the current image as verified
    Ctrl++  Zoom in
    Ctrl--  Zoom out
    ↑→↓←    Keyboard arrows to move selected rect box

### Rules
    - Automatic skip only for long term frame without person
    - cache deleted box, area ratio > 0.6 and iou > 0.55
    - show track box and original box together. Once stop track box, the tracking of this box stop.
    - Save sequence, add track box first. then add others depending on iou < 0.5 and union part ratio each area < 0.8 (large overlap small)
    - recommend to delete original box manually, if u not sure whether it will be deleted automaticly.

### Modes
you can use 't' to change mode.
    Modify mode:
        - Automatic skip, Cache deleted RectBox, load last picture's RectBox (add box load, modified box compare and replace, unmodified skip)
    Track mode:
        - Automatic skip, Single page recovery. Cache deleted RectBox, Automatic track new RectBox and modified RectBox, and the mark of tracker is red.