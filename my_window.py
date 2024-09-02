import dearpygui.dearpygui as dpg

class myWindow():
    def close_window(sender):
        dpg.delete_item(sender)

    def proc_callbalcs(self):
        jobs = dpg.get_callback_queue
        dpg.run_callbacks(jobs)