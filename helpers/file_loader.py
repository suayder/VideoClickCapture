"""
Helpers
"""
import os
import pandas as pd

def file_loader(path, ret='dataframe'):
    """
    This is a function that load the annotated text files and load to a DataFrame with columns frame,x,y

    Args:
        ret: type for returned data, can be ['dict','dataframe']
    
    Return:
        Daframe with columns frame,x,y or a dict like this {frame_number: {'x': x, 'y': y}, ...}
    """
    files = [f for f in os.listdir(path) if f.endswith('.txt')]

    all_clicks = []
    for file in files:
        with open(os.path.join(path, file)) as f:
            line = f.readline().strip().split(',')

        all_clicks.append(file.split('.')[:1] + line)
    
    df_clicked = pd.DataFrame(all_clicks, columns=['frame','x','y']).astype(int)
    df_clicked.sort_values('frame', inplace=True)

    assert(ret in ['dataframe', 'dict'])
    if ret == 'dataframe':
        return df_clicked
    else:
        return df_clicked.set_index('frame').to_dict(orient='index')

def multiple_file_loader(path, ret='dataframe'):
    """
    Load many files by different users.

    Args:
        path: to the annotation folder. Is expected all folders to be from the same video annotated by different users.
    """
    
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

    all_clicks = []
    for i, folder in enumerate(folders):
        df_clicks = file_loader(os.path.join(path, folder))
        df_clicks['user'] = i
        all_clicks.append(df_clicks)
    
    return pd.concat(all_clicks).set_index(['frame'])