import streamlit as st
from Firebase.cred import initialize_firebase
from Firebase.db_interaction import NGO_Database
from Firebase.db_interaction import ImageDatabase
import time

def search_ngos(db):
    # Page header with consistent design
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🔍 Search NGOs</h1>", unsafe_allow_html=True)
    st.write("Enter keywords or item names to find relevant NGOs and their needs.")

    # Input field for search query
    search_query = st.text_input("Search for NGOs (e.g., clothes, food, books, etc.)")

    if st.button("Search"):
        if search_query:
            # Display a searching animation
            with st.spinner("🔍 Searching for NGOs..."):
                time.sleep(2)  # Simulate search time

                # Initialize Firebase
                ngo_db = NGO_Database(db)

                # Split the query into keywords
                keywords = search_query.lower().split()

                # Fetch matching NGOs from Firestore
                ngos = ngo_db.search_NGO_by_items(keywords)

                # Display matching NGOs
                display_ngos(ngos)
        else:
            st.warning("⚠️ Please enter a keyword to search for NGOs.")

def display_ngos(ngos):
    if ngos:
        st.markdown("<h3 style='color: #FF4B4B;'>🎯 Matching NGOs Found:</h3>", unsafe_allow_html=True)
        
        # Loop through the NGOs and display each with consistent design
        for ngo in ngos:
            st.subheader(f"🌟 NGO: {ngo['Name']}")
            st.write(f"**Description**: {ngo['Description']}")
            st.write(f"**Needs**: {', '.join(ngo['needs'])}")
            
            # Try to display the logo image, if available
            try:
                st.image(ImageDatabase().get_image(ngo['Logo']), use_column_width=True, caption="NGO Logo")
            except:
                st.write("No image available.")
            
            st.write("---")  # Divider for each NGO
    else:
        # Display no matching results found
        st.markdown("<h3 style='color: #FF4B4B;'>🚫 No matching NGOs found</h3>", unsafe_allow_html=True)

if __name__ == "__main__":
    search_ngos()

