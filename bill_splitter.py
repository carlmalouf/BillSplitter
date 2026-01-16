import streamlit as st

st.set_page_config(page_title="Electricity Bill Splitter", layout="wide")

st.title("⚡ Electricity Bill Splitter")
st.markdown("Calculate how much to charge each tenant based on their electricity consumption")

# Section 1: Total Bill Parameters
st.header("1. Total Bill Parameters")
st.subheader("Enter rates ($/kWh) and total consumption (kWh)")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("### 🔌 Controlled Load")
        cl_rate = st.number_input("Rate ($/kWh)", min_value=0.0, value=0.32648, step=0.00001, format="%.5f", key="cl_rate")
        cl_consumption = st.number_input("Total Consumption (kWh)", min_value=0.0, value=0.0, step=0.001, format="%.3f", key="cl_consumption")

with col2:
    with st.container(border=True):
        st.markdown("### 🌙 Usage - Off Peak")
        offpeak_rate = st.number_input("Rate ($/kWh)", min_value=0.0, value=0.41855, step=0.00001, format="%.5f", key="offpeak_rate")
        offpeak_consumption = st.number_input("Total Consumption (kWh)", min_value=0.0, value=0.0, step=0.001, format="%.3f", key="offpeak_consumption")

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.markdown("### ☀️ Usage - Peak")
        peak_rate = st.number_input("Rate ($/kWh)", min_value=0.0, value=0.65120, step=0.00001, format="%.5f", key="peak_rate")
        peak_consumption = st.number_input("Total Consumption (kWh)", min_value=0.0, value=0.0, step=0.001, format="%.3f", key="peak_consumption")

with col4:
    with st.container(border=True):
        st.markdown("### 🌅 Usage - Shoulder")
        shoulder_rate = st.number_input("Rate ($/kWh)", min_value=0.0, value=0.49049, step=0.00001, format="%.5f", key="shoulder_rate")
        shoulder_consumption = st.number_input("Total Consumption (kWh)", min_value=0.0, value=0.0, step=0.001, format="%.3f", key="shoulder_consumption")

st.divider()

# Section 2: Tenant Consumption
st.header("2. Tenant Consumption")

col_t1, col_t2 = st.columns(2)

with col_t1:
    st.subheader("Unit 1")
    t1_cl = st.number_input("Controlled Load (kWh)", min_value=0.0, value=0.0, step=0.001, format="%.3f", key="t1_cl")
    t1_usage = st.number_input("Usage (kWh)", min_value=0.0, value=0.0, step=0.001, format="%.3f", key="t1_usage")

with col_t2:
    st.subheader("Unit 2")
    t2_cl = st.number_input("Controlled Load (kWh)", min_value=0.0, value=0.0, step=0.001, format="%.3f", key="t2_cl")
    t2_usage = st.number_input("Usage (kWh)", min_value=0.0, value=0.0, step=0.001, format="%.3f", key="t2_usage")

st.divider()

# Calculations
st.header("3. Bill Split Calculation")

# Calculate total costs
total_cl_cost = cl_rate * cl_consumption
total_offpeak_cost = offpeak_rate * offpeak_consumption
total_peak_cost = peak_rate * peak_consumption
total_shoulder_cost = shoulder_rate * shoulder_consumption

# Calculate total usage consumption and cost
total_usage_consumption = offpeak_consumption + peak_consumption + shoulder_consumption
total_usage_cost = total_offpeak_cost + total_peak_cost + total_shoulder_cost

# Calculate volume-weighted average usage rate
if total_usage_consumption > 0:
    weighted_avg_usage_rate = total_usage_cost / total_usage_consumption
    offpeak_proportion = (offpeak_consumption / total_usage_consumption) * 100
    peak_proportion = (peak_consumption / total_usage_consumption) * 100
    shoulder_proportion = (shoulder_consumption / total_usage_consumption) * 100
else:
    weighted_avg_usage_rate = 0
    offpeak_proportion = 0
    peak_proportion = 0
    shoulder_proportion = 0

# Display usage rate proportions
st.subheader("Usage Rate Breakdown")
col_prop1, col_prop2, col_prop3 = st.columns(3)
with col_prop1:
    st.metric("Off Peak", f"{offpeak_proportion:.1f}%", help=f"${offpeak_rate:.5f}/kWh")
with col_prop2:
    st.metric("Peak", f"{peak_proportion:.1f}%", help=f"${peak_rate:.5f}/kWh")
with col_prop3:
    st.metric("Shoulder", f"{shoulder_proportion:.1f}%", help=f"${shoulder_rate:.5f}/kWh")

st.caption(f"Weighted Average Usage Rate: ${weighted_avg_usage_rate:.5f}/kWh")

st.divider()

# Total tenant consumption
total_tenant_cl = t1_cl + t2_cl
total_tenant_usage = t1_usage + t2_usage

# Calculate charges for each tenant
if total_tenant_cl > 0:
    t1_cl_charge = (t1_cl / total_tenant_cl) * total_cl_cost
    t2_cl_charge = (t2_cl / total_tenant_cl) * total_cl_cost
else:
    t1_cl_charge = 0
    t2_cl_charge = 0

if total_tenant_usage > 0:
    t1_usage_charge = (t1_usage / total_tenant_usage) * total_usage_cost
    t2_usage_charge = (t2_usage / total_tenant_usage) * total_usage_cost
else:
    t1_usage_charge = 0
    t2_usage_charge = 0

# Total charges
t1_total = t1_cl_charge + t1_usage_charge
t2_total = t2_cl_charge + t2_usage_charge

# Display tenant charges
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.subheader("Unit 1 - Bill Breakdown")
    st.metric("Total Amount Due", f"${t1_total:.2f}", delta=None)
    
    with st.expander("View Breakdown", expanded=True):
        st.write(f"**Controlled Load:** ${t1_cl_charge:.2f}")
        st.write(f"  • Consumption: {t1_cl:.2f} kWh @ ${cl_rate:.4f}/kWh")
        
        st.write(f"**Usage:** ${t1_usage_charge:.2f}")
        st.write(f"  • Consumption: {t1_usage:.2f} kWh @ ${weighted_avg_usage_rate:.4f}/kWh (weighted avg)")

with col_c2:
    st.subheader("Unit 2 - Bill Breakdown")
    st.metric("Total Amount Due", f"${t2_total:.2f}", delta=None)
    
    with st.expander("View Breakdown", expanded=True):
        st.write(f"**Controlled Load:** ${t2_cl_charge:.2f}")
        st.write(f"  • Consumption: {t2_cl:.2f} kWh @ ${cl_rate:.4f}/kWh")
        
        st.write(f"**Usage:** ${t2_usage_charge:.2f}")
        st.write(f"  • Consumption: {t2_usage:.2f} kWh @ ${weighted_avg_usage_rate:.4f}/kWh (weighted avg)")

