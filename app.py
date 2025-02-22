import streamlit as st
import pandas as pd
from datetime import date
import random

# Enhanced challenges list
challenges = [
    "Write down 3 things you're grateful for today 📝",
    "Try something new that challenges you 🚀",
    "Practice mindful meditation for 5 minutes 🧘",
    "Learn one new word and use it in conversation 📖",
    "Perform a random act of kindness 💝",
    "Set a small goal and achieve it today 🎯",
    "Read about a new topic for 15 minutes 📚",
    "Practice active listening in a conversation 👂",
    "Write down one fear and one way to overcome it 💪",
    "Learn from a mistake you made recently 🌱",
    "Share knowledge with someone else 🎓",
    "Try solving a puzzle or brain teaser 🧩",
    "Practice positive self-talk 🗣️",
    "Take a small step outside your comfort zone 🦋",
    "Write down a new skill you want to learn 📝"
]

# Enhanced quotes list
quotes = [
    "Growth begins at the end of your comfort zone. 🌱",
    "Every challenge is an opportunity to learn. 📚",
    "The only way to do great work is to love what you do. ❤️",
    "Success is not final, failure is not fatal. 🌟",
    "Your attitude determines your direction. 🧭",
    "Small progress is still progress. 🎯",
    "Believe you can and you're halfway there. ✨",
    "The future depends on what you do today. 🌅",
    "Dream big, start small. 💫",
    "Fall seven times, stand up eight. 💪"
]

# Achievement badges
badges = {
    5: "Growth Seedling 🌱",
    10: "Mindset Explorer 🗺️",
    15: "Challenge Champion 🏆",
    20: "Growth Master 👑",
    30: "Mindset Warrior ⚔️"
}

def load_data():
    try:
        return pd.read_csv("progress.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Challenge", "Status"])

def save_data(df):
    df.to_csv("progress.csv", index=False)

def calculate_streak(df):
    if df.empty or "Completed" not in df["Status"].values:
        return 0
    
    df_completed = df[df["Status"] == "Completed"].copy()
    df_completed["Date"] = pd.to_datetime(df_completed["Date"])
    df_completed = df_completed.sort_values("Date")
    
    current_streak = 1
    max_streak = 1
    
    for i in range(1, len(df_completed)):
        if (df_completed.iloc[i]["Date"] - df_completed.iloc[i-1]["Date"]).days == 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
            
    return max_streak

# Page configuration
st.set_page_config(
    page_title="Growth Mindset Challenge",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1fae5;
        border: 1px solid #059669;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🌱 Growth Mindset Daily Challenge")
st.markdown("---")

# Load Data
df = load_data()

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Today's Challenge")
    
    # Generate today's challenge
    today = str(date.today())
    if today not in df["Date"].values:
        challenge = random.choice(challenges)
        new_entry = pd.DataFrame([[today, challenge, "Pending"]], columns=["Date", "Challenge", "Status"])
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)
    else:
        challenge = df[df["Date"] == today]["Challenge"].values[0]

    st.info(challenge)
    
    # Update progress
    status = st.radio("Mark Challenge Status:", ["Pending", "Completed"])
    if st.button("Update Progress"):
        df.loc[df["Date"] == today, "Status"] = status
        save_data(df)
        st.success("Progress updated successfully! 🎉")

with col2:
    st.subheader("💫 Daily Motivation")
    st.write(random.choice(quotes))
    
    # Show streak
    current_streak = calculate_streak(df)
    st.metric("🔥 Current Streak", f"{current_streak} days")

# Progress Analysis
st.markdown("---")
st.subheader("📊 Progress Analysis")

col3, col4 = st.columns(2)

with col3:
    # Progress over time using Streamlit's native chart
    if not df.empty:
        df_plot = df.copy()
        df_plot["Date"] = pd.to_datetime(df_plot["Date"])
        df_plot["Completed"] = df_plot["Status"].map({"Completed": 1, "Pending": 0})
        st.line_chart(df_plot.set_index("Date")["Completed"])
        st.caption("Challenge Completion Over Time (1 = Completed, 0 = Pending)")

with col4:
    # Achievement badges
    st.subheader("🏆 Achievements")
    completed_count = len(df[df["Status"] == "Completed"])
    
    for count, badge in badges.items():
        if completed_count >= count:
            st.markdown(f"### {badge}")
            st.write(f"Unlocked at {count} completed challenges!")

# Statistics
st.markdown("---")
st.subheader("📈 Statistics")
col5, col6, col7 = st.columns(3)

with col5:
    total_challenges = len(df)
    st.metric("Total Challenges", total_challenges)

with col6:
    completed_challenges = len(df[df["Status"] == "Completed"])
    st.metric("Completed Challenges", completed_challenges)

with col7:
    completion_rate = (completed_challenges / total_challenges * 100) if total_challenges > 0 else 0
    st.metric("Completion Rate", f"{completion_rate:.1f}%")

# Recent History
st.markdown("---")
st.subheader("📝 Recent History")
if not df.empty:
    recent_df = df.tail(5).sort_values("Date", ascending=False)
    st.dataframe(recent_df, use_container_width=True)

# Motivational Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <h4>🌟 Remember: Every small step counts towards your growth! 🌟</h4>
    </div>
    """, 
    unsafe_allow_html=True
)