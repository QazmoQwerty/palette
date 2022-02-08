from typing import Dict

import strictyaml
from strictyaml import Map, Str, Int, Seq, Optional, Bool, YAML, EmptyList

g_configuration_singleton = None

def get_configuration() -> YAML:
    assert g_configuration_singleton is not None
    return g_configuration_singleton

def set_configuration_singleton(value: YAML) -> None:
    global g_configuration_singleton
    g_configuration_singleton = value

class ConfigurationFactory:
    _path: str

    def __init__(self, path: str) -> None:
        self._path = path

        def subcategory(name: str, inner_schema: Dict[Optional, str]) -> dict:
            defaults = {i.key: i.default for i in inner_schema.keys()}
            return { Optional(name, default = defaults): Map(inner_schema)}

        self._schema = Map({
            **subcategory('rofi', {
                Optional('opposite_align_commands_and_shortcuts', default = False): Bool(),
                Optional('window_width', default = 91): Int(),
                Optional('additional_arguments', default = []): EmptyList() | Seq(Str()),
                **subcategory('mode_script', {
                    Optional('input_path', default = "/tmp/palette_rofi_script_input"): Str(),
                }),
                **subcategory('modifier_icons', {
                    Optional('is_active', default = False): Bool(),
                    Optional('ctrl',  default = "\ufb33"): Str(),
                    Optional('shift', default = "\ufb35"): Str(),
                    Optional('super', default = "\ufb32"): Str(),
                    Optional('alt',   default = "\ufb34"): Str(),
                }),
            }),
            "commands": Seq(Map({
                'description': Str(),
                'exec': Str(),
                Optional('keybinding'): Str(),
                Optional('meta'): Str(),
            }))
        })

    def create(self) -> YAML:
        with open(self._path) as file:
            return strictyaml.load(file.read(), schema=self._schema)
