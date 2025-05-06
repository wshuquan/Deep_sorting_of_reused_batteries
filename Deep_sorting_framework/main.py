import numpy as np
import pandas as pd
from metrics import calculate_difference_all, calculate_capacity, calculate_lifetime
from model import optimize_group
import matplotlib.pyplot as plt
import pickle
import warnings
warnings.filterwarnings(action='ignore')

from matplotlib import rcParams
config = {
    "font.family": 'Arial',
    "font.size": 8
}
rcParams.update(config)


def load_capa_trajs():

    capa_trajs_2 = {}
    capa_trajs_df = pd.read_csv(r'../Feature_engineering/dataset/capacity_trajectories.csv', header=0, index_col=None)
    bat_nums = np.unique(list(capa_trajs_df['bat_num']))
    for bat_num in bat_nums:
        bat_capa_traj = capa_trajs_df[capa_trajs_df['bat_num'] == bat_num]
        capa_trajs_2[str(bat_num)] = list(bat_capa_traj['capacity'])

    return capa_trajs_2


def plot_bat_groups(bat_num_array_groups, capa_trajs_2, title):

    cmap = plt.cm.get_cmap('coolwarm')

    for i in range(len(bat_num_array_groups)):
        bat_num_array = bat_num_array_groups[i]

        fig, ax = plt.subplots(figsize=(7, 5))
        plt.subplots_adjust(left=0.4, right=0.60, top=0.6, bottom=0.4)
        ax.set_xlabel('Cycle number')
        ax.set_ylabel('State of health')
        ax.set_xlim(0, 1950)
        ax.set_xticks([0, 500, 1000, 1500])
        ax.set_xticklabels([0, 500, 1000, 1500])
        ax.set_ylim(1.15, 2.0)
        ax.set_yticks([1.2, 1.44, 1.68, 1.92])
        ax.set_yticklabels([0.5, 0.6, 0.7, 0.8])
        ax.set_title(f'{title} - {i + 1}th group')

        for bat_num in bat_num_array:

            capa_traj_2 = capa_trajs_2[str(bat_num)]
            cyc_2 = list(range(1, len(capa_traj_2) + 1))
            ax.plot(cyc_2, capa_traj_2, linewidth=1, c=cmap((cyc_2[-1] - 100) / 700)) # '#BA0716'


def main():

    bat_nums = np.array(list(range(1, 61)) + list(range(63, 89)))

    capa_trajs_2 = load_capa_trajs()

    # ************* Get grouping results **************************
    all_feature_dir = '../Feature_engineering/dataset/features.csv'
    all_features = pd.read_csv(all_feature_dir, header=0, index_col=None)

    features_cluster_results_list = optimize_group(data=all_features, bat_nums=bat_nums, data_source=[1, 2, 3, 4],
                                                       n_clusters=8)  # Deep sorting
    index = 0
    steps = ['initial_grouping', 'first_refinement', 'second_refinement']

    for features_cluster_results in features_cluster_results_list:

        # ************ Convert old battery serial number to new battery ID ***************
        sorted_bat_nums = [29, 30, 31, 32, 57, 58, 59, 60, 1, 2, 3, 4, 49, 50, 51, 52, 5, 6, 7, 8, 63, 64, 9, 10, 11, 12, 53, 54, 55, 56,
                   33, 34, 35, 36, 65, 66, 67, 68, 13, 14, 15, 16, 71, 72, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 41, 42, 27, 28, 43, 44,
                   37, 38, 45, 46, 39, 40, 47, 48, 69, 70, 79, 80, 73, 74, 77, 75, 76, 78, 85, 86, 87, 88, 81, 82, 83, 84]
        for cluster_result in features_cluster_results:
            c = list()
            for i in range(len(cluster_result)):
                c.append(sorted_bat_nums.index(cluster_result[i]) + 1)

        # ********* Calculate sorting evaluation metrics **********
        features_total_lifetime_2, features_available_lifetime_2, features_available_mean_lifetimes_2, cell_available_lifetimes = calculate_lifetime(
            features_cluster_results, capa_trajs_2)

        all_differences, array_differences, cell_diffs = calculate_difference_all(features_cluster_results, capa_trajs_2)

        features_total_capa_2, features_available_capa_2, features_total_capas_2, features_available_capas_2, cell_capa_util = calculate_capacity(features_cluster_results, capa_trajs_2)

        metrics = {'cell_diffs': cell_diffs, 'group_diffs': array_differences, 'diff': all_differences,
                        'cell_capa_util': cell_capa_util, 'group_capa_util': features_available_capas_2 / features_total_capas_2, 'capa_util': features_available_capa_2 / features_total_capa_2,
                        'cell_lifetime': cell_available_lifetimes, 'group_lifetime': features_available_mean_lifetimes_2, 'lifetime': features_available_lifetime_2 / len(bat_nums)}
        with open(f'./metrics/metrics_deep_sorting_{steps[index]}.pickle', 'wb') as handle:
            pickle.dump(metrics, handle, protocol=2)

        print(f'\n************* Metrics_{steps[index]}*************')
        for key in metrics.keys():
            print(f'********{key}********\n{metrics[key]}')

        plot_bat_groups(features_cluster_results, capa_trajs_2, title=steps[index])

        index += 1

    plt.show()


if __name__ == '__main__':
    main()