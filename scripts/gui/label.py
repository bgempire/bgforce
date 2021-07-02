import bge
import aud

from bge.logic import globalDict
from ast import literal_eval

__all__ = ['label']

labelDb = globalDict["Database"]["Gui"]["Label"]

TRANSITION_ANIMS = {
    "SlideLeft" : [0, 20],
    "SlideRight" : [30, 50],
    "FallBack" : [60, 80],
}


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
        if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            if labelDb["TypeSoundEnable"] and not "LabelTypeSound" in own.scene:
                factory = aud.Factory.file(globalDict["Sounds"]["Sfx"]["GuiLabelType"])
                own.scene["LabelTypeSound"] = aud.device().play(factory, keep=True)
                own.scene["LabelTypeSound"].pause()
                
            own.parent.setParent(group)
            _updateLabel(cont)
            
        if own["InTransition"]:
            if own["Transition"] == "Type":
                _transitionType(cont)
                
            elif own["Transition"] in TRANSITION_ANIMS.keys():
                _transitionAnim(cont)
        
        else:
            if message.positive:
                _updateLabel(cont)


def _getTextFromGroup(obj):
    # type: (bge.types.KX_GameObject) -> str
    
    if "Label" in obj:
        if str(obj["Label"]).startswith(">"):
            try:
                return str(literal_eval(obj["Label"][1:]))
            except:
                return str(obj["Label"])
        else:
            return str(obj["Label"])
        
    else:
        return ""


def _updateLabel(cont):
    # type: (bge.types.SCA_PythonController) -> None
    
    # Helper variables
    own = cont.owner
    group = own.groupObject
    shadow = group.groupMembers["LabelTextShadow"]
    targetText = _getTextFromGroup(group)
    
    # Set options
    labelOffset = list(labelDb["Offset"] if not "Offset" in group else literal_eval(group["Offset"]))
    own.localPosition = labelOffset + [own.localPosition.z]
    own.color = labelDb["Color"] if not "Color" in group else literal_eval(group["Color"])
    own["Transition"] = labelDb["Transition"] if not "Transition" in group else group["Transition"]
    
    if labelDb["ShadowEnable"]:
        shadow.visible = True
        shadowOffset = list(labelDb["ShadowOffset"] if not "ShadowOffset" in group else literal_eval(group["ShadowOffset"]))
        shadow.localPosition = shadowOffset + [shadow.localPosition.z]
        shadow.color = labelDb["ShadowColor"] if not "ShadowColor" in group else literal_eval(group["ShadowColor"])
        
    else:
        shadow.visible = False

    if own.text != targetText:
        
        # Transition: Typewriter
        if own["Transition"] == "Type":
            own["TransitionState"] = "Showing" if own.text == "" else "Hiding"
            own["InTransition"] = True
            own["TypeCurChar"] = 0
            own["TypeTargetText"] = _getTextFromGroup(group)
            always = cont.sensors["Always"] # type: bge.types.SCA_AlwaysSensor
            always.usePosPulseMode = True
            always.skippedTicks = labelDb["TypeDelay"]
            
        # Transition: Animation
        elif own["Transition"] in TRANSITION_ANIMS.keys():
            own["TransitionState"] = "Showing" if own.text == "" else "Hiding"
            own["InTransition"] = True
            always = cont.sensors["Always"] # type: bge.types.SCA_AlwaysSensor
            always.usePosPulseMode = True
            always.skippedTicks = 0
            
        # Transition: None
        else:
            text = _getTextFromGroup(group)
            own.text = shadow.text = text


def _transitionType(cont):
    # type: (bge.types.SCA_PythonController) -> None
    
    own = cont.owner
    group = own.groupObject
    shadow = group.groupMembers["LabelTextShadow"]
    
    if own["TransitionState"] == "Showing":
        if own["TypeTargetText"] != own.text:
            curChar = own["TypeTargetText"][own["TypeCurChar"]]
            own.text = shadow.text = own.text + curChar
            own["TypeCurChar"] += 1
            
            if own["TypeCurChar"] < len(own["TypeTargetText"]) and own["TypeTargetText"][own["TypeCurChar"]] == " ":
                curChar = own["TypeTargetText"][own["TypeCurChar"]]
                own.text = shadow.text = own.text + curChar
                own["TypeCurChar"] += 1
            
            if "LabelTypeSound" in own.scene:
                own.scene["LabelTypeSound"].volume = globalDict["Config"]["VolSfx"] * labelDb["TypeSoundVol"]
                own.scene["LabelTypeSound"].position = 0.0
                own.scene["LabelTypeSound"].resume()
            
        else:
            own["InTransition"] = False
            own["TransitionState"] = "Shown"
            cont.sensors["Always"].usePosPulseMode = False
    
    elif own["TransitionState"] == "Hiding":
        if own.text != "":
            if "LabelTypeSound" in own.scene:
                own.scene["LabelTypeSound"].volume = globalDict["Config"]["VolSfx"] * labelDb["TypeSoundVol"]
                own.scene["LabelTypeSound"].position = 0.0
                own.scene["LabelTypeSound"].resume()
            
            own.text = shadow.text = own.text[0:-1]
            
            if len(own.text) > 0 and own.text[-1] == " ":
                own.text = shadow.text = own.text[0:-1]
            
        else:
            own["TransitionState"] = "Showing"


def _transitionAnim(cont):
    # type: (bge.types.SCA_PythonController) -> None
    
    own = cont.owner
    group = own.groupObject
    shadow = group.groupMembers["LabelTextShadow"]
    curAnim = TRANSITION_ANIMS[own["Transition"]]
    targetText = _getTextFromGroup(own.groupObject)
    
    if not own.parent.isPlayingAction():
        
        if own.text != targetText:
            own.parent.playAction("GuiTransitions", curAnim[0], curAnim[1])
            
        elif own.parent.getActionFrame() == curAnim[1]:
            own.text = shadow.text = targetText
            own.parent.playAction("GuiTransitions", curAnim[1], curAnim[0])
            
        elif own.text == targetText:
            own["InTransition"] = False
            cont.sensors["Always"].usePosPulseMode = False