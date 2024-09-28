import dearpygui.dearpygui as dpg
from abc import ABC, abstractmethod

class myWindow(ABC):
    @abstractmethod
    def criar_janela():
        pass

    def close_window(sender):
        dpg.delete_item(sender)
        
    def proc_callbalcs(self):
        jobs = dpg.get_callback_queue()
        dpg.run_callbacks(jobs)