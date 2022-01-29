import bge
import string

from bge.types import *
from ast import literal_eval
from textwrap import wrap
from math import radians
from pathlib import Path
from hashlib import md5

from . import DEBUG, config, database, state, lang, cache, curPath
from .request import Request
from .thirdparty.pyp3rclip import copy, paste


__all__ = ["widget", "mouseCursor"]


ALWAYS_SKIPPED_TICKS = 5
COMMAND_SEPARATOR = " | "
IMPORTANT_PREFIX = "!"
EXEC_PREFIX = ">"
LANG_PREFIX = "#"
COMPUTED_PREFIX = "$"
TRANSITION_ANIMS = {
    "SlideL": {"Shown" : 0, "Hidden" : 20},
    "SlideR": {"Shown" : 30, "Hidden" : 50},
    "ScaleV": {"Shown" : 60, "Hidden" : 80},
    "ScaleH": {"Shown" : 90, "Hidden" : 110},
    "Arc": {"Shown" : 120, "Hidden" : 140},
}
OBJ_REF_PROPS = {
    "LabelObj" : "LABEL",
    "LabelShadowObj" : "LABEL_SHADOW",
    "ClickableObj" : "CLICKABLE",
    "IconObj" : "ICON",
    "ArrowLeftObj" : "ARROW_LEFT",
    "ArrowRightObj" : "ARROW_RIGHT"
}
INPUT_VALID_CHARS = {
    "ALL" : "",
    "ALPHABETIC" : string.ascii_letters,
    "ALPHANUMERICNOSPACE" : string.ascii_letters + string.digits,
    "ALPHANUMERIC" : string.ascii_letters + string.digits + " ",
    "NUMERIC" : string.digits,
    "PRINTABLE" : string.printable,
}


if not hasattr(bge.logic, "widgetHovered"):
    bge.logic.__widgetHovered = None
    bge.logic.__widgetDescription = ""


# Controller endpoint
def widget(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    camera = own.scene.active_camera
    
    # Sensors
    always = cont.sensors["Always"]  # type: SCA_AlwaysSensor
    message = cont.sensors["Message"] # type: KX_NetworkMessageSensor

    if not group:
        own.endObject()
        return

    if always.positive:
        
        # Initialize widget at start
        if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            widgetInit(cont)
            
            if own["ClickableObj"]:
                clickableSetVisual(cont, "Normal")
        
        # Update label if property Update is provided
        if own.isPlayingAction():
            always.skippedTicks = ALWAYS_SKIPPED_TICKS
        
        elif "Update" in group and group["Update"] >= 0:
            always.skippedTicks = group["Update"]
            labelUpdateTextObj(cont)
            
        else:
            always.skippedTicks = own["UpdateFrequency"]
        
        # Start transition when GUI update is requested
        if message.positive and not own.isPlayingAction():
            bodies = [i.strip() for i in message.bodies if i.strip()]
            groups = [] # type: list[str]
            command = ""
            
            for body in bodies:
                if body[0] in ("[", "("):
                    command = _processCommand(body)
                else:
                    groups += [g.strip() for g in body.split(",")]
                
            if not groups or "Group" in group and str(group["Group"]).strip() in groups:
                own["TransitionState"] = "Hiding"
                
            if command:
                own.scene["CommandCamera"] = command
            
        widgetProcessEnabled(cont)
        processTransition(cont)
        
        # Process clickable widget if applicable
        if own["ClickableObj"]:
            clickableProcess(cont)
    

def mouseCursor(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    always = cont.sensors["Always"]  # type: SCA_AlwaysSensor
    mouseOver = cont.sensors["MouseOver"] # type: KX_MouseFocusSensor
    lmb = cont.sensors.get("LMB", None) # type: SCA_MouseSensor
    rmb = cont.sensors.get("RMB", None) # type: SCA_MouseSensor
    
    cursorObj = own.childrenRecursive["MouseCursor"]
    canvasObj = own.childrenRecursive["MouseCursorCanvas"]
    curWidget = bge.logic.__widgetHovered # type: KX_GameObject
    
    if always.positive:
        
        if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            _getPropsFromDb(cont)
            cursorObj.localScale = list(own["Size"]) + [1]
            canvasObj.localScale = list(own["CanvasSize"]) + [1]
            
            if not hasattr(bge.logic, "__cursorVisible"):
                bge.logic.__showMouseCursor = True
            
        if bge.logic.__showMouseCursor and mouseOver.positive:
            cursorObj.visible = True
            cursorObj.worldPosition = mouseOver.hitPosition
            cursorObj.worldPosition.x += list(own["Offset"])[0]
            cursorObj.worldPosition.y += list(own["Offset"])[1]
            meshName = "MouseCursor"
            color = own["ColorNormal"]
            
            if curWidget and not curWidget.invalid:
                if not curWidget["Enabled"]:
                    meshName += "Disabled"
                    color = own["ColorDisabled"]
                    
                elif curWidget["WidgetType"] == "Input":
                    meshName += "Beam"
                    color = own["ColorHover"]
                    
                elif lmb.positive or rmb.positive:
                    meshName += "HandClick"
                    color = own["ColorClick"]
                    
                else:
                    meshName += "HandNormal"
                    color = own["ColorHover"]
                
            else:
                if lmb.positive or rmb.positive:
                    meshName += "ArrowClick"
                    color = own["ColorClick"]
                    
                else:
                    meshName += "ArrowNormal"
                
            if cursorObj.meshes[0].name != meshName:
                cursorObj.replaceMesh(meshName)
                cursorObj.color = color
            
        else:
            cursorObj.visible = False


# Abstraction functions
def widgetInit(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    debugProps = True if "Debug" in group and group["Debug"] else False
    
    # Parent children of group to widget parent
    for obj in group.children:
        obj.setParent(own)
    
    # Set widget parent to group object
    own.setParent(group)
    
    # Store references to individual objects in widget's parent
    for prop in OBJ_REF_PROPS.keys():
        own[prop] = ([obj for obj in group.groupMembers if OBJ_REF_PROPS[prop] in obj] + [None])[0]
    
    # Create widget properties based on its database config
    _getPropsFromDb(cont)
    
    # Create additional props in widget
    additionalProps = {
        "TargetLabel" : "",
        "TransitionState" : "Shown",
    }
    
    for prop in additionalProps.keys():
        own[prop] = additionalProps[prop]
        if debugProps: own.addDebugProperty(prop)
    
    # Set label and shadow properties if they exist
    widgetProcessEnabled(cont)
    labelUpdateTextObj(cont)
    
    # Set clickable widget properties
    if own["ClickableObj"]:
        own["Commands"] = _getCommandsFromGroup(cont)
        own["Clicked"] = False
        own["ClickableObj"].localScale = list(own["Size"]) + [1.0]
        own["ClickableObj"].localPosition = list(own["Offset"]) + [own["ClickableObj"].localPosition.z]
    
    # Show transition at start
    if own["Transition"] in TRANSITION_ANIMS.keys():
        own["TransitionState"] = "Showing"
    own["InitTransition"] = False
    
    # Show objects at start
    for objRef in OBJ_REF_PROPS.keys():
        if objRef != "LabelShadowObj" and own[objRef]:
            own[objRef].visible = True
            
    if own["WidgetType"] == "Checkbox":
        checkboxAction(cont, True)
        
    elif own["WidgetType"] == "List":
        listAction(cont, "Init")
        
    elif own["WidgetType"] == "IconButton":
        iconButtonAction(cont, "Init")
        
    elif own["WidgetType"] == "Input":
        inputAction(cont, "Init")
        
    elif own["WidgetType"] == "Image":
        imageAction(cont, "Init")
        
    elif own["WidgetType"] == "MeshButton":
        meshButtonAction(cont, "ReplaceMesh")


def widgetProcessEnabled(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    camera = own.scene.active_camera
    
    if "Enabled" in group:
        if type(group["Enabled"]) == str:
            try:
                expression = group["Enabled"].strip() # type: str
                
                if expression.startswith(COMPUTED_PREFIX):
                    own["Enabled"] = bool(_getComputed(expression))
                else:
                    own["Enabled"] = bool(eval(expression))
            except:
                own["Enabled"] = True
        else:
            own["Enabled"] = bool(group["Enabled"])
    else:
        own["Enabled"] = True


def labelUpdateTextObj(cont, setLabel=True):
    # type: (SCA_PythonController, bool) -> None

    own = cont.owner
    
    if own["LabelObj"] and own["LabelShadowObj"]:
        labelObj = own["LabelObj"]
        shadowObj = own["LabelShadowObj"]
        
        # Set text to label and shadow
        if setLabel:
            own["TargetLabel"] = labelObj.text = shadowObj.text = _getTextFromGroup(cont)
        
        # Set color and offset of label
        labelObj.color = own["LabelColor"] if own["Enabled"] else own["LabelColorDisabled"]
        labelObj.localPosition = list(own["LabelOffset"]) + [labelObj.localPosition.z]
        labelObj.localScale = [own["LabelSize"], own["LabelSize"], 1.0]
        
        # Set visibility, color and offset of shadow
        shadowObj.visible = bool(own["ShadowEnable"])
        shadowObj.color = own["ShadowColor"] if own["Enabled"] else own["ShadowColorDisabled"]
        shadowObj.localPosition = list(labelObj.localPosition)[0:2] + [shadowObj.localPosition.z]
        shadowObj.localPosition.x += own["ShadowOffset"][0]
        shadowObj.localPosition.y += own["ShadowOffset"][1]
        shadowObj.localScale = [own["LabelSize"], own["LabelSize"], 1.0]

        if own["WidgetType"] == "Input" and not own["InputText"]:
            labelObj.color = own["PlaceholderColor"] if own["Enabled"] else own["PlaceholderColorDisabled"]
            shadowObj.color = own["PlaceholderShadowColor"] if own["Enabled"] else own["PlaceholderShadowColorDisabled"]


def processTransition(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    camera = own.scene.active_camera
    curAnim = TRANSITION_ANIMS.get(own["Transition"])
    always = cont.sensors["Always"] # type: SCA_AlwaysSensor
    
    if own["TransitionState"] == "Shown" and not own["InitTransition"]:
        own["InitTransition"] = True
    
    if not own.isPlayingAction() and curAnim:
        
        # Play hide animation
        if own["TransitionState"] == "Hiding":
            own.playAction("GuiTransitions", curAnim["Shown"], curAnim["Hidden"], speed=own["TransitionSpeed"])
            own["TransitionState"] = "Showing"
        
        # Play show animation
        elif own["TransitionState"] == "Showing":
            own.playAction("GuiTransitions", curAnim["Hidden"], curAnim["Shown"], speed=own["TransitionSpeed"])
            own["TransitionState"] = "Shown"
            
            # Execute camera move command
            if "CommandCamera" in own.scene:
                try:
                    exec(own.scene["CommandCamera"])
                except Exception as e:
                    if DEBUG: print(e)
                finally:
                    del own.scene["CommandCamera"]
            
            if own["ClickableObj"] and own["TransitionOnClick"] and own["Clicked"]:
                own["Clicked"] = False
                _execCommands(cont, False)
            
            # Update label while it's still hidden
            labelUpdateTextObj(cont)


def clickableSetVisual(cont, state, button=""):
    # type: (SCA_PythonController, str, str) -> None
    
    own = cont.owner
    clickableObj = own["ClickableObj"] # type: KX_GameObject
    colorState = state
    other = ""
    meshName = own["WidgetType"] # type: str
    performReplace = True
    
    if own["WidgetType"] == "Checkbox":
        other = str(own["Checked"])
        other = "Radio" + other if "Value" in own.groupObject else other
    
    elif own["WidgetType"] == "List":
        arrowLeftObj = own["ArrowLeftObj"] # type: KX_GameObject
        arrowRighttObj = own["ArrowRightObj"] # type: KX_GameObject
        meshName_ = "ListArrowClick" if state == "Click" else "ListArrow"
            
        arrowLeftObj.replaceMesh(meshName_ + "Left")
        arrowLeftObj.color = own["ArrowColorClick"] if button == "Right" else own["ArrowColorNormal"]
        arrowRighttObj.replaceMesh(meshName_ + "Right")
        arrowRighttObj.color = own["ArrowColorClick"] if button == "Left" else own["ArrowColorNormal"]
        
    elif own["WidgetType"] == "Input":
        if own["InputEnable"]:
            state = "Click"
        
    elif own["WidgetType"] in ("Image", "MeshButton"):
        performReplace = False
    
    if performReplace:
        clickableObj.replaceMesh(meshName + other + state)
        
    clickableObj.color = own["Color" + colorState]
    labelUpdateTextObj(cont, False)
    
    if own["WidgetType"] == "Image" and own["ImagePath"] != own["ImagePathTarget"]:
        imageAction(cont, "LoadImage")


def clickableProcess(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    mouseOver = cont.sensors.get("MouseOver", None) # type: KX_MouseFocusSensor
    lmb = cont.sensors.get("LMB", None) # type: SCA_MouseSensor
    rmb = cont.sensors.get("RMB", None) # type: SCA_MouseSensor
    
    # Used by mouse cursor
    if mouseOver.positive:
        bge.logic.__widgetHovered = own
        bge.logic.__widgetDescription = _getTextFromGroup(cont, True)
    elif bge.logic.__widgetHovered is own:
        bge.logic.__widgetHovered = None
        bge.logic.__widgetDescription = ""
    
    if own["WidgetType"] == "Checkbox":
        checkboxAction(cont, True)
    
    if not own["Enabled"]:
        clickableSetVisual(cont, "Disabled")
        
    elif mouseOver.positive and not own.isPlayingAction():
        
        if lmb and lmb.positive:
            
            if own["WidgetType"] == "Input":
                own["InputEnable"] = True
                
            clickableSetVisual(cont, "Click", button="Left")
                
        elif rmb and rmb.positive:
            clickableSetVisual(cont, "Click", button="Right")
        else:
            clickableSetVisual(cont, "Hover")
            
        if lmb and lmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
            _execCommands(cont, True)
            
            if not own["TransitionOnClick"]:
                _execCommands(cont, False)
            else:
                own["Clicked"] = True
                bge.logic.sendMessage("UpdateGui")
                
            if own["WidgetType"] == "Checkbox":
                checkboxAction(cont)
                
            elif own["WidgetType"] == "List":
                listAction(cont, "Increase")
            
        elif rmb and rmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
            _execCommands(cont, True)
            
            if not own["TransitionOnClick"]:
                _execCommands(cont, False)
            else:
                own["Clicked"] = True
                bge.logic.sendMessage("UpdateGui")
            
            if own["WidgetType"] == "List":
                listAction(cont, "Decrease")
                
    else:
        if own["WidgetType"] == "Input":
            own["InputEnable"] = False
            
        clickableSetVisual(cont, "Normal")
    if own["WidgetType"] == "Input":
        inputAction(cont, "Update")


def listUpdate(cont):
    # type: (SCA_PythonController) -> None
    
    own = cont.owner
    group = own.groupObject
    tempList = []
    tempIndex = -1
    
    if "List" in group:
        try:
            sourceList = eval(str(group["List"]))
            
            if type(sourceList) == dict:
                tempList = [key for key in sourceList.keys()]
                tempList.sort()
                
            elif hasattr(sourceList, "__iter__"):
                tempList = list(sourceList)
                
                if "Sort" in group and group["Sort"]:
                    tempList.sort()
            
            else:
                if DEBUG: print("X List", group, "source must be iterable:", group["List"])
            
            tempIndex = 0 if len(tempList) > 0 else -1
            
        except:
            if DEBUG: print("X List", group, "invalid source:", group["List"])
            
    if "Target" in group:
        tempTarget = str(group["Target"])
        
        if not tempTarget.startswith("!"):
            try:
                tempTarget = eval(tempTarget)
                own["Target"] = str(group["Target"])
                tempIndex = tempList.index(tempTarget) if tempTarget in tempList else tempIndex
            except:
                if DEBUG: print("X List", group, "invalid target:", group["Target"])
            
        else:
            tempTarget = tempTarget[1:]
            
            if tempIndex > -1:
                try:
                    exec(tempTarget + " = " + repr(tempList[tempIndex]))
                    own["Target"] = tempTarget
                except:
                    if DEBUG: print("X List", group, "invalid target:", group["Target"])
                    
            else:
                if DEBUG: print("X List", group, "no source List for Target:", group["Target"])
            
    own["List"] = tempList
    own["Index"] = tempIndex
    if DEBUG: print("> List", group, "updated:", own["List"])


# Widget actions
def checkboxAction(cont, visualOnly=False):
    # type: (SCA_PythonController, bool) -> None
    
    own = cont.owner
    group = own.groupObject
    result = None
    
    if "Target" in group:
        
        if "Value" in group:
            value = group["Value"]
            
            if type(value) == str:
                try:
                    value = eval(value)
                except:
                    pass
            
            command = group["Target"] + " = " + repr(value)
            try:
                if not visualOnly: exec(command)
                own["Checked"] = result = eval(group["Target"]) == value
            except:
                if DEBUG: print("X Could not set value to target:", repr(command))
            
        else:
            command = group["Target"] + " = not bool(" + str(group["Target"]) + ")"
            try:
                if not visualOnly: exec(command)
                own["Checked"] = result = eval(group["Target"])
            except:
                if DEBUG: print("X Could not invert target:", repr(command))
        
    else:
        if not visualOnly: own["Checked"] = result = not own["Checked"]
        
    if DEBUG and not visualOnly: print("> Checkbox", group, "set to:", result)
    clickableSetVisual(cont, "Hover")
    

def listAction(cont, event):
    # type: (SCA_PythonController, str) -> None
    
    own = cont.owner
    group = own.groupObject
    
    if event == "Init":
        listUpdate(cont)
        
    listLen = len(own["List"])
    
    if listLen > 0:
        command = own["Target"] + " = " if "Target" in own else ""
        
        if event == "Increase":
            if own["Index"] < listLen - 1:
                own["Index"] += 1
            elif own["Index"] == listLen - 1 and own["Wrap"]:
                own["Index"] = 0
            if "Target" in own: exec(command + repr(own["List"][own["Index"]]))
                
        elif event == "Decrease":
            if own["Index"] > 0:
                own["Index"] -= 1
            elif own["Index"] == 0 and own["Wrap"]:
                own["Index"] = listLen - 1
                
        if event in ("Increase", "Decrease") and "Target" in own:
            exec(command + repr(own["List"][own["Index"]]))
            
        if DEBUG: print("> List", group, "set to", own["List"][own["Index"]])
        labelUpdateTextObj(cont)


def iconButtonAction(cont, event):
    # type: (SCA_PythonController, str) -> None
    
    own = cont.owner
    group = own.groupObject
    
    # Set icon widget properties
    if event == "Init":
        iconObj = own["IconObj"] # type: KX_GameObject
        
        iconObj.localScale = list(own["IconSize"]) + [1.0]
        
        if own["ClickableObj"]:
            clickablePos = list(own["ClickableObj"].localPosition)[0:2] + [iconObj.localPosition.z]
            iconObj.localPosition = clickablePos
            
        iconObj.localPosition.x += own["IconOffset"][0]
        iconObj.localPosition.y += own["IconOffset"][1]
        iconObj.localOrientation = list(iconObj.localOrientation.to_euler())[0:2] + [radians(own["IconRotation"])]
        iconObj.color = own["IconColor"]
        
        if "Icon" in group:
            meshName = "IconButtonIcon" + str(group["Icon"])
            try:
                iconObj.replaceMesh(meshName)
            except:
                if DEBUG: print("X Icon mesh of", group, "not found:", meshName)


def inputAction(cont, event):
    # type: (SCA_PythonController, str) -> str
    
    def _validateText(cont):
        # type: (SCA_PythonController) -> None
        
        own = cont.owner
        charsAllowed = str(own["CharsAllowed"])
        curText = own["InputText"]
        validText = []
        
        # Get valid chars from constant
        if charsAllowed and charsAllowed.upper() in INPUT_VALID_CHARS.keys():
            charsAllowed = INPUT_VALID_CHARS[charsAllowed.upper()]
        
        if own["LineBreak"]:
            curText = curText.replace("\r", "\n")
            
            if charsAllowed:
                charsAllowed += "\n"
            
        # Remove invalid chars from text
        for char in curText:
            if charsAllowed:
                if char in charsAllowed:
                    validText.append(char)
            else:
                validText.append(char)
                
        lineBreak = "\n" if own["LineBreak"] else ""
        validText = "".join(validText)
        validText = validText.replace("\r", lineBreak)
                
        if own["CharsLimit"] and len(validText) > own["CharsLimit"]:
            validText = validText[:own["CharsLimit"]]
            
        own["InputText"] = validText
    
    own = cont.owner
    group = own.groupObject
    keyboard = cont.sensors.get("Keyboard", None) # type: SCA_KeyboardSensor
    target = ""
    targetValue = ""
    ensureTarget = False
    
    if "Target" in group:
            
        try:
            if str(group["Target"]).startswith(IMPORTANT_PREFIX):
                ensureTarget = True
                target = str(group["Target"])[1:]
                
            else:
                target = group["Target"]
                targetValue = eval(target)
            
        except:
            if DEBUG: print("> Input", group, "invalid target:", group["Target"])
    
    if event == "Init":
        if ensureTarget and target:
            try:
                exec(target + " = ''")
                if DEBUG: print("> Input", group, "target was created:", target)
                
            except:
                if DEBUG: print("X Input", group, "target couldn't be created:", target)
            
        own["InputText"] = str(targetValue)
        labelUpdateTextObj(cont)
        
    elif event == "Update":
        
        if not own["InputEnable"] and own["Cursor"]:
            own["Cursor"] = False
            labelUpdateTextObj(cont)
        
        elif own["InputEnable"]:
            
            if own["CursorSpeed"] > 0 and own["Timer"] > 0:
                own["Cursor"] = not own["Cursor"]
                own["Timer"] = -own["CursorSpeed"]
        
            elif own["CursorSpeed"] == 0:
                own["Cursor"] = True
                
            _validateText(cont)
        
            if keyboard.positive:
                kbEvents = bge.logic.keyboard.events
                
                if kbEvents[bge.events.LEFTCTRLKEY] == 2 or kbEvents[bge.events.RIGHTCTRLKEY] == 2:
                    
                    if kbEvents[bge.events.BACKSPACEKEY] == 1:
                        own["InputText"] = ""
                        if DEBUG: print("> Input", group, "cleared")
                    
                    elif kbEvents[bge.events.CKEY] == 1:
                        copy(str(own["InputText"]))
                        if DEBUG: print("> Input", group, "copied to clipboard:", repr(own["InputText"]))
                    
                    elif kbEvents[bge.events.VKEY] == 1:
                        value = paste()
                        if value:
                            own["InputText"] = value
                            _validateText(cont)
                            if DEBUG: print("> Input", group, "pasted from clipboard:", value)
                        else:
                            if DEBUG: print("X Input", group, ", no value in clipboard")
            
            labelUpdateTextObj(cont)
        
        if target and keyboard.positive and own["InputEnable"]:
            try:
                exec(target + " = " + repr(own["InputText"]))
                if DEBUG and keyboard.positive: print("> Input", group, "set target to:", repr(eval(target)))
            except:
                if DEBUG: print("X Input", group, "couldn't set to target:", target)


def imageAction(cont, event):
    # type: (SCA_PythonController, str) -> None
    
    def _writeImageToCache(args):
        # type: (list) -> None
        
        request = args[0] # type: Request
        own = args[1] # type: KX_GameObject
        filePath = args[2] # type: Path
        cache = args[3] # type: dict
        
        if request.data and type(request.data) == bytes:
            
            with open(filePath.as_posix(), "wb") as openedFile:
                openedFile.write(request.data)
                cache[filePath.name] = filePath
                own["ImagePathTarget"] = filePath.as_posix()
                if DEBUG: print("> Cached file written to:", filePath.as_posix())
                
        else:
            own["ImageStatus"] = "NotFound"
            own["ImagePath"] = ""
            own["ImagePathTarget"] = ""
    
    own = cont.owner
    group = own.groupObject
    global DEBUG
    
    # Set image widget properties
    if event == "Init":
        DEBUG = 1
        IMAGE_DEFAULT_PROPS = {
            "ImagePath" : "",
            "ImagePathTarget" : "",
            "ImageStatus" : "",
            "Request" : None,
        }
        for prop in IMAGE_DEFAULT_PROPS.keys():
            own[prop] = IMAGE_DEFAULT_PROPS[prop]
            if "Debug" in group and group["Debug"]: own.addDebugProperty(prop)
            
        if not "UsedMeshes" in own.scene:
            own.scene["UsedMeshes"] = {}
            
    # Get image file and ensure if it exists locally
    if "Image" in group and group["Image"]:
        imagePath = str(group["Image"])
        fileCached = curPath / (".cache/" + md5(imagePath.encode()).hexdigest())
        
        # Process image from external URL
        if imagePath.startswith(("http:", "https:", "ftp:")):
            imagePath = imagePath.replace("\\", "")
            
            # Request image from URL and enable image loading
            if own["ImageStatus"] == "" and not fileCached.stem in cache.keys():
                own["ImageStatus"] = "Loading"
                own["Request"] = Request(
                    imagePath, 
                    callback=_writeImageToCache, 
                    callbackArgs=[own, fileCached, cache]
                )
                
            # Set cached image as target image
            elif fileCached.stem in cache.keys():
                imagePath = Path(cache[fileCached.stem])
                
                if imagePath.exists():
                    own["ImageStatus"] = "Exists"
                    own["ImagePathTarget"] = imagePath.as_posix()
                else:
                    own["ImageStatus"] = "NotFound"
                    own["ImagePath"] = ""
                    own["ImagePathTarget"] = ""
                    if DEBUG: print("X Cached image do not exist:", imagePath)
            
        # Process local image
        else:
            imagePath = Path(bge.logic.expandPath("//" + imagePath))
            
            if imagePath.exists():
                own["ImagePathTarget"] = imagePath.as_posix()
                if DEBUG: print("> Relative image:", imagePath)
            else:
                own["ImagePath"] = ""
                own["ImagePathTarget"] = ""
                if DEBUG: print("X Image do not exist:", imagePath)
    
    # Load and set image to material
    if event == "LoadImage" and own["ImagePath"] != own["ImagePathTarget"]:
        
        try:
            clicakbleObj = own["ClickableObj"] # type: KX_GameObject
            matId = clicakbleObj.meshes[0].materials[0].material_index # type: int
            texture = bge.texture.Texture(clicakbleObj, matId)
            texture.source = bge.texture.ImageFFmpeg(own["ImagePathTarget"])
            clicakbleObj["TextureImageFFmpeg"] = texture
            texture.refresh(True)
            own["ImagePath"] = own["ImagePathTarget"]
            if DEBUG: print("> Load image on", group)
            
        except Exception as exception:
            if DEBUG:
                print("X Could not load image on", group)
                print("  X Exception:", exception)


def meshButtonAction(cont, event):
    # type: (SCA_PythonController, str) -> None
    
    own = cont.owner
    group = own.groupObject
    clickable = own["ClickableObj"] # type: KX_GameObject
    
    # Set mesh
    if event == "ReplaceMesh" and "Mesh" in group:
        mesh = str(group["Mesh"])
        clickable.replaceMesh(mesh, True, True)
        

# Helper functions
def _getPropsFromDb(cont):
    # type: (SCA_PythonController) -> str
    
    own = cont.owner
    group = own.groupObject if own.groupObject else []
    debugProps = True if "Debug" in group and group["Debug"] else False
    
    widgetDb = database["Gui"][own["WidgetType"]] # type: dict
    own["InlineProps"] = []
    
    for prop in widgetDb.keys():
        propValue = widgetDb[prop]
        
        if prop in group:
            propValue = group[prop]
            own["InlineProps"].append(prop)
        
        if type(propValue) == str:
            try:
                propValue = literal_eval(propValue)
            except:
                pass
                
        own[prop] = propValue
        if debugProps: own.addDebugProperty(prop)
        
    # Apply default style to current widget
    if own["WidgetType"] in database["Styles"].keys():
        
        for prop in database["Styles"][own["WidgetType"]].keys():
            if not prop in own["InlineProps"] and prop in own:
                own[prop] = database["Styles"][own["WidgetType"]][prop]
        
    # Apply custom style to current widget
    if "Style" in group:
        styleName = str(group["Style"])
        styleDb = {}
        
        if styleName in database["Styles"].keys():
            styleDb = database["Styles"][styleName]
        
        elif styleName in database["Gui"].keys():
            styleDb = database["Gui"][styleName]
        
        for prop in styleDb.keys():
            if not prop in own["InlineProps"] and prop in own:
                own[prop] = styleDb[prop]


def _getTextFromGroup(cont, description=False):
    # type: (SCA_PythonController, bool) -> str
    
    own = cont.owner
    group = own.groupObject
    curLang = lang[config["Lang"]]
    
    label = str(group["Label"]).strip() if "Label" in group else ""
    
    if label == "DESCRIPTION":
        return bge.logic.__widgetDescription
        
    else:
        try:
            # Get label from code execution
            if label.startswith(EXEC_PREFIX):
                label = eval(label[1:])
                
            # Get label from current lang strings
            elif label.startswith(LANG_PREFIX):
                    
                if not description:
                    label = curLang[label[1:]]
                
                elif description and "Label" in group:
                    label = (str(group["Label"]).strip() + "Desc")[1:]
                    label = curLang[label]
                
            # Get label from code execution
            elif label.startswith(COMPUTED_PREFIX):
                label = _getComputed(label)
                
        except:
            label = ""
        
    if not description:
        other = ""
        
        if own["WidgetType"] == "List" and "List" in own and len(own["List"]) > 0:
            other = str(own["List"][own["Index"]])
            
            if own["Translate"]:
                other = curLang.get(other, other)
                    
            other = " " + other if label else other
            
        elif own["WidgetType"] == "Input":
            label = own["InputText"] if own["InputText"] else label
                
            if own["Cursor"]:
                other += str(own["CursorCharacter"])
            
        # Process label line breaks
        lineSize = own["LineSize"]
        
        if own["WidgetType"] == "Input" and own["Cursor"]:
            lineSize += 1
            
        lineBreaks = not own["LineBreak"] if "LineBreak" in own else True
        label = wrap(str(label) + other, lineSize, replace_whitespace=lineBreaks)
        labelTemp = [i.split("\n") for i in label]
        label.clear()
        
        for l in labelTemp:
            for s in l:
                label.append(s)
        del labelTemp
        
        # Process label text align
        if own["Justify"].lower() == "center":
            label = [i.center(lineSize) for i in label]
            
            if own["WidgetType"] == "Input" and own["Cursor"]:
                for i in range(len(label)):
                    oddChars = bool(len(label[i].strip()) % 2)
                    oddLineSize = bool(lineSize % 2)
                    
                    if not oddLineSize and oddChars:
                        label[i] = " " + label[i]
                        
                    elif oddLineSize and not oddChars and label[i] and label[i][0].isspace():
                        label[i] = label[i][1:]
                        
        elif own["Justify"].lower() == "right":
            label = [i.rjust(lineSize) for i in label]
            
        label = "\n".join(label)
    
    return label


def _getCommandsFromGroup(cont):
    # type: (SCA_PythonController) -> list[str]
            
    own = cont.owner
    group = own.groupObject
    
    commands = [[], []] # Instant commands, wait commands
    
    if "Commands" in group:
        commandsTemp = group["Commands"].split(COMMAND_SEPARATOR) # type: list[str]
        
        for i in range(len(commands)):
            commandsTemp[i] = _processCommand(commandsTemp[i])
            commands = commandsTemp
            
        for command in commandsTemp:
            if str(command).strip().startswith(IMPORTANT_PREFIX):
                commands[0].append(_processCommand(command[1:]))
            else:
                commands[1].append(_processCommand(command))
            
    else:
        props = group.getPropertyNames() # type: list[str]
        props.sort()
        
        for prop in props:
            if prop.startswith("Command"):
                if str(group[prop]).strip().startswith(IMPORTANT_PREFIX):
                    commands[0].append(_processCommand(group[prop][1:]))
                else:
                    commands[1].append(_processCommand(group[prop]))
                    
    return commands


def _processCommand(command):
    # type: (str) -> str
    
    command = command.strip()
    
    if command.startswith(EXEC_PREFIX):
        return command[1:].strip()
    elif command.startswith("(") or command.startswith("["):
        return "own.scene.active_camera.worldPosition = list(" + command.strip() \
            + ") + [own.scene.active_camera.worldPosition.z]"
    else:
        command = [i.strip() for i in command.split(":")]
        resultCommand = "bge.logic.sendMessage('"
        
        if len(command):
            resultCommand += command.pop(0)
        if len(command):
            resultCommand += "', '" + ":".join(command)
            
        resultCommand += "')"
        return resultCommand


def _execCommands(cont, instant):
    # type: (SCA_PythonController, bool) -> None
    
    own = cont.owner
    group = own.groupObject
    index = 0 if instant else 1
    commands = own["Commands"][index] # type: list[str]
    
    if DEBUG and len(commands) > 0: print("> Exec commands of", group)
    
    for command in commands:
        try:
            exec(command)
            if DEBUG: print("  >", command)
        except:
            if DEBUG: print("  X", command)


def _getComputed(expression):
    # type: (str) -> object
    
    from .. import computed
    
    expression = expression.lstrip().split(":", maxsplit=1)
    args = repr(expression[1]) if len(expression) == 2 else ""
    expression = "computed." + expression[0][1:].strip() + "(" + args + ")"
    return eval(expression)
        
