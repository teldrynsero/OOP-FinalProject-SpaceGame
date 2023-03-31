class Npc:
    npc_talking = False #npc starts out not talking
    first_time_talking = True
    fps = 5 #animation speed
    value = 0 #to animate through npc sprites
    next_frame_time = 0 #calculate when to animate npc