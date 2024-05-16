from bus.option import __Option
from bus.signal import __FloatWindowSignal, __MainInfoSignal
from bus.update_target_window import __UpdateTargetWindow
from bus.window import __GAME_WINDOW, __TARGET_WINDOW
from control_mouse.auto_aim import AutoAim

auto_aim = AutoAim()
option = __Option()
float_window_signal = __FloatWindowSignal()
main_info_signal = __MainInfoSignal()
update_target_window = __UpdateTargetWindow()
target_window = __TARGET_WINDOW()
game_window = __GAME_WINDOW()
