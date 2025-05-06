import os
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
import warnings
warnings.filterwarnings(action='ignore')

initial_capa = 1.90

data_folder_dir = '../Second_life_phase'

capa_trajs = list()
bat_nums = list(range(1, 61)) + list(range(63, 89))
for bat_num in bat_nums:

    print(bat_num)

    bat_cycle_data = pd.read_csv(os.path.join(data_folder_dir, f'{bat_num}.csv'), header=0, index_col=None)
    if len(bat_cycle_data) == 0:
        continue

    cycles = sorted(np.unique(bat_cycle_data['Cycle_Index']))
    cyc, capa = list(), list()
    for cycle in cycles:

        if cycle % 5 != 1:
            continue

        if (bat_num == 3) and (cycle in [221, 226]):
            continue
        if (bat_num == 5) and (cycle in [161, 166, 171]):
            continue
        if (bat_num == 10) and (cycle in [116]):
            continue
        if (bat_num == 13) and (cycle in [261, 266]):
            continue
        if (bat_num == 14) and (cycle in [266, 271, 276, 281]):
            continue
        if (bat_num == 15) and (cycle in [256, 261, 266, 271]):
            continue
        if (bat_num == 16) and (cycle in [266]):
            continue
        if (bat_num == 17) and (cycle in [81, 86]):
            continue
        if (bat_num == 18) and (cycle in [101, 106, 111, 116, 216]):
            continue
        if (bat_num == 19) and (cycle in [76, 81, 86, 236, 241]):
            continue
        if (bat_num == 20) and (cycle in [86, 91, 176, 196, 241, 246]):
            continue
        if (bat_num == 21) and (cycle in [821, 826, 831, 836, 1221, 1511]):
            continue
        if (bat_num == 22) and (cycle in [736, 741, 746, 751, 756, 761, 766, 811, 816, 1086]):
            continue
        if (bat_num == 23) and (cycle in [116, 721, 726, 731, 736, 741, 1106, 1111]):
            continue
        if (bat_num == 24) and (cycle in [946, 951, 956]):
            continue
        if (bat_num == 27) and (cycle in [316]):
            continue
        if (bat_num == 29) and (cycle in [156, 161, 166, 171, 176]):
            continue
        if (bat_num == 30) and (cycle in [216, 221, 226]):
            continue
        if (bat_num == 31) and (cycle in [281]):
            continue
        if (bat_num == 32) and (cycle in [231, 236]):
            continue
        if (bat_num == 37) and (cycle in [36, 41, 46]):
            continue
        if (bat_num == 40) and (cycle in [166, 171]):
            continue
        if (bat_num == 41) and (cycle in [206]):
            continue
        if (bat_num == 42) and (cycle in [196, 201]):
            continue
        if (bat_num == 43) and (cycle in [16, 266]):
            continue
        if (bat_num == 44) and (cycle in [16]):
            continue
        if (bat_num == 47) and (cycle in [56]):
            continue
        if (bat_num == 48) and (cycle in [56, 61]):
            continue
        if (bat_num == 51) and (cycle in [216, 221]):
            continue
        if (bat_num == 52) and (cycle in [216, 221]):
            continue
        if (bat_num == 53) and (cycle in [201]):
            continue
        if (bat_num == 54) and (cycle in [201]):
            continue
        if (bat_num == 55) and (cycle in [136]):
            continue
        if (bat_num == 56) and (cycle in [201]):
            continue
        if (bat_num == 59) and (cycle in [151, 201]):
            continue
        if (bat_num == 60) and (cycle in [241]):
            continue
        if (bat_num == 63) and (cycle in [106, 111]):
            continue
        if (bat_num == 64) and (cycle in [96, 101]):
            continue
        if (bat_num == 68) and (cycle in [276]):
            continue
        if (bat_num == 69) and (cycle in [346, 601]):
            continue
        if (bat_num == 70) and (cycle in [316, 561]):
            continue
        if (bat_num == 73) and (cycle in [106]):
            continue
        if (bat_num == 74) and (cycle in [226, 336, 491, 496]):
            continue
        if (bat_num == 77) and (cycle in [11, 511, 516]):
            continue
        if (bat_num == 79) and (cycle in [56, 61, 66, 446]):
            continue
        if (bat_num == 80) and (cycle in [56, 61, 66, 446]):
            continue
        if (bat_num == 83) and (cycle in [396]):
            continue
        if (bat_num == 84) and (cycle in [41]):
            continue
        if (bat_num == 85) and (cycle in [261]):
            continue
        if (bat_num == 86) and (cycle in [276]):
            continue
        if (bat_num == 87) and (cycle in [146, 151]):
            continue
        if (bat_num == 88) and (cycle in [191]):
            continue

        cycle_data = bat_cycle_data[bat_cycle_data['Cycle_Index'] == cycle]
        discharge_data = cycle_data[cycle_data['Step_Index'] == 15]
        if len(list(discharge_data['Discharge_Capacity(Ah)'])) == 0:
            continue
        discharge_capacity = list(discharge_data['Discharge_Capacity(Ah)'])[-1]

        if discharge_capacity > 1.9:
            continue

        cyc.append(cycle)
        capa.append(discharge_capacity)

    cyc = [c - cyc[0] + 1 for c in cyc]

    cyc_2 = np.linspace(1, cyc[-1], cyc[-1])
    capa_2 = make_interp_spline(cyc, capa)(cyc_2)

    capa_trajs.append(pd.DataFrame({'bat_num': bat_num, 'cycle': cyc_2, 'capacity': capa_2}))

capa_trajs_df = pd.concat(capa_trajs)
capa_trajs_df.to_csv('./dataset/capacity_trajectories.csv')
