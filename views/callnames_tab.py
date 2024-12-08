from tkinter import ttk, Listbox
from views.custom_widget import Entry

class CallnamesTab(ttk.Frame):
    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.callnames_id_lbl = ttk.Label(self,text = "Callname ID: ")
        self.callnames_id_box = Entry(self, width=4, state = "readonly")
        self.callnames_lbl = ttk.Label(self, text = "Name: ")
        self.callnames_box = Entry(self, width=40)
        self.callnames_file_id_1_lbl = ttk.Label(self, text = "File ID 1: ")
        self.callnames_file_id_1_box = Entry(self, width=6)
        self.callnames_afs_id_1_lbl = ttk.Label(self, text = "AFS ID 1: ")
        self.callnames_afs_id_1_cbox = ttk.Combobox(
            self, 
            width=12, 
            values=[
                "0_SOUND.AFS",
                "0_TEXT.AFS",
                "X_SOUND.AFS",
                "X_TEXT.AFS",
                "OVER.AFS",
            ],
            state="readonly",
        )

        self.callnames_file_id_2_lbl = ttk.Label(self, text = "File ID 2: ")
        self.callnames_file_id_2_box = Entry(self, width=6)
        self.callnames_afs_id_2_lbl = ttk.Label(self, text = "AFS ID 2: ")
        self.callnames_afs_id_2_cbox = ttk.Combobox(
            self, 
            width=12, 
            values=[
                "0_SOUND.AFS",
                "0_TEXT.AFS",
                "X_SOUND.AFS",
                "X_TEXT.AFS",
                "OVER.AFS",
            ],
            state="readonly",
        )
        self.callnames_apply_btn = ttk.Button(
            self, 
            text = "Apply", 
            command=lambda : self.controller.callnames_apply_btn_action(
                int(self.callnames_id_box.get()),
                self.callnames_box.get(),
                int(self.callnames_file_id_1_box.get()),
                self.callnames_afs_id_1_cbox.current(),
                int(self.callnames_file_id_2_box.get()),
                self.callnames_afs_id_2_cbox.current(),
            )
        )
        self.callnames_cancel_btn = ttk.Button(self, text = "Cancel",)

        self.callnames_list_box = Listbox(self, height = 34, width = 50, exportselection = False)
        self.callnames_list_box_sb = ttk.Scrollbar(self, orient="vertical") 
        self.callnames_list_box_sb.config(command = self.callnames_list_box.yview)
        self.callnames_list_box.config(yscrollcommand = self.callnames_list_box_sb.set)

        self.callnames_id_lbl.place(x = 360, y = 20)
        self.callnames_id_box.place(x = 440, y = 20)
        self.callnames_lbl.place(x = 360, y = 50)
        self.callnames_box.place(x = 440, y = 50)
        self.callnames_file_id_1_lbl.place(x = 370, y = 80)
        self.callnames_afs_id_1_lbl.place(x = 440, y = 80)
        self.callnames_file_id_1_box.place(x = 370, y = 110)
        self.callnames_afs_id_1_cbox.place(x = 440, y = 110)
        self.callnames_file_id_2_lbl.place(x = 370, y = 140)
        self.callnames_afs_id_2_lbl.place(x = 440, y = 140)
        self.callnames_file_id_2_box.place(x = 370, y = 170)
        self.callnames_afs_id_2_cbox.place(x = 440, y = 170)


        self.callnames_apply_btn.place(x = 400, y = 210)
        self.callnames_cancel_btn.place(x = 480, y = 210)

        self.callnames_list_box.place(x = 5, y = 20)
        self.callnames_list_box_sb.place(x = 310, y = 20, height = 550)

    @property
    def tab_name(self):
        return "Callnames"

