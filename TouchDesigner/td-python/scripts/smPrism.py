import json
import os
from dataclasses import dataclass


def Convert(value: str):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))


@dataclass
class palette:
    name: str
    uuid: str
    colors: list[TDU.Color]

    @staticmethod
    def from_dict(info: dict):
        name_from_info: str = info.get('name', 'no name')
        uuid_from_info: str = info.get('uuid')
        colors_from_info: list[str] = info.get('colors')
        converted_from_hex = []

        for each in colors_from_info:
            converted = Convert(each)
            new_color = TDU.Color(
                converted[0]/255, converted[1]/255, converted[2]/255, 1)
            converted_from_hex.append(new_color)

        return palette(name=name_from_info, uuid=uuid_from_info, colors=converted_from_hex)


class prism:

    def __init__(self, ownerOp: OP):
        self.owner = ownerOp
        self.Palettes: dict = {}
        self.palette_file = ownerOp.par.Prismpalettefile

        self.Num_palettes = tdu.Dependency(0)

        self._start_up()
        self.Empty_palette = palette(
            name='empty', uuid='xxxx', colors=[TDU.Color()])

        print('prism init')

    def _start_up(self) -> None:
        self.Load_palettes()

    @property
    def expanded_palette_file(self) -> str:
        prism_palette_file = tdu.expandPath(self.palette_file)
        return prism_palette_file

    def _load_palettes_from_file(self) -> None:

        print(self.expanded_palette_file)
        with open(self.expanded_palette_file, 'r', encoding='utf-8') as paletteFile:
            palettes = {}
            palette_json = json.load(paletteFile)

            for each_key, each_val in palette_json.items():
                new_palette = palette.from_dict(each_val)
                palettes[each_key] = new_palette

            self.Num_palettes.val = len(palettes.keys())

            self.Palettes = palettes
            self._build_menu_par()

    def _build_menu_par(self) -> None:
        menu_names: list = []
        menu_labels: list = []
        for each_key, each_val in self.Palettes.items():
            menu_labels.append(each_val.name)
            menu_names.append(each_key)

        self.owner.par.Palettes.menuLabels = menu_labels
        self.owner.par.Palettes.menuNames = menu_names

    def Load_palettes(self) -> None:
        if self.expanded_palette_file != '':
            # ensure parameter isn't empty

            if os.path.isfile(self.expanded_palette_file):
                # ensure par is a valid file
                print(f'loading from file {self.expanded_palette_file}')
                self._load_palettes_from_file()
        else:
            self._build_menu_par()
