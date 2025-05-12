import streamlit as st
import requests
import json
import os

# Set page config
st.set_page_config(
    page_title="Port Tariff Calculator",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint URL - detects environment for Docker or local development
API_URL = os.environ.get("API_URL", "http://localhost:8000")

def main():
    # Page title and introduction
    st.title("🚢 South African Port Tariff Calculator")
    st.write("""
    This application calculates various port tariffs for vessels berthing at South African ports.
    Enter your query in the text area below.
    """)
    
    # Example query template
    example_query = """Calculate the different tariffs payable by the following vessel berthing at the port of Durban:

Vessel Details:

General
Vessel Name: SUDESTADA
Built: 2010
Flag: MLT - Malta
Classification Society: Registro Italiano Navale

Main Details
Type: Bulk Carrier
DWT: 93,274
GT / NT: 51,300 / 31,192
LOA (m): 229.2
Beam (m): 38
Moulded Depth (m): 20.7
LBP: 222
Drafts SW S / W / T (m): 14.9 / 0 / 0
Suez GT / NT: - / 49,069

DRY
Number of Holds: 7

Cargo Details
Cargo Quantity: 40,000 MT
Days Alongside: 3.39 days
Arrival Time: 15 Nov 2024 10:12
Departure Time: 22 Nov 2024 13:00

Activity/Operations
Activity: Exporting Iron Ore
Number of Operations: 2"""
    
    # Text input for user query
    user_query = st.text_area("Enter your query:", example_query, height=400)
    
    # Submit button
    if st.button("Calculate Tariffs"):
        if user_query:
            try:
                # Show a loading state
                with st.spinner("Calculating tariffs..."):
                    # Make API request
                    response = requests.post(
                        f"{API_URL}/calculate",
                        json={"query": user_query},
                        headers={"Content-Type": "application/json"}
                    )
                    
                    # Check if request was successful
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display results
                        st.success("Tariff calculation complete!")
                        
                        # Display the result in a text area
                        # st.text_area(, , height=300)
                        st.markdown("# Calculated Tariffs:\n\n" + result["result"])
                        
                        # Add download button for text result
                        st.download_button(
                            "Download Results as Markdown",
                            result["result"],
                            "port_tariffs_calculation.md",
                            "text/markdown",
                            key='download-md'
                        )
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error connecting to API: {str(e)}")
        else:
            st.warning("Please enter a query.")
    
    # Add information about the calculator
    with st.sidebar:
        st.header("About")
        st.write("""
        This calculator uses a RAG (Retrieval Augmented Generation) system to calculate
        port tariffs based on the South African port tariff document guidelines.
        
        The calculated tariffs include:
        - Light dues
        - Port dues
        - Towage dues
        - Vehicle traffic services (VTS) dues
        - Pilotage dues
        - Running of vessel lines dues
        
        The calculations depend on vessel parameters and the specific port where the vessel arrives.
        """)
        
        st.header("Expected Values")
        st.write("For the example vessel SUDESTADA in Durban:")
        expected_values = {
            "Light Dues": "ZAR 60,062.04",
            "Port Dues": "ZAR 199,549.22",
            "Towage Dues": "ZAR 147,074.38",
            "VTS Dues": "ZAR 33,315.75",
            "Pilotage Dues": "ZAR 47,189.94",
            "Vessel Lines Dues": "ZAR 19,639.50"
        }
        for tariff, value in expected_values.items():
            st.write(f"- {tariff}: {value}")
        
        st.header("Query Format")
        st.write("""
        Your query should be in the following format:
        
        ```
        Calculate the different tariffs payable by the following vessel berthing at the port of [PORT_NAME]:
        
        [VESSEL_DETAILS]
        ```
        
        Where:
        - PORT_NAME is one of: Durban, Saldanha, or Richards Bay
        - VESSEL_DETAILS include all relevant vessel information
        """)

if __name__ == "__main__":
    main() 