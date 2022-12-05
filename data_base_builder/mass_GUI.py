import attr
from pathlib import Path
import platform
import PySimpleGUI as sg

@attr.s
class mass_GUI:
    """Main GUI for Data base builder'.
    Recieves from user files/folder.
    Attributes: filelist.
    Methods: get_user_input, get_filelist, run.
    """
    filelist = attr.ib(default=attr.Factory(list))

    def get_user_input(self) -> bool:
        """GUI func to get input from GUI"""
        layout = [
            [sg.Text('Select files or a folder to analyze')],
            [sg.Text('Files', size=(8, 1)) ,sg.Input(), sg.FilesBrowse(file_types=(("txt Files", "*.txt"),)) if platform.system() == 'Windows' else sg.FilesBrowse()],
            [sg.Text('OR Folder', size=(8, 1)), sg.Input(), sg.FolderBrowse()],
            [sg.OK(size=(7,1)), sg.Cancel(size=(7,1))]
        ]

        window = sg.Window('Data base builder', layout)
        event, self.values = window.Read()
        window.Close()
        return True if event == 'OK' else False
    
    def get_filelist(self) -> None:
        """Extract filelist from GUI"""
        if self.values[0]:
            self.filelist = self.values[0].split(';')
        elif self.values[1]:
            folder = Path(self.values[1])
            print ('folder found')
            print (self.values[1])
            # self.filelist = [file for file in folder.glob('*.txt')] #check here
            self.filelist = [f for f in folder.resolve().glob('**/*') if f.is_file()] #scans through a folder with all of its subfolders
            # for name in folder.glob('*.txt'):
            #     print (name)
            # self.filelist = [file for file in folder.glob('*.*')] #check here
            print (self.filelist)
        else:
            raise Exception('Folder/files not found')

    
    def run(self) -> bool:
        """Main function to run the GUI"""
        if not self.get_user_input():
            return False
        self.get_filelist()
        # self.get_ref_images()
        # self.get_screen_res()
        # self.get_fix_point()
        return True


if __name__ == "__main__":
    user_input=mass_GUI()
    assert user_input.run()
    # print(user_input.ref_images)