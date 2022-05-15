from time import sleep

def play(frame, anim):
    for modif_list in anim:
        for modif in modif_list:
            modif(frame)
        # refresh only after all the modifications
        frame.refresh()
        # sleep(0.02)
    frame.pause()

