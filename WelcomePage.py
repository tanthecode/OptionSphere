import streamlit as st
import pandas as pd
import numpy as np
# Set page configuration


st.set_page_config(page_title="OptionSphere", page_icon="\U0001F4B0", layout="centered")

# Custom CSS for Animations and Enhanced Design
st.markdown(
    """
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to bottom, #1a2a6c, #b21f1f, #fdbb2d);
            color: white;
            margin: 0;
            padding: 0;
        }
        .main-title {
            text-align: center;
            font-size: 4em;
            font-weight: bold;
            margin-top: 15vh;
        }
        .sub-title {
            text-align: center;
            font-size: 1.8em;
            color: #f1f1f1;
            margin-bottom: 50px;
        }
        .description {
            text-align: center;
            margin: 0 auto;
            max-width: 900px;
            font-size: 1.2em;
            line-height: 1.8;
            color: #f8f9fa;
        }
        hr {
            border: 0;
            height: 1px;
            background: #fff;
            margin: 50px 0;
        }
        .footer {
            text-align: center;
            font-size: 1em;
            color: #f8f9fa;
            margin-top: 50px;
        }
        .footer a {
            color: #ffdd00;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for navigation and data
if "page" not in st.session_state:
    st.session_state.page = "home"
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "option" not in st.session_state:
    st.session_state.option = ""

# Function to reset session state
def reset_to_home():
    st.session_state.page = "home"
    st.session_state.search_query = ""
    st.session_state.option = ""

# Page Logic
if st.session_state.page == "home":
    # Home Page
    st.markdown(
        """
        <div class="main-title">Welcome to OptionSphere</div>
        <div class="sub-title">Ai-Driven Analytics for Better Option Pricing</div>
        """,
        unsafe_allow_html=True
    )

    # Search Inputs
    option = st.selectbox("Choose an option:", ["Index", "Stock"])
    placeholder_text = "Search the index name here" if option == "Index" else "Search the trading symbol of the stock here"
    search_query = st.text_input("Search for the underlying:", placeholder=placeholder_text)

    # Handle Search
    if st.button("Search") and search_query:
        st.session_state.search_query = search_query
        st.session_state.option = option
        st.session_state.page = "results"
        st.experimental_rerun()  # Ensures immediate page transition

    # About Us Section
    st.markdown(
        """
        <div class="description">
            <h2>About Us</h2>
            Welcome to Option Sphere, your trusted platform for cutting-edge financial analysis tailored for options trading. We bridge the gap between theoretical models and real-world market behavior, empowering traders and investors with actionable insights. Our mission is to provide clarity in the complex world of options pricing through advanced analytics, data visualization, and AI-driven recommendations. Whether you're a seasoned trader or just starting out, Option Sphere equips you with the tools to make informed decisions confidently.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Separator
    st.markdown("<hr>", unsafe_allow_html=True)

    # Key Features Section
    st.markdown(
        """
        <div class="description">
            <h2>Key Features</h2>
            <ul>
                <li><b>Accurate Options Valuation</b>: Utilize the Black-Scholes model to compute theoretical option prices and assess their alignment with real-world market prices.</li>
                <li><b>Market vs. Theoretical Price Analysis</b>: Interactive line charts offer a clear comparison between market and theoretical option prices.</li>
                <li><b>Dynamic Underlying Price Tracking</b>: Visualize price changes of the underlying asset through intuitive line charts.</li>
                <li><b>AI-Powered Insights</b>: Receive concise, AI-driven summaries recommending whether an option is worth considering, based on advanced analysis.</li>
                <li><b>User-Friendly Interface</b>: Our platform is designed for seamless navigation and understanding, catering to traders and investors of all expertise levels.</li>
                <li><b>Real-Time Data Updates</b>: Access live market data and analysis to stay ahead of the curve in a fast-paced trading environment.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

elif st.session_state.page == "results":
    # Results Page
    st.title("Search Results")
    st.write(f"Results for: {st.session_state.search_query} ({st.session_state.option})")

    # Generate a DataFrame with the requested columns
    data = {
        'No': np.arange(51),  # Numbers from 0 to 50
        'Name': [f'Name {i}' for i in range(51)],
        'Trading Symbol': [f'SYM{i}' for i in range(51)],
        'Strike Price': np.round(np.random.uniform(100, 200, 51), 2),  # Random strike prices between 100 and 200
        'Instrument Type': ['Option' if i % 2 == 0 else 'Future' for i in range(51)],
        'Expiry': pd.to_datetime(np.random.choice(pd.date_range('2024-12-01', '2025-12-31', freq='D'), 51)),  # Random expiry dates
        'Instrument Key': [f'KEY{i}' for i in range(51)],
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Display the DataFrame as an interactive dataframe with increased size
    st.dataframe(df, use_container_width=True)

    # Dropdown for selecting a row
    selected_row = st.selectbox("Select a row to view details:", df['Name'])

    # Find the selected row details from the dataframe
    row_details = df[df['Name'] == selected_row].iloc[0]

    # Display the details of the selected row
    if selected_row:
        st.write(f"Selected Row: {selected_row}")
        st.write(f"Instrument Key: {row_details['Instrument Key']}")
        st.write(f"Strike Price: {row_details['Strike Price']}")
        st.write(f"Instrument Type: {row_details['Instrument Type']}")
        st.write(f"Expiry: {row_details['Expiry']}")

    # Select button to confirm the row selection
    if st.button("Select Row"):
        st.session_state.selected_row = row_details
        st.write(f"You have selected the row: {selected_row}")
        # Redirect to http://localhost:8502
        st.markdown(
            """
            <script>
            window.location.href="https://optionspheremain.streamlit.app/";
            </script>
            """,
            unsafe_allow_html=True,
        )

    # Back button
    if st.button("Go Back"):
        reset_to_home()
        st.experimental_rerun()

# Footer
st.markdown(
    """
    <div class="footer">
        <a href="#">Contact</a>
    </div>
    """,
    unsafe_allow_html=True
)
