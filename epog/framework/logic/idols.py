import parse
from dataclasses import dataclass, field
from framework.util.util import open_scraped_data
from more_itertools import flatten
from weakref import proxy

IDOLS = ['idols11', 'idols11_2', 'idols12', 'idols21', 'idols13', 'idols31', 'idols14', 'idols41', 'idols22']

IDOL_GRID = [
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0],
]

def fit_into_grid(grid, y, x, idol):
    w, h = idol.width, idol.height
    grid_slice = [line[x:x+w] for line in grid[y:y+h]]
    all_cells = list(flatten(grid_slice))
    return len(all_cells) == w * h and all(cell == 1 for cell in all_cells)

def put_on_grid(grid, y, x, idol):
    p = proxy(idol)
    for i in range(y, y + idol.height):
        for j in range(x, x + idol.width):
            grid[i][j] = p

def remove_from_grid(grid, y, x, idol):
    for i in range(y, y + idol.height):
        for j in range(x, x + idol.width):
            grid[i][j] = 1

@dataclass
class Affix:
    name: str
    form: str
    values: list
    required_level: str
    required_class: str
    rarity: str

    def relevant_to(self, item, class_name):
        return not item.is_class_specific() or class_name in self.required_class or not self.is_class_specific()

    def is_class_specific(self):
        return self.required_class != 'Any'

class Prefix(Affix):
    pass

class Suffix(Affix):
    pass

@dataclass
class Idol:
    name: str
    width: int
    height: int
    required_class: str
    required_level: int
    drop_level: int
    all_prefixes: list = field(default_factory=list)
    all_suffixes: list = field(default_factory=list)

    def is_class_specific(self):
        return self.required_class != 'Any'

def parse_all_idols() -> "list[Idol]":
    idols = []
    idol_prefixes = []
    idol_suffixes = []

    for idol in IDOLS:
        all_idols_data = open_scraped_data(f'{idol}/bases')
        for idol_data in all_idols_data:
            # parse width and height
            size = next(implicit for implicit in idol_data['implicits'] if 'Size: ' in implicit)
            width, height = size.split(' ')[1].split('\u00d7')
            # parse required_class
            class_implicit = next((implicit for implicit in idol_data['implicits'] if 'Class: ' in implicit), None)
            class_req = class_implicit.split(': ')[-1] if class_implicit else 'Any'
            # parse level
            level_implicit = next((implicit for implicit in idol_data['implicits'] if 'Level: ' in implicit), None)
            level_req = int(level_implicit.split(' ')[-1]) if level_implicit else 1
            # parse drop level
            drop_level = idol_data['level_requirement']

            parsed_idol = Idol(idol_data['item_name'], int(width), int(height), class_req, level_req, drop_level)
            idols.append(parsed_idol)
        
        prefixes = []
        idol_prefixes_data = open_scraped_data(f'{idol}/prefixes')
        for prefix_data in idol_prefixes_data:
            class_req = prefix_data['class_requirement'].split(': ')[1] if prefix_data['class_requirement'] else 'Any'
            level_req = int(prefix_data['level_requirement'].split(' ')[-1])
            rarity = parse.parse('{}({rarity})', prefix_data['rarity']).named['rarity']
            prefix = Prefix(prefix_data['affix_name'], prefix_data['affix_form'], prefix_data['affix_values'], level_req, class_req, rarity)
            prefixes.append(prefix)
        idol_prefixes.append(prefixes)
        
        suffixes = []
        idol_suffixes_data = open_scraped_data(f'{idol}/suffixes')
        for suffix_data in idol_suffixes_data:
            class_req = suffix_data['class_requirement'].split(': ')[1] if suffix_data['class_requirement'] else 'Any'
            level_req = int(suffix_data['level_requirement'].split(' ')[-1])
            rarity = parse.parse('{}({rarity})', suffix_data['rarity']).named['rarity']
            suffix = Suffix(suffix_data['affix_name'], suffix_data['affix_form'], suffix_data['affix_values'], level_req, class_req, rarity)
            suffixes.append(suffix)
        idol_suffixes.append(suffixes)
        
    return idols, idol_prefixes, idol_suffixes
    

def get_idols(class_name):
    all_idols, all_prefixes, all_suffixes = parse_all_idols()    
    relevant_idols = [idol for idol in all_idols if class_name == idol.required_class or not idol.is_class_specific()]
    
    for idol, prefix_group, suffix_group in zip(relevant_idols, all_prefixes, all_suffixes):
        idol.all_prefixes = [prefix for prefix in prefix_group if prefix.relevant_to(idol, class_name)]
        idol.all_suffixes = [suffix for suffix in suffix_group if suffix.relevant_to(idol, class_name)]
        
    return relevant_idols
    