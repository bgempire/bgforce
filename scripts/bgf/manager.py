import bge
import aud

from bge.logic import globalDict
from bge.types import *
from ast import literal_eval

from . import DEBUG, config, database, state, sounds
from .. import operators


__all__ = ["manager"]


CONTEXT_FADE_SPEED = 0.02
BGM_FADE_SPEED = 0.01
DEFAULT_PROPS_MANAGER = {
    "ContextTransition" : True,
    "Context" : ([ctx for ctx in database["Contexts"].keys() if database["Contexts"][ctx].get("Default")] + [""])[0],
    "ContextState" : "Done",
}
DEFAULT_PROPS_FADE = {
    "State" : "FadeOut",
}
DEFAULT_PROPS_BGM = {
    "BgmTransition" : True,
    "Bgm" : "",
    "BgmState" : "FadeOut",
    "BgmHandle" : None,
}

# Controller endpoint
def manager(cont):
    # type: (SCA_PythonController) -> None

    own = cont.owner
    
    # Sensors
    always = cont.sensors["Always"] # type: SCA_AlwaysSensor

    if always.positive:
        
        if always.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            managerInit(cont)
            
        messageManager(cont)
        contextManager(cont)
        bgmManager(cont)


# Abstraction functions
def managerInit(cont):
    # type: (SCA_PythonController) -> None
    
    own = cont.owner
    own["FadeObj"] = fadeInOut = own.scene.objects.get("FadeInOut", own)
    
    # Init manager props
    for prop in DEFAULT_PROPS_MANAGER.keys():
        own[prop] = DEFAULT_PROPS_MANAGER[prop]
        if DEBUG: own.addDebugProperty(prop)
    
    # Init fade props
    for prop in DEFAULT_PROPS_FADE.keys():
        fadeInOut[prop] = DEFAULT_PROPS_FADE[prop]
        if DEBUG: fadeInOut.addDebugProperty(prop)
    
    # Init BGM props
    for prop in DEFAULT_PROPS_BGM.keys():
        own[prop] = DEFAULT_PROPS_BGM[prop]
        if DEBUG: own.addDebugProperty(prop)


def messageManager(cont):
    # type: (SCA_PythonController) -> None
    
    own = cont.owner
    message = cont.sensors["Message"] # type: KX_NetworkMessageSensor
        
    if message.positive:
        subjects = [s for s in message.subjects if s]
        bodies = [b for b in message.bodies if b]
        
        if "SetContext" in subjects:
            for context in database["Contexts"].keys():
                if context in bodies:
                    own["Context"] = context
                    own["ContextTransition"] = True
                    break
        
        if "ExitGame" in subjects:
            own["ContextState"] = "ExitGame"
            own["ContextTransition"] = True


def contextManager(cont):
    # type: (SCA_PythonController) -> None
    
    own = cont.owner
    curContext = database["Contexts"].get(own["Context"]) # type: dict
    fadeObj = own["FadeObj"] # type: KX_GameObject
    fadeSpeedFactor = database["Global"]["ContextFadeSpeed"]
    
    if own["ContextTransition"] and curContext:
        alpha = round(fadeObj.color[3], 2)
        
        # Perform fade out
        if fadeObj["State"] == "FadeOut":
            
            # Increase fade alpha while transparent
            if alpha < 1:
                fadeObj.color[3] += CONTEXT_FADE_SPEED * fadeSpeedFactor
                
            # Exit game when requested
            elif own["ContextState"] == "ExitGame":
                bge.logic.endGame()
                
            # Remove scenes when fade is opaque
            elif own["ContextState"] == "Done":
                own["ContextState"] = "RemoveScenes"
                _replaceContextScenes(cont, curContext)
                
            # Add scenes after last scenes removed
            elif own["ContextState"] == "RemoveScenes":
                
                # Add loading scene if specified in context
                if curContext.get("Loading"):
                    own["ContextState"] = "AddLoading"
                    _replaceContextScenes(cont, curContext)
                    fadeObj["State"] = "FadeIn"
                    
                # Add context scenes of context
                else:
                    own["ContextState"] = "AddScenes"
                    _replaceContextScenes(cont, curContext)
                    own["ContextState"] = "Done"
                    fadeObj["State"] = "FadeIn"
                
            # Remove loading scene and go to fade in
            elif own["ContextState"] == "AddScenesAfterLoading":
                own["ContextState"] = "RemoveLoading"
                _replaceContextScenes(cont, curContext)
                fadeObj["State"] = "FadeIn"
                own["ContextState"] = "Done"
        
        # Perform fade in
        elif fadeObj["State"] == "FadeIn":
            
            # Decrease fade alpha while opaque
            if alpha > 0:
                fadeObj.color[3] -= CONTEXT_FADE_SPEED * fadeSpeedFactor
                
            # Add scenes on loading screen and start fade out after
            elif own["ContextState"] == "AddLoading":
                own["ContextState"] = "AddScenesAfterLoading"
                _replaceContextScenes(cont, curContext)
                fadeObj["State"] = "FadeOut"
                
            # End context transition
            else:
                fadeObj["State"] = "FadeOut"
                own["ContextTransition"] = False


def bgmManager(cont):
    # type: (SCA_PythonController) -> None
    
    own = cont.owner
    curContext = database["Contexts"].get(own["Context"]) # type: dict
    bgmDb = sounds["Bgm"] # type: dict
    handle = own["BgmHandle"] # type: aud.Handle
    bgmFadeFactor = BGM_FADE_SPEED * config["VolBgm"] * database["Global"]["BgmFadeSpeed"]
    curBgm = ""
    
    if curContext:
        curBgm = curContext.get("Bgm", "")
        
        if own["Bgm"] != curBgm:
            own["Bgm"] = curBgm
            own["BgmTransition"] = True
        
        if own["BgmTransition"]:
            
            if own["BgmState"] == "FadeOut":
                
                if handle:
                    
                    if round(handle.volume, 1) > 0:
                        handle.volume -= bgmFadeFactor
                        
                    else:
                        handle.stop()
                        own["BgmHandle"] = handle = None
                        
                elif curBgm in bgmDb.keys():
                    factory = aud.Factory.file(bgmDb[curBgm])
                    own["BgmHandle"] = handle = aud.device().play(factory, keep=True)
                    handle.volume = 0
                    handle.loop_count = -1
                    own["BgmState"] = "FadeIn"
                    
                else:
                    own["BgmTransition"] = False
                
            elif own["BgmState"] == "FadeIn":
                
                if handle:
                    
                    if round(handle.volume, 1) < config["VolBgm"]:
                        handle.volume += bgmFadeFactor
                        
                    else:
                        handle.volume = round(handle.volume, 2)
                        own["BgmState"] = "FadeOut"
                        own["BgmTransition"] = False
                        
                else:
                    own["BgmState"] = "FadeOut"
                    own["BgmTransition"] = False


# Helper functions
def _replaceContextScenes(cont, context):
    # type: (SCA_PythonController, dict) -> None
    
    own = cont.owner
    scenes = bge.logic.getSceneList()
    
    # Remove scenes from last context
    if own["ContextState"] == "RemoveScenes":
        if DEBUG: print("> Remove scenes from context:")
        for scn in scenes:
            if scn.name != own.scene.name and not scn.name in context.keys():
                if DEBUG: print("  > Removed scene:", scn.name)
                scn.end()
    
    # Add scenes of current context
    elif own["ContextState"] in ("AddScenes", "AddScenesAfterLoading"):
        if DEBUG: print("> Add scenes of context:")
        for scn in context["Scenes"]:
            bge.logic.addScene(scn["Name"], 0)
            if DEBUG: print("  > Added scene:", scn["Name"])
    
    # Add loading scene
    elif own["ContextState"] == "AddLoading":
        if DEBUG: print("> Add loading scene:", context["Loading"])
        bge.logic.addScene(context["Loading"], 0)
    
    # Remove loading scene
    elif own["ContextState"] == "RemoveLoading":
        if DEBUG: print("> Remove loading scene:", context["Loading"])
        for scn in scenes:
            if scn.name == context["Loading"]:
                scn.end()
                break