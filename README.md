# Nexus NGO

NexusNGO is a platform designed to connect donors with NGOs, facilitating donations of items and funds. The platform also provides a user-friendly interface for NGOs to manage their profiles and interact with donors.

## Table of Contents

- Installation
- Usage
- [Project Structure](#project-structure)
- Features


## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/NexusNGO.git
    cd NexusNGO
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    - Create a `.env` file in the root directory.
    - Add your environment variables (e.g., [`INFURA_API_KEY`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsathvik_rao%2FColossus%2FNexus_Public%2Fblockchain%2Fblockchain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A9%2C%22character%22%3A60%7D%7D%5D%2C%22e01f52a6-1a46-49a1-b8fc-abdbb680daaf%22%5D "Go to definition") for blockchain interaction).

4. **Run the application:**
    ```sh
    streamlit run NexusNGO/app.py
    ```

## Usage

- **Donors:**
  - Navigate through the sidebar to donate items, donate funds, search for NGOs, or view top NGOs.
  - Use the search functionality to find NGOs based on specific needs.

- **NGOs:**
  - Log in or register through the sidebar.
  - Manage your profile, update information, and interact with donors.

## Project Structure

```
.gitignore
blockchain/
    blockchain.py
NexusNGO/
    app.py
    Firebase/
        authenticate.py
        cred.py
        db_interaction.py
    Image_Detection/
        image_to_text.py
        prompts.py
    Ngos/
        ngo_interface.py
        register_ngo.py
        update_ngo.py
    requirements.txt
    Users/
        search_ngos.py
        top_ngos.py
        user_interface.py
```

### Key Files and Directories

- **[`blockchain/blockchain.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsathvik_rao%2FColossus%2FNexus_Public%2Fblockchain%2Fblockchain.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22e01f52a6-1a46-49a1-b8fc-abdbb680daaf%22%5D "/home/sathvik_rao/Colossus/Nexus_Public/blockchain/blockchain.py")**: Contains functions for blockchain interactions, such as fetching transactions.
- **[`NexusNGO/app.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsathvik_rao%2FColossus%2FNexus_Public%2FNexusNGO%2Fapp.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22e01f52a6-1a46-49a1-b8fc-abdbb680daaf%22%5D "/home/sathvik_rao/Colossus/Nexus_Public/NexusNGO/app.py")**: Main entry point for the Streamlit application.
- **[`NexusNGO/Firebase/`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsathvik_rao%2FColossus%2FNexus_Public%2FNexusNGO%2FFirebase%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22e01f52a6-1a46-49a1-b8fc-abdbb680daaf%22%5D "/home/sathvik_rao/Colossus/Nexus_Public/NexusNGO/Firebase/")**: Contains modules for Firebase authentication and database interactions.
- **[`NexusNGO/Image_Detection/`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsathvik_rao%2FColossus%2FNexus_Public%2FNexusNGO%2FImage_Detection%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22e01f52a6-1a46-49a1-b8fc-abdbb680daaf%22%5D "/home/sathvik_rao/Colossus/Nexus_Public/NexusNGO/Image_Detection/")**: Modules for image processing and text extraction.
- **[`NexusNGO/Ngos/`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsathvik_rao%2FColossus%2FNexus_Public%2FNexusNGO%2FNgos%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22e01f52a6-1a46-49a1-b8fc-abdbb680daaf%22%5D "/home/sathvik_rao/Colossus/Nexus_Public/NexusNGO/Ngos/")**: Modules for NGO-related functionalities, including registration and profile updates.
- **[`NexusNGO/Users/`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fsathvik_rao%2FColossus%2FNexus_Public%2FNexusNGO%2FUsers%2F%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22e01f52a6-1a46-49a1-b8fc-abdbb680daaf%22%5D "/home/sathvik_rao/Colossus/Nexus_Public/NexusNGO/Users/")**: Modules for user-related functionalities, including searching and displaying NGOs.

## Features

- **Donor Interface**: User-friendly interface for donors to search for NGOs, donate items, and funds.
- **NGO Management**: Easy-to-use interface for NGOs to manage their profiles and interact with donors.
- **Blockchain Integration**: Fetch and display recent transactions using blockchain technology.
- **Firebase Integration**: Secure authentication and database management using Firebase.
- **Image Detection**: Extract text from images to facilitate item donations.

