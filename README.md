# 🏏 IPL Score & Match Prediction
### *Real-time Cricket Intelligence using Machine Learning*
🌐 Live App: https://ipl-prediction-tkitlhbkdu9ddqcqgk4pss.streamlit.app/

<div align="center">

![IPL Banner](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&pause=1000&color=FF6B00&center=true&vCenter=true&width=600&lines=IPL+Score+%26+Match+Prediction+%F0%9F%8F%8F;Powered+by+XGBoost+%F0%9F%A4%96;Real-time+Ball-by-Ball+Analysis+%F0%9F%93%8A;66%25+Match+Winner+Accuracy+%E2%9C%85)

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML%20Model-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Colab](https://img.shields.io/badge/Google%20Colab-Notebook-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete%20✅-brightgreen?style=for-the-badge)]()

<br/>

> **Predict IPL final scores and match winners in real-time using ball-by-ball data and Machine Learning**

</div>

---

## 🎯 What Does This Project Do?

<table>
<tr>
<td width="50%">

### 🔢 Score Prediction
Given the **current match state** during the 1st innings, predict what the **final score** will be at the end of 20 overs.

**Example:**
> Mumbai Indians: 85/2 in 10 overs  
> 🤖 Model Predicts → **172 runs**

</td>
<td width="50%">

### 🏆 Winner Prediction
During the **2nd innings chase**, predict which team will **win the match** with live win probabilities.

**Example:**
> CSK chasing 175 | 120/5 in 15 overs  
> 🤖 Model Predicts → **CSK: 42% | MI: 58%**

</td>
</tr>
</table>

---

## 📊 Results at a Glance

<div align="center">

| 🎯 Model | 📐 Algorithm | 📏 Metric | 🏅 Score |
|:--------:|:------------:|:---------:|:--------:|
| Score Prediction | XGBoost Regressor | Mean Absolute Error | **~20 runs** |
| Match Winner | XGBoost Classifier | Accuracy | **66.05%** |
| Dataset Size | Ball-by-ball IPL | Rows after cleaning | **68,814** |
| Train/Test Split | By Match ID | No data leakage | **80% / 20%** |

</div>

---

## 🗂️ Project Structure

```
📁 IPL-Prediction/
│
├── 📓 IPL_Prediction.ipynb       ← Main notebook (run this!)
├── 🐍 ipl_exact_prediction.py    ← Full pipeline as Python script
├── 📊 IPL.csv                    ← Ball-by-ball dataset
│
├── 🤖 Models/
│   ├── score_model.pkl           ← Trained XGBoost Regressor
│   ├── match_model.pkl           ← Trained XGBoost Classifier
│   └── label_encoders.pkl        ← Saved encoders for all categories
│
└── 📄 README.md
```

---

## 🔄 Project Pipeline

```
Raw IPL Data (2,83,678 rows)
        │
        ▼
🧹 Data Cleaning
   ├── Drop high-null columns (extra_type, wicket_kind, fielders...)
   ├── Fill runs_target NaN → 0 (1st innings)
   ├── Fill win_outcome NaN → 'no_result'
   └── Result: 68,814 clean rows
        │
        ▼
⚙️ Feature Engineering
   ├── current_run_rate = team_runs / (team_balls/6)
   ├── required_run_rate = runs_needed / overs_remaining
   ├── balls_remaining = 120 - team_balls
   ├── wickets_remaining = 10 - team_wicket
   ├── pressure_index = RRR / CRR
   ├── is_powerplay (over ≤ 6)
   └── is_death_over (over ≥ 16)
        │
        ▼
🔤 Label Encoding
   └── batting_team, bowling_team, batter, bowler, venue, city...
        │
        ▼
✂️ Train/Test Split (by match_id — NO leakage)
   ├── Train: 232 matches (54,934 rows)
   └── Test:   59 matches (13,880 rows)
        │
        ▼
🤖 XGBoost Models
   ├── Regressor  → Score Prediction (MAE: 19.89 runs)
   └── Classifier → Match Winner    (Accuracy: 66.05%)
        │
        ▼
🎯 Live Prediction Function
```

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy xgboost scikit-learn joblib
```

### Run in Google Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com)

### Run Locally
```bash
# 1. Clone this repo
git clone https://github.com/YOUR_USERNAME/IPL-Prediction.git
cd IPL-Prediction

# 2. Install requirements
pip install -r requirements.txt

# 3. Run the notebook
jupyter notebook IPL_Prediction.ipynb
```

---

## 🎮 Live Prediction Examples

### 🔢 Predict Final Score (1st Innings)
```python
predict_score(
    batting_team  = 'Mumbai Indians',
    bowling_team  = 'Chennai Super Kings',
    batter        = 'RG Sharma',
    bowler        = 'R Jadeja',
    venue         = 'Wankhede Stadium',
    city          = 'Mumbai',
    team_runs     = 85,       # Current score
    team_balls    = 60,       # Balls bowled
    team_wicket   = 2,        # Wickets fallen
    bat_pos       = 1,
    batter_runs   = 45,
    batter_balls  = 32,
    over          = 10,
    ball          = 1,
    toss_winner   = 'Mumbai Indians',
    toss_decision = 'bat'
)
```
```
════════════════════════════════════════
  Mumbai Indians vs Chennai Super Kings
  Current: 85/2 in 10.1 overs
  CRR: 8.50
  ✅ Predicted Final Score: 172 runs
════════════════════════════════════════
```

---

### 🏆 Predict Match Winner (2nd Innings)
```python
predict_winner(
    batting_team  = 'Chennai Super Kings',
    bowling_team  = 'Mumbai Indians',
    batter        = 'MS Dhoni',
    bowler        = 'JJ Bumrah',
    venue         = 'Wankhede Stadium',
    city          = 'Mumbai',
    team_runs     = 120,      # Current score
    team_balls    = 90,       # Balls faced
    team_wicket   = 5,        # Wickets down
    bat_pos       = 5,
    batter_runs   = 20,
    batter_balls  = 15,
    over          = 15,
    ball          = 1,
    runs_target   = 175,      # Target to chase
    toss_winner   = 'Mumbai Indians',
    toss_decision = 'bat'
)
```
```
════════════════════════════════════════
  Chennai Super Kings vs Mumbai Indians
  Chasing 175 | Need 55 off 30 balls
  Score: 120/5 in 15.1 overs
  CRR: 8.00  |  RRR: 11.00
  🏏 Chennai Super Kings : 42.3%
  🎳 Mumbai Indians      : 57.7%
════════════════════════════════════════
```

---

## ⚙️ Feature Engineering Details

| Feature | Formula | Purpose |
|---------|---------|---------|
| `current_run_rate` | `team_runs / (team_balls/6)` | Batting momentum |
| `required_run_rate` | `runs_needed / overs_remaining` | Chase difficulty |
| `balls_remaining` | `120 - team_balls` | Time left |
| `wickets_remaining` | `10 - team_wicket` | Resources left |
| `pressure_index` | `RRR / CRR` | Match pressure |
| `is_powerplay` | `over ≤ 6` | Field restriction phase |
| `is_death_over` | `over ≥ 16` | Death overs phase |
| `batting_won_toss` | `batting_team == toss_winner` | Toss advantage |

---

## 🧠 Model Details

<table>
<tr>
<td width="50%">

### XGBoost Regressor (Score)
```
n_estimators  = 300
max_depth     = 6
learning_rate = 0.05
subsample     = 0.8
colsample     = 0.8
random_state  = 42
```
**Result: MAE = 19.89 runs**

</td>
<td width="50%">

### XGBoost Classifier (Winner)
```
n_estimators  = 300
max_depth     = 5
learning_rate = 0.05
subsample     = 0.8
colsample     = 0.8
eval_metric   = logloss
```
**Result: Accuracy = 66.05%**

</td>
</tr>
</table>

---

## 🐛 Challenges & Solutions

| ❌ Challenge | ✅ Fix Applied |
|-------------|--------------|
| **100% accuracy** — data leakage suspected | Found `win_outcome` had margin ("140 runs") not team name |
| **All-zero target** — model couldn't learn | Used `match_won_by` column which has actual team name |
| **Last-over leakage** | Trained only on overs 1–18, excluded final over |
| **Class imbalance** | Correct target gave perfect 50/50 split (13,263 vs 13,137) |
| **runs_target NaN** in 1st innings | Filled with 0 — no target exists in 1st innings |

---

## 📈 Dataset Info

```
Source        : Ball-by-ball IPL Dataset
Original Rows : 2,83,678
Clean Rows    : 68,814
Columns       : 65 → 50 (after dropping nulls)
Matches       : 291 total
Seasons       : IPL Season 1 to latest
Teams         : All IPL franchises
```

---

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=for-the-badge)
![Google Colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

</div>

---

## 🔮 Future Improvements

- [ ] 🌐 **Streamlit Web App** — interactive live prediction dashboard
- [ ] 📱 **Mobile App** — predict from your phone during live matches
- [ ] 📉 **LSTM Model** — sequence-based deep learning for better accuracy
- [ ] 🌤️ **Weather & Pitch Data** — add external match conditions
- [ ] 🏃 **Player Form** — rolling average of last 5 match performance
- [ ] ☁️ **Cloud Deployment** — host on AWS/Heroku for public access

---

## 👤 Author

<div align="center">

**GADDAM SAI KRISHNA**

*B.Tech [AI & DS] — B.V.Raju Institute of Technology, Nasapur*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/YOUR_PROFILE)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/YOUR_USERNAME)

</div>

---

## ⭐ Support

If you found this project helpful, please give it a **⭐ Star** on GitHub!

---

<div align="center">

*Made with ❤️ and 🏏 by [Your Name]*

</div>
