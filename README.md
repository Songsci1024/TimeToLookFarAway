# Time to look far away


## Function 
Set a time to rest your eyes, and instead of manually starting, monitor the mouse, keyboard, and sound device to determine if you are looking at the screen.

## Requirement package
Look at the requirement.txt

## Define
Activities：
- mouse click or move
- any key in keyboard is pressed
- audio device is working

Work time: the time which any one of these activities happens

Clear time: any longer than this will clear the previous working hours which is accumulated

## Remind
In the windows11, if you want to receive the notification when you watching the full screen video or playing games, please change the config in the windows11 setting > notification > Automatically enable Do Not Disturb


## how to work

``` shell
conda create --name new_env python=3.8
conda activate new_env
pip install -r requirement.txt
python main.py
```