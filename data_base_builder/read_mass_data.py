import attr
from attr.validators import instance_of
import pandas as pd
from pathlib import Path
import time
import numpy as np
from process_mass_gui import *

###  need to add intrap func for data before saving it to df

class SampleData:
    """Pipeline to process data of one ID on one design (both fixations and conditions).
    Attributes: fixations, events, id_num, design, df_fixations, df_cond, df_id.
    Methods: create_fixation_df, create_cond_df, merge_df, run count_data.
    """
    def __init__(self, pos: MassFile, neg: MassFile):
        # self.pos = pd.read_csv(pos.path, sep="\t", header=None)
        # self.neg = pd.read_csv(neg.path, sep="\t", header=None)
        self.pos_path = pos.path
        self.neg_path = neg.path
        self.pos = None
        self.neg = None
        self.fname = pos.fname
        self.bat = pos.bat
        self.food = pos.food
        # self.date = pos.date
        self.sample_time = pos.sample_time
        self.sample = pos.sample
        # self.sample_kind = pos.sample_kind
        self.sample_kind = pos.sample_kind
        # self.pos_df = self.create_pos_neg_df('pos')
        # self.neg_df = self.create_pos_neg_df('neg')
        self.df = pd.DataFrame(columns=['sample_id','bat','sample_time',
                                        'food','oral/anal'])
        self.sample_df = pd.DataFrame()
   
        
    def run(self):
        self.df_append()
        self.pos = self.mass_file_to_df(self.pos_path,'pos')
        self.neg = self.mass_file_to_df(self.neg_path,'neg')
        self.pos = self.pos.to_dict('records')[0] #to dict
        self.neg = self.neg.to_dict('records')[0] #to dict
        pos_df = self.create_pos_neg_df('pos')
        neg_df = self.create_pos_neg_df('neg')
        self.df = self.df.assign(**pos_df)
        self.df = self.df.assign(**neg_df) 
        self.df = self.df.assign(**self.pos)
        self.df = self.df.assign(**self.neg)
        # self.df = pd.concat([self.df,self.pos,self.neg,self.pos_df,self.neg_df], sort = False)
        # self.df = df.set_index(['ID', 'design'])
        # print (self.df)
        df = self.df.T
        df.to_csv('df2')

    def mass_file_to_df (self,path,p_s):
        mass_file = pd.read_csv(path, sep="\t", header=None)
        mass_file.index = mass_file[0]
        mass_file = mass_file.drop(columns=[0])
        mass_file = mass_file.T
        mass_file.columns = [f'{p_s}_'+ str(col) for col in mass_file.columns]
        return mass_file

    def create_pos_neg_df(self, p_s):
        df = pd.DataFrame(index=np.around(np.arange(100,2000,0.1), decimals=1), columns=['A'])
        df = df.T
        df.columns = [f'{p_s}_'+ str(col) for col in df.columns]
        df.to_dict('records')[0]
        return df

    def df_append(self):
        # attr_dict = {'sample_id':self.sample, 'bat':self.bat , 'date' : self.date, 
        #                           'sample_time': self.sample_time,'food' :self.food}
        self.df = self.df.append({'sample_id':self.sample, 'bat':self.bat, 'sample_time': self.sample_time, 
                                'oral/anal': self.sample_kind, 'food' :self.food}, ignore_index=True)

        # self.df.assign(**attr_dict)
 
@attr.s
class AllId:
    """A unified dataframe, multi-indexed by ID and design.
    Attributes: df_list, df_all, cond_dict.
    Methods: merge_df, create_big_data, cond_names, save_csv, run.
    """
    df_list = attr.ib(validator=instance_of(list))
    df_all = attr.ib(default=pd.DataFrame)
    cond_dict = attr.ib(default=attr.Factory(dict))

    def merge_df(self, basic_df: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
        """Appends dataframe given by create_big_data func into one multi-index data frame"""
        df_merge = pd.concat([basic_df, df])
        # df_merge = df_merge.dropna()
        return df_merge

    def create_big_data(self) -> None:
        """Merges all data frames in the list into one big data frame"""
        basic_df = self.df_list.pop(0)
        for df in self.df_list:
            basic_df = self.merge_df(basic_df, df)
        self.df_all = basic_df

    # def cond_names(self) -> None:
    #     """Replaces all conditions names in 'cond_int' column into int"""
    #     conds_names = self.df_all.condition.unique()
    #     num = 1
    #     for cond in conds_names:
    #         self.cond_dict[f'{cond}'] = num
    #         num+=1
    #     self.df_all = self.df_all.replace({"cond_int": self.cond_dict})

    def save_csv(self) -> None:
        """Saves dataframe into csv file"""
        output_file = (f"Data_Frame_{pd.Timestamp.now().strftime('%Y_%m_%d_%H_%M_%S')}.csv")
        output_dir = Path('Results')
        output_dir.mkdir(parents=True, exist_ok=True)
        self.df_all.to_csv(output_dir / output_file)

    def run(self) -> None:
        """Main pipeline"""
        self.create_big_data()
        self.save_csv()

        
if __name__ == "__main__":
    pass