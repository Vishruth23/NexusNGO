import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import pandas as pd

# Import necessary functions from other modules
from Image_Detection.image_to_text import Response, encode_image
from streamlit_option_menu import option_menu
from Firebase.cred import initialize_firebase
from Firebase.db_interaction import NGO_Database
from Firebase.db_interaction import ImageDatabase
from Ngos.ngo_interface import display_ngo_dashboard
from blockchain.blockchain import get_transactions_last_3_minutes
from Info.about_us import about_us

import os  
import pandas as pd
from dotenv import load_dotenv  
from web3 import Web3, exceptions
from datetime import datetime, timedelta
import plotly.express as px

load_dotenv()
def user_ui(db):
    # Initialize Firebase
    ngo_db = NGO_Database(db)

    # Apply custom CSS for consistent design and animation
    st.markdown("""
        <style>
        body {
            font-family: 'Arial', sans-serif;
        }
        .stButton > button {
            background-color: #FF4B4B; /* Consistent color with app.py */
            color: white;
            border-radius: 30px;
            padding: 10px 24px;
            border: none;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 0 10px;
            width: 200px;
        }
        .stButton > button:hover {
            background-color: #FFFFFF; /* Hover effect */
            color: #FF4B4B;
            transform: scale(1.05);
            font-weight: bold;
        }
        
        .css-1d391kg {  /* Targets the sidebar */
        background: linear-gradient(to bottom, #1a202c, #000000);
        }
        .css-1d391kg > div { /* This centers the content within the sidebar */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .css-1d391kg .css-2vl3m9 {  /* Targets the option menu */
            background-color: transparent;  /* Keep transparent to show gradient */
        }
        .css-2vl3m9 .nav-item {  /* Aligns the individual nav items to center */
            text-align: center;
            width: 100%;
        }
        .header {
            text-align: center;
            color: #60a5fa;
            animation: fadeInDown 1s ease-out;
        }
        .section-header {
            font-size: 36px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        .sidebar-content {
            background-image: linear-gradient(#D6EAF8,#AED6F1);
            color: white;
        }
        .fade-in {
            animation: fadeIn 2s ease-in-out;
        }
        .fade-in-slow {
            animation: fadeIn 3s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar navigation with fade-in effect
    # st.sidebar.title("Navigation")
    with st.sidebar:
        # option = st.sidebar.radio("", ["Donate Items", "Donate Funds", "Search NGOs", "Top NGOs"], key="nav_option")
        option = option_menu("Donor Navigation",["Donate Items", "Donate Funds", "Search NGOs", "Top NGOs","About Us"] ,icons=["gift", "cash" , "search" , "bar-chart","info-circle"],key="nav_option")

    if option == "Donate Items":
        donate_items(ngo_db)
    elif option == "Donate Funds":
        donate_funds(ngo_db)
    elif option == "Search NGOs":
        search_ngos(ngo_db)
    elif option == "Top NGOs":
        display_top_ngos(ngo_db)
    elif option == "About Us":
        about_us()


# Update "Donate Items" function with consistent animations and styles
def donate_items(ngo_db):
    # Page header with fade-in effect
    st.markdown("<h1 class='fade-in' style='text-align: center; color: #FFFFFF;'>👐 Donate Items</h1>", unsafe_allow_html=True)
    st.write("You can either upload an image of the item or describe it to find matching NGOs.")

    # Choose method of donation (image or description)
    option = st.selectbox(
        "How would you like to proceed?",
        ("📸 Upload an Image", "📝 Describe the Item")
    )

    if option == "📸 Upload an Image":
        # Image upload option
        st.subheader("Upload an Image of the Item")
        uploaded_image = st.file_uploader("Upload an image of the item (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

        if uploaded_image:
            # Display uploaded image
            image = Image.open(uploaded_image)
            st.image(image, caption='🖼 Uploaded Image', use_column_width=True)
            
            # Convert image to base64 for processing
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')

            # Button to find matching NGOs with animation
            if st.button("🔍 Find Matching NGOs"):
                response_object = Response("image", encoded_image)
                detected_items = response_object.objects
                st.markdown(f"<h3 class='fade-in-slow' style='color: #FF4B4B;'>🔍 Detected Items: {', '.join(detected_items)}</h3>", unsafe_allow_html=True)
                
                ngo_data = ngo_db.get_ngos()
                ngo_item_mapping = {ngo_data[i]['Name']: ngo_data[i]['needs'] for i in range(len(ngo_data))}
                resp = response_object._categorise_objects_to_NGO(ngo_item_mapping)
                resp = [resp[i].replace("'", "").lower().strip() for i in range(len(resp)) if resp[i] != ""]
                data = {"NGO Name": resp}
                data["Contact"] = [ngo_data[i]['Phone'] for i in range(len(ngo_data)) if ngo_data[i]['Name'].lower().strip() in resp]
                print(data)
                df = pd.DataFrame(data)
                styled_df = df.style.set_properties({
                    'background-color': '#f5f5f5',
                    'color': '#333',
                    'border-color': '#FF6F61',
                    'border-width': '2px',
                    'border-style': 'solid',
                    'text-align': 'left'
                }).set_table_styles([
                    {
                        'selector': 'thead th',
                        'props': [('background-color', '#FF6F61'), ('color', 'white')]
                    }
                ])


                # Display matching NGOs
                st.markdown("<h3 class='fade-in' style='color: #FF4B4B;'>🎯 Matching NGOs Found:</h3>", unsafe_allow_html=True)
                # st.dataframe(df)
                col1, col2, col3 = st.columns([3, 2, 1])
                col1.markdown("*NGO Name*")
                col2.markdown("*Contact*")
                col3.markdown("")

                # Display each row in the table with a "View More" button
                for index, row in df.iterrows():
                        ngo_name = row['NGO Name']
                        contact = row['Contact']
                        st.markdown(f"### {index + 1}: {ngo_name}")
                        st.write(f"📞 Contact: {contact}")
                        # Use an expander for needs and description
                        with st.expander(f"More details about {ngo_name}"):
                            for ngo_details in ngo_data:
                                if ngo_details["Name"]==ngo_name:
                                    break
                            st.write(f"*Needs*: {', '.join(ngo_details.get('needs', []))}")
                            desc=ngo_details.get('Description', 'No description available').replace("<br>","\n")
                            st.write(f"{desc}")

    elif option == "📝 Describe the Item":
        st.subheader("Describe the Item You Wish to Donate")
        item_description = st.text_area("📝 Describe the item you wish to donate", height=150, max_chars=300)

        # Button to find NGOs based on description
        if st.button("🔍 Find Matching NGOs"):
            if item_description:
                response_object = Response("text", item_description)
                detected_items = response_object.objects
                st.markdown(f"<h3 class='fade-in' style='color: #FF4B4B;'>🔍 Detected Items: {', '.join(detected_items)}</h3>", unsafe_allow_html=True)
                
                ngo_data = ngo_db.get_ngos()
                ngo_item_mapping = {ngo_data[i]['Name']: ngo_data[i]['needs'] for i in range(len(ngo_data))}
                resp = response_object._categorise_objects_to_NGO(ngo_item_mapping)
                resp = [resp[i].replace("'", "").lower().strip() for i in range(len(resp))]
                data = {"NGO Name": resp}
                data["Contact"] = [ngo_data[i]['Phone'] for i in range(len(ngo_data)) if ngo_data[i]['Name'].lower() in resp]
                df = pd.DataFrame(data)
                st.markdown("<h3 class='fade-in' style='color: #FF4B4B;'>🎯 Matching NGOs Found:</h3>", unsafe_allow_html=True)
                st.dataframe(df)
                for index, row in df.iterrows():
                        ngo_name = row['NGO Name']
                        contact = row['Contact']
                        st.markdown(f"### {index + 1}: {ngo_name}")
                        st.write(f"📞 Contact: {contact}")
                        # Use an expander for needs and description
                        with st.expander(f"More details about {ngo_name}"):
                            for ngo_details in ngo_data:
                                if ngo_details["Name"]==ngo_name:
                                    break
                            st.write(f"*Needs*: {', '.join(ngo_details.get('needs', []))}")
                            desc=ngo_details.get('Description', 'No description available').replace("<br>","\n")
                            st.write(f"{desc}")
            else:
                st.warning("⚠️ Please enter a description of the item.")


def donate_funds(ngo_db):
    st.markdown("<h1 class='header section-header fade-in' style='color:#FFFFFF;'>💰 Donate Funds</h1>", unsafe_allow_html=True)
    st.write("Choose an NGO and securely donate funds.")

    # Donation Section
    ngos = ngo_db.get_ngos()
    ngo_names = [ngo['Name'] for ngo in ngos]
    selected_ngo = st.selectbox("Select an NGO to donate to:", ngo_names)
    
    # Display selected NGO
    st.write(f"You selected: {selected_ngo}")
    
    # Transaction Monitoring Section
    st.subheader("Blockchain Transaction Monitor")

    # Create a mapping of MetaMask addresses to NGO names
    PUBLIC_KEYS = []
    for ngo in ngos:
        if 'metamask_address' in ngo and ngo["Name"] == selected_ngo:
            PUBLIC_KEYS.append(ngo['metamask_address'])

    if not PUBLIC_KEYS:
        st.info("No MetaMask address found for the selected NGO.")
        return
     
    st.text("{}".format(PUBLIC_KEYS[0]))
    

    # View transactions button
    if st.button('View Detailed Transactions'):

        # Read transactions from CSV
        if os.path.exists('transactions.csv'):
            df = pd.read_csv('transactions.csv')

            # Map MetaMask addresses to NGO names
            df_filtered = df[df["from"].isin(PUBLIC_KEYS)]
            if df_filtered.empty:
                st.info("No transactions found for the selected NGO.")
                return

            df_filtered = classify_transaction(df_filtered)

            # Display transaction details
            with st.expander("View Transaction Details"):
                st.table(df_filtered.loc[:, ["value", "status", "gas", "gasPrice", "timestamp"]])

            st.subheader("Transaction Values by NGO and Status")

            # Aggregate transaction values by NGO and status
            df_counts = df_filtered['status'].value_counts().reset_index()
            df_counts.columns = ['Status', 'Count']

            # Plot the count of status graph using plotly
            fig = px.bar(df_counts, x='Status', y='Count', color='Status', title='Transaction Status Count')
            st.plotly_chart(fig)
        else:
            st.info("No transactions found in the CSV file.")
    else:
        st.info("No public keys found for transaction monitoring.")

# Example usage of the function
if __name__ == "__main__":
    # Assuming ngo_db is an instance of your database class
    ngo_db = ...  # Initialize your NGO database object here
    donate_funds(ngo_db)



def search_ngos(ngo_db):
    st.markdown("<h1>🔍 Search NGOs by Name</h1>", unsafe_allow_html=True)
    search_query = st.text_input("Search for NGOs by name:")

    if search_query:
        ngo_data = ngo_db.get_ngos()  # Fetch all NGO data
        filtered_ngos = [ngo for ngo in ngo_data if search_query.lower() in ngo['Name'].lower()]

        if filtered_ngos:
            for ngo in filtered_ngos:
                ngo_name = ngo['Name']
                ngo_phone = ngo.get('Phone', 'No phone available')
                ngo_email = ngo.get('email', 'No email available')

                # NGO description in Markdown format (assume this is pre-formatted in Markdown)
                ngo_description = ngo.get('Description', 'No description available').replace('<br>', '\n')

                with st.expander(f"{ngo_name}"):
                    st.write(f"*Phone:* {ngo_phone}")
                    st.write(f"*Email:* {ngo_email}")

                    # Render description as markdown
                    st.markdown(ngo_description, unsafe_allow_html=True)

                    # Display needs (if available) at the end
                    ngo_needs = ngo.get('needs', [])
                    if ngo_needs:
                        st.write(f"*Needs:* {', '.join(ngo_needs)}")
        else:
            st.write("No NGOs found with that name.")


def display_top_ngos(ngo_db):
    st.markdown("<h1 class='header section-header fade-in' style='color:white;'>🌟 Top NGOs</h1>", unsafe_allow_html=True)
    
    ngos = ngo_db.get_ngos()
    for ngo in ngos:
        st.markdown(f"<h3 class='fade-in-slow'>NGO: {ngo['Name']}</h3>", unsafe_allow_html=True)
        desc=(ngo.get('Description', 'No description available')).replace('<br>','\n')
        st.markdown(f"{desc}",unsafe_allow_html=True)
        st.markdown(f"**Phone**: {ngo.get('Phone', 'No phone available')}",unsafe_allow_html=True)

        if 'Logo' in ngo:
            image = ImageDatabase().get_image(ngo['Logo'])
            st.image(image, caption="NGO Logo", use_column_width=True)
        st.write(f"**Needs**: {', '.join(ngo.get('needs', []))}")
        st.write("---")


def process_donation(ngo_name, amount):
    transaction_id = "TXN" + str(hash(f"{ngo_name}{amount}"))
    return transaction_id


        
def classify_transaction(df):
        if not df.empty:
            # If transaction value is twice the mean value of normal transactions, mark it as suspected
            df['status'] = 'normal'
            normal_df = df[df['status'] == 'normal']
            if not normal_df.empty:
                mean_value = normal_df['value'].mean()
                df.loc[df['value'] > 2 * mean_value, 'status'] = 'suspected'
        return df

def transaction_page(ngo_db):

    st.title("Blockchain Transaction Monitor")

    # Create a mapping of MetaMask addresses to NGO names
    ngos=ngo_db.get_ngos()
    address_to_name = {ngo['metamask_address']: ngo['Name'] for ngo in ngos if ngo.get('metamask_address')}

    PUBLIC_KEYS = list(address_to_name.keys())
    # Update the transactions every 3 minutes
    if PUBLIC_KEYS:
        get_transactions_last_3_minutes(PUBLIC_KEYS)

        # Read transactions from CSV
        if os.path.exists('transactions.csv'):
            df = pd.read_csv('transactions.csv')

            # Map MetaMask addresses to NGO names
            df['ngo_name_from'] = df['from'].map(address_to_name)
            df['ngo_name_to'] = df['to'].map(address_to_name)
            
            df = classify_transaction(df)

            # Create a summary table
            summary = df['status'].value_counts().reset_index()
            summary.columns = ['Status', 'Count']

            # Display the summary table first
            st.subheader("Transaction Summary")
            st.write(summary)

            # Button to view detailed transaction table
            if st.button('View Detailed Transactions'):
                # Display the table with the required columns
                st.subheader("Transaction Table")
                st.write(df[['ngo_name_from', 'ngo_name_to', 'value', 'status']])

                # Plot the value of transactions over time as a bar chart
                st.subheader("Transaction Values by NGO and Status")
                # Aggregate transaction values by NGO and status
                df_aggregated = df.groupby(['ngo_name_from', 'status'], as_index=False)['value'].sum()
                fig = px.bar(df_aggregated, x='ngo_name_from', y='value', color='status',
                             title='Transaction Value Distribution by NGO and Status')
                st.plotly_chart(fig)
            
        else:
            st.info("No transactions found in the CSV file.")



# Run the user interface
if __name__ == "__main__":
    user_ui()

