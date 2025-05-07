# 🚀 Code for: Deep sorting of reused batteries for enabling long-term consistency grouping with unknown prior conditions

---

## 📝 Abstract
When reusing lithium-ion batteries retired from electric vehicles, the main challenge lies in accurately grouping cells to ensure stable, long-term consistency, especially given their unknown usage histories and heterogeneous aging pathways. Here, we propose a deep sorting framework that leverages implicit features derived from a single charge cycle, achieving improved performance compared to conventional explicit feature-based methods. Our method extracts 108 implicit features from characteristic curves and their derivatives, followed by a two-step refinement based on derivative features. This strategy extends usable service life by 30% and reduces aging differences by 40% compared to state-of-the-art methods, highlighting the broader potential of implicit feature-based decision-making in complex systems.

---

## 📚 Introduction
With the increasing retirement of electric vehicle batteries, **effective second-life utilization** has become critical. Traditional sorting methods mainly rely on **explicit features** such as capacity and internal resistance. However, these features often fail to predict the batteries' long-term aging behavior accurately.

This project proposes a **deep sorting strategy** combining:
- **Feature Engineering**: Extract 108 implicit features based on characteristic curves (voltage–capacity, current–time, voltage–time curves) and their first- and second-order derivatives.
- **Deep Sorting Framework**: Perform three-step sorting — initial grouping by baseline features, then refining by velocity and acceleration features to achieve superior consistency.

---

![Deep sorting framework](https://github.com/wshuquan/Deep_sorting_of_reused_batteries/blob/main/Deep_sorting_framework.png)

---

## 🌟 Highlights
- **Single-Cycle Based Sorting**: Only requires one charge cycle, greatly reducing testing time.  
- **Implicit Feature Extraction**: Extends traditional feature sets to capture deeper degradation signatures.  
- **Hierarchical Grouping**: Refines initial groups with additional dynamic features for long-term consistency.  
- **Real-world Validation**: Achieves a 30% service life extension compared to existing sorting methods.

---

## 🏗️ Project Structure
```bash
├── Feature_engineering
│   ├── 1_cycle_data_extraction.py
│   ├── 2_feature_extraction.py
│   ├── 3_capa_trajectory_extraction.py
│   └── dataset/
├── Deep_sorting_framework
│   ├── main.py
│   ├── metrics.py       # computes evaluation metrics
│   ├── model.py         # implements the deep sorting algorithm
│   └── metrics/
│       └── load_metrics.py  # loads and visualizes saved metrics
├── Deep_sorting_framework.png
```

---

## ⚙️ Requirements
- Python 3.8  
- numpy == 1.21.5  
- scikit-learn == 1.0.2  

Install dependencies:
```bash
pip install numpy==1.21.5 scikit-learn==1.0.2
```

---

## 📊 Raw dataset  
Please download the raw dataset from Zenodo (DOI: [10.5281/zenodo.14859405](https://doi.org/10.5281/zenodo.14859405)) and extract it into the root of this repository before running any scripts.

---

## 🚀 Usage Instructions

### 1. Download Dataset
Download the raw dataset from Zenodo and extract it into the root directory:
```bash
# In the project root directory
wget https://zenodo.org/record/14859405/files/Second_life_phase.zip
unzip second_life_phase.zip
```

### 2. Feature Engineering
```bash
cd Feature_engineering

# 1) Extract single cycle data
python 1_cycle_data_extraction.py

# 2) Extract 108 implicit features
python 2_feature_extraction.py

# 3) Extract capacity trajectories during second-life usage
python 3_capa_trajectory_extraction.py
```
Processed data will be saved under: `Feature_engineering/dataset/`

### 3. Deep Sorting
```bash
cd ../Deep_sorting_framework

# Perform deep sorting
python main.py
```
Metrics will be computed by `metrics.py` and results saved automatically.

To load and view saved metrics:
```bash
# Inside Deep_sorting_framework/metrics
python load_metrics.py
```

---

## 📄 Citation
If you use this code, please cite:  
> Wang, S., Gao, F., Tian, H.  
> *Deep sorting of reused batteries for enabling long-term consistency grouping with unknown prior conditions*.  
> Cell Reports Physical Science (2025). DOI: (to be updated)

---

## 📬 Contact
For questions or collaboration, contact:  
**wshuquan@mail.sdu.edu.cn**

---
