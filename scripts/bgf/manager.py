import bge
import aud
from bge.types import *
from . import DEBUG, config, database, sounds


def main(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    always = cont.sensors["Always"] # type: SCA_AlwaysSensor

    if always.positive:

        if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            own = Manager(own, cont)

        own.update()


class Manager(KX_GameObject):
    CONTEXT_FADE_SPEED = 0.02
    BGM_FADE_SPEED = 0.01
    DEFAULT_PROPS_FADE = {
        "State" : "FadeOut",
    }

    def __init__(self, obj, cont):
        # type: (KX_GameObject, SCA_PythonController) -> None

        import sys

        self.currentController = cont # type: SCA_PythonController
        """ Controller triggering manager logic. """

        self.fadeObj = self.scene.objects["FadeInOut"] # type: KX_GameObject
        """ FadeObj: Fade in and out object. """

        self.context = ([ctx for ctx in database["Contexts"].keys() \
            if database["Contexts"][ctx].get("Default")] + [""])[0] # type: str
        """ Context: Current game context. """

        self.contextTransition = True
        """ ContextTransition: True if context transition is active. """

        self.contextState = "Done" # type: str
        """ ContextState: Current context state. """

        self.bgm = "" # type: str
        """ Bgm: Current background music. """

        self.bgmTransition = True # type: bool
        """ BgmTransition: True if background music transition is active. """

        self.bgmState = "FadeOut" # type: str
        """ BgmState: Current background music transition state. """

        self.bgmHandle = None # type: aud.Handle
        """ BgmHandle: Current background music handle. """

        # Get context from command line arguments
        if sys.argv[-1] in database["Contexts"].keys():
            self.context = sys.argv[-1]

        # Init fade props
        for prop in self.DEFAULT_PROPS_FADE.keys():
            self.fadeObj[prop] = self.DEFAULT_PROPS_FADE[prop]

        # Send startup operator messages
        if database["Bgf"]["Global"].get("StartupOperators"):
            for operator in database["Bgf"]["Global"]["StartupOperators"]:
                bge.logic.sendMessage(operator)

    def update(self):
        # type: () -> None

        self.messageManager()
        self.contextManager()
        self.bgmManager()

    def messageManager(self):
        # type: () -> None

        from . import operators as operatorsDefault
        from .. import operators as operatorsCustom

        cont = self.currentController # type: SCA_PythonController
        message = cont.sensors["Message"] # type: KX_NetworkMessageSensor

        if message.positive:
            subjects = list(message.subjects) # type: list[str]
            bodies = list(message.bodies) # type: list[str]

            # Get one-line operators
            for i in range(len(subjects)):
                subject = [s.strip() for s in subjects[i].split(":", 1) if s.strip()]

                if len(subject) == 2:
                    subjects[i] = subject[0]
                    bodies[i] = subject[1]

            # Run operators
            for i in range(len(subjects)):
                subject = subjects[i][0].lower() + subjects[i][1:]
                body = bodies[i]

                # Run custom operator
                if hasattr(operatorsDefault, subject) or hasattr(operatorsCustom, subject):
                    operatorFunction = None # type: function

                    try:
                        operatorFunction = eval("operatorsDefault." + subject)
                    except:
                        try:
                            operatorFunction = eval("operatorsCustom." + subject)
                        except:
                            pass

                    if operatorFunction is not None:
                        if body:
                            operatorFunction(cont, body)
                        else:
                            operatorFunction(cont)

    def contextManager(self):
        # type: () -> None

        cont = self.currentController # type: SCA_PythonController
        curContext = database["Contexts"].get(self.context) # type: dict
        fadeSpeedFactor = database["Bgf"]["Global"]["ContextFadeSpeed"]

        if self.contextTransition and curContext:
            alpha = round(self.fadeObj.color[3], 2)

            # Perform fade out
            if self.fadeObj["State"] == "FadeOut":

                # Increase fade alpha while transparent
                if alpha < 1:
                    self.fadeObj.color[3] += self.CONTEXT_FADE_SPEED * fadeSpeedFactor

                # Exit game when requested
                elif self.contextState == "ExitGame":
                    bge.logic.endGame()

                # Remove scenes when fade is opaque
                elif self.contextState == "Done":
                    self.contextState = "RemoveScenes"
                    self._replaceContextScenes(curContext)

                # Add scenes after last scenes removed
                elif self.contextState == "RemoveScenes":

                    # Add loading scene if specified in context
                    if curContext.get("Loading"):
                        self.contextState = "AddLoading"
                        self._replaceContextScenes(curContext)
                        self.fadeObj["State"] = "FadeIn"

                    # Add context scenes of context
                    else:
                        self.contextState = "AddScenes"
                        self._replaceContextScenes(curContext)
                        self.contextState = "Done"
                        self.fadeObj["State"] = "FadeIn"

                # Remove loading scene and go to fade in
                elif self.contextState == "AddScenesAfterLoading":
                    self.contextState = "RemoveLoading"
                    self._replaceContextScenes(curContext)
                    self.fadeObj["State"] = "FadeIn"
                    self.contextState = "Done"

            # Perform fade in
            elif self.fadeObj["State"] == "FadeIn":

                # Decrease fade alpha while opaque
                if alpha > 0:
                    self.fadeObj.color[3] -= self.CONTEXT_FADE_SPEED * fadeSpeedFactor

                # Add scenes on loading screen and start fade out after
                elif self.contextState == "AddLoading":
                    self.contextState = "AddScenesAfterLoading"
                    self._replaceContextScenes(curContext)
                    self.fadeObj["State"] = "FadeOut"

                # End context transition
                else:
                    self.fadeObj["State"] = "FadeOut"
                    self.contextTransition = False

    def bgmManager(self):
        # type: () -> None

        curContext = database["Contexts"].get(self.context) # type: dict
        bgmDb = sounds["Bgm"] # type: dict
        handle = self.bgmHandle # type: aud.Handle
        bgmFadeFactor = self.BGM_FADE_SPEED * config["BgmVol"] \
            * database["Bgf"]["Global"]["BgmFadeSpeed"] # type: float
        curBgm = ""

        if curContext:
            curBgm = curContext.get("Bgm", self.bgm)

            if curBgm and curBgm != self.bgm:
                self.bgm = curBgm
                self.bgmTransition = True

            if self.bgmTransition:

                if self.bgmState == "FadeOut":

                    if handle:

                        if round(handle.volume, 1) > 0:
                            handle.volume -= bgmFadeFactor

                        else:
                            handle.stop()
                            self.bgmHandle = handle = None

                    elif curBgm in bgmDb.keys():
                        factory = aud.Factory.file(bgmDb[curBgm])
                        self.bgmHandle = handle = aud.device().play(factory, keep=True)
                        handle.volume = 0
                        handle.loop_count = -1
                        self.bgmState = "FadeIn"

                    else:
                        self.bgmTransition = False

                elif self.bgmState == "FadeIn":

                    if handle:

                        if round(handle.volume, 1) < config["BgmVol"]:
                            handle.volume += bgmFadeFactor

                        else:
                            handle.volume = round(handle.volume, 2)
                            self.bgmState = "FadeOut"
                            self.bgmTransition = False

                    else:
                        self.bgmState = "FadeOut"
                        self.bgmTransition = False

            elif not self.bgmTransition and handle:
                handle.volume = config["BgmVol"]

    def _replaceContextScenes(self, context):
        # type: (dict) -> None

        cont = self.currentController # type: SCA_PythonController
        scenes = bge.logic.getSceneList()

        # Remove scenes from last context
        if self.contextState == "RemoveScenes":
            if DEBUG: print("> Remove scenes from context:")
            for scn in scenes:
                if scn.name != self.scene.name and not scn.name in context.keys():
                    if DEBUG: print("  > Removed scene:", scn.name)
                    scn.end()

        # Add scenes of current context
        elif self.contextState in ("AddScenes", "AddScenesAfterLoading"):
            if DEBUG: print("> Add scenes of context:")
            for scn in context["Scenes"]:
                bge.logic.addScene(scn["Name"], 0)
                if DEBUG: print("  > Added scene:", scn["Name"])

        # Add loading scene
        elif self.contextState == "AddLoading":
            if DEBUG: print("> Add loading scene:", context["Loading"])
            bge.logic.addScene(context["Loading"], 0)

        # Remove loading scene
        elif self.contextState == "RemoveLoading":
            if DEBUG: print("> Remove loading scene:", context["Loading"])
            for scn in scenes:
                if scn.name == context["Loading"]:
                    scn.end()
                    break
