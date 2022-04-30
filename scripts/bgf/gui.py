import bge
from bge.types import *
from . import operators as _operators_builtin
from .. import operators as _operators_custom

# Public variables accessible from widgets
from . import DEBUG, config, database, state, lang


if not hasattr(bge.logic, "_widgetHovered"):
    bge.logic._widgetHovered = None
    bge.logic._showMouseCursor = True
    bge.logic._widgetDescription = ""


def main(cont):
    # type: (SCA_PythonController) -> None
    """ Main script entrypoint. """

    own = cont.owner  # type: GuiWidget
    always = cont.sensors["Always"]  # type: SCA_AlwaysSensor

    if always.positive:

        if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:

            CLASSES = {
                "MouseCursor": GuiMouseCursor,
                "Label": GuiLabel,
                "Button": GuiButton,
                "IconButton": GuiIconButton,
                "MeshButton": GuiMeshButton,
                "Checkbox": GuiCheckbox,
                "List": GuiList,
                "Input": GuiInput,
            }

            own = CLASSES[own["WidgetType"]](own, cont)

        own.update()


class GuiBase(KX_GameObject):
    """ Base class of widgets. Initialize helper attributes, properties from database and inline properties. """

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None

        group = self.groupObject

        self.currentController = cont  # type: SCA_PythonController
        """ Current controller triggering this widget. """

        self.type = self["WidgetType"] if "WidgetType" in self else ""  # type: str
        """ WidgetType: This widget's type. """

        self.debugProps = bool(group["Debug"]) if group and "Debug" in group else False  # type: bool
        """ Debug: If print debug properties in console. """

        self.props = self._getPropsFromDb()
        """ This widget's style and behavior properties get from database and inline properties. """

        for prop in self.getPropertyNames():
            if self.debugProps:
                self.addDebugProperty(prop, True)

    def getChildByProp(self, prop):
        # type: (str) -> KX_GameObject | KX_FontObject
        """ Get child object by property. """

        for obj in self.childrenRecursive:
            if prop in obj:
                return obj

        return None

    def _getPropsFromDb(self):
        # type: () -> dict[str, object]
        """ Get control properties from database based on current control type. """

        from ast import literal_eval

        WIDGET_DB = database["Gui"][self.type]  # type: dict[str, object]
        STYLES_DB = database["Styles"]  # type: dict[str, dict[str, object]]

        group = self.groupObject
        props = {}  # type: dict[str, object]
        propsInline = []  # type: list[str]

        # Set widget properties from database
        for prop in WIDGET_DB.keys():
            propValue = WIDGET_DB[prop]

            if group and prop in group:
                propValue = group[prop]
                propsInline.append(prop)

            if type(propValue) == str:
                try:
                    propValue = literal_eval(propValue)
                except:
                    pass

            props[prop] = propValue

        # Apply default style to current widget
        if self.type in STYLES_DB.keys():

            for prop in STYLES_DB[self.type].keys():
                if not prop in propsInline and prop in props.keys():
                    props[prop] = STYLES_DB[self.type][prop]

        # Apply custom style to current widget
        if group and "Style" in group:
            style = STYLES_DB.get(str(group["Style"]), {})

            for prop in style.keys():
                if not prop in propsInline and prop in props.keys():
                    props[prop] = style[prop]

        return props


class GuiMouseCursor(GuiBase):
    """ Mouse cursor component. """

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None
        super().__init__(obj, cont)

    def update(self):
        # type: () -> None

        cont = self.currentController
        always = cont.sensors["Always"]  # type: SCA_AlwaysSensor
        mouseOver = cont.sensors["MouseOver"]  # type: KX_MouseFocusSensor
        lmb = cont.sensors["LMB"]  # type: SCA_MouseSensor
        rmb = cont.sensors["RMB"]  # type: SCA_MouseSensor

        cursorObj = self.childrenRecursive["MouseCursor"]  # type: KX_GameObject
        canvasObj = self.childrenRecursive["MouseCursorCanvas"]  # type: KX_GameObject
        curWidget = bge.logic._widgetHovered  # type: GuiClickable

        if always.positive:

            if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
                self._getPropsFromDb()
                cursorObj.localScale = list(self.props["Size"]) + [1]
                canvasObj.localScale = list(self.props["CanvasSize"]) + [1]

            if bge.logic._showMouseCursor and mouseOver.positive:
                cursorObj.visible = True
                cursorObj.worldPosition = mouseOver.hitPosition
                cursorObj.worldPosition.x += list(self.props["Offset"])[0]
                cursorObj.worldPosition.y += list(self.props["Offset"])[1]
                meshName = "MouseCursor"
                color = self.props["ColorNormal"]

                if curWidget and not curWidget.invalid:

                    if not curWidget.enabled:
                        meshName += "Disabled"
                        color = self.props["ColorDisabled"]

                    elif curWidget.type == "Input":
                        meshName += "Beam"
                        color = self.props["ColorHover"]

                    elif lmb.positive or rmb.positive:
                        meshName += "HandClick"
                        color = self.props["ColorClick"]

                    else:
                        meshName += "HandNormal"
                        color = self.props["ColorHover"]

                else:
                    if lmb.positive or rmb.positive:
                        meshName += "ArrowClick"
                        color = self.props["ColorClick"]

                    else:
                        meshName += "ArrowNormal"

                if cursorObj.meshes[0].name != meshName:
                    cursorObj.replaceMesh(meshName)
                    cursorObj.color = color

            else:
                cursorObj.visible = False


class GuiWidget(GuiBase):
    """ Base widget class. Manages widget base state and transitions. """

    ALWAYS_SKIPPED_TICKS = 5
    COMPUTED_PREFIX = "$"
    EXEC_PREFIX = ">"
    LANG_PREFIX = "#"
    OPERATOR_PREFIX = "@"
    UPDATE_GUI_ACTIONS = {
        "Input": ["ClearInputs"],
    }
    TRANSITION_ANIMS = {
        "SlideL": {"Shown": 0, "Hidden": 20},
        "SlideR": {"Shown": 30, "Hidden": 50},
        "ScaleV": {"Shown": 60, "Hidden": 80},
        "ScaleH": {"Shown": 90, "Hidden": 110},
        "Arc": {"Shown": 120, "Hidden": 140},
    }

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None

        super().__init__(obj, cont)

        group = self.groupObject

        self.transitionState = "Shown"  # type: str
        """ TransitionState: This widget's transition animation state. """

        self.enabled = self.isEnabled()
        """ Enabled: If this widget is enabled for specific colors and behaviors. """

        self.labelObject = self.getChildByProp("LABEL")  # type: KX_FontObject
        """ LabelObj: This widget's label as a text object. May be None if widget has no label. """

        self.labelShadowObject = self.getChildByProp("LABEL_SHADOW")  # type: KX_FontObject
        """ LabelShadowObj: This widget's label shadow as a text object. May be None if widget has no label. """

        self.targetLabel = ""  # type: str
        """ TargetLabel: This widget's temporary label text. Used if widget has label. """

        self.translate = bool(self.props["Translate"]) if "Translate" in self.props.keys() else False  # type: bool
        """ TargetLabel: This widget's temporary label text. Used if widget has label. """

        # Parent children of group to widget parent
        for o in group.children:
            o = o  # type: KX_GameObject
            o.setParent(self)

        # Set widget parent to group object
        self.setParent(group)

        # Show transition at start
        if self.props["Transition"] in self.TRANSITION_ANIMS.keys():
            self.transitionState = "Showing"

        self._initTransition = False

        # Show objects at start
        for o in group.groupMembers:
            if not "shadow" in o.name.lower():
                o.visible = True

        # Update widget text objects, if any
        self._updateLabelObjects()

    def update(self):
        """ Update widget. """

        cont = self.currentController
        group = self.groupObject

        # Sensors
        always = cont.sensors["Always"]  # type: SCA_AlwaysSensor
        message = cont.sensors["Message"]  # type: KX_NetworkMessageSensor

        if not group:
            print("X Widget must run as a group instance!")
            self.endObject()
            return

        if always.positive:

            # Update label if property Update is provided
            if self.isPlayingAction():
                always.skippedTicks = self.ALWAYS_SKIPPED_TICKS

            elif "Update" in group and group["Update"] >= 0:
                always.skippedTicks = group["Update"]
                self._updateLabelObjects()

            else:
                always.skippedTicks = self.props["UpdateFrequency"]

            # Start transition when GUI update is requested
            if message.positive and not self.isPlayingAction():
                bodies = [i.strip() for i in message.bodies if i.strip()]
                groups = []  # type: list[str]
                command = ""
                isAction = False

                for body in bodies:
                    if body[0] in ("[", "("):
                        command = self._processCommand(body)
                    elif body in self.UPDATE_GUI_ACTIONS.get(self.type, []):
                        isAction = True
                        break
                    else:
                        groups += [g.strip() for g in body.split(",")]

                if not isAction and (not groups or "Group" in group and str(group["Group"]).strip() in groups):
                    self.transitionState = "Hiding"

                if command:
                    self.scene["CommandCamera"] = command

            self.enabled = self.isEnabled()
            self._processTransition()

    def isEnabled(self):
        # type: () -> bool

        own = self.currentController.owner
        group = own.groupObject

        if "Enabled" in group:
            if type(group["Enabled"]) == str:
                try:
                    expression = group["Enabled"].strip()  # type: str

                    if expression.startswith(self.COMPUTED_PREFIX):
                        return bool(self._getComputed(expression))
                    else:
                        return bool(eval(expression))
                except:
                    return True
            else:
                return bool(group["Enabled"])
        else:
            return True

    def _updateLabelObjects(self, setLabel=True):
        # type: (bool) -> None

        if self.labelObject and self.labelShadowObject:

            # Set text to label and shadow
            if setLabel:
                self.targetLabel = self.labelObject.text = self.labelShadowObject.text = self._getTextFromGroup()

            # Set color and offset of label
            self.labelObject.color = self.props["LabelColor"] if self.enabled else self.props["LabelColorDisabled"]
            self.labelObject.localPosition = list(self.props["LabelOffset"]) + [self.labelObject.localPosition.z]
            self.labelObject.localScale = [self.props["LabelSize"], self.props["LabelSize"], 1.0]

            # Set visibility, color and offset of shadow
            self.labelShadowObject.visible = bool(self.props["ShadowEnable"])
            self.labelShadowObject.color = self.props["ShadowColor"] if self.enabled else self.props["ShadowColorDisabled"]
            self.labelShadowObject.localPosition = list(self.labelObject.localPosition)[0:2] \
                + [self.labelShadowObject.localPosition.z]
            self.labelShadowObject.localPosition.x += self.props["ShadowOffset"][0]
            self.labelShadowObject.localPosition.y += self.props["ShadowOffset"][1]
            self.labelShadowObject.localScale = [self.props["LabelSize"], self.props["LabelSize"], 1.0]

    def _processTransition(self):
        # type: () -> None
        """ Process widget transition animation. """

        curAnim = self.TRANSITION_ANIMS.get(self.props["Transition"])

        if self.transitionState == "Shown" and not self._initTransition:
            self._initTransition = True

        if curAnim and not self.isPlayingAction():

            # Play hide animation
            if self.transitionState == "Hiding":
                self.playAction(
                    "GuiTransitions", curAnim["Shown"],
                    curAnim["Hidden"], speed=self.props["TransitionSpeed"]
                )
                self.transitionState = "Showing"

            # Play show animation
            elif self.transitionState == "Showing":
                self.playAction(
                    "GuiTransitions", curAnim["Hidden"],
                    curAnim["Shown"], speed=self.props["TransitionSpeed"]
                )
                self.transitionState = "Shown"

                # Execute camera move command
                if "CommandCamera" in self.scene:
                    print(self.scene["CommandCamera"])
                    try:
                        exec(self.scene["CommandCamera"])
                    except Exception as e:
                        if DEBUG:
                            print(e)
                    finally:
                        del self.scene["CommandCamera"]

                self._updateLabelObjects()

    def _getTextFromGroup(self, description=False):
        # type: (bool) -> str
        from textwrap import wrap

        def _wrapText(text, justify, lineSize):
            # type: (str, str, int) -> str

            justify = justify.lower()
            text = wrap(text, lineSize)

            if justify == "left":
                return "\n".join(text)

            elif justify == "center":
                return "\n".join([i.center(lineSize) for i in text])

            elif justify == "right":
                return "\n".join([i.rjust(lineSize) for i in text])

        def _replaceNonSpacesWithChar(text, char):
            # type: (str, str) -> str

            import re
            return re.sub(r"\S", char, text)

        group = self.groupObject
        curLang = lang[config["Lang"]]

        label = str(group["Label"]).strip() if "Label" in group else ""

        if label == "DESCRIPTION":
            return _wrapText(bge.logic._widgetDescription, self.props["Justify"], self.props["LineSize"])

        else:
            try:
                # Get label from code execution
                if label.startswith(self.EXEC_PREFIX):
                    label = eval(label[1:])

                # Get label from current lang strings
                elif label.startswith(self.LANG_PREFIX):

                    if not description:
                        label = curLang[label[1:]]

                    elif description and "Label" in group:
                        label = (str(group["Label"]).strip() + "Desc")[1:]
                        label = curLang[label]

                # Get label from code execution
                elif label.startswith(self.COMPUTED_PREFIX):
                    label = self._getComputed(label)

            except Exception as e:
                label = ""

        if not description:
            other = ""

            if self.type == "List" and self.list:
                other = str(self.list[self.index])

                if self.translate:
                    other = curLang.get(other, other)

                other = " " + other if label else other

            elif self.type == "Input":
                label = self["InputText"] if self["InputText"] else label

                if self.props.get("PasswordCharacter") and self["InputText"]:
                    label = _replaceNonSpacesWithChar(label, self.props["PasswordCharacter"])

                if self.cursor:
                    other += str(self.props["CursorCharacter"])

            # Process label line breaks
            lineSize = self.props["LineSize"]

            if self.type == "Input" and self.cursor:
                lineSize += 1

            label = wrap(str(label) + other, lineSize, replace_whitespace=not self.props["LineBreak"])
            labelTemp = [i.split("\n") for i in label]
            label.clear()

            for l in labelTemp:
                for s in l:
                    label.append(s)
            del labelTemp

            # Process label text align
            if self.props["Justify"].lower() == "center":
                label = [i.center(lineSize) for i in label]

                if self.type == "Input" and self.cursor:
                    for i in range(len(label)):
                        oddChars = bool(len(label[i].strip()) % 2)
                        oddLineSize = bool(lineSize % 2)

                        if not oddLineSize and oddChars:
                            label[i] = " " + label[i]

                        elif oddLineSize and not oddChars and label[i] and label[i][0].isspace():
                            label[i] = label[i][1:]

            elif self.props["Justify"].lower() == "right":
                label = [i.rjust(lineSize) for i in label]

            label = "\n".join(label)

        return label

    @staticmethod
    def _getActionArgs(action):
        # type: (str) -> list[str]

        args = [i.strip() for i in action.split(":", maxsplit=1) if i.strip()]

        if len(args) == 1:
            args.append("")

        return args

    @staticmethod
    def _getComputed(expression):
        # type: (str) -> object

        from .. import computed

        expression = expression.lstrip().split(":", maxsplit=1)
        args = repr(expression[1]) if len(expression) == 2 else ""
        expression = "computed." + expression[0][1:].strip() + "(" + args + ")"
        return eval(expression)


class GuiLabel(GuiWidget):
    """ Label widget. """

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None
        super().__init__(obj, cont)


class GuiClickable(GuiWidget):
    """ Base clickable widget. Manages click commands and style based on mouse events. """

    COMMAND_SEPARATOR = " | "
    IMPORTANT_PREFIX = "!"

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None
        super().__init__(obj, cont)

        self.commands = self._getCommandsFromGroup()
        """ List of commands to execute on click. """

        self.clickableObject = self.getChildByProp("CLICKABLE")  # type: KX_GameObject
        """ ClickableObj: This widget's clickable object. """

        self.clicked = False
        """ Clicked: True when this widget is clicked. Becomes false after commands are executed. """

        self.clickableObject.localScale = list(self.props["Size"]) + [1.0]
        self.clickableObject.localPosition = list(self.props["Offset"]) + [self.clickableObject.localPosition.z]

    def update(self):
        # type: () -> None

        super().update()

        cont = self.currentController
        mouseOver = cont.sensors.get("MouseOver", None)  # type: KX_MouseFocusSensor
        lmb = cont.sensors.get("LMB", None)  # type: SCA_MouseSensor
        rmb = cont.sensors.get("RMB", None)  # type: SCA_MouseSensor

        self.commands = self._getCommandsFromGroup()

        # Used by mouse cursor
        if mouseOver.positive:
            bge.logic._widgetHovered = self
            bge.logic._widgetDescription = self._getTextFromGroup(description=True)

        elif bge.logic._widgetHovered is self:
            bge.logic._widgetHovered = None
            bge.logic._widgetDescription = ""

        if not self.enabled:
            self._setVisual("Disabled")

        elif mouseOver.positive and not self.isPlayingAction():

            if lmb and lmb.positive:
                self._setVisual("Click", button="Left")

            elif rmb and rmb.positive:
                self._setVisual("Click", button="Right")

            else:
                self._setVisual("Hover")

            if lmb and lmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED or rmb and rmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
                self._execCommands(self.commands[0])

                if not self.props["TransitionOnClick"]:
                    self._execCommands(self.commands[1])

                else:
                    self.clicked = True
                    bge.logic.sendMessage("UpdateGui")

        else:
            self._setVisual("Normal")

    def isHovered(self):
        # type: () -> bool
        """Returns if this widget is hovered."""

        return bge.logic._widgetHovered and bge.logic._widgetHovered is self

    def _setVisual(self, state, button=""):
        # type: (str, str) -> None

        meshName = self.type

        self.clickableObject.replaceMesh(meshName + state)

        self.clickableObject.color = self.props["Color" + state]
        self._updateLabelObjects(False)

    def _processTransition(self):
        # type: () -> None

        if not self.isPlayingAction():

            # Execute commands when widget is in the middle of transition
            if self.clicked and self.transitionState == "Showing" and self.props["TransitionOnClick"]:
                self.clicked = False
                self._execCommands(self.commands[1])

        super()._processTransition()

    def _getCommandsFromGroup(self):
        # type: () -> list[str]
        """ Get click commands from group. """

        group = self.groupObject

        commands = [[], []]  # Instant commands, wait commands

        if "Commands" in group:
            commandsTemp = str(group["Commands"]).split(self.COMMAND_SEPARATOR)  # type: list[str]

            for i in range(len(commands)):
                commandsTemp[i] = self._processCommand(commandsTemp[i])
                commands = commandsTemp

            for command in commandsTemp:
                if str(command).strip().startswith(self.IMPORTANT_PREFIX):
                    commands[0].append(self._processCommand(command[1:]))
                else:
                    commands[1].append(self._processCommand(command))

        else:
            props = group.getPropertyNames()  # type: list[str]
            props.sort()

            for prop in props:
                if prop.startswith("Command"):
                    if str(group[prop]).strip().startswith(self.IMPORTANT_PREFIX):
                        commands[0].append(self._processCommand(group[prop][1:]))
                    else:
                        commands[1].append(self._processCommand(group[prop]))

        return commands

    def _execCommands(self, commands):
        # type: (list[str]) -> None

        group = self.groupObject

        if DEBUG and len(commands) > 0:
            print("> Exec commands of", group)

        for command in commands:
            try:
                exec(command)
                if DEBUG:
                    print("  >", command)
            except Exception as e:
                if DEBUG:
                    print("  X", command, e)

    @classmethod
    def _processCommand(cls, command):
        # type: (str) -> str

        command = command.strip()

        if command.startswith(cls.EXEC_PREFIX):
            return command[1:].strip()

        elif command.startswith("(") or command.startswith("["):
            return "own.scene.active_camera.worldPosition = list(" + command.strip() \
                + ") + [own.scene.active_camera.worldPosition.z]"

        elif command.startswith(cls.OPERATOR_PREFIX):
            commandParts = command[1:].strip().split(":", 1)
            command = commandParts[0].strip()
            args = commandParts[1].strip() if len(commandParts) > 1 else ""

            modules = {
                "_operators_builtin": _operators_builtin,
                "_operators_custom": _operators_custom
            }
            operators = [command, command[0].lower() + command[1:], command[0].upper() + command[1:]]

            for mod in modules.keys():
                for op in operators:
                    if op in dir(modules[mod]):
                        resultCommand = "{}.{}(cont, {})".format(mod, op, repr(args))
                        return resultCommand
            return ""

        else:
            command = [i.strip() for i in command.split(":")]
            resultCommand = "bge.logic.sendMessage('"

            if len(command):
                resultCommand += command.pop(0)
            if len(command):
                resultCommand += "', '" + ":".join(command)

            resultCommand += "')"
            return resultCommand

    @staticmethod
    def anyHovered():
        # type: () -> bool
        """Returns if any widget is hovered."""

        return bool(bge.logic._widgetHovered)


class GuiButton(GuiClickable):
    """ Button widget. Includes a label. """

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None
        super().__init__(obj, cont)


class GuiIconButton(GuiButton):
    """ Icon button widget. Includes a label and a icon. """

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None

        from math import radians

        super().__init__(obj, cont)

        group = self.groupObject

        self.iconObject = self.getChildByProp("ICON")  # type: KX_GameObject
        """ IconObj: This widget's icon object. """

        # Initialize icon transform and color
        self.iconObject.localScale = list(self.props["IconSize"]) + [1.0]
        self.iconObject.localPosition = list(self.clickableObject.localPosition)[0:2] \
            + [self.iconObject.localPosition.z]
        self.iconObject.localPosition.x += self.props["IconOffset"][0]
        self.iconObject.localPosition.y += self.props["IconOffset"][1]
        self.iconObject.localOrientation = list(self.iconObject.localOrientation.to_euler())[0:2] \
            + [radians(self.props["IconRotation"])]
        self.iconObject.color = self.props["IconColor"]

        if self.props["Icon"] and 0 < self.props["Icon"] <= 25:
            meshName = "IconButtonIcon" + str(self.props["Icon"])

            try:
                self.iconObject.replaceMesh(meshName)
            except:
                if DEBUG:
                    print("X Icon mesh of", group, "not found:", meshName)


class GuiMeshButton(GuiButton):
    """ Mesh button widget. Includes a mesh. """

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None
        super().__init__(obj, cont)

        group = self.groupObject

        self.mesh = str(self.props["Mesh"])  # type: str
        """ Mesh: This widget's mesh to be set. """

    def _setVisual(self, state, button=""):
        # type: (str, str) -> None

        self.clickableObject.replaceMesh(self.mesh, True, True)
        self.clickableObject.color = self.props["Color" + state]


class GuiCheckbox(GuiClickable):
    """ Checkbox widget. Also can have a radio button behavior. """

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None
        super().__init__(obj, cont)

        self.checked = False  # type: bool
        """ Checked: Whether this checkbox is checked. """

    def update(self):
        # type: () -> None
        super().update()

        cont = self.currentController
        mouseOver = cont.sensors.get("MouseOver", None)  # type: KX_MouseFocusSensor
        lmb = cont.sensors["LMB"]  # type: SCA_MouseSensor

        self._checkbox(visualOnly=True)

        if mouseOver.positive and not self.isPlayingAction() and lmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
            self._checkbox()

    def _checkbox(self, visualOnly=False):
        # type: (bool) -> None

        group = self.groupObject
        result = None

        if "Target" in group:
            target = group["Target"]  # type: str

            if "Value" in group:
                value = group["Value"]  # type: str

                if type(value) == str:
                    try:
                        value = eval(value)

                    except:
                        pass

                command = target + " = " + repr(value)

                try:
                    if not visualOnly:
                        exec(command)

                    self.checked = result = eval(target) == value

                except:
                    if DEBUG:
                        print("X Could not set value to target:", repr(command))

            else:
                command = target + " = not bool(" + target + ")"

                try:
                    if not visualOnly:
                        exec(command)

                    self.checked = result = eval(group["Target"])

                except:
                    if DEBUG:
                        print("X Could not invert target:", repr(command))

        elif not visualOnly:
            self.checked = result = not self.checked

        if DEBUG and not visualOnly:
            print("> Checkbox", group, "set to:", result)

        self._setVisual("Hover")

    def _setVisual(self, state, button=""):
        # type: (str, str) -> None

        other = str(self.checked)
        other = "Radio" + other if "Value" in self.groupObject else other

        self.clickableObject.replaceMesh(self.type + other + state)
        self.clickableObject.color = self.props["Color" + state]
        self._updateLabelObjects(False)


class GuiList(GuiClickable):
    """ List widget. """

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None

        self.list = []  # type: list
        """ List: This widget's list of items. """

        self.index = 0  # type: int
        """ Index: Currently selected item in the list. """

        self.target = ""  # type: str
        """ Target: Target property this widget should modify. """

        self.arrowLeftObject = self.getChildByProp("ARROW_LEFT")  # type: KX_GameObject
        """ ArrowLeftObj: Mesh object representing the left arrow of the list. """

        self.arrowRightObject = self.getChildByProp("ARROW_RIGHT")  # type: KX_GameObject
        """ ArrowRightObj: Mesh object representing the right arrow of the list. """

        self._updateList()
        super().__init__(obj, cont)

    def update(self):
        # type: () -> None
        super().update()

        cont = self.currentController
        mouseOver = cont.sensors["MouseOver"]  # type: KX_MouseFocusSensor
        lmb = cont.sensors.get("LMB", None)  # type: SCA_MouseSensor
        rmb = cont.sensors.get("RMB", None)  # type: SCA_MouseSensor

        if mouseOver.positive and not self.isPlayingAction():

            if lmb and lmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
                self._list("Increase")

            elif rmb and rmb.status == bge.logic.KX_SENSOR_JUST_DEACTIVATED:
                self._list("Decrease")

    def _setVisual(self, state, button=""):
        # type: (str, str) -> None
        super()._setVisual(state, button)

        meshName_ = "ListArrowClick" if state == "Click" else "ListArrow"

        self.arrowLeftObject.replaceMesh(meshName_ + "Left")
        self.arrowLeftObject.color = self.props["ArrowColorClick"] if button == "Right" else self.props["ArrowColorNormal"]
        self.arrowRightObject.replaceMesh(meshName_ + "Right")
        self.arrowRightObject.color = self.props["ArrowColorClick"] if button == "Left" else self.props["ArrowColorNormal"]

    def _list(self, event):
        # type: (str) -> None

        group = self.groupObject

        listLen = len(self.list)

        if listLen > 0:
            command = self.target + " = " if self.target else ""

            if event == "Increase":

                if self.index < listLen - 1:
                    self.index += 1

                elif self.index == listLen - 1 and self.props["Wrap"]:
                    self.index = 0

                if self.target:
                    exec(command + repr(self.list[self.index]))

            elif event == "Decrease":

                if self.index > 0:
                    self.index -= 1

                elif self.index == 0 and self.props["Wrap"]:
                    self.index = listLen - 1

            if event in ("Increase", "Decrease") and self.target:
                exec(command + repr(self.list[self.index]))

            if DEBUG:
                print("> List", group, "set to", self.list[self.index])
            self._updateLabelObjects()

    def _updateList(self):
        # type: () -> None

        group = self.groupObject
        tempList = []
        tempIndex = -1

        if "List" in group:

            try:
                sourceList = eval(str(group["List"]))  # type: list | dict

                if type(sourceList) == dict:
                    tempList = [key for key in sourceList.keys()]
                    tempList.sort()

                elif hasattr(sourceList, "__iter__"):
                    tempList = list(sourceList)

                    if self.props["Sort"]:
                        tempList.sort()

                else:
                    if DEBUG:
                        print("X List", group, "source must be iterable:", group["List"])

                tempIndex = 0 if len(tempList) > 0 else -1

            except:
                if DEBUG:
                    print("X List", group, "invalid source:", group["List"])

        if "Target" in group:
            tempTarget = str(group["Target"])

            if not tempTarget.startswith("!"):

                try:
                    tempTarget = eval(tempTarget)
                    self.target = str(group["Target"])
                    tempIndex = tempList.index(tempTarget) if tempTarget in tempList else tempIndex

                except:
                    if DEBUG:
                        print("X List", group, "invalid target:", group["Target"])

            else:
                tempTarget = tempTarget[1:]

                if tempIndex > -1:

                    try:
                        exec(tempTarget + " = " + repr(tempList[tempIndex]))
                        self.target = tempTarget

                    except:
                        if DEBUG:
                            print("X List", group, "invalid target:", group["Target"])

                else:
                    if DEBUG:
                        print("X List", group, "no source List for Target:", group["Target"])

        self.list = tempList
        self.index = tempIndex
        if DEBUG:
            print("> List", group, "updated:", self.list)


class GuiInput(GuiClickable):
    """ Text input widget. """

    import string

    INPUT_VALID_CHARS = {
        "ALL": "",
        "ALPHABETIC": string.ascii_letters,
        "ALPHANUMERICNOSPACE": string.ascii_letters + string.digits,
        "ALPHANUMERIC": string.ascii_letters + string.digits + " ",
        "NUMERIC": string.digits,
        "PRINTABLE": string.printable,
    }

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None

        self.inputTarget = ""  # type: str
        """ Target: Target property this widget should modify. """

        self.cursor = False  # type: bool
        """ Cursor: Cursor blink flag. """

        super().__init__(obj, cont)

    def update(self):
        # type: () -> None
        super().update()

        cont = self.currentController
        mouseOver = cont.sensors["MouseOver"]  # type: KX_MouseFocusSensor
        lmb = cont.sensors["LMB"]  # type: SCA_MouseSensor

        if mouseOver.positive and not self.isPlayingAction():

            if lmb and lmb.positive:
                self["InputEnable"] = True

        else:
            self["InputEnable"] = False

        self._input()

    def _input(self):
        # type: () -> None

        from .thirdparty.pyp3rclip import copy, paste

        cont = self.currentController
        group = self.groupObject
        keyboard = cont.sensors["Keyboard"]  # type: SCA_KeyboardSensor

        self._ensureTarget()
        self._processActions()

        if not self["InputEnable"] and self.cursor:
            self.cursor = False
            self._updateLabelObjects()

        elif self["InputEnable"]:

            if self.props["CursorSpeed"] > 0 and self["Timer"] > 0:
                self.cursor = not self.cursor
                self["Timer"] = -self.props["CursorSpeed"]

            elif self.props["CursorSpeed"] == 0:
                self.cursor = True

            self._validateInputText()

            if keyboard.positive:
                kbEvents = bge.logic.keyboard.events  # type: dict[int, int]

                if kbEvents[bge.events.LEFTCTRLKEY] == 2 or kbEvents[bge.events.RIGHTCTRLKEY] == 2:

                    if kbEvents[bge.events.BACKSPACEKEY] == 1:
                        self["InputText"] = ""
                        if DEBUG:
                            print("> Input", group, "cleared")

                    elif kbEvents[bge.events.CKEY] == 1:
                        copy(str(self["InputText"]))
                        if DEBUG:
                            print("> Input", group, "copied to clipboard:", repr(self["InputText"]))

                    elif kbEvents[bge.events.VKEY] == 1:
                        value = paste()

                        if value:
                            self["InputText"] = value
                            self._validateInputText()
                            if DEBUG:
                                print("> Input", group, "pasted from clipboard:", value)

                        else:
                            if DEBUG:
                                print("X Input", group, ", no value in clipboard")

            self._updateLabelObjects()

        if self.inputTarget and keyboard.positive and self["InputEnable"]:

            try:
                exec(self.inputTarget + " = " + repr(self["InputText"]))
                if DEBUG and keyboard.positive:
                    print("> Input", group, "set target to:", repr(eval(self.inputTarget)))

            except:
                if DEBUG:
                    print("X Input", group, "couldn't set to target:", self.inputTarget)

    def _processActions(self):
        # type: () -> None

        cont = self.currentController
        group = self.groupObject
        message = cont.sensors["Message"]  # type: KX_NetworkMessageSensor

        if message.positive:
            bodies = [b.strip() for b in message.bodies]  # type: list[str]
            widgetGroup = str(group["Group"]) if "Group" in group else ""

            for body in bodies:
                body = self._getActionArgs(body)

                if body and body[0].startswith("ClearInput") and body[1] == widgetGroup:
                    self["InputText"] = ""
                    self._updateLabelObjects(cont)

    def _ensureTarget(self):
        # type: () -> None

        group = self.groupObject
        target = ""
        targetValue = ""
        ensureTarget = False

        # Check if target is valid
        if "Target" in group:

            try:
                if str(group["Target"]).startswith(self.IMPORTANT_PREFIX):
                    target = str(group["Target"])[1:]
                    ensureTarget = True

                else:
                    target = group["Target"]
                    targetValue = eval(target)

            except:
                if DEBUG:
                    print("> Input", group, "invalid target:", group["Target"])

        # Create target at startup if requested
        if not self.inputTarget and ensureTarget and target:

            try:
                exec(target + " = ''")
                if DEBUG:
                    print("> Input", group, "target was created:", target)

            except:
                if DEBUG:
                    print("X Input", group, "target couldn't be created:", target)

            self["InputText"] = str(targetValue)
            self.inputTarget = target
            self._updateLabelObjects()

    def _validateInputText(self):
        # type: (GuiWidget) -> None

        charsAllowed = str(self.props["CharsAllowed"])
        curText = self["InputText"]  # type: str
        validText = []

        # Get valid chars from constant
        if charsAllowed and charsAllowed.upper() in self.INPUT_VALID_CHARS.keys():
            charsAllowed = self.INPUT_VALID_CHARS[charsAllowed.upper()]

        if self.props["LineBreak"]:
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

        lineBreak = "\n" if self.props["LineBreak"] else ""
        validText = "".join(validText)
        validText = validText.replace("\r", lineBreak)

        if self.props["CharsLimit"] and len(validText) > self.props["CharsLimit"]:
            validText = validText[:self.props["CharsLimit"]]

        self["InputText"] = validText

    def _updateLabelObjects(self, setLabel=True) -> None:
        super()._updateLabelObjects(setLabel)

        if not self["InputText"]:
            self.labelObject.color = self.props["PlaceholderColor"] if self.enabled else self.props["PlaceholderColorDisabled"]
            self.labelShadowObject.color = self.props["PlaceholderShadowColor"] if self.enabled else self.props["PlaceholderShadowColorDisabled"]

    def _setVisual(self, state, button=""):
        # type: (str, str) -> None
        super()._setVisual(state, button)

        if self["InputEnable"]:
            state = "Click"

        self.clickableObject.replaceMesh(self.type + state)
        self.clickableObject.color = self.props["Color" + state]
        self._updateLabelObjects(setLabel=False)
