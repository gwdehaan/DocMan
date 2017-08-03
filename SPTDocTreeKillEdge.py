# Functie om lopende Edge processen te killen
# GdH - (3-8-2017)
# ********************************************

import psutil
def KillEdge():
    '''
    Functie om Lopende Edge processen te killen
    '''
    for proc in psutil.process_iter():
        if str(proc.name).find('Edge.exe') > 0:
            proc.kill()

KillEdge()
