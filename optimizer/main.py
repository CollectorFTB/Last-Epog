from dataclasses import dataclass
import itertools

def generate_items_for_slot(slot):
    for i in range(3):
        yield slot + str(i)


def optimize():
    slots = ['boots', 'staff']

    item_gens = [list(generate_items_for_slot(slot)) for slot in slots]

    for item_combo in itertools.product(*item_gens):
        print(item_combo)

optimize()
