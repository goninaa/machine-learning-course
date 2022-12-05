import attr
from attr.validators import instance_of
from typing import Union
import pandas as pd
from pathlib import Path
import pathlib
import time
import numpy as np

@attr.s(frozen=True)
class MassFile:
    """File objects with path attribute and several metadata attributes.
    Instantiated by the ProcessFilelist class, passed to the ProcessData class
    Attributes: path, fname, bat ,food, sample_time, sample, sample_kind, pos_neg.
    """
    path = attr.ib(validator=instance_of(Path))
    fname = attr.ib(validator=instance_of(str))
    bat = attr.ib(validator=instance_of(str))
    food = attr.ib(validator=instance_of(str))
    # date = attr.ib(validator=instance_of(str))
    sample_time = attr.ib(validator=instance_of(str))
    sample_kind = attr.ib(validator=instance_of(str))
    sample = attr.ib(validator=instance_of(str))
    pos_neg = attr.ib(validator=instance_of(str))


class ProcessFilelist:

    def __init__(self, filelist):
        self.sample_df = pd.DataFrame(columns=['sample_id','bat','sample_time',
                                        'food','oral/anal','pos/neg'])
        self.df = None
        self.filelist = filelist
        self.invalid_files = [] ### should add invalid files output ###
        self.massdict = {} # nested dict of MassFile instances to pass forward

        
  

    def get_file_attrs(self) -> None:
        """Analizes file attributes and instantiate EyeFile objects"""
        for mfile in self.filelist:
            path = Path(mfile)
            fname = path.name
            bat = path.parent.parent.parent.parent.name
            sample_time = path.parent.name
            food = path.parent.parent.parent.name #before/after
            sample_kind = path.parent.parent.name
            #/Users/gonina/Dropbox/classes/machine_learning/project/1_Vova/Banana/Oral/After 8/fname.txt

            if not self.assert_txt(path): # accepts only .txt files
                self.invalid_files.append(fname)
                print ('some of the files are not txt files')
                continue
            if not self.assert_not_empty(path):
                self.invalid_files.append(fname)
                print ('some of the files are empty')
                continue
            if not self.assert_format(path):
                self.invalid_files.append(fname)
                print ('some of the files are not in the right name format')
                continue
            if not self.assert_fname(path): 
                self.invalid_files.append(fname)
                print ('some of the files name are too long')
                continue
         
            fattrs = self.extract_file_attrs(fname)
            if not fattrs: # accepts files only if named in the appropriate pattern
                self.invalid_files.append(fname)
                print ('some of the files are not in the right name format (attrs)')
                continue
            sample, pos_neg  = fattrs[0],fattrs[1] 
            self.instantiate_mass_file(path, fname, bat, food, sample_time, sample, sample_kind, pos_neg)
           
            # try:
            #     fattrs = self.extract_file_attrs(fname)
            #     if not fattrs: # accepts files only if named in the appropriate pattern
            #         self.invalid_files.append(fname)
            #         print ('some of the files are not in the right name format (attrs)')
            #         continue
            #     sample, pos_neg  = fattrs[0],fattrs[1] 
            #     self.instantiate_mass_file(path, fname, bat, food, sample_time, sample, sample_kind, pos_neg)
            # except TypeError:
            #     print ("can't get attrs")
            #     self.invalid_files.append(fname)


    def df_append(self,path, fname, bat, food, sample_time, sample, sample_kind, pos_neg):
        self.sample_df = self.sample_df.append({'sample_id':sample, 'bat':bat ,'sample_time': sample_time,'food' :food, 'oral/anal':sample_kind, 'pos/neg':pos_neg} , ignore_index=True)

    def create_pos_neg_df(self, p_s):
        #need to fix
        df = pd.DataFrame(index=np.around(np.arange(0,2500,0.1), decimals=1))
        df = df.T
        df.columns = [f'{p_s}_'+ str(col) for col in df.columns]
        return df

    def mass_file_to_df (self,path,p_s):
        mass_file = pd.read_csv(path, sep="\t", header=None)
        mass_file.index = mass_file[0]
        mass_file = mass_file.drop(columns=[0])
        mass_file = mass_file.T
        mass_file.columns = [f'{p_s}_'+ str(col) for col in mass_file.columns]
        # value_df = pd.read_csv(path, sep="\t", header=None)
        # value_df = value_df.T
        # value_df.columns = value_df.iloc[0]
        # value_df.columns = [f'{p_s}_'+ str(col) for col in value_df.columns]
        # value_df = value_df.drop(columns=[0])
        # mass_file = mass_file.to_dict('records')[0] #to dict
        # print (value_df)
        return mass_file

    def assert_txt(self, path: Path) -> bool:
        """Asserts that a file is a txt file"""
        return str.lower(path.suffix) == '.txt'

    # def assert_format (self, path: Path) -> bool:
    #     """Asserts that the file is either pos or neg file"""
    #     if 'pos' or 'neg' in path.name:
    #         return True
    #     else:
    #         return False
    
    def assert_format (self, path: Path) -> bool:
        """Asserts that the file is in the right name format"""
        return ('neg' or 'pos') and 'YY' in path.name
        # return path.name.contains(('neg' or 'pos') and 'YY')

    def assert_fname (self, path: Path) -> bool:
        """Asserts that the file is in the right name format (and not too long)"""
        return len(path.name) == 16
    

    def assert_not_empty (self, path: Path) -> bool:
        """Asserts that the file is not empty"""
        return path.stat().st_size != 0

    def extract_file_attrs(self, fname: str) -> Union[list, bool]:
        """If the file named appropriately, extracts its attributes from filename"""
        fattrs = fname.split(' ')
        fattrs[1] = fattrs[1].split(".")[0]
        return fattrs if len(fattrs) == 2 else False


    def instantiate_mass_file(self, path: Path, fname: str, bat: str, food: str, sample_time: str, sample: str,sample_kind:str, pos_neg: str,) -> MassFile:
        """Instantiates EyeFile objects"""
        massitem = MassFile(path=path, fname=fname, bat=bat, food=food, sample_time=sample_time, sample=sample, sample_kind=sample_kind, pos_neg=pos_neg)
        try:
            self.massdict[f'{bat}_{sample}'][pos_neg] = massitem
        except KeyError:
            self.massdict[f'{bat}_{sample}']= {pos_neg: massitem}




if __name__ == "__main__":
    # filelist =    ['/Users/gonina/Dropbox/classes/machine_learning/project/1_clio/After feeding/food/Yovel_20190513_3_neg.txt','/Users/gonina/Dropbox/classes/machine_learning/project/1_clio/After feeding/food/Yovel_20190513_3_pos.txt']
    filelist =    ['/Users/gonina/Dropbox/classes/machine_learning/project/1_Vova/Banana/Oral/After 8/YY20-044 neg.txt']
    files = ProcessFilelist(filelist)
    files.get_file_attrs()
    file_dict = files.massdict
    print(files.massdict)
    # # print(files.invalid_files)
    # print (file_dict['Yovel_20190513_3_neg.txt'].date)
    # sample_df = pd.DataFrame(columns=['sample_id','bat','date','sample_time',
                                        # 'food','mouth/anus', 'pos/neg'])
    # sample_df.append({'sample_id':file_dict['Yovel_20190513_3_neg.txt'].sample), 'bat':file_dict['Yovel_20190513_3_neg.txt'].bat , 'bat1_loc' : 101, 'pump_1': 1,'bat2_id' :'2A'} , ignore_index=True)
    # print(files.sample)
    # print (files.sample_df)
    # print (files.df)