from bus.signal import __FloatWindowSignal, __MainInfoSignal, __Option, __GameWindow, __MouseEvent, __TargetWindow
from bus.update_target_task import __UpdateTarget

update_target = __UpdateTarget()
float_window_signal = __FloatWindowSignal()
info_signal = __MainInfoSignal()
mouse_event = __MouseEvent()

target_window = __TargetWindow()
game_window = __GameWindow()
option = __Option()
