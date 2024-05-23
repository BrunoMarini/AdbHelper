import customtkinter
import os
from CTkTable import *
from DbHelper import DbHelper
from CmdHelper import AdbCommandHelper
from windows_toasts import Toast, WindowsToaster

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

adb = AdbCommandHelper()
db_helper = DbHelper()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure Window
        self.title("ADB Helper")
        self.geometry("1100x500")

        # Configure Grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create Sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, padx=10, pady=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="ADB Helper", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=0, column=1, rowspan=4, padx=10, pady=10, sticky="nsew")

        self.tabview.add("Android Database")
        self.tabview.tab("Android Database").grid_columnconfigure(0, weight=1)
        tab_db = self.tabview.tab("Android Database")
        label = customtkinter.CTkLabel(tab_db, text="Select Database:")
        label.grid(row=0, column=0, pady=10)
        self.drop_down_dbs = customtkinter.CTkOptionMenu(tab_db, values=adb.listAvailableDB(), command=self.load_db_callback)
        self.drop_down_dbs.grid(row=0, column=1, pady=10)

        self.tabview.add("Logcat")
        self.tabview.tab("Logcat").grid_columnconfigure(0, weight=1)
        tab_logcat = self.tabview.tab("Logcat")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=tab_logcat, text="-")
        self.checkbox_1.grid(row=1, column=0, columnspan=2, pady=(20, 0), padx=20, sticky="we")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=tab_logcat)
        self.checkbox_2.grid(row=2, column=0, columnspan=2, pady=(20, 0), padx=20, sticky="we")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=tab_logcat)
        self.checkbox_3.grid(row=3, column=0, columnspan=2, pady=(20, 0), padx=20, sticky="we")

        customtkinter.CTkButton(master=tab_logcat, text="Clear logcat bufffer\n(logcat -c)").grid(row=1, column=2, columnspan=2, sticky="nsew")

        customtkinter.CTkLabel(master=tab_logcat, text="grep").grid(row=2, column=2, columnspan=2, sticky="nsew")
        customtkinter.CTkEntry(master=tab_logcat).grid(row=3, column=2, columnspan=2, sticky="nsew")

        # customtkinter.CTkEntry(master=tab_logcat, state="disabled").grid(row=4, column=0, rowspan=3, sticky="nsew")
        # customtkinter.CTkButton(master=tab_logcat, text="RUN").grid(row=4, column=4, padx=10, sticky="nsew")

        #self.tabview.add("Pull / Push")
        #self.tabview.tab("Logcat").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        #self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
        #                                                values=["Value 1", "Value 2", "Value Long Long Long"])
        #self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        #self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("CTkTabview"),
        #                                            values=["Value 1", "Value 2", "Value Long....."])
        #self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        #self.string_input_button = customtkinter.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
        #                                                   command=self.open_input_dialog_event)
        #self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        #self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        #self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)




        self.load_connected_devices()


    def load_db_callback(self, choice):
        global adb
        global db_helper

        db_path = adb.loadDb(choice)
        db_helper.load_db(db_path)

        self.drop_down_dbs = customtkinter.CTkOptionMenu(self.tabview.tab("Android Database"),
                                                         values=db_helper.listTables(), command=self.load_db_table)
        self.drop_down_dbs.grid(row=0, column=2, pady=10, padx=10, sticky="nsew")

    def load_db_table(self, choice):
        global db_helper
        table = db_helper.query_table(choice)
        print(table)
        columns = len(table[0])
        rows = len(table)

        self.db_table = CTkTable(master=self.tabview.tab("Android Database"), row=rows, column=columns,
                                 header_color="blue", command=self.handle_table_row_pressed, values=table)
        self.db_table.grid(row=1, column=0, columnspan=4)

    def handle_table_row_pressed(self, pressed):
        os.system(f"echo {pressed['value']} | clip")
        new_toast = Toast()
        new_toast.text_fields = ["Copied to clipboard!"]
        new_toast.on_activated = lambda _: print('Toast clicked!')
        WindowsToaster('Python').show_toast(new_toast)

    def change_appearance_mode_event(self, new_mode: str):
        customtkinter.set_appearance_mode(new_mode)

    def load_connected_devices(self):
        global adb
        devices = adb.listDevices()

        for i, device in enumerate(devices):
            (customtkinter.CTkRadioButton(self.sidebar_frame, text=f"{i+1}. {device[0]}", value=device[0])
             .grid(row=i+1, column=0, padx=20, pady=10))

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())


if __name__ == "__main__":
    app = App()
    app.mainloop()