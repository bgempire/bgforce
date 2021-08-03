import bge

from bge.logic import globalDict
from bge.types import *
from ast import literal_eval

from . import DEBUG
from .. import operators


__all__ = ["manager"]


config = globalDict["Config"]
db = globalDict["Database"]
state = globalDict["State"]


FADE_SPEED = 0.02
DEFAULT_PROPS_MANAGER = {
    "ContextTransition" : True,
    "Context" : ([ctx for ctx in db["Contexts"].keys() if db["Contexts"][ctx].get("Default")] + [""])[0],
    "ContextState" : "Done",
}
DEFAULT_PROPS_FADE = {
    "State" : "FadeOut",
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


def messageManager(cont):
    # type: (SCA_PythonController) -> None
    
    own = cont.owner
    message = cont.sensors["Message"] # type: KX_NetworkMessageSensor
        
    if message.positive:
        subjects = [s for s in message.subjects if s]
        bodies = [b for b in message.bodies if b]
        
        if "SetContext" in subjects:
            for context in db["Contexts"].keys():
                if context in bodies:
                    own["Context"] = context
                    own["ContextTransition"] = True
                    break


def contextManager(cont):
    # type: (SCA_PythonController) -> None
    
    own = cont.owner
    curContext = db["Contexts"].get(own["Context"]) # type: dict
    fadeObj = own["FadeObj"] # type: KX_GameObject
    fadeSpeedFactor = db["Global"]["ContextFadeSpeed"]
    
    if own["ContextTransition"] and curContext:
        alpha = round(fadeObj.color[3], 2)
        
        # Perform fade out
        if fadeObj["State"] == "FadeOut":
            
            # Increase fade alpha while transparent
            if alpha < 1:
                fadeObj.color[3] += FADE_SPEED * fadeSpeedFactor
                
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
                fadeObj.color[3] -= FADE_SPEED * fadeSpeedFactor
                
            # Add scenes on loading screen and start fade out after
            elif own["ContextState"] == "AddLoading":
                own["ContextState"] = "AddScenesAfterLoading"
                _replaceContextScenes(cont, curContext)
                fadeObj["State"] = "FadeOut"
                
            # End context transition
            else:
                fadeObj["State"] = "FadeOut"
                own["ContextTransition"] = False
        

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