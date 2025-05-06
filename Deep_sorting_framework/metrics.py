import numpy as np
import pandas as pd
import os

initial_capa = 1.90

folder_dir = '../Second_life_phase'


def calculate_difference(x, y):
    if len(x) > len(y):
        l = len(x)
        y = y + [1.2] * (l - len(y))
    elif len(x) <= len(y):
        l = len(y)
        x = x + [1.2] * (l - len(x))
    diff = [np.abs(i - j) for i, j in zip(x, y)]
    diff = np.sum(diff)
    return diff


def calculate_difference_all(bat_num_arrays, capa_trajs):
    array_diffs = list()
    all_diffs = list()
    cell_diffs = list()
    for bat_num_array in bat_num_arrays:
        diff = list()
        for i in range(len(bat_num_array)):
            if str(bat_num_array[i]) not in capa_trajs.keys():
                continue
            for j in range(i+1, len(bat_num_array)):
                if str(bat_num_array[j]) not in capa_trajs.keys():
                    continue
                capa_traj_1 = capa_trajs[str(bat_num_array[i])]
                capa_traj_2 = capa_trajs[str(bat_num_array[j])]
                diff.append(calculate_difference(capa_traj_1, capa_traj_2))
                all_diffs.append(calculate_difference(capa_traj_1, capa_traj_2))
        array_diffs.append(np.mean(diff))
        cell_diffs.append(diff)
    all_diffs = np.mean(all_diffs)
    return all_diffs, array_diffs, cell_diffs


def calculate_capacity(bat_num_arrays, capa_trajs_2):

    all_total_capas = list()
    all_available_capas = list()

    cell_capa_util = list()

    for bat_num_array in bat_num_arrays:

        bat_lives = list()
        for bat_num in bat_num_array:
            bat_capa_traj = capa_trajs_2[str(bat_num)]
            bat_lives.append(len(bat_capa_traj))
        life_min = np.min(bat_lives)

        total_capas = list()
        available_capas = list()

        for bat_num in bat_num_array:
            total_capa = list()
            available_capa = list()
            bat_cycle_data_2 = pd.read_csv(os.path.join(folder_dir, f'{bat_num}.csv'))
            last_cycle = np.max(list(bat_cycle_data_2['Cycle_Index']))
            initial_cyc = 1
            for cycle in list(range(1, last_cycle + 1, 5)):
                cycle_data_2 = bat_cycle_data_2[bat_cycle_data_2['Cycle_Index'] == cycle]
                discharge_capa = list(cycle_data_2[cycle_data_2['Step_Index'] == 15]['Discharge_Capacity(Ah)'])[-1]
                if discharge_capa < initial_capa:
                    initial_cyc = cycle
                    break
            for cycle in list(range(initial_cyc, last_cycle + 1, 1)):
                cycle_data_2 = bat_cycle_data_2[bat_cycle_data_2['Cycle_Index'] == cycle]
                if cycle % 5 == 1:
                    discharge_capa = list(cycle_data_2[cycle_data_2['Step_Index'] == 15]['Discharge_Capacity(Ah)'])[-1]
                else:
                    discharge_capa = list(cycle_data_2[cycle_data_2['Step_Index'] == 24]['Discharge_Capacity(Ah)'])[-1]
                total_capa.append(discharge_capa)
                if cycle - initial_cyc < life_min:
                    available_capa.append(discharge_capa)
            total_capas.append(np.sum(total_capa))
            available_capas.append(np.sum(available_capa))
        cell_capa_util.append(np.array(available_capas) / np.array(total_capas))
        all_total_capas.append(np.sum(total_capas))
        all_available_capas.append(np.sum(available_capas))
    return np.sum(all_total_capas), np.sum(all_available_capas), np.array(all_total_capas), np.array(all_available_capas), cell_capa_util


def calculate_lifetime(bat_num_arrays, capa_trajs_2):

    all_total_lifetimes = list()
    all_available_lifetimes = list()
    all_available_mean_lifetimes = list()
    cell_available_lifetimes = list()

    for bat_num_array in bat_num_arrays:

        bat_lives = list()
        for bat_num in bat_num_array:
            bat_capa_traj = capa_trajs_2[str(bat_num)]
            bat_lives.append(len(bat_capa_traj))
        life_min = np.min(bat_lives)

        all_total_lifetimes.append(np.sum(bat_lives))
        all_available_lifetimes.append(life_min * len(bat_lives))
        all_available_mean_lifetimes.append(life_min)
        cell_available_lifetimes.append([life_min] * len(bat_lives))

    return np.sum(all_total_lifetimes), np.sum(all_available_lifetimes), all_available_mean_lifetimes, cell_available_lifetimes
