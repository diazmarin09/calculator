import streamlit as st
import pandas as pd

# Set up page config for mobile screens
st.set_page_config(page_title="Compound Interest", page_icon="💸", layout="centered")

st.title("💸 Compound Interest Calculator")
st.write("Track your long-term investment growth.")

# 1. Inputs Section
st.header("⚙️ Investment Settings")
P = st.number_input("Initial Principal ($)", min_value=0.0, value=1000.0, step=100.0)
annual_contribution = st.number_input("Annual Contribution ($)", min_value=0.0, value=100.0, step=50.0)
rate_percent = st.slider("Annual Interest Rate (%)", min_value=0.0, max_value=30.0, value=7.0, step=0.1)
total_years = st.number_input("Time Horizon (Years)", min_value=1, max_value=50, value=10, step=1)
n = st.selectbox("Compounding Frequency", options=[1, 4, 12, 365], index=2, 
                 format_func=lambda x: {1: "Annually", 4: "Quarterly", 12: "Monthly", 365: "Daily"}[x])

# 2. Calculation Engine
annual_rate = rate_percent / 100
running_balance = P
total_deposits = P
schedule_data = []

for year in range(1, int(total_years) + 1):
    starting_balance = running_balance
    current_year_contribution = 0.0
    
    if year > 1:
        current_year_contribution = annual_contribution
        starting_balance += annual_contribution
        total_deposits += annual_contribution
    
    end_balance = starting_balance * ((1 + (annual_rate / n)) ** (n * 1))
    interest_earned = end_balance - starting_balance
    
    # Save row data
    schedule_data.append({
        "Timeline": f"Year {year}",
        "Starting Balance": round(starting_balance - current_year_contribution, 2),
        "Contribution Added": round(current_year_contribution, 2),
        "Interest Earned": round(interest_earned, 2),
        "Ending Balance": round(end_balance, 2)
    })
    running_balance = end_balance

total_interest = running_balance - total_deposits

# 3. Mobile Performance Dashboard
st.header("📊 Performance Summary")
col1, col2 = st.columns(2)
with col1:
    st.metric("Final Balance", f"${running_balance:,.2f}")
    st.metric("Total Deposited", f"${total_deposits:,.2f}")
with col2:
    st.metric("Total Interest", f"${total_interest:,.2f}")

# 4. Interactive Data Table
st.header("📈 Year-by-Year Schedule")
df = pd.DataFrame(schedule_data)

# Format table for cleaner presentation
st.dataframe(
    df.set_index("Timeline"),
    column_config={
        "Starting Balance": st.column_config.NumberColumn(format="$%,.2f"),
        "Contribution Added": st.column_config.NumberColumn(format="$%,.2f"),
        "Interest Earned": st.column_config.NumberColumn(format="$%,.2f"),
        "Ending Balance": st.column_config.NumberColumn(format="$%,.2f"),
    },
    use_container_width=True
)
