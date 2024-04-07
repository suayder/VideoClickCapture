"""
Helpers
"""
import os

import pandas as pd

def file_loader(path):
    """
    This is a function that load the annotated text files and load to a DataFrame with columns frame,x,y

    :return: Daframe with columns frame,x,y
    """
    files = [f for f in os.listdir(path) if f.endswith('.txt')]

    all_clicks = []
    for file in files:
        with open(os.path.join(path, file)) as f:
            line = f.readline().strip().split(',')

        all_clicks.append(file.split('.')[:1] + line)
    
    df_clicked = pd.DataFrame(all_clicks, columns=['frame','x','y']).astype(int)
    df_clicked.sort_values('frame', inplace=True)

    return df_clicked
