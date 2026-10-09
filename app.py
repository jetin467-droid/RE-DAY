import random
import streamlit as st

# Page Configuration for Mobile View
st.set_page_config(
    page_title="Re:Day - AI Fitness & Focus",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom Styling for Dark Mobile Theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E1E2E;
        color: #CDD6F4;
    }
    div[data-testid="stMetricValue"] {
        color: #74C7EC;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State Variables
if "onboarded" not in st.session_state:
    st.session_state.onboarded = False
if "screen_time_mins" not in st.session_state:
    st.session_state.screen_time_mins = 0.0
if "notifications_allowed" not in st.session_state:
    st.session_state.notifications_allowed = False
if "last_advice" not in st.session_state:
    st.session_state.last_advice = "Waiting for your first exercise scan..."
if "locked_apps" not in st.session_state:
    st.session_state.locked_apps = {
        "Instagram": True,
        "YouTube": True,
        "TikTok": False,
        "Games": False,
    }


# ----------------------------------------------------
# SCREEN 1: ONBOARDING FLOW
# ----------------------------------------------------
if not st.session_state.onboarded:
    st.title("Re:Day 🔥")
    st.caption("Reset Your Posture • Lock Distractions")
    st.write("### Profile Setup")

    age = st.number_input("Age", min_value=10, max_value=100, value=22)

    col1, col2 = st.columns([3, 1])
    with col1:
        weight = st.number_input("Weight", min_value=20.0, value=65.0)
    with col2:
        weight_unit = st.selectbox("Unit", ["kg", "lbs"], key="w_unit")

    col3, col4 = st.columns([3, 1])
    with col3:
        height = st.number_input("Height", min_value=50.0, value=175.0)
    with col4:
        height_unit = st.selectbox("Unit", ["cm", "inch"], key="h_unit")

    st.write("---")
    if st.button("Start Re:Day App 🚀", use_container_width=True):
        st.session_state.onboarded = True
        st.session_state.user_age = age
        st.session_state.user_weight = f"{weight} {weight_unit}"
        st.session_state.user_height = f"{height} {height_unit}"
        st.rerun()

# ----------------------------------------------------
# SCREEN 2: MAIN DASHBOARD
# ----------------------------------------------------
else:
    # Top Header
    st.title("Re:Day Dashboard")

    # Notification Permission Banner
    if not st.session_state.notifications_allowed:
        with st.warning("🔔 Allow App Notifications for posture alerts?"):
            if st.button("Allow Notifications"):
                st.session_state.notifications_allowed = True
                st.success("Notifications enabled!")
                st.rerun()

    # 1. Earned Screen Time & App Launcher Test
    st.subheader("⏳ Earned Screen Time")
    st.metric(
        label="Available Focus Time",
        value=f"{st.session_state.screen_time_mins:.1f} Mins",
    )
    st.caption("• 1 Push-up/Squat = 1 Min  • 1 Sec Plank = 1 Sec")

    st.write("**Test Locked Apps:**")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Open Instagram", use_container_width=True):
            if (
                st.session_state.locked_apps["Instagram"]
                and st.session_state.screen_time_mins <= 0
            ):
                st.error(
                    "🔒 Instagram is locked! Earn screen time by completing workouts."
                )
            else:
                st.session_state.screen_time_mins = max(
                    0.0, st.session_state.screen_time_mins - 1.0
                )
                st.success("Opened Instagram! 1 min used.")
                st.rerun()

    with col_b:
        if st.button("Open YouTube", use_container_width=True):
            if (
                st.session_state.locked_apps["YouTube"]
                and st.session_state.screen_time_mins <= 0
            ):
                st.error(
                    "🔒 YouTube is locked! Earn screen time by completing workouts."
                )
            else:
                st.session_state.screen_time_mins = max(
                    0.0, st.session_state.screen_time_mins - 1.0
                )
                st.success("Opened YouTube! 1 min used.")
                st.rerun()

    st.write("---")

    # 2. Daily Tasks Checklist
    st.subheader("📋 Daily Tasks")
    st.checkbox("💧 Drink 2L Water")
    st.checkbox("🧘 5-Min Shoulder Stretch")
    st.checkbox("🚶 10-Min Posture Walk")
    st.checkbox("📱 Desk Break Pose Scan")

    st.write("---")

    # 3. AI Pose & Exercise Scanner
    st.subheader("🎯 AI Pose & Exercise Scanner")

    btn1, btn2, btn3, btn4 = st.columns(4)

    if btn1.button("Posture"):
        score = random.randint(82, 98)
        st.session_state.last_advice = (
            "⚡ Smart Advice: Pull your shoulders back 1 inch and tuck chin in."
        )
        st.info(f"Posture Alignment Score: {score}/100 ✅")

    if btn2.button("Push-up"):
        reps = random.randint(10, 25)
        st.session_state.screen_time_mins += reps
        st.session_state.last_advice = (
            "⚡ Smart Advice: Keep elbows tucked at a 45° angle. Excellent depth!"
        )
        st.success(f"Completed {reps} Push-ups! (+{reps} Mins Screen Time)")
        st.rerun()

    if btn3.button("Squat"):
        reps = random.randint(12, 30)
        st.session_state.screen_time_mins += reps
        st.session_state.last_advice = (
            "⚡ Smart Advice: Knees tracked properly over toes. Great depth!"
        )
        st.success(f"Completed {reps} Squats! (+{reps} Mins Screen Time)")
        st.rerun()

    if btn4.button("Plank"):
        secs = random.randint(30, 90)
        st.session_state.screen_time_mins += secs / 60.0
        st.session_state.last_advice = (
            "⚡ Smart Advice: Back flat and shoulders aligned perfectly over elbows."
        )
        st.success(f"Held Plank for {secs}s! (+{secs}s Screen Time)")
        st.rerun()

    # 4. Smart Advice Box
    st.subheader("💡 Smart Form Advice")
    st.info(st.session_state.last_advice)

    # 5. Progress Graph
    st.subheader("📊 Weekly Posture Progress")
    chart_data = {
        "Mon": 78,
        "Tue": 82,
        "Wed": 85,
        "Thu": 80,
        "Fri": 88,
        "Sat": 92,
        "Sun": 95,
    }
    st.bar_chart(chart_data)

    # Sidebar Settings
    with st.sidebar:
        st.header("⚙️ App Settings")
        st.write(f"**Age:** {st.session_state.user_age}")
        st.write(f"**Weight:** {st.session_state.user_weight}")
        st.write(f"**Height:** {st.session_state.user_height}")

        st.subheader("🔒 App Blocker Settings")
        for app in list(st.session_state.locked_apps.keys()):
            st.session_state.locked_apps[app] = st.checkbox(
                f"Lock {app}", value=st.session_state.locked_apps[app]
            )
