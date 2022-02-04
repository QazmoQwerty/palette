from typing import Optional, NamedTuple

class Configuration(NamedTuple):
    # TODO - more rofi customization
    opposite_align_commands_and_shortcuts: bool = True
    rofi_window_width:   int  = 85

    # NOTE - modifier icons are not recommended as they are pretty ugly at the moment.
    use_modifier_icons:  bool = False
    ctrl_modifier_icon:  str  = '\ufb33'
    shift_modifier_icon: str  = '\ufb35'
    super_modifier_icon: str  = '\ufb32'
    alt_modifier_icon:   str  = '\ufb34'
