##########################
## BENJAMIN DANNEVILLE  ##
## Auto Turnaround      ##
##                      ##
## Version : 1.0        ##
## Date : February 2021 ##
##########################

import maya.cmds as cmds
from functools import partial

#############
## GLOBALS ##
#############

#Timeslider 0
pb_min = "0sec"
#Names
turn_loc_name = "turnaround_loc"
autoTurn_cam_name = "Render_cam"
hd_checkBox_name = "HD_Playblast_CheckBox"
dir_checkBox_name = "Direction_Playblast_CheckBox"
playblast_txt_field = "playblast_txt_field"
file_name ="Unnamed"
#Curve type for the keyframes
curve_type = "linear"
#Windows_size
window_width = 300
window_height = 230
#Modifiers to check when I click on button
mods = cmds.getModifiers()

###############
## FUNCTIONS ##
###############

#Quality of the playblast
def hd_playblast():
    cmds.setAttr(autoTurn_cam_name + "Shape.filmFit", 3)
    cmds.setAttr(autoTurn_cam_name + "Shape.postScale", 1)
    cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)
    cmds.setAttr("hardwareRenderingGlobals.aasc", 16)

def ld_playblast():
    cmds.setAttr(autoTurn_cam_name + "Shape.filmFit", 1)
    cmds.setAttr("hardwareRenderingGlobals.aasc", 8)
    cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 0)

#Playblast
def playblast(quality_value, scale_value, duration_value,_):   
    #Getting the value of the sliders
    quality_value = cmds.intSliderGrp(quality_value, q=1, value=1)
    scale_value = cmds.intSliderGrp(scale_value, q=1, value=1)
    duration_value = str(cmds.intSliderGrp(duration_value, q=1, value=1)) + "sec"

    #Setting the timeslider to the actual needed value for the playblast
    cmds.playbackOptions(minTime=pb_min, maxTime=duration_value)

    #Case when you are doing a playblast when you already did one
    if (cmds.objExists(turn_loc_name)):
        #Info
        print ("Playblast has already been launched at least once")

        #Deleting old keyframes and creating new ones
        cmds.cutKey(turn_loc_name, time=(1,360))

    #Case when you are doing your first playblast
    else: 
        #Get the actual cam
        pan = cmds.getPanel(withFocus=True)
        base_cam_name = cmds.modelPanel(pan, query=True, camera=True)

        #Duplicating and renaming the actual cam
        cmds.duplicate(base_cam_name, name=autoTurn_cam_name)

        #Change of cam
        cmds.lookThru(autoTurn_cam_name)

        #Creating the locator for the turnaround
        turn_loc = cmds.spaceLocator(name=turn_loc_name)
        cmds.setAttr(turn_loc_name + ".visibility", 0)

        #Parenting the cam under the locator
        cmds.parent(autoTurn_cam_name, turn_loc_name)

        #Setting the keyframes
        cmds.setKeyframe(turn_loc_name, t=pb_min, itt= curve_type, ott=curve_type)

    #Choix de direction
    #Right
    if (cmds.checkBox(dir_checkBox_name, q=True, value=True)):
        cmds.setKeyframe(turn_loc_name, v=360, at="rotateY", t=duration_value, itt= curve_type, ott=curve_type)
    #Left
    else :
        cmds.setKeyframe(turn_loc_name, v=-360, at="rotateY", t=duration_value, itt= curve_type, ott=curve_type)
    #Choix entre le HD ou le LD
    if (cmds.checkBox(hd_checkBox_name, q=True, value=True)):
        hd_playblast()

    else :
        ld_playblast() 

    #Playblasting
    cmds.playblast(f="movies/" + cmds.textFieldGrp(playblast_txt_field, q=True, tx=True), p=scale_value, qlt =quality_value, fmt="qt", fo=True, v=True, cc=True, orn=False, c="H.264", wh=[cmds.getAttr("defaultResolution.width"),cmds.getAttr("defaultResolution.height")])

############
## WINDOW ##
############

try:
    cmds.deleteUI(AutoTurn, window=True)
except (NameError, RuntimeError):
    pass
AutoTurn = cmds.window(title = "BD Auto Turnaround", w=window_width, h=window_height)
cmds.rowColumnLayout (nc =1)

#Header    
cmds.text('\n',h=5)
cmds.text("BD Auto Turnaround")
cmds.separator(style="out",h=5,w=5)
cmds.text('\n',h=5)

#Body
cmds.text("  1 -   Hide everything you don't want to see", align="left")
cmds.text('\n',h=5)
cmds.text("  2 -   Place you camera and choose your settings", align="left")
cmds.text('\n',h=5)
cmds.text("  3 -   Click in your VIEWPORT ! and hit Playblast", align="left")
cmds.text('\n',h=10)
cmds.textFieldGrp(playblast_txt_field, label="Name :", tx=file_name)
x = cmds.intSliderGrp(l= "Quality (%): ", v=100,min=1, max=100, field=True)
y = cmds.intSliderGrp(l= "Scale (%): ", v=100,min=1, max=100, field=True)
z = cmds.intSliderGrp(l= "Duration (s): ", v=8,min=1, max=15, field=True)
cmds.checkBox(hd_checkBox_name ,label="HD Playblast", value = 1)
cmds.checkBox(dir_checkBox_name ,label="Inverse direction", value = 0)
cmds.text('\n',h=10)
cmds.button(label = "Playblast", command=partial(playblast, x, y,z))
cmds.text('\n',h=5)

#Credits
cmds.text("copyright Benjamin Danneville                                                 licence GNU GPL")

#Check if LB or Shift + LB
mods = cmds.getModifiers()
if mods == 0:
    playblast(x,y,z,"_")
if mods == 1:
    #Show Window
    cmds.showWindow(AutoTurn)