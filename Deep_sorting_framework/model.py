import numpy as np
import pandas as pd
from copy import deepcopy
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def get_implicit_features(all_features, data_dource, derivative):
    features = {}
    for i in range(1, len(all_features.columns)):
        features[list(all_features.columns)[i]] = list(all_features[list(all_features.columns)[i]])
    data = {}
    for i in data_dource:
        for j in derivative:
            j += 1
            for k in range(1, 10):
                data[f'feature_{i}_{j}_{k}'] = features[f'feature_{i}_{j}_{k}']
    features_selected = pd.DataFrame(data).values
    return features_selected


def compute_group_center(data_dict, group_samples):
    if len(group_samples) == 0:
        return None
    group_vectors = [data_dict[sample] for sample in group_samples]
    return np.mean(group_vectors, axis=0)


def refine_groups(groups, data_dict, distance_threshold=0.1):
    group_centers = {}
    for g, samples in groups.items():
        center = compute_group_center(data_dict, samples)
        if center is not None:
            group_centers[g] = center
        else:
            group_centers[g] = None

    new_groups = deepcopy(groups)
    moved_samples = set()

    moved_count = 0
    for g, samples in groups.items():
        if group_centers[g] is None:
            continue
        center_g = group_centers[g]

        for sample in samples:
            if sample in moved_samples:
                continue
            sample_vec = data_dict[sample]

            dist_to_current = np.linalg.norm(sample_vec - center_g)

            distances = []
            for other_g, c_vec in group_centers.items():
                if other_g == g or c_vec is None:
                    continue
                dist_to_other = np.linalg.norm(sample_vec - c_vec)
                distances.append((other_g, dist_to_other))

            if len(distances) > 0:
                distances.sort(key=lambda x: x[1])
                closest_group, closest_dist = distances[0]

                if closest_dist + distance_threshold < dist_to_current:
                    new_groups[g].remove(sample)
                    new_groups[closest_group].append(sample)
                    moved_samples.add(sample)
                    moved_count += 1

    return new_groups, moved_count


def iterative_refinement(groups, data_dict, distance_threshold=0.1, max_iterations=10):
    current_groups = deepcopy(groups)
    for i in range(max_iterations):
        new_groups, moved_count = refine_groups(current_groups, data_dict, distance_threshold=distance_threshold)
        if moved_count == 0:
            print(f"Refinement stabilized after {i+1} iterations.")
            return new_groups
        current_groups = new_groups
    print("Reached maximum refinement iterations.")
    return current_groups


def optimize_group(data, bat_nums, data_source, n_clusters, seed=78825):
    """Deep sorting method"""

    # ***************** Step 1: Initial group ******************
    baseline_features = get_implicit_features(data, data_dource=data_source, derivative=[0])
    scaler0 = StandardScaler()
    X_features_0 = scaler0.fit_transform(baseline_features)

    initial_cluster_model = KMeans(n_clusters=n_clusters, init='k-means++', random_state=seed)

    initial_cluster_pred = initial_cluster_model.fit_predict(X_features_0)
    initial_groups = {i: [] for i in range(n_clusters)}
    for i, c in enumerate(initial_cluster_pred):
        initial_groups[c].append(bat_nums[i])
    print(initial_groups.values)

    # ************** Step 2: First refinement ********************
    velocity_features = get_implicit_features(data, data_dource=data_source, derivative=[1])
    scaler1 = StandardScaler()
    X_features_1 = scaler1.fit_transform(velocity_features)
    X_features_1_dic = {bat: X_features_1[idx] for idx, bat in enumerate(bat_nums)}
    refined_groups_1 = iterative_refinement(initial_groups, X_features_1_dic, distance_threshold=0.0, max_iterations=10)

    # ************** Step 3: Second refinement ********************
    acceleration_features = get_implicit_features(data, data_dource=data_source, derivative=[2])
    scaler2 = StandardScaler()
    X_features_2 = scaler2.fit_transform(acceleration_features)
    X_features_2_dic = {bat: X_features_2[idx] for idx, bat in enumerate(bat_nums)}
    refined_groups_2 = iterative_refinement(refined_groups_1, X_features_2_dic, distance_threshold=0.0, max_iterations=10)

    return list(initial_groups.values()), list(refined_groups_1.values()), list(refined_groups_2.values())
