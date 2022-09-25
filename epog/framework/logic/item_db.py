import json
import pygame

all_items_image = pygame.image.load('assets/all_images.png')
sprite_index = json.load(open('assets/all_images_index'))

item_db = {"Small Eterran Idol": "I445",
"Small Lagonian Idol": "I446",
"Humble Eterran Idol": "I447",
"Stout Lagonian Idol": "I448",
"Grand Heorot Idol": "I449",
"Grand Glass Idol": "I450",
"Grand Solar Idol": "I451",
"Grand Bone Idol": "I452",
"Grand Majasan Idol": "I453",
"Large Nomad Idol": "I454",
"Large Arcane Idol": "I455",
"Large Rahyeh Idol": "I456",
"Large Immortal Idol": "I457",
"Large Shadow Idol": "I458",
"Ornate Heorot Idol": "I459",
"Ornate Glass Idol": "I460",
"Ornate Solar Idol": "I461",
"Ornate Bone Idol": "I462",
"Ornate Majasan Idol": "I463",
"Huge Nomad Idol": "I464",
"Huge Arcane Idol": "I465",
"Huge Rahyeh Idol": "I466",
"Huge Immortal Idol": "I467",
"Huge Shadow Idol": "I468",
"Adorned Heorot Idol": "I469",
"Adorned Arcane Idol": "I470",
"Adorned Rahyeh Idol": "I471",
"Adorned Immortal Idol": "I472",
"Adorned Majasan Idol": "I473",
"Adorned Silver Idol": "I474",
"Adorned Volcano Idol": "I475"}

cached_images = {}

def get_image_from_db(name):
    try:
        return cached_images[name]
    except:
        (_, (x, y)), (_, w), (_, h) = sprite_index[item_db[name]].items()
        cached_images[name] = all_items_image.subsurface((x,y,w,h))
        return cached_images[name]