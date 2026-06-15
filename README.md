🏏 IPL Score & Match Prediction using Machine Learning
�
�
�
�
Load image
Load image
Load image
Load image
Predicts final innings score and match winner in real-time using ball-by-ball IPL data.
📌 Project Overview
Model
Type
Result
Score Prediction
XGBoost Regressor
MAE: 19.89 runs
Match Winner
XGBoost Classifier
Accuracy: 66.05%
📂 Project Structure
Code
🔧 Steps Performed
1️⃣ Data Cleaning
Dataset: 2,83,678 rows → 68,814 rows (IPL T20 filtered)
Dropped high-null columns: extra_type, wicket_kind, player_out, fielders, etc.
Filled runs_target NaN with 0 (1st innings has no target)
Fixed win_outcome NaN → 'no_result'
2️⃣ Feature Engineering
Feature
Formula
current_run_rate
team_runs / (team_balls / 6)
required_run_rate
runs_needed / overs_remaining
balls_remaining
120 - team_balls
wickets_remaining
10 - team_wicket
pressure_index
RRR / CRR
is_powerplay
1 if over ≤ 6
is_death_over
1 if over ≥ 16
3️⃣ Encoding
Label encoded: batting_team, bowling_team, batter, bowler, venue, city, stage, toss_winner, toss_decision
4️⃣ Train/Test Split
Split by match_id (not randomly) to avoid data leakage
80% train (232 matches) / 20% test (59 matches)
5️⃣ Models
Score Prediction: XGBoost Regressor on 1st innings data
Match Winner: XGBoost Classifier on 2nd innings data (overs 1–18 only)
🚀 How to Run
Python
🎯 Live Prediction
Predict 1st Innings Score
Python
Predict Match Winner
Python
⚠️ Key Challenges & Fixes
Challenge
Fix
100% accuracy (data leakage)
win_outcome had margin not team name → used match_won_by
All-zero target
Correct target column fixed class balance to 50/50
Last over leakage
Trained only on overs 1–18
runs_target NaN in 1st innings
Filled with 0
🛠️ Tech Stack
Python 3, Pandas, NumPy
XGBoost, Scikit-learn
Google Colab
GitHub
📊 Results
Metric
Value
Score MAE
~20 runs
Winner Accuracy
66.05%
Train/Test Split
80/20 by match
Dataset Size
68,814 rows
🔮 Future Work
[ ] Streamlit web app for live predictions
[ ] Add player recent form features
[ ] LSTM model for sequence prediction
[ ] Deploy on cloud
👤 Author
GADDAM SAI KRISHNA
B.Tech  — B.V.Raju instiution of technology , narsapur
[LinkedIn] | Saikrishna-ctrlkit
