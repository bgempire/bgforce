import bge
from bge.render import getWindowWidth, getWindowHeight
from .bgf import DEBUG


# Player
def player(cont):
    """ Get player position and rotation and store them. """
    
    # Objects
    own = cont.owner
    
    # Sensors
    sensor = cont.sensors[0]
    
    if sensor.positive:
        
        # Add minimap scene at start
        if sensor.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            bge.logic.addScene("ScnGameMap", 1)
        
        # Store player position and rotation
        bge.logic.playerPosition = list(own.worldPosition)
        bge.logic.playerRotation = list(own.localOrientation.to_euler())


# Minimap
def mapArrow(cont):
    
    # Objects
    own = cont.owner
    
    # Sensors
    sensor = cont.sensors[0]
    
    if sensor.positive:
        
        # Set viewport at start
        if sensor.status == bge.logic.KX_SENSOR_JUST_ACTIVATED:
            
            # Enable viewport use on map camera
            own.scene.active_camera.useViewport = True
            
            # Set viewport coordinates
            own.scene.active_camera.setViewport(
                getWindowWidth() // 2, 
                getWindowHeight() // 2, 
                getWindowWidth(),
                getWindowHeight()
            )
        
        if hasattr(bge.logic, "playerPosition") and hasattr(bge.logic, "playerRotation"):
            
            # Update arrow's position and rotation
            own.worldPosition = bge.logic.playerPosition
            own.worldPosition.z = 0.0
            own.localOrientation = bge.logic.playerRotation
    
