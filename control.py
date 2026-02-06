from pywinauto import Application
import time

app = Application(backend="uia").connect(title_re=".*VMware.*")
win = app.top_window()


# print all UI elements
win.print_control_identifiers()

# win.restore()          # in case minimized
# win.set_focus()  
# try:
#     win.set_foreground()   # make top window (important)
# except:
#     pass

# time.sleep(0.5)  

# item = win.child_window(
#     title="185.83.80.32",
#     control_type="ListItem"
# ).wrapper_object()

# item.double_click_input()