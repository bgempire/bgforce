import bge

EXEC_PREFIX = ">"
LOCALE_PREFIX = "#"

TRANSITION_ANIMS = {
    "SlideLeft": [0, 20],
    "SlideRight": [30, 50],
    "FallBack": [60, 80],
    "BendBack": [90, 110],
    "BendArc": [120, 140],
}


def getLabelFromGroup(group):
    # type: (bge.types.KX_GameObject) -> str

    from bge.logic import globalDict

    if "Label" in group:
        if str(group["Label"]).startswith(EXEC_PREFIX):
            try:
                return str(eval(group["Label"][1:]))
            except:
                return str(group["Label"])
        elif str(group["Label"]).startswith(LOCALE_PREFIX):
            try:
                return globalDict["Locale"][globalDict["Config"]["Lang"]][group["Label"][1:]]
            except:
                return str(group["Label"])
        else:
            return str(group["Label"])

    else:
        return ""
