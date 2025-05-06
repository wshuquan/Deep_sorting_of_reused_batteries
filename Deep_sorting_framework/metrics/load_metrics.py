import pickle

steps= ['initial_grouping', 'first_refinement', 'second_refinement']

for step in steps:
    print(f'\n************* Metrics_{step}*************')

    file_dir = f'./metrics_deep_sorting_{step}.pickle'

    with open(file_dir, 'rb') as handle:
        metrics = pickle.load(handle)

    for key in metrics.keys():
        print(f'********{key}********\n{metrics[key]}')

