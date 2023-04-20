class Npc:
    npc_talking = False #player is talking to npc
    first_time_talking = True
    fps = 5 #animation speed
    value = 0 #to animate through npc sprites
    next_frame_time = 0 #calculate when to animate npc

class Shopkeeper:
    shop_talking = False #player is talking to shop
    purchasing = False #player is purchasing from shop
    selling = False #player is selling to shop
    fps = 5
    value = 0
    next_frame_time = 0