import tkinter as tk
import pandas as pd
import numpy as np
import os
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import linear_model, datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,mean_squared_error, r2_score
from sklearn.preprocessing import Imputer
from tkinter.ttk import * 
import tkinter.font as font
from sklearn.base import TransformerMixin
from missingpy import KNNImputer
import numpy
import missingno as msno

from tkinter import messagebox

os.chdir("C:/Users/Intel/Desktop/ChasersOfLostData")
CSV_FILE=""
CSV1="C:/Users/Intel/Desktop/ChasersOfLostData/Output.csv"
CSV2="C:/Users/Intel/Desktop/ChasersOfLostData/xyzw.csv"

# Functions
def popup(title, msg):
    '''Open popup window with title and msg'''
    w = tk.Toplevel(root)
    w.title(title)
    w.minsize(200, 200)
    tk.Label(w, text=msg).pack()
    tk.Button(w, text="Close", command=w.destroy).pack(pady=10)
    w.bind("<Return>", lambda f: w.destroy())



def read_from_file():
    '''Read csv file and return a list like: [[username, password, count]]'''
    try:
        with open(CSV_FILE, 'rt') as f:
            users = []
            reader = csv.reader(f)
            for row in reader:
                users.append(row)
            return users
    except IOError:
        popup("Error", "File not found!")




class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack(anchor="c")
    
        myFont = font.Font(family='Helvetica', size=15)
        myFont1 = font.Font(family='Helvetica', size=12, weight='bold')
        myFont2 = font.Font(family='Helvetica', size=13, weight='bold')
        
        
        # Labels
        label0 = tk.Label(self, text="An app to fill missing data with the best possible method")
        
        label0.grid(row=0,column=0,padx=15,pady=10,columnspan=3,sticky="w")
        label0['font']=myFont
        
        label1=tk.Label(self, text="Input Your file name ")
        label1.grid(row=1,column=0,padx=15,pady=10,sticky="w")
        label1['font']=myFont
        # Entries
        self.path = tk.StringVar()

        name = tk.Entry(self, textvariable=self.path, width=20)
        name.grid(row=1, column=1, padx=0,pady=20,sticky="we")
        name['font']=myFont2
        
        # Login Button
        fill = tk.Button(self, text="Fill the data", bg='#ffffff', fg='#0052cc', command=self.fill)
        fill.grid(row=2, column=0, padx=30,pady=10)
        fill['font']=myFont1
        
        btn1 = tk.Button(self, text = 'Quit !',bg='white', fg='red', command = root.destroy) 
        btn1.grid(row =2,column = 1, padx=10,pady=10)

        btn1['font']=myFont1

        # Binding
        self.master.bind("<Return>", self.fill)

    def fill(self, event=None):
        var=self.path.get()
        self.path=str(var)
        self.path=self.path.replace("\\", "/")
        users = []
        try:
            aa=pd.read_csv(self.path)
        except:
            messagebox.showinfo("Error","Invalid File")
        print(aa)
        data=aa

        data.head()

        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']   #Selecting only numerical columns

        newdf = data.select_dtypes(include=numerics)

        columnsfill=[]
        for col in data.select_dtypes(include=numerics).columns:
            columnsfill.append(col)
        columnsfill

        # Let X be an array containing missing values

        imputer = KNNImputer()
        for i in columnsfill:
            X_imputed = imputer.fit_transform(data[[i]])
            data[i]=X_imputed

        #data['GeoLocation'] = '('+round(data['reclat'],4).astype(str) + ',' + round(data['reclong'],4).astype(str)+')'   #Combining lat and long to form coordinate

        null_data = data[data.isnull().any(axis=1)]
        print(len(null_data))
        null_data


        class SeriesImputer(TransformerMixin):

            def __init__(self):
                def fit(self, X, y=None):
                    if   X.dtype == numpy.dtype('O'): self.fill = X.value_counts().index[0]
                    return self

            def transform(self, X, y=None):
                return X.fillna(self.fill)

        stringcol=data.columns[data.isna().any()].tolist()
        stringcol

        for i in stringcol:
            a  = SeriesImputer()   # Initialize the imputer
            a.fit(data[i])              # Fit the imputer
            data[i] = a.transform(data[i])   # Get a new series

        null_data = data[data.isnull().any(axis=1)]
        print(len(null_data))
        null_data

        print(data)

        data.to_csv(CSV1)
        messagebox.showinfo("Data Filled Successfully","Your new file is saved as \"Output.csv\"")


# GUI settings
root = tk.Tk()
app = App(root)

root.title("Chasing Lost Data")
root.minsize(800, 450)


# Initalize GUI
root.mainloop()

