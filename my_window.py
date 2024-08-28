import dearpygui.dearpygui as dpg

class myWindow():
    def close_window(sender):
        dpg.delete_item(sender)