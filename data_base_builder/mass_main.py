from mass_GUI import *
from process_mass_gui import *
from read_mass_data import *


@attr.s
class MassData:
    """Mass data base builder tool.
    Attributes: user_input, massdict, df_list, b_data.
    Methods:
    method input() prompts for user input.
    method read_data() creates raw data objects for each file.
    method data() converts data of each trail to a pd.Dataframe.
    method big_data() creates one big pd.DataFrame from all data frames of a given experiment.
    method run() is the main function for this process.
    """
    user_input = attr.ib(default=mass_GUI)
    massdict = attr.ib(default=attr.Factory(dict))
    df_list = attr.ib(default=attr.Factory(list))
    invalid_files = attr.ib(default=attr.Factory(list)) #new
    missing_data = attr.ib(default=attr.Factory(list)) #new
    # b_data = attr.ib(default=AllId)
    
        
    def input(self) -> bool:
        """prompts for user input"""
        user_input = mass_GUI()
        assert_input = user_input.run()
        if not assert_input:
            return False
        self.user_input = user_input
        return True
    
    def raw_data(self) -> None:
        """creates raw data objects for each file"""
        filelist = ProcessFilelist(self.user_input.filelist)
        filelist.get_file_attrs()
        self.massdict = filelist.massdict
        self.invalid_files = filelist.invalid_files #new


    def data(self) -> None:
        """creates data frame list"""
        
        for key, value in self.massdict.items():
            try:
                val1, val2 = value.values()
            except ValueError:
                self.missing_data.append(key)
                continue
            if val1.pos_neg == 'neg' and val2.pos_neg == 'pos':
                neg_f = val1
                pos_f = val2
            elif val1.pos_neg == 'pos' and val2.pos_neg == 'neg':
                neg_f = val2
                pos_f = val1
            data = SampleData(pos=pos_f, neg=neg_f)
            data.run()
            self.df_list.append(data.df)

    
    def big_data(self) -> None:
        """creates one big data frame from all data frames in the list"""
        b_data = AllId (self.df_list)
        b_data.run()
        self.b_data = b_data

    def invalid_files_list (self):
        print (f'invalid files: {self.invalid_files}')
        with open('invalid files.txt', 'w') as f:
            for item in self.invalid_files:
                f.write("%s\n" % item)

    def missing_data_list (self):
        print (f'missing data: {self.missing_data}')
        with open('missing data.txt', 'w') as f:
            for item in self.missing_data:
                f.write("%s\n" % item)


    def run(self) -> bool:
        """main function to run the process"""
        if not self.input():
            print('Cancelling...')
            return False
        print('Collecting files...')
        self.raw_data()
        print('Reading files...')
        self.data()
        print('Building dataframe...')
        self.big_data()
        print('Analyzing...')
        self.invalid_files_list()
        self.missing_data_list()
        print('Done.')
        return True

if __name__ == "__main__":
    MassData().run()