import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from data_generator import SampleDatabase


def establish_creds():
    # Use a service account
    cred = credentials.Certificate('cred_pidor.json')
    firebase_admin.initialize_app(cred)


def main():
    establish_creds()
    db = firestore.client()
    params = {
        'patients': 1200,
        'doctors': 400,
        'others': 700,
        'medicines': 1000,
        'records': 2500,
        'rooms': 300,
        'reports': 500,
        'prescriptions': 1000,
        'roomAssigns': 500,
        'bills': 700,
        'chats': 1000,
    }
    database = SampleDatabase(db=db, **params)
    # database = SampleDatabase(db=db)
    database.generate()
    print("The database is generated and saved in Firestore")


if __name__ == "__main__":
    main()
