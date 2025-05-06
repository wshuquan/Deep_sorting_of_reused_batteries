from scipy.stats import skew, kurtosis
import pandas as pd
from scipy.interpolate import make_interp_spline
from scipy.signal import savgol_filter
import numpy as np

data_length = 401


def dy_dx(x, y):
    y = savgol_filter(y, 101, 2)
    dy_dx = [(y[1]-y[0]) / (x[1]-x[0])]
    for i in range(1, len(x)):
        dy_dx.append((y[i]-y[i-1]) / (x[i]-x[i-1]))
    dy_dx = savgol_filter(dy_dx, 101, 2)
    return dy_dx


def dny_dxn(x, y, n):
    t = y
    dny_dxn = list()
    dny_dxn.append(np.array(t))
    for i in range(n):
        t = dy_dx(x, t)
        dny_dxn.append(t)
    return dny_dxn


data_file_dir = './dataset/bat_cycle_data_first_cycle.csv'
bat_cycle_data = pd.read_csv(data_file_dir, header=0, index_col=None)

data_cycle5_file_dir = './dataset/bat_cycle_data_first5_cycle.csv'
bat_cycle5_data = pd.read_csv(data_cycle5_file_dir, header=0, index_col=None)

features = {}
for i in range(1, 5):
    for j in range(1, 4):
        for k in range(1, 10):
            features[f'feature_{i}_{j}_{k}'] = list()

features['capacity'] = list()
features['voltage'] = list()
features['internal_resistance'] = list()
features['coulombic_efficiency'] = list()
features['energy_efficiency'] = list()
features['ica_1'] = list()
features['ica_2'] = list()

bat_nums = list(range(1, 61)) + list(range(63, 89))

for bat_num in bat_nums:

    print(bat_num)

    cycle_data = bat_cycle_data[bat_cycle_data['bat_num'] == bat_num]

    if len(cycle_data) == 0:
        continue

    charge_data = cycle_data[cycle_data['Step_Index'] == 12]

    CC_charge_data = charge_data[charge_data['Current(A)'] >= 1.199]
    CC_charge_time = list(CC_charge_data['Step_Time(s)'])
    CC_charge_temp = list(CC_charge_data['Aux_Temperature_1(C)'])
    CC_charge_vol = list(CC_charge_data['Voltage(V)'])
    CC_charge_vol = savgol_filter(CC_charge_vol, 21, 2)
    CC_charge_cur = list(CC_charge_data['Current(A)'])
    CC_charge_Ah = list(CC_charge_data['Charge_Capacity(Ah)'])
    CC_charge_Ah = savgol_filter(CC_charge_Ah, 21, 2)
    CC_charge_vol_, CC_charge_Ah_ = [CC_charge_vol[0]], [CC_charge_Ah[0]]
    for i in range(1, len(CC_charge_vol)):
        if (CC_charge_vol[i] > CC_charge_vol_[-1]) and (CC_charge_Ah[i] > CC_charge_Ah_[-1]):
            CC_charge_vol_.append(CC_charge_vol[i])
            CC_charge_Ah_.append(CC_charge_Ah[i])
    CC_charge_vol_new_1 = np.linspace(CC_charge_vol_[0], CC_charge_vol_[-1], data_length)
    CC_charge_Ah_new_1 = make_interp_spline(CC_charge_vol_, CC_charge_Ah_)(CC_charge_vol_new_1)
    CC_charge_dnQ_dVn = dny_dxn(CC_charge_vol_new_1, CC_charge_Ah_new_1, 2)
    features['feature_1_1_1'].append(np.mean(CC_charge_dnQ_dVn[0]))
    features['feature_1_1_2'].append(np.var(CC_charge_dnQ_dVn[0]))
    features['feature_1_1_3'].append(skew(CC_charge_dnQ_dVn[0], axis=0, bias=False))
    features['feature_1_1_4'].append(kurtosis(CC_charge_dnQ_dVn[0], axis=0, bias=False))
    features['feature_1_1_5'].append(CC_charge_dnQ_dVn[0][0])
    features['feature_1_1_6'].append(CC_charge_dnQ_dVn[0][100])
    features['feature_1_1_7'].append(CC_charge_dnQ_dVn[0][200])
    features['feature_1_1_8'].append(CC_charge_dnQ_dVn[0][300])
    features['feature_1_1_9'].append(CC_charge_dnQ_dVn[0][400])
    features['feature_1_2_1'].append(np.mean(CC_charge_dnQ_dVn[1]))
    features['feature_1_2_2'].append(np.var(CC_charge_dnQ_dVn[1]))
    features['feature_1_2_3'].append(skew(CC_charge_dnQ_dVn[1], axis=0, bias=False))
    features['feature_1_2_4'].append(kurtosis(CC_charge_dnQ_dVn[1], axis=0, bias=False))
    features['feature_1_2_5'].append(CC_charge_dnQ_dVn[1][0])
    features['feature_1_2_6'].append(CC_charge_dnQ_dVn[1][100])
    features['feature_1_2_7'].append(CC_charge_dnQ_dVn[1][200])
    features['feature_1_2_8'].append(CC_charge_dnQ_dVn[1][300])
    features['feature_1_2_9'].append(CC_charge_dnQ_dVn[1][400])
    features['feature_1_3_1'].append(np.mean(CC_charge_dnQ_dVn[2]))
    features['feature_1_3_2'].append(np.var(CC_charge_dnQ_dVn[2]))
    features['feature_1_3_3'].append(skew(CC_charge_dnQ_dVn[2], axis=0, bias=False))
    features['feature_1_3_4'].append(kurtosis(CC_charge_dnQ_dVn[2], axis=0, bias=False))
    features['feature_1_3_5'].append(CC_charge_dnQ_dVn[2][0])
    features['feature_1_3_6'].append(CC_charge_dnQ_dVn[2][100])
    features['feature_1_3_7'].append(CC_charge_dnQ_dVn[2][200])
    features['feature_1_3_8'].append(CC_charge_dnQ_dVn[2][300])
    features['feature_1_3_9'].append(CC_charge_dnQ_dVn[2][400])

    CC_charge_Ah_new_2 = np.linspace(CC_charge_Ah_[0], CC_charge_Ah_[-1], data_length)
    CC_charge_vol_new_2 = make_interp_spline(CC_charge_Ah_, CC_charge_vol_)(CC_charge_Ah_new_2)
    CC_charge_dnV_dQn = dny_dxn(CC_charge_Ah_new_2, CC_charge_vol_new_2, 2)
    features['feature_2_1_1'].append(np.mean(CC_charge_dnV_dQn[0]))
    features['feature_2_1_2'].append(np.var(CC_charge_dnV_dQn[0]))
    features['feature_2_1_3'].append(skew(CC_charge_dnV_dQn[0], axis=0, bias=False))
    features['feature_2_1_4'].append(kurtosis(CC_charge_dnV_dQn[0], axis=0, bias=False))
    features['feature_2_1_5'].append(CC_charge_dnV_dQn[0][0])
    features['feature_2_1_6'].append(CC_charge_dnV_dQn[0][100])
    features['feature_2_1_7'].append(CC_charge_dnV_dQn[0][200])
    features['feature_2_1_8'].append(CC_charge_dnV_dQn[0][300])
    features['feature_2_1_9'].append(CC_charge_dnV_dQn[0][400])
    features['feature_2_2_1'].append(np.mean(CC_charge_dnV_dQn[1]))
    features['feature_2_2_2'].append(np.var(CC_charge_dnV_dQn[1]))
    features['feature_2_2_3'].append(skew(CC_charge_dnV_dQn[1], axis=0, bias=False))
    features['feature_2_2_4'].append(kurtosis(CC_charge_dnV_dQn[1], axis=0, bias=False))
    features['feature_2_2_5'].append(CC_charge_dnV_dQn[1][0])
    features['feature_2_2_6'].append(CC_charge_dnV_dQn[1][100])
    features['feature_2_2_7'].append(CC_charge_dnV_dQn[1][200])
    features['feature_2_2_8'].append(CC_charge_dnV_dQn[1][300])
    features['feature_2_2_9'].append(CC_charge_dnV_dQn[1][400])
    features['feature_2_3_1'].append(np.mean(CC_charge_dnV_dQn[2]))
    features['feature_2_3_2'].append(np.var(CC_charge_dnV_dQn[2]))
    features['feature_2_3_3'].append(skew(CC_charge_dnV_dQn[2], axis=0, bias=False))
    features['feature_2_3_4'].append(kurtosis(CC_charge_dnV_dQn[2], axis=0, bias=False))
    features['feature_2_3_5'].append(CC_charge_dnV_dQn[2][0])
    features['feature_2_3_6'].append(CC_charge_dnV_dQn[2][100])
    features['feature_2_3_7'].append(CC_charge_dnV_dQn[2][200])
    features['feature_2_3_8'].append(CC_charge_dnV_dQn[2][300])
    features['feature_2_3_9'].append(CC_charge_dnV_dQn[2][400])

    CV_charge_data = charge_data[charge_data['Current(A)'] < 1.199]
    CV_charge_time = [t - list(CV_charge_data['Step_Time(s)'])[0] for t in list(CV_charge_data['Step_Time(s)'])]
    CV_charge_temp = list(CV_charge_data['Aux_Temperature_1(C)'])
    CV_charge_vol = list(CV_charge_data['Voltage(V)'])
    CV_charge_cur = list(CV_charge_data['Current(A)'])
    CV_charge_cur = savgol_filter(CV_charge_cur, 21, 2)
    CV_charge_Ah = list(CV_charge_data['Charge_Capacity(Ah)'])
    CV_charge_Ah = savgol_filter(CV_charge_Ah, 21, 2)
    CV_charge_time_new = np.linspace(CV_charge_time[0], CV_charge_time[-1], data_length)
    CV_charge_cur_new = make_interp_spline(CV_charge_time, CV_charge_cur)(CV_charge_time_new)
    CV_charge_Ah_new = make_interp_spline(CV_charge_time, CV_charge_Ah)(CV_charge_time_new)
    CV_charge_dnI_dtn = dny_dxn(CV_charge_time_new, CV_charge_cur_new, 2)
    features['feature_3_1_1'].append(np.mean(CV_charge_dnI_dtn[0]))
    features['feature_3_1_2'].append(np.var(CV_charge_dnI_dtn[0]))
    features['feature_3_1_3'].append(skew(CV_charge_dnI_dtn[0], axis=0, bias=False))
    features['feature_3_1_4'].append(kurtosis(CV_charge_dnI_dtn[0], axis=0, bias=False))
    features['feature_3_1_5'].append(CV_charge_dnI_dtn[0][0])
    features['feature_3_1_6'].append(CV_charge_dnI_dtn[0][100])
    features['feature_3_1_7'].append(CV_charge_dnI_dtn[0][200])
    features['feature_3_1_8'].append(CV_charge_dnI_dtn[0][300])
    features['feature_3_1_9'].append(CV_charge_dnI_dtn[0][400])
    features['feature_3_2_1'].append(np.mean(CV_charge_dnI_dtn[1]))
    features['feature_3_2_2'].append(np.var(CV_charge_dnI_dtn[1]))
    features['feature_3_2_3'].append(skew(CV_charge_dnI_dtn[1], axis=0, bias=False))
    features['feature_3_2_4'].append(kurtosis(CV_charge_dnI_dtn[1], axis=0, bias=False))
    features['feature_3_2_5'].append(CV_charge_dnI_dtn[1][0])
    features['feature_3_2_6'].append(CV_charge_dnI_dtn[1][100])
    features['feature_3_2_7'].append(CV_charge_dnI_dtn[1][200])
    features['feature_3_2_8'].append(CV_charge_dnI_dtn[1][300])
    features['feature_3_2_9'].append(CV_charge_dnI_dtn[1][400])
    features['feature_3_3_1'].append(np.mean(CV_charge_dnI_dtn[2]))
    features['feature_3_3_2'].append(np.var(CV_charge_dnI_dtn[2]))
    features['feature_3_3_3'].append(skew(CV_charge_dnI_dtn[2], axis=0, bias=False))
    features['feature_3_3_4'].append(kurtosis(CV_charge_dnI_dtn[2], axis=0, bias=False))
    features['feature_3_3_5'].append(CV_charge_dnI_dtn[2][0])
    features['feature_3_3_6'].append(CV_charge_dnI_dtn[2][100])
    features['feature_3_3_7'].append(CV_charge_dnI_dtn[2][200])
    features['feature_3_3_8'].append(CV_charge_dnI_dtn[2][300])
    features['feature_3_3_9'].append(CV_charge_dnI_dtn[2][400])

    ch_rest_data = cycle_data[cycle_data['Step_Index'] == 13]
    ch_rest_time = list(ch_rest_data['Step_Time(s)'])
    ch_rest_temp = list(ch_rest_data['Aux_Temperature_1(C)'])
    ch_rest_vol = list(ch_rest_data['Voltage(V)'])
    ch_rest_vol = savgol_filter(ch_rest_vol, 21, 2)
    ch_rest_time_new = np.linspace(ch_rest_time[0], ch_rest_time[-1], data_length)
    ch_rest_vol_new = make_interp_spline(ch_rest_time[:-1], ch_rest_vol[:-1])(ch_rest_time_new)
    ch_rest_vol_new = savgol_filter(ch_rest_vol_new, 21, 2)
    ch_rest_dnV_dtn = dny_dxn(ch_rest_time_new, ch_rest_vol_new, 2)
    features['feature_4_1_1'].append(np.mean(ch_rest_dnV_dtn[0]))
    features['feature_4_1_2'].append(np.var(ch_rest_dnV_dtn[0]))
    features['feature_4_1_3'].append(skew(ch_rest_dnV_dtn[0], axis=0, bias=False))
    features['feature_4_1_4'].append(kurtosis(ch_rest_dnV_dtn[0], axis=0, bias=False))
    features['feature_4_1_5'].append(ch_rest_dnV_dtn[0][0])
    features['feature_4_1_6'].append(ch_rest_dnV_dtn[0][100])
    features['feature_4_1_7'].append(ch_rest_dnV_dtn[0][200])
    features['feature_4_1_8'].append(ch_rest_dnV_dtn[0][300])
    features['feature_4_1_9'].append(ch_rest_dnV_dtn[0][400])
    features['feature_4_2_1'].append(np.mean(ch_rest_dnV_dtn[1]))
    features['feature_4_2_2'].append(np.var(ch_rest_dnV_dtn[1]))
    features['feature_4_2_3'].append(skew(ch_rest_dnV_dtn[1], axis=0, bias=False))
    features['feature_4_2_4'].append(kurtosis(ch_rest_dnV_dtn[1], axis=0, bias=False))
    features['feature_4_2_5'].append(ch_rest_dnV_dtn[1][0])
    features['feature_4_2_6'].append(ch_rest_dnV_dtn[1][100])
    features['feature_4_2_7'].append(ch_rest_dnV_dtn[1][200])
    features['feature_4_2_8'].append(ch_rest_dnV_dtn[1][300])
    features['feature_4_2_9'].append(ch_rest_dnV_dtn[1][400])
    features['feature_4_3_1'].append(np.mean(ch_rest_dnV_dtn[2]))
    features['feature_4_3_2'].append(np.var(ch_rest_dnV_dtn[2]))
    features['feature_4_3_3'].append(skew(ch_rest_dnV_dtn[2], axis=0, bias=False))
    features['feature_4_3_4'].append(kurtosis(ch_rest_dnV_dtn[2], axis=0, bias=False))
    features['feature_4_3_5'].append(ch_rest_dnV_dtn[2][0])
    features['feature_4_3_6'].append(ch_rest_dnV_dtn[2][100])
    features['feature_4_3_7'].append(ch_rest_dnV_dtn[2][200])
    features['feature_4_3_8'].append(ch_rest_dnV_dtn[2][300])
    features['feature_4_3_9'].append(ch_rest_dnV_dtn[2][400])

    capacity = list(cycle_data[cycle_data['Step_Index'] == 15]['Discharge_Capacity(Ah)'])[-1]
    features['capacity'].append(capacity)

    voltage = np.mean(list(charge_data['Voltage(V)']))
    features['voltage'].append(voltage)

    internal_resistance = list(cycle_data[cycle_data['Step_Index'] == 14]['Internal_Resistance(Ohm)'])[0]
    features['internal_resistance'].append(internal_resistance)

    cycle5_data = bat_cycle5_data[bat_cycle5_data['bat_num'] == bat_num]
    cycle5_charge_data = cycle5_data[cycle5_data['Step_Index'] == 22]
    cycle5_discharge_data = cycle5_data[cycle5_data['Step_Index'] == 24]

    coulombic_efficiency = list(cycle5_discharge_data['Discharge_Capacity(Ah)'])[-1] / list(cycle5_charge_data['Charge_Capacity(Ah)'])[-1]
    features['coulombic_efficiency'].append(coulombic_efficiency)

    energy_efficiency = list(cycle5_discharge_data['Discharge_Energy(Wh)'])[-1] / list(cycle5_charge_data['Charge_Energy(Wh)'])[-1]
    features['energy_efficiency'].append(energy_efficiency)

    features['ica_1'].append(np.max(CC_charge_dnQ_dVn[1]))
    CC_charge_vol_new_1 = np.linspace(3.5, 4.5, 100)
    CC_charge_dnQ_dVn_1 = np.sin(CC_charge_vol_new_1)
    mask = (CC_charge_vol_new_1 >= 3.8) & (CC_charge_vol_new_1 <= 4.1)
    x_selected = CC_charge_vol_new_1[mask]
    y_selected = CC_charge_dnQ_dVn_1[mask]
    area = np.trapz(y_selected, x_selected)
    features['ica_2'].append(area)

features['bat_num'] = bat_nums

features = pd.DataFrame(features)
features.to_csv('./dataset/features.csv')

