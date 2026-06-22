import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load models
score_model = joblib.load('score_model.pkl')
match_model = joblib.load('match_model.pkl')
le_dict     = joblib.load('label_encoders.pkl')

def safe_encode(le, val):
    val = str(val)
    return list(le.classes_).index(val) if val in le.classes_ else -1

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="IPL Predictor 🏏",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Score & Match Predictor")
st.markdown("*Real-time predictions using Machine Learning*")

# ── SIDEBAR ──
mode = st.sidebar.radio(
    "Select Prediction Type",
    ["🔢 Score Prediction (1st Innings)",
     "🏆 Match Winner (2nd Innings)"]
)

teams = sorted(le_dict['batting_team'].classes_)
venues = sorted(le_dict['venue'].classes_)
cities = sorted(le_dict['city'].classes_)

# ══════════════════════════════════
# SCORE PREDICTION
# ══════════════════════════════════
if mode == "🔢 Score Prediction (1st Innings)":
    st.header("🔢 Predict Final Score")

    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox("Batting Team", teams)
        bowling_team = st.selectbox("Bowling Team",
                        [t for t in teams if t != batting_team])
        venue  = st.selectbox("Venue", venues)
        city   = st.selectbox("City", cities)

    with col2:
        team_runs   = st.number_input("Current Runs",   0, 300, 85)
        team_wicket = st.number_input("Wickets Fallen", 0, 10,  2)
        over        = st.number_input("Current Over",   1, 20,  10)
        ball        = st.number_input("Current Ball",   1, 6,   1)

    col3, col4 = st.columns(2)
    with col3:
        batter      = st.text_input("Batter Name", "RG Sharma")
        batter_runs = st.number_input("Batter Runs", 0, 200, 45)
        batter_balls= st.number_input("Batter Balls",0, 120, 32)
        bat_pos     = st.number_input("Bat Position", 1, 11,  1)
    with col4:
        bowler        = st.text_input("Bowler Name", "R Jadeja")
        toss_winner   = st.selectbox("Toss Winner", teams)
        toss_decision = st.selectbox("Toss Decision", ["bat","field"])
        month         = st.number_input("Month", 1, 12, 4)

    if st.button("🔮 Predict Score", use_container_width=True):
        team_balls = int(over * 6 + ball - 1)
        crr = team_runs / (team_balls/6) if team_balls > 0 else 0
        balls_remaining = max(0, 120 - team_balls)

        row = pd.DataFrame([{
            'team_runs': team_runs, 'team_balls': team_balls,
            'team_wicket': team_wicket,
            'wickets_remaining': 10 - team_wicket,
            'current_run_rate': crr,
            'balls_remaining': balls_remaining,
            'over': over, 'ball': ball, 'bat_pos': bat_pos,
            'batter_runs': batter_runs, 'batter_balls': batter_balls,
            'is_powerplay': int(over<=6),
            'is_death_over': int(over>=16),
            'batting_won_toss': int(batting_team==toss_winner),
            'toss_bat': int(toss_decision=='bat'),
            'batting_team_enc': safe_encode(le_dict['batting_team'], batting_team),
            'bowling_team_enc': safe_encode(le_dict['bowling_team'], bowling_team),
            'batter_enc': safe_encode(le_dict['batter'], batter),
            'bowler_enc': safe_encode(le_dict['bowler'], bowler),
            'venue_enc': safe_encode(le_dict['venue'], venue),
            'city_enc': safe_encode(le_dict['city'], city),
            'month': month, 'day': 15
        }])

        score_features = [
            'team_runs','team_balls','team_wicket','wickets_remaining',
            'current_run_rate','balls_remaining','over','ball','bat_pos',
            'batter_runs','batter_balls','is_powerplay','is_death_over',
            'batting_won_toss','toss_bat','batting_team_enc',
            'bowling_team_enc','batter_enc','bowler_enc',
            'venue_enc','city_enc','month','day'
        ]

        pred = int(score_model.predict(row[score_features])[0])

        st.success(f"### 🎯 Predicted Final Score: {pred} runs")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Current Score", f"{team_runs}/{team_wicket}")
        col_b.metric("Current RR", f"{crr:.2f}")
        col_c.metric("Predicted Total", f"{pred} runs")

# ══════════════════════════════════
# MATCH WINNER PREDICTION
# ══════════════════════════════════
else:
    st.header("🏆 Predict Match Winner")

    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox("Batting Team (Chasing)", teams)
        bowling_team = st.selectbox("Bowling Team (Defending)",
                        [t for t in teams if t != batting_team])
        venue  = st.selectbox("Venue", venues)
        city   = st.selectbox("City", cities)
        runs_target = st.number_input("Target Runs", 100, 300, 175)

    with col2:
        team_runs   = st.number_input("Current Runs",   0, 300, 120)
        team_wicket = st.number_input("Wickets Fallen", 0, 10,  5)
        over        = st.number_input("Current Over",   1, 19,  15)
        ball        = st.number_input("Current Ball",   1, 6,   1)

    col3, col4 = st.columns(2)
    with col3:
        batter       = st.text_input("Batter Name", "MS Dhoni")
        batter_runs  = st.number_input("Batter Runs",  0, 200, 20)
        batter_balls = st.number_input("Batter Balls", 0, 120, 15)
        bat_pos      = st.number_input("Bat Position", 1, 11,  5)
    with col4:
        bowler        = st.text_input("Bowler Name", "JJ Bumrah")
        toss_winner   = st.selectbox("Toss Winner", teams)
        toss_decision = st.selectbox("Toss Decision", ["bat","field"])
        month         = st.number_input("Month", 1, 12, 4)

    if st.button("🔮 Predict Winner", use_container_width=True):
        team_balls = int(over * 6 + ball - 1)
        crr = team_runs / (team_balls/6) if team_balls > 0 else 0
        balls_remaining = max(0, 120 - team_balls)
        overs_remaining = balls_remaining / 6
        runs_needed = runs_target - team_runs
        rrr = runs_needed / overs_remaining if overs_remaining > 0 else 0
        pressure = rrr / crr if crr > 0 else 0

        row = pd.DataFrame([{
            'team_runs': team_runs, 'team_balls': team_balls,
            'team_wicket': team_wicket,
            'wickets_remaining': 10 - team_wicket,
            'current_run_rate': crr,
            'required_run_rate': max(0, rrr),
            'balls_remaining': balls_remaining,
            'runs_target': runs_target,
            'runs_needed': runs_needed,
            'pressure_index': pressure,
            'over': over, 'ball': ball, 'bat_pos': bat_pos,
            'batter_runs': batter_runs, 'batter_balls': batter_balls,
            'is_powerplay': int(over<=6),
            'is_death_over': int(over>=16),
            'batting_won_toss': int(batting_team==toss_winner),
            'toss_bat': int(toss_decision=='bat'),
            'batting_team_enc': safe_encode(le_dict['batting_team'], batting_team),
            'bowling_team_enc': safe_encode(le_dict['bowling_team'], bowling_team),
            'batter_enc': safe_encode(le_dict['batter'], batter),
            'bowler_enc': safe_encode(le_dict['bowler'], bowler),
            'venue_enc': safe_encode(le_dict['venue'], venue),
            'city_enc': safe_encode(le_dict['city'], city),
            'month': month, 'day': 15
        }])

        match_features = [
            'team_runs','team_balls','team_wicket','wickets_remaining',
            'current_run_rate','required_run_rate','balls_remaining',
            'runs_target','runs_needed','pressure_index','over','ball',
            'bat_pos','batter_runs','batter_balls','is_powerplay',
            'is_death_over','batting_won_toss','toss_bat',
            'batting_team_enc','bowling_team_enc','batter_enc',
            'bowler_enc','venue_enc','city_enc','month','day'
        ]

        proba = match_model.predict_proba(row[match_features])[0]
        bat_pct  = round(proba[1] * 100, 1)
        bowl_pct = round(proba[0] * 100, 1)

        st.markdown("### 🏆 Win Probability")
        col_a, col_b = st.columns(2)
        col_a.metric(f"🏏 {batting_team}", f"{bat_pct}%",
                     delta="Chasing")
        col_b.metric(f"🎳 {bowling_team}", f"{bowl_pct}%",
                     delta="Defending")

        st.progress(int(bat_pct))

        col_x, col_y, col_z = st.columns(3)
        col_x.metric("Runs Needed", int(runs_needed))
        col_y.metric("Balls Left",  balls_remaining)
        col_z.metric("RRR", f"{rrr:.2f}")

        if bat_pct > 60:
            st.success(f"✅ {batting_team} likely to WIN!")
        elif bowl_pct > 60:
            st.error(f"❌ {batting_team} likely to LOSE!")
        else:
            st.warning("⚠️ Too close to call!")
