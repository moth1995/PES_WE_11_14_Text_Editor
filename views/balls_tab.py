from tkinter import ttk, Listbox
from views.custom_widget import Entry

class BallsTab(ttk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.balls_id_lbl = ttk.Label(self,text = "Ball ID: ")
        self.balls_id_box = Entry(self, width=4, state = "readonly")
        self.balls_lbl = ttk.Label(self, text = "Ball Name: ")
        self.balls_box = Entry(self, width=40)
        self.balls_apply_btn = ttk.Button(
            self, 
            text = "Apply", 
            command=lambda : self.controller.balls_apply_btn_action(
                int(self.balls_id_box.get()),
                self.balls_box.get(),
            )
        )
        self.balls_cancel_btn = ttk.Button(self, text = "Cancel", command=None)

        self.balls_list_box = Listbox(self, height = 34, width = 50, exportselection = False)
        self.balls_list_box_sb = ttk.Scrollbar(self, orient="vertical") 
        self.balls_list_box_sb.config(command = self.balls_list_box.yview)
        self.balls_list_box.config(yscrollcommand = self.balls_list_box_sb.set)

        self.balls_id_lbl.place(x = 360, y = 20)
        self.balls_id_box.place(x = 460, y = 20)
        self.balls_lbl.place(x = 360, y = 50)
        self.balls_box.place(x = 460, y = 50)
        self.balls_apply_btn.place(x = 400, y = 80)
        self.balls_cancel_btn.place(x = 480, y = 80)

        self.balls_list_box.place(x = 5, y = 20)
        self.balls_list_box_sb.place(x = 310, y = 20 , height = 550)

    @property
    def tab_name(self):
        return "Balls"

