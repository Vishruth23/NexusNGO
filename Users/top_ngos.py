import streamlit as st
from Firebase.cred import initialize_firebase
from Firebase.db_interaction import NGO_Database
from Firebase.db_interaction import ImageDatabase

def display_top_ngos(db):
    st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🌟 Top NGOs</h1>", unsafe_allow_html=True)

    # Initialize Firebase
    ngo_db = NGO_Database(db)

    # Get the top NGOs from Firestore database
    ngos = ngo_db.get_ngos()

    if ngos:
        for ngo in ngos:
            # Display each NGO's name and description
            st.markdown(f"<h3 class='fade-in' style='color: #FF4B4B;'>NGO: {ngo['Name']}</h3>", unsafe_allow_html=True)
            st.write(f"**Description**: {ngo.get('Description', 'No description available')}")
            st.write("---")

            # Circular NGO logo with fixed size
            if 'Logo' in ngo:
                logo_image = ImageDatabase().get_image(ngo['Logo'])
                if logo_image:
                    st.markdown(f"""
                        <div style="text-align: center;">
                            <img src="data:image/png;base64,{logo_image}" style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover;">
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.write("Logo not available.")

            # Spacer between NGOs
            st.write("<br>", unsafe_allow_html=True)

    else:
        st.write("No NGOs available to display at the moment.")

# Custom CSS for consistency and animations
st.markdown("""
    <style>
        .fade-in {
            animation: fadeIn 2s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .stButton > button {
            background-color: #FF4B4B; 
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
            background-color: white;
            color: #FF4B4B;
            transform: scale(1.05);
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    display_top_ngos()
