import firebase_admin
from firebase_admin import credentials, auth, firestore, storage
import uuid
from Firebase.cred import initialize_firebase
from PIL import Image


class ImageDatabase:
    def __init__(self) -> None:
        self.bucket = storage.bucket()

    def upload_image(self, base64_image, directory):
        filename = directory + "/" + str(uuid.uuid4()) + ".png"
        blob = self.bucket.blob(filename)
        blob.upload_from_string(base64_image,content_type="image/png")
        blob.make_public()
        return filename

    def get_image(self, image_path):
        blob = self.bucket.blob(image_path)
        blob.download_to_filename("temp.png")
        return Image.open("temp.png")

class NGO_Database:
    def __init__(self,db) -> None:
        self.db = db
        self.imageUploader = ImageDatabase()

    def authenticate_user(self, id_token: str) -> str:
        """
        Verifies if the provided id_token belongs to an authenticated user.
        Returns the UID of the user if authenticated.
        """
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token['uid']  # Get the user's UID
            return uid
        except auth.InvalidIdTokenError:
            raise Exception("Invalid token. Authentication failed.")
        except auth.ExpiredIdTokenError:
            raise Exception("Token expired. Please log in again.")

    def add_NGO(self, id_token, NGO_name, NGO_category, image_logo, description, phone,needs,email,metamask_address):
        uid = self.authenticate_user(id_token)
        if not uid:
            raise Exception("User not authenticated")

        # Proceed with adding NGO
        doc_ref = self.db.collection(u'NGO').document()
        doc_ref.set({
            u'Name': NGO_name,
            u'Category': NGO_category,
            u'Description': description.replace("\n", "<br>"),
            u'Phone': phone,
            u'Logo': self.imageUploader.upload_image(image_logo, "NGO_Logos") ,
            u'needs': needs,
            u'email':email,
            u'metamask_address': metamask_address
        })

    def update_NGO_Category(self, id_token, NGO_name, category):
        uid = self.authenticate_user(id_token)
        if not uid:
            raise Exception("User not authenticated")

        # Proceed with updating category
        docs = self.db.collection(u'NGO').where(u'Name', u'==', NGO_name).stream()
        for doc in docs:
            doc.reference.update({u'Category': category})

    def update_NGO_Description(self, id_token, NGO_name, description):
        uid = self.authenticate_user(id_token)
        if not uid:
            raise Exception("User not authenticated")

        # Proceed with updating description
        docs = self.db.collection(u'NGO').where(u'Name', u'==', NGO_name).stream()
        for doc in docs:
            doc.reference.update({u'Description': description})

    def update_NGO_Phone(self, id_token, NGO_name, phone):
        uid = self.authenticate_user(id_token)
        if not uid:
            raise Exception("User not authenticated")

        # Proceed with updating phone
        docs = self.db.collection(u'NGO').where(u'Name', u'==', NGO_name).stream()
        for doc in docs:
            doc.reference.update({u'Phone': phone})
            
    def update_NGO_Needs(self, id_token, NGO_name, needs):
        uid = self.authenticate_user(id_token)
        if not uid:
            raise Exception("User not authenticated")

        # Proceed with updating needs
        docs = self.db.collection(u'NGO').where(u'Name', u'==', NGO_name).stream()
        for doc in docs:
            doc.reference.update({u'needs': needs})

    def update_NGO_Logo(self, id_token, NGO_name, image_logo):
        uid = self.authenticate_user(id_token)
        if not uid:
            raise Exception("User not authenticated")

        # Proceed with updating logo
        docs = self.db.collection(u'NGO').where(u'Name', u'==', NGO_name).stream()
        for doc in docs:
            doc.reference.update({u'Logo': self.imageUploader.upload_image(image_logo, "logos")})
            
    #function to get NGOs

    def get_ngos(self):
              
        docs = self.db.collection(u'NGO').stream()
        ngos = []
        for doc in docs:
            ngos.append(doc.to_dict())
        return ngos