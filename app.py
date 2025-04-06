import streamlit as st

# Page config
st.set_page_config(page_title=Agri AI Prototype, layout=wide)

# Load custom styling
with open(style.css) as f
    st.markdown(fstyle{f.read()}style, unsafe_allow_html=True)

# Title section
st.title(🌾 Sustainable Agriculture AI Prototype)
st.subheader(Multi-Agent System Interface)

# Sidebar
st.sidebar.title(Agent Options)
agent_selected = st.sidebar.selectbox(Choose an Agent, [Farmer Advisor, Market Researcher, Weather Watcher])

# Main content
if agent_selected == Farmer Advisor
    st.markdown(### 👨‍🌾 Farmer Advisor)
    land_size = st.slider(Land size (in acres), 1, 100, 10)
    crop_type = st.selectbox(Select preferred crop type, [Wheat, Rice, Maize, Soybean])
    financial_goal = st.number_input(Enter your financial goal (₹), step=1000)

    if st.button(Generate Advice)
        st.success(f✅ Based on your input, we recommend starting with {crop_type} on {land_size} acres for an expected income goal of ₹{financial_goal}.)

elif agent_selected == Market Researcher
    st.markdown(### 📈 Market Researcher)
    region = st.text_input(Enter your region)
    if st.button(Analyze Market)
        st.info(f🔍 In {region}, current market trend suggests high demand for Millets with profitable pricing.)

elif agent_selected == Weather Watcher
    st.markdown(### ⛅ Weather Watcher)
    st.warning(Live weather integration coming soon!)
    st.write(📅 Next expected rain 3 days from now (based on historical averages).)

# Footer
st.markdown(---)
st.markdown(💡 This is a prototype UI for the multi-agent AI system to support sustainable agriculture.)
