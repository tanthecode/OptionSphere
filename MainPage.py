import streamlit as st
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# Page Configuration - Must be first
st.set_page_config(page_title="OptionSphere - Option Pricing Model", layout="wide")

# Load Lottie Animation
def load_lottieurl(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # returns the JSON data if the request is successful
    else:
        st.error(f"Failed to load Lottie animation from {url}")
        return None  # returns None if the URL is not accessible or invalid

# Custom CSS for Styling
gradient_css = """
<style>
    /* Gradient Heading */
    .gradient-text {
        background: linear-gradient(120deg, #4A90E2, #50C878);
        -webkit-background-clip: text;
        color: transparent;
        text-align: center; /* Center align the text */
        display: block; /* Ensure it behaves like a block element */
        margin: 0 auto; /* Center horizontally */
    }

    /* Gradient for sliders but plain text for end values */
    .stSlider>div>div>div {
        background: linear-gradient(90deg, #4A90E2,wh #50C878);
    }

    .stSlider>div>div>div>span {
        color: white !important;
        background: none !important;
        font-weight: bold !important;
    }

    /* General Body Styling */
    body {
        font-family: 'Arial', sans-serif;
        background: linear-gradient(120deg, #f4f7f6, #dbe9f1);
        color: #333;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #4A90E2, #357ABD);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    /* Sidebar Header Styling */
    .css-1lcbmhc {
        font-size: 20px !important; /* Increase font size */
        font-weight: bold !important;
        color: #4A90E2 !important;
        margin-bottom: 10px; /* Add spacing below header */
    }

    /* AI Prediction Box */
    .ai-predicted-box {
        background-color: #e7f7f7;
        border: 2px solid #4CAF50;
        padding: 15px;
        margin-top: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 30px;
        color: #4CAF50;
        font-weight: bold;
    }

    /* Disclaimer */
    .disclaimer {
        font-size: 14px;
        color: gray;
        text-align: center;
        margin-top: 40px;
        padding: 10px;
    }
</style>
"""

st.markdown(gradient_css, unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.header("Option Greeks")

# Preset Option Selection
selected_option = "Nifty 50 - Call Option"  # Pre-select option, modify if needed
delta, gamma, vega, theta = 0.65, 0.05, 0.12, -0.08  # Default Greeks for the selected option

# Sidebar Sliders
st.sidebar.slider("Delta", 0.0, 1.0, delta, step=0.01, disabled=True)
st.sidebar.slider("Gamma", 0.0, 1.0, gamma, step=0.01, disabled=True)
st.sidebar.slider("Vega", 0.0, 1.0, vega, step=0.01, disabled=True)
st.sidebar.slider("Theta", -1.0, 0.0, theta, step=0.01, disabled=True)

# Main Content
st.markdown("<h1 class='gradient-text'>OptionSphere</h1>", unsafe_allow_html=True)
st.title("Option Pricing Model")

# Data Setup
real_prices = [170, 172, 186, 144, 179, 200, 175, 185]
predicted_prices = [133, 144, 174, 190, 128, 159, 142, 134]
underlying_prices = [5000, 5200, 4911, 4950, 5500, 5050, 5060, 5070]
ai_predicted_value = 184
timestamps = ["10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45"]

# Create two columns for side-by-side layout
col1, col2 = st.columns(2)

# Plotly Chart - Market vs AI-Predicted Prices in col1
with col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=timestamps, y=real_prices, mode='lines+markers', name='Real-Time Prices'))
    fig1.add_trace(go.Scatter(x=timestamps, y=predicted_prices, mode='lines+markers', name='Model Price',
                             line=dict(dash='dash')))
    fig1.update_layout(
        title=f"{selected_option}: Market vs Model Price",
        xaxis_title="Time",
        yaxis_title="Price (INR)",
        template="plotly_white",
    )

    st.plotly_chart(fig1)

# Plotly Chart - Underlying Prices in col2
with col2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=timestamps, y=underlying_prices, mode='lines+markers', name='Underlying Prices'))
    fig2.update_layout(
        title=f"{selected_option}: Underlying Price vs Time",
        xaxis_title="Time",
        yaxis_title="Underlying Price (INR)",
        template="plotly_white",
    )

    st.plotly_chart(fig2)

# AI Prediction Box
st.markdown(f"""
<div class='ai-predicted-box'>
    Model Price: {ai_predicted_value}
</div>
""", unsafe_allow_html=True)

# Disclaimer Section
st.markdown(f"""
<div class='disclaimer'>
    Disclaimer: The values and charts are for informational purposes only. They are not intended to provide financial advice. Please consult a financial advisor before making any investment decisions.
</div>
""", unsafe_allow_html=True)
