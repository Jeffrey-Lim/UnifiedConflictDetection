'''
This script is used to make gifs from the images generated by the visualisation scripts.
'''

import os
import cv2
import glob
from tqdm import tqdm
import pandas as pd
import imageio

# Set input and output paths
path_output = './Data/OutputData/'
path_figure = './Data/DynamicFigures/'


# video making highD

summary2vis = pd.read_csv(path_output + 'intensity_evaluation/highD_conflict_LC_to_visualse.csv')

for idx in tqdm(summary2vis.index, desc='highD'):
    if summary2vis.loc[idx, 'num_conflicts']<1:
        continue

    loc_id = summary2vis.loc[idx, 'location']
    veh_id_i = summary2vis.loc[idx, 'veh_id_i']
    veh_id_j = summary2vis.loc[idx, 'veh_id_j']

    save_dir = path_output+'video_images/highD_LC/'
    save_dir = save_dir + summary2vis.loc[idx,'specification']+'/'
    save_dir = save_dir + f"intensity_{summary2vis.loc[idx,'intensity_lower']:.1f}" + '-' + f"{summary2vis.loc[idx,'intensity_upper']:.1f}/"
    image_dir = save_dir + f'{loc_id}_{veh_id_i}_{veh_id_j}/'
    filelists = sorted(glob.glob(image_dir+'*.png'), key=lambda x: int(x[-10:-4]))

    frames = []
    for file in filelists:
        img = cv2.resize(cv2.imread(file), None, fx=0.25, fy=0.25)
        frames.append(img)

    save_dir = path_figure+'IntensityEvaluation/gifs/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    gif_dir = save_dir + summary2vis.loc[idx,'specification'].replace(' ', '_')+'_'
    gif_dir = gif_dir + f"intensity_{summary2vis.loc[idx,'intensity_lower']:.1f}" + '-' + f"{summary2vis.loc[idx,'intensity_upper']:.1f}"
    gif_dir = gif_dir + '.gif'

    with imageio.get_writer(gif_dir, mode='I', duration=0.1) as writer:
        for frame in frames:
            # Convert color from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            writer.append_data(frame_rgb)

    writer.close()


# video making 100Car

folder_list = ['unified1_ttc1_drac0', 
               'unified1_ttc0_drac1',
               'unified1_ttc0_drac0',
               'unified0_ttc1_drac1',
               'unified0_ttc0_drac1',
               'unified_false_warning']
trip_list = [[8622,9101], 
             [8702], 
             [8463,8810,8854],
             [8793],
             [8332],
             [8395,8460,8463,8565,9044]]

for idx, folder in tqdm(enumerate(folder_list), desc='100Car', total=len(folder_list)):
    trip_id_list = trip_list[idx]
    for trip_id in trip_id_list:
        save_dir = path_output + f'video_images/100Car/{folder}/{trip_id}/'
        filelists = sorted(glob.glob(save_dir+'*.png'), key=lambda x: int(x.split('_')[-1].split('.')[0]))

        frames = []
        for file in filelists:
            img = cv2.resize(cv2.imread(file), None, fx=0.25, fy=0.25)
            frames.append(img)

        save_dir = path_figure+'ProbabilityEstimation/gifs/'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        gif_dir = save_dir + folder + '_'
        gif_dir = gif_dir + f"trip_{trip_id}"
        gif_dir = gif_dir + '.gif'

        with imageio.get_writer(gif_dir, mode='I', duration=0.1) as writer:
            for frame in frames:
                # Convert color from BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                writer.append_data(frame_rgb)

        writer.close()
