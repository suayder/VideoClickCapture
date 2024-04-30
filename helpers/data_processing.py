"""
This file contains the annotation's processing functions
"""
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import pandas as pd
import numpy as np


def interpolate(df_clicks:pd.DataFrame, ret='dataframe', user_name=None):
    """
    apply cubic interpolation in a DataFrame

    Args:
        df_clicks (pd.DataFrame):
        ret (dataframe | dict, optional)
        user_name (str, optional): Just used to render the name of the user when plot the point. Defaults to None.

    Returns:
        pd.DataFrame: the frames interpolated
    """
    df_clicks = df_clicks.sort_index()
    all_frames = set(range(df_clicks.index.min(), df_clicks.index.max()))

    x = df_clicks['x'].to_numpy()
    y = df_clicks['y'].to_numpy()
    z = df_clicks.index

    missing_frames = list(all_frames - set(z))

    interpx = interp1d(z, x, kind='cubic')
    interpy = interp1d(z, y, kind='cubic')
    x_interp = interpx(missing_frames)
    y_interp = interpy(missing_frames)

    interpolated_df = pd.DataFrame({
            'x': x_interp,
            'y': y_interp
        }, index=missing_frames)

    interpolated_df = pd.concat([interpolated_df, df_clicks], axis=0)
    interpolated_df = interpolated_df.astype({'x': int, 'y': int})
    interpolated_df = interpolated_df.sort_index()

    # plot
    rcParams['figure.figsize'] = 11.7,5.27
    g = sns.lineplot(data=interpolated_df, markers=True, lw=0.3)
    plt.title(f'(x,y) interpolated for user {user_name}')
    plt.show()

    assert(ret in ['dataframe', 'dict'])
    if ret == 'dict':
        return interpolated_df.to_dict(orient='index')
    
    return interpolated_df


def gen_gaussian_blob(image_shape, px, py, sigma=10, denormalize=False):
    """
    Given the shape of an image and two points (px,py), this function will generate an image with a gaussian centered at (px, py).

    Args:
        image_shape: (width,height)
    """

    image_shape = image_shape[::-1]
    mask = np.zeros(image_shape, dtype=np.uint8)

    y, x = np.ogrid[:image_shape[0], :image_shape[1]]
    gaussian = np.exp(-((x - px) ** 2 + (y - py) ** 2) / (2 * sigma ** 2))
    
    mask = gaussian / np.max(gaussian)

    if denormalize:
        return (mask*255).astype(np.uint8)

    return mask