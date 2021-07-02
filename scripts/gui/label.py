import bge
import aud

from bge.logic import globalDict
from ast import literal_eval
from textwrap import wrap

from .common import *

__all__ = ['label']

labelDb = globalDict["Database"]["Gui"]["Label"]


def label(cont):
    # type: (bge.types.SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject

    # Sensors
    always = cont.sensors["Always"]  # type: bge.types.SCA_ISensor
    message = cont.sensors["Message"]
    
    # Ensure group instance
    if group is None:
        own.endObject()
        return
        
    if always.positive:
        
        # Run once at start
        if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            if labelDb["TypeSoundEnable"] and not "LabelTypeSound" in own.scene:
                factory = aud.Factory.file(globalDict["Sounds"]["Sfx"]["GuiLabelType"])
                own.scene["LabelTypeSound"] = aud.device().play(factory, keep=True)
                own.scene["LabelTypeSound"].pause()
                
            own.parent.setParent(group)
            updateLabel(cont)
            
        # Update transition
        if own["InTransition"]:
            if own["Transition"] == "Type":
                transitionType(cont)
                
            elif own["Transition"] in TRANSITION_ANIMS.keys():
                transitionAnim(cont)
        
        # Update label when asked
        else:
            if message.positive:
                updateLabel(cont)


def updateLabel(cont):
    # type: (bge.types.SCA_PythonController) -> None
    
    # Helper variables
    own = cont.owner
    group = own.groupObject
    shadow = group.groupMembers["LabelTextShadow"]
    targetText = getLabelFromGroup(group)
    
    # Set options to label
    labelOffset = list(labelDb["Offset"] if not "Offset" in group else literal_eval(group["Offset"]))
    own.localPosition = labelOffset + [own.localPosition.z]
    own.color = labelDb["Color"] if not "Color" in group else literal_eval(group["Color"])
    own["Transition"] = labelDb["Transition"] if not "Transition" in group else group["Transition"]
    own["LineSize"] = group["LineSize"] if "LineSize" in group else 0
    own["Justify"] = group["Justify"] if "Justify" in group else "Left"
    
    # Set options to shadow
    if labelDb["ShadowEnable"]:
        shadow.visible = True
        shadowOffset = list(labelDb["ShadowOffset"] if not "ShadowOffset" in group else literal_eval(group["ShadowOffset"]))
        shadow.localPosition = shadowOffset + [shadow.localPosition.z]
        shadow.color = labelDb["ShadowColor"] if not "ShadowColor" in group else literal_eval(group["ShadowColor"])
        
    else:
        shadow.visible = False

    if own.text != targetText:
        if own["LineSize"]:
            targetText = wrap(targetText, own["LineSize"])
            if own["Justify"].lower() == "center":
                targetText = [i.center(own["LineSize"]) for i in targetText]
            elif own["Justify"].lower() == "right":
                targetText = [i.rjust(own["LineSize"]) for i in targetText]
            targetText = "\n".join(targetText)
        own["TargetText"] = targetText
        
        # Transition: Typewriter
        if own["Transition"] == "Type":
            own["TransitionState"] = "Showing" if own.text == "" else "Hiding"
            own["InTransition"] = True
            own["TypeCurChar"] = 0
            always = cont.sensors["Always"] # type: bge.types.SCA_AlwaysSensor
            always.usePosPulseMode = True
            always.skippedTicks = labelDb["TypeDelay"]
            
        # Transition: Animation
        elif own["Transition"] in TRANSITION_ANIMS.keys():
            own["InTransition"] = True
            always = cont.sensors["Always"] # type: bge.types.SCA_AlwaysSensor
            always.usePosPulseMode = True
            always.skippedTicks = 0
            
        # Transition: None
        else:
            own.text = shadow.text = targetText


def transitionType(cont):
    # type: (bge.types.SCA_PythonController) -> None
    
    def playTypeSound(obj):
        # type: (bge.types.KX_GameObject) -> None
        
        obj.scene["LabelTypeSound"].volume = globalDict["Config"]["VolSfx"] * labelDb["TypeSoundVol"]
        obj.scene["LabelTypeSound"].position = 0.0
        obj.scene["LabelTypeSound"].resume()
    
    own = cont.owner
    group = own.groupObject
    shadow = group.groupMembers["LabelTextShadow"]
    
    if own["TransitionState"] == "Showing":
        if own["TargetText"] != own.text:
            curChar = own["TargetText"][own["TypeCurChar"]]
            own.text = shadow.text = own.text + curChar
            own["TypeCurChar"] += 1
            
            if own["TypeCurChar"] < len(own["TargetText"]) and own["TargetText"][own["TypeCurChar"]] == " ":
                curChar = own["TargetText"][own["TypeCurChar"]]
                own.text = shadow.text = own.text + curChar
                own["TypeCurChar"] += 1
            
            if "LabelTypeSound" in own.scene:
                playTypeSound(own)
            
        else:
            own["InTransition"] = False
            own["TransitionState"] = "Shown"
            cont.sensors["Always"].usePosPulseMode = False
    
    elif own["TransitionState"] == "Hiding":
        if own.text != "":
            if "LabelTypeSound" in own.scene:
                playTypeSound(own)
            
            own.text = shadow.text = own.text[0:-1]
            
            if len(own.text) > 0 and own.text[-1] == " ":
                own.text = shadow.text = own.text[0:-1]
            
        else:
            own["TransitionState"] = "Showing"


def transitionAnim(cont):
    # type: (bge.types.SCA_PythonController) -> None
    
    own = cont.owner
    group = own.groupObject
    curAnim = TRANSITION_ANIMS[own["Transition"]]
    curFrame = round(own.parent.getActionFrame(), 1)
    
    if not own.parent.isPlayingAction():
        
        if own.text == "":
            curFrame = curAnim[1]
        
        if own.text != own["TargetText"] and curFrame != curAnim[1]:
            own.parent.playAction("GuiTransitions", curAnim[0], curAnim[1], speed=labelDb["TransitionSpeed"])
            
        elif curFrame == curAnim[1]:
            own.text = group.groupMembers["LabelTextShadow"].text = own["TargetText"]
            own.parent.playAction("GuiTransitions", curAnim[1], curAnim[0], speed=labelDb["TransitionSpeed"])
            
        elif own.text == own["TargetText"]:
            own["InTransition"] = False
            cont.sensors["Always"].usePosPulseMode = False
            
