import bge
import string

from bge.logic import globalDict
from bge.types import *
from ast import literal_eval
from textwrap import wrap
from math import radians

from . import DEBUG
from .thirdparty.pyp3rclip import copy, paste


__all__ = ["widget", "mouseCursor"]


ALWAYS_SKIPPED_TICKS = 10
COMMAND_SEPARATOR = " | "
IMPORTANT_PREFIX = "!"
EXEC_PREFIX = ">"
LANG_PREFIX = "#"
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

config = globalDict["Config"]
db = globalDict["Database"]
state = globalDict["State"]

if not hasattr(bge.logic, "widgetHovered"):
    bge.logic.widgetHovered = None


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
        
        # Update label if property Update is provided
        if "Update" in group and group["Update"] >= 0 and not own.isPlayingAction():
            always.skippedTicks = group["Update"]
            labelUpdateTextObj(cont)
            
        else:
            always.skippedTicks = ALWAYS_SKIPPED_TICKS
        
        # Start transition when GUI update is requested
        if message.positive and not own.isPlayingAction():
            bodies = []
            
            for body in message.bodies:
                if body:
                    for i in body.split(","):
                        bodies.append(i.strip())
                
            if not bodies or "Group" in group and str(group["Group"]).strip() in bodies:
                own["TransitionState"] = "Hiding"
            
        widgetProcessEnabled(cont)
        processTransition(cont)
        
        # Process clickable widget if applicable
        if own["ClickableObj"]:
            clickableProcess(cont)
    

def mouseCursor(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    always = cont.sensors["Always"]  # type: SCA_AlwaysSensor
    mouseOver = cont.sensors["MouseOver"] # type: KX_MouseFocusSensor
    lmb = cont.sensors.get("LMB", None) # type: SCA_MouseSensor
    rmb = cont.sensors.get("RMB", None) # type: SCA_MouseSensor
    
    cursorObj = own.childrenRecursive["MouseCursor"]
    canvasObj = own.childrenRecursive["MouseCursorCanvas"]
    curWidget = bge.logic.widgetHovered # type: KX_GameObject
    
    if not group:
        own.endObject()
        return
    
    if always.positive:
        
        if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            own.setParent(group)
            _getPropsFromDb(cont)
            cursorObj.localScale = list(own["Size"]) + [1]
            canvasObj.localScale = list(own["CanvasSize"]) + [1]
            
        if mouseOver.positive:
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
        
    if own["WidgetType"] == "Checkbox":
        checkboxAction(cont, True)
        
    elif own["WidgetType"] == "List":
        listAction(cont, "Init")
        
    elif own["WidgetType"] == "IconButton":
        iconButtonAction(cont, "Init")
        
    elif own["WidgetType"] == "Input":
        inputAction(cont, "Init")


def widgetProcessEnabled(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    group = own.groupObject
    camera = own.scene.active_camera
    
    if "Enabled" in group:
        if type(group["Enabled"]) == str:
            try:
                own["Enabled"] = bool(eval(group["Enabled"]))
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
    
    if own["TransitionState"] == "Shown" and not own["InitTransition"]:
        for objRef in OBJ_REF_PROPS.keys():
            if objRef != "LabelShadowObj" and own[objRef]:
                own[objRef].visible = True
                
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
            
            if own["ClickableObj"] and own["TransitionOnClick"] and own["Clicked"]:
                own["Clicked"] = False
                _execCommands(cont, False)
            
            # Update label while it's still hidden
            labelUpdateTextObj(cont)


def clickableSetVisual(cont, state, button=""):
    # type: (SCA_PythonController, str, str) -> None
    
    own = cont.owner
    clickableObj = own["ClickableObj"]
    other = ""
    
    if own["WidgetType"] == "Checkbox":
        other = str(own["Checked"])
        other = "Radio" + other if "Value" in own.groupObject else other
    
    elif own["WidgetType"] == "List":
        arrowLeftObj = own["ArrowLeftObj"] # type: KX_GameObject
        arrowRighttObj = own["ArrowRightObj"] # type: KX_GameObject
        meshName = "ListArrowClick" if state == "Click" else "ListArrow"
            
        arrowLeftObj.replaceMesh(meshName + "Left")
        arrowLeftObj.color = own["ArrowColorClick"] if button == "Right" else own["ArrowColorNormal"]
        arrowRighttObj.replaceMesh(meshName + "Right")
        arrowRighttObj.color = own["ArrowColorClick"] if button == "Left" else own["ArrowColorNormal"]
        
    elif own["WidgetType"] == "Input":
        if own["InputEnable"]:
            state = "Click"
    
    clickableObj.replaceMesh(own["WidgetType"] + other + state)
    clickableObj.color = own["Color" + state]
    labelUpdateTextObj(cont, False)


def clickableProcess(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    mouseOver = cont.sensors.get("MouseOver", None) # type: KX_MouseFocusSensor
    lmb = cont.sensors.get("LMB", None) # type: SCA_MouseSensor
    rmb = cont.sensors.get("RMB", None) # type: SCA_MouseSensor
    
    # Used by mouse cursor
    if mouseOver.positive:
        bge.logic.widgetHovered = own
        state["Description"] = _getTextFromGroup(cont, True)
    elif bge.logic.widgetHovered is own:
        bge.logic.widgetHovered = None
        state["Description"] = ""
    
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
            sourceList = eval(group["List"])
            
            if type(sourceList) == dict:
                tempList = [key for key in sourceList.keys()]
                tempList.sort()
                
            elif hasattr(sourceList, "__iter__"):
                tempList = list(sourceList)
                tempList.sort()
            
            else:
                if DEBUG: print("X List", group, "source must be iterable:", group["List"])
            
            tempIndex = 0 if len(tempList) > 0 else -1
            
        except:
            if DEBUG: print("X List", group, "invalid source:", group["List"])
            
    if "Target" in group:
        try:
            tempTarget = eval(group["Target"])
            own["Target"] = group["Target"]
            tempIndex = tempList.index(tempTarget) if tempTarget in tempList else tempIndex
            
        except:
            if DEBUG: print("X List", group, "invalid target:", group["Target"])
            
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


# Helper functions
def _getPropsFromDb(cont):
    # type: (SCA_PythonController) -> str
    
    own = cont.owner
    group = own.groupObject
    debugProps = True if "Debug" in group and group["Debug"] else False
    
    widgetDb = globalDict["Database"]["Gui"][own["WidgetType"]] # type: dict
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
        
    # Apply style to current widget
    if "Style" in group:
        styleName = str(group["Style"])
        styleDb = {}
        
        if styleName in globalDict["Database"]["Styles"].keys():
            styleDb = globalDict["Database"]["Styles"][styleName]
        
        elif styleName in globalDict["Database"]["Gui"].keys():
            styleDb = globalDict["Database"]["Gui"][styleName]
            
        for prop in styleDb.keys():
            if not prop in own["InlineProps"] and prop in own:
                own[prop] = styleDb[prop]


def _getTextFromGroup(cont, description=False):
    # type: (SCA_PythonController, bool) -> str
    
    own = cont.owner
    group = own.groupObject
    curLang = globalDict["Lang"][config["Lang"]]
    labelSource = "Label" if not description else "Description"
    
    label = str(group[labelSource]).strip() if labelSource in group else ""
    
    try:
        # Get label from code execution
        if label.startswith(EXEC_PREFIX):
            label = eval(label[1:])
            
        # Get label from current lang strings
        elif label.startswith(LANG_PREFIX):
            label = curLang[label[1:]]
            
    except:
        pass
        
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
    
    def processCommand(command):
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
            
    own = cont.owner
    group = own.groupObject
    
    commands = [[], []] # Instant commands, wait commands
    
    if "Commands" in group:
        commandsTemp = group["Commands"].split(COMMAND_SEPARATOR) # type: list[str]
        
        for i in range(len(commands)):
            commandsTemp[i] = processCommand(commandsTemp[i])
            commands = commandsTemp
            
        for command in commandsTemp:
            if str(command).strip().startswith(IMPORTANT_PREFIX):
                commands[0].append(processCommand(command[1:]))
            else:
                commands[1].append(processCommand(command))
            
    else:
        props = group.getPropertyNames() # type: list[str]
        props.sort()
        
        for prop in props:
            if prop.startswith("Command"):
                if str(group[prop]).strip().startswith(IMPORTANT_PREFIX):
                    commands[0].append(processCommand(group[prop][1:]))
                else:
                    commands[1].append(processCommand(group[prop]))
                    
    return commands


def _execCommands(cont, instant):
    # type: (SCA_PythonController, bool) -> None
    
    own = cont.owner
    group = own.groupObject
    config = globalDict["Config"]
    index = 0 if instant else 1
    
    if DEBUG and len(own["Commands"][index]) > 0: print("> Exec commands of", group)
    
    for command in own["Commands"][index]:
        try:
            exec(command)
            if DEBUG: print("  >", command)
        except:
            if DEBUG: print("  X", command)
