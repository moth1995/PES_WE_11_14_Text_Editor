from pathlib import Path
from tkinter import Listbox, messagebox, ttk
from models.binary_file import BinaryFile
from models.callname import Callname
from models.config import Config
from models.model import Model
from views.view import View
from utils import *
import yaml, os, sys

class Controller():
    def __init__(self):
        self.my_config = Config()
        self.model = Model()
        self.view = View(self)
        self.executable = BinaryFile("")
        self.database_x = BinaryFile("")
        self.default_dataset = BinaryFile("")
        self.callnames = BinaryFile("")
        self._load_settings()
        self.leagues_max_len = 61
        self.teams = []
        self.nationalities = []
        self.stadiums_list = []
        self.leagues_names_list = []
        self.callnames_list = []
        self.balls_list = []
        
        self.view.teamnames_tab.teamnames_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _: self.tn_nt_data_to_entry(
                self.view.teamnames_tab.teamnames_list_box, 
                self.view.teamnames_tab.teamnames_box,
                self.view.teamnames_tab.teamnames_abb_box,
                self.view.teamnames_tab.teamnames_id_box,
                self.teams,
            )
        )
        
        self.view.nationalities_tab.nationalities_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _: self.tn_nt_data_to_entry(
                self.view.nationalities_tab.nationalities_list_box, 
                self.view.nationalities_tab.nationalities_box,
                self.view.nationalities_tab.nationalities_abb_box,
                self.view.nationalities_tab.nationalities_id_box,
                self.nationalities,
            )
        )

        self.view.stadiums_tab.stadiums_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _: self.st_lg_data_to_entry(
                self.view.stadiums_tab.stadiums_list_box, 
                self.view.stadiums_tab.stadiums_box,
                self.view.stadiums_tab.stadiums_id_box,
                self.stadiums_list,
            )
        )

        self.view.leagues_tab.league_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _: self.st_lg_data_to_entry(
                self.view.leagues_tab.league_list_box, 
                self.view.leagues_tab.league_box,
                self.view.leagues_tab.league_id_box,
                self.leagues_names_list,
            )
        )

        self.view.callnames_tab.callnames_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _: self.callnames_data_to_entry(
                self.view.callnames_tab.callnames_list_box, 
                self.view.callnames_tab.callnames_box,
                self.view.callnames_tab.callnames_id_box,
                self.view.callnames_tab.callnames_file_id_1_box,
                self.view.callnames_tab.callnames_afs_id_1_cbox,
                self.view.callnames_tab.callnames_file_id_2_box,
                self.view.callnames_tab.callnames_afs_id_2_cbox,
                self.callnames_list,
            )
        )

        self.view.balls_tab.balls_list_box.bind(
            '<<ListboxSelect>>', 
            lambda _: self.st_lg_data_to_entry(
                self.view.balls_tab.balls_list_box, 
                self.view.balls_tab.balls_box,
                self.view.balls_tab.balls_id_box,
                self.balls_list,
            )
        )

    def _load_settings(self):
        try:
            with open(str(Path().absolute()) + "/settings.yaml") as stream:
                self.settings_file = yaml.safe_load(stream)
                self._load_config(self.my_config.filelist.index(self.settings_file.get('Last Config File Used')))
        except Exception as e:
            messagebox.showinfo(title=self.view.appname, message=f"No setting file found\nLoading first config file")
            try:
                self._load_config(0)
            except Exception as e:
                messagebox.showerror(title=self.view.appname, message=f"No config files found code error {e}")
                self.view.destroy()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def save_settings_and_close(self):
        settings_file_name = str(Path().absolute()) + "/settings.yaml"
        
        dict_file = {
            'Last Config File Used' : self.my_config.file_location,
        }

        settings_file = open(settings_file_name, "w")
        yaml.dump(dict_file, settings_file)
        settings_file.close()
        self.view.destroy()


    def _load_config(self, idx):
        self.my_config.load_config(idx)
        self.view.appname = "%s %s" % (APP_NAME, self.my_config.file["Gui"]["Game Name"])
        self.view.title(self.view.appname)
        # Game data
        self.total_stadiums = self.my_config.file["Game Data"]["Total Stadiums"]
        self.stadiums_max_len = self.my_config.file["Game Data"]["Stadium Name Lenght"]
        self.total_leagues = self.my_config.file["Game Data"]["Total Leagues"]
        self.total_teams = self.my_config.file["Game Data"]["Total Teams"]
        self.total_nationalities = self.my_config.file["Game Data"]["Total Nationalities"]
        self.total_balls = self.my_config.file["Game Data"]["Total Balls"]
        self.executable_base_address = self.my_config.file["Game Data"]["Base Address"]

        # Balls offsets
        self.balls_offsets_table = self.my_config.file["SLXX Offsets"]["Balls Offsets Table"]
        self.balls_data_offset = self.my_config.file["SLXX Offsets"]["Balls Text Data Offset"]
        self.balls_text_size = self.my_config.file["SLXX Offsets"]["Balls Text Data Size"]

        # DATABASE_X offsets

        self.names_offsets_table = self.my_config.file["DATABASE_X Offsets"]["Teams Offsets Table"]
        self.teams_names_data_offset = self.my_config.file["DATABASE_X Offsets"]["Teams Text Data Offset"]
        self.teams_names_text_size = self.my_config.file["DATABASE_X Offsets"]["Teams Text Data Size"]

        self.nationalities_offsets_table = self.my_config.file["DATABASE_X Offsets"]["Nationalities Offsets Table"]
        self.nationalities_data_offset = self.my_config.file["DATABASE_X Offsets"]["Nationalities Text Data Offset"]
        self.nationalities_text_size = self.my_config.file["DATABASE_X Offsets"]["Nationalities Text Data Size"]

        # DEFAULT_DATASET offsets
        self.stadiums_offsets_table = self.my_config.file["DEFAULT_DATASET Offsets"]["Stadiums Offsets Table 1"]
        self.stadiums_offsets_table2 = self.my_config.file["DEFAULT_DATASET Offsets"]["Stadiums Offsets Table 2"]
        self.leagues_offsets_table = self.my_config.file["DEFAULT_DATASET Offsets"]["Leagues Offsets Table 1"]
        self.leagues_offsets_table2 = self.my_config.file["DEFAULT_DATASET Offsets"]["Leagues Offsets Table 2"]

        # callname
        self.callname_len = self.my_config.file["Callnames"]["Name Lenght"]
        self.callname_encoding = self.my_config.file["Callnames"]["Encoding"]

        self.clear_view()

    def clear_view(self):
        self.view.teamnames_tab.teamnames_list_box.delete(0, "end")
        self.view.nationalities_tab.nationalities_list_box.delete(0, "end")
        self.view.stadiums_tab.stadiums_list_box.delete(0, "end")
        self.view.leagues_tab.league_list_box.delete(0, "end")
        self.view.callnames_tab.callnames_list_box.delete(0, "end")
        self.view.balls_tab.balls_list_box.delete(0, "end")
        self.view.file_menu.entryconfig(FILE_MENU_SAVE_EXECUTABLE_TEXT, state='disabled')
        self.view.file_menu.entryconfig(FILE_MENU_SAVE_DATABASE_X_TEXT, state='disabled')
        self.view.file_menu.entryconfig(FILE_MENU_SAVE_DEFAULT_DATASET_TEXT, state='disabled')
        self.view.file_menu.entryconfig(FILE_MENU_SAVE_CALLNAME_TEXT, state='disabled')

    def main(self):
        self.view.main()

    def on_open_slxx_menu_click(self):
        file_path = self.model.open_file()
        if not file_path: return

        self.executable.filename = file_path

        if not self.executable.size: return

        # loading balls into listbox
        
        self.balls_list = self.model.get_balls_names(
            self.executable.file_bytes, 
            self.balls_offsets_table, 
            self.total_balls, 
            self.executable_base_address
        )
        
        self.view.balls_tab.balls_list_box.delete(0, "end")
        self.view.balls_tab.balls_list_box.insert("end", *self.balls_list)
        self.view.file_menu.entryconfig(FILE_MENU_SAVE_EXECUTABLE_TEXT, state='normal')

    def on_open_detabase_x_menu_click(self):
        file_path = self.model.open_file()
        if not file_path: return
        self.database_x.filename = file_path

        if not (
            self.database_x.size and
            self.names_offsets_table and
            self.nationalities_offsets_table
        ): return

        self.base_address = self.model.get_base_address(self.database_x.file_bytes)
        # loading teamnames into listbox
        self.teams = self.model.get_teams(self.database_x.file_bytes, self.names_offsets_table, self.total_teams, self.base_address)
        self.view.teamnames_tab.teamnames_list_box.delete(0, "end")
        self.view.teamnames_tab.teamnames_list_box.insert("end", *[team.full_name for team in self.teams])
        
        # loading nationalities into listbox
        self.nationalities = self.model.get_nationalities(self.database_x.file_bytes, self.nationalities_offsets_table, self.total_nationalities, self.base_address)
        self.view.nationalities_tab.nationalities_list_box.delete(0, "end")
        self.view.nationalities_tab.nationalities_list_box.insert("end", *[nationality.full_name for nationality in self.nationalities])

        self.view.file_menu.entryconfig(FILE_MENU_SAVE_DATABASE_X_TEXT, state='normal')


    def on_open_default_dataset_menu_click(self):
        file_path = self.model.open_file()
        if not file_path: return

        self.default_dataset.filename = file_path

        if not self.default_dataset.size: return

        if self.stadiums_offsets_table and self.stadiums_offsets_table2:

            # loading stadiums into listbox
            
            self.stadiums_list = self.model.get_stadiums_names(self.default_dataset.file_bytes, self.stadiums_offsets_table, self.total_stadiums, self.stadiums_max_len)
            
            self.view.stadiums_tab.stadiums_list_box.delete(0, "end")
            self.view.stadiums_tab.stadiums_list_box.insert("end", *self.stadiums_list)

        if self.leagues_offsets_table and self.leagues_offsets_table2:

            # loading leagues into listbox
            
            self.leagues_names_list = self.model.get_leagues_names(self.default_dataset.file_bytes, self.leagues_offsets_table, self.total_leagues, self.leagues_max_len)
            
            self.view.leagues_tab.league_list_box.delete(0, "end")
            self.view.leagues_tab.league_list_box.insert("end", *self.leagues_names_list)
        self.view.file_menu.entryconfig(FILE_MENU_SAVE_DEFAULT_DATASET_TEXT, state='normal')

    def on_open_callname_file_menu_click(self):
        file_path = self.model.open_file()
        if not file_path: return
        self.callnames.filename = file_path

        if not (self.callnames.size and self.callname_len): return

        # loading teamnames into listbox
        self.callnames_list = self.model.get_callnames(
            self.callnames.file_bytes, 
            self.callname_len,
            self.callname_encoding,
        )
        
        self.view.callnames_tab.callnames_list_box.delete(0, "end")
        self.view.callnames_tab.callnames_list_box.insert("end", *[callname.name for callname in self.callnames_list])
        
        self.view.file_menu.entryconfig(FILE_MENU_SAVE_CALLNAME_TEXT, state='normal')


    def tn_nt_data_to_entry(self, listbox: Listbox, full_name: ttk.Entry, abb: ttk.Entry, id_entry: ttk.Entry, tn_or_nt_list:list):
        if not listbox.curselection(): return

        idx = listbox.curselection()[0]
        
        item = tn_or_nt_list[idx]
        
        full_name.delete(0,'end')
        full_name.insert(0, item.full_name)
        
        abb.delete(0,'end')
        abb.insert(0, item.abb_name)
        
        id_entry.configure(state='normal')
        id_entry.delete(0,'end')
        id_entry.insert(0, idx)
        id_entry.configure(state='readonly')

    def st_lg_data_to_entry(self, listbox: Listbox, full_name: ttk.Entry, id_entry: ttk.Entry, fullnames_list:list):
        if not listbox.curselection(): return
        idx = listbox.curselection()[0]
        
        item = fullnames_list[idx]
        
        full_name.delete(0,'end')
        full_name.insert(0, item)
                
        id_entry.configure(state='normal')
        id_entry.delete(0,'end')
        id_entry.insert(0, idx)
        id_entry.configure(state='readonly')

    def callnames_data_to_entry(
        self, 
        listbox: Listbox, 
        callnames_box: ttk.Entry, 
        id_entry: ttk.Entry, 
        file_id_1_box: ttk.Entry, 
        afs_id_1_cbox: ttk.Combobox, 
        file_id_2_box: ttk.Entry, 
        afs_id_2_cbox: ttk.Combobox, 
        callnames:"list[Callname]",
    ):
        if not listbox.curselection(): return
        idx = listbox.curselection()[0]

        callname = callnames[idx]

        id_entry.configure(state='normal')
        id_entry.delete(0,'end')

        id_entry.insert(0, callname.idx)
        id_entry.configure(state='readonly')

        callnames_box.delete(0,'end')
        callnames_box.insert(0, callname.name)

        file_id_1_box.delete(0,'end')
        file_id_1_box.insert(0, callname.file_1_id)

        afs_id_1_cbox.current(callname.afs_1_id)

        file_id_2_box.delete(0,'end')
        file_id_2_box.insert(0, callname.file_2_id)

        afs_id_2_cbox.current(callname.afs_2_id)


    def teams_apply_btn_action(self, idx: int, name:str, abb:str):
        self.teams[idx].full_name = name
        self.teams[idx].abb_name = abb
        self.view.teamnames_tab.teamnames_list_box.delete(idx,idx)
        self.view.teamnames_tab.teamnames_list_box.insert(idx, self.teams[idx].full_name)
        self.view.teamnames_tab.teamnames_list_box.select_set(idx)

    def nationality_apply_btn_action(self, idx: int, name:str, abb:str):
        self.nationalities[idx].full_name = name
        self.nationalities[idx].abb_name = abb
        self.view.nationalities_tab.nationalities_list_box.delete(idx,idx)
        self.view.nationalities_tab.nationalities_list_box.insert(idx, self.nationalities[idx].full_name)
        self.view.nationalities_tab.nationalities_list_box.select_set(idx)

    def stadiums_apply_btn_action(self, idx: int, name:str):
        if len(name)>= self.stadiums_max_len:
            messagebox.showerror(title = self.view.appname, message = f"Stadium name can be only {self.stadiums_max_len - 1} long")
            return
        self.stadiums_list[idx] = name
        self.view.stadiums_tab.stadiums_list_box.delete(idx,idx)
        self.view.stadiums_tab.stadiums_list_box.insert(idx, self.stadiums_list[idx])
        self.view.stadiums_tab.stadiums_list_box.select_set(idx)

    def leagues_apply_btn_action(self, idx: int, name:str):
        if len(name)>= self.leagues_max_len:
            messagebox.showerror(title = self.view.appname, message = f"League name can be only {self.leagues_max_len - 1} long")
            return
        self.leagues_names_list[idx] = name
        self.view.leagues_tab.league_list_box.delete(idx,idx)
        self.view.leagues_tab.league_list_box.insert(idx, self.leagues_names_list[idx])
        self.view.leagues_tab.league_list_box.select_set(idx)

    def callnames_apply_btn_action(self, idx: int, name:str, file_id_1:int, afs_id_1:int, file_id_2:int, afs_id_2:int):
        if len(name)>self.callname_len:
            messagebox.showerror(title = self.view.appname, message = f"Callname name can be only {self.callname_len -1} long")
            return
        self.callnames_list[idx].name = name
        self.callnames_list[idx].file_1_id = file_id_1
        self.callnames_list[idx].file_2_id = file_id_2
        self.callnames_list[idx].afs_1_id = afs_id_1
        self.callnames_list[idx].afs_2_id = afs_id_2

        self.view.callnames_tab.callnames_list_box.delete(idx,idx)
        self.view.callnames_tab.callnames_list_box.insert(idx, self.callnames_list[idx].name)
        self.view.callnames_tab.callnames_list_box.select_set(idx)

    def balls_apply_btn_action(self, idx: int, name:str):
        self.balls_list[idx] = name
        self.view.balls_tab.balls_list_box.delete(idx,idx)
        self.view.balls_tab.balls_list_box.insert(idx, self.balls_list[idx])
        self.view.balls_tab.balls_list_box.select_set(idx)

    def on_click_on_database_X(self):
        try:
            self.model.set_team_names(
                self.teams, 
                self.base_address, 
                self.teams_names_data_offset,
                self.names_offsets_table, 
                self.teams_names_text_size, 
                self.database_x
            )
            self.model.set_nationalities(
                self.nationalities, 
                self.base_address, 
                self.nationalities_data_offset,
                self.nationalities_offsets_table, 
                self.nationalities_text_size, 
                self.database_x
            )
            messagebox.showinfo(title = self.view.appname, message = f"All changes saved at {self.database_x.filename}")
        except Exception as e:
            messagebox.showinfo(title = self.view.appname, message = f"Error while saving, error type: {e}")

    def on_click_on_save_default_dataset(self):
        try:
            if self.stadiums_offsets_table and self.stadiums_offsets_table2:
                self.model.set_stadiums_names(self.stadiums_list, self.stadiums_offsets_table,self.stadiums_max_len, self.default_dataset)
                self.model.set_stadiums_names(self.stadiums_list, self.stadiums_offsets_table2,self.stadiums_max_len, self.default_dataset)

            if self.leagues_offsets_table and self.leagues_offsets_table2:
                self.model.set_leagues_names(self.leagues_names_list, self.leagues_offsets_table,self.leagues_max_len, self.default_dataset)
                self.model.set_leagues_names(self.leagues_names_list, self.leagues_offsets_table2,self.leagues_max_len, self.default_dataset)

            messagebox.showinfo(title = self.view.appname, message = f"All changes saved at {self.default_dataset.filename}")
        except Exception as e:
            messagebox.showinfo(title = self.view.appname, message = f"Error while saving, error type: {e}")

    def on_click_on_save_callname(self):
        try:
            self.model.set_callnames(self.callnames_list, self.callname_len, self.callnames)
            messagebox.showinfo(title = self.view.appname, message = f"All changes saved at {self.callnames.filename}")
        except Exception as e:
            messagebox.showinfo(title = self.view.appname, message = f"Error while saving, error type: {e}")
        
    def on_click_on_save_SLXX(self):
        try:
            self.model.set_balls_names(self.balls_list, self.executable_base_address, self.balls_data_offset, self.balls_offsets_table, self.balls_text_size, self.executable)
            messagebox.showinfo(title = self.view.appname, message = f"All changes saved at {self.executable.filename}")
        except Exception as e:
            messagebox.showinfo(title = self.view.appname, message = f"Error while saving, error type: {e}")

if __name__ == "__main__":
    text_editor = Controller()
    text_editor.main()
