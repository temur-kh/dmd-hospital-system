from firebase_admin import firestore
from data_generator.utils import fake, get_fake_datetime
from data_generator.abstracts import Entity
from datetime import timedelta, datetime
from random import choice, sample, randint
from collections import defaultdict

timeSlots = ["10:00-10:30", "10:30-11:00", "11:00-11:30", "11:30-12:00", "12:00-12:30", "12:30-13:00", "13:00-13:30",
             "13:30-14:00", "14:00-14:30", "14:30-15:00"]
statusSlots = ["pending", "approved", "declined"]
empRole = ["laboratorist", "nurse", "accountant", "pharmacist", "receptionist"]
medNamed = ["Aspirin", "Viagra", "Trimoll", "Citramon", "Nosh-pa", "Abakavir", "Azinoks", "Azaran",
            "Avaril", "Apap", "Zantak", "Zivox", "Zinerit", "Zitrek", "Zodak", "Imidil",
            "Imuran", "Indap", "Itrazol", "Kagocel", "Kanizon", "Ketoph", "Klemastin"]
medPrice = {"Aspirin": 1000, "Viagra": 250, "Trimoll": 350, "Citramon": 20, "Nosh-pa": 320, "Abakavir": 1500,
            "Azinoks": 800, "Azaran": 440,
            "Avaril": 880, "Apap": 35, "Zantak": 175, "Zivox": 220, "Zinerit": 270, "Zitrek": 950, "Zodak": 720,
            "Imidil": 910,
            "Imuran": 1000, "Indap": 1200, "Itrazol": 40, "Kagocel": 2000, "Kanizon": 255, "Ketoph": 90,
            "Klemastin": 140}
testTypes = ['Mammography', 'Echocardiography', 'Complete Blood Count', 'Colonoscopy', 'Prothrombin Time',
             'Bone Density Study', 'Basic Metabolic Panel', 'Comprehensive Metabolic Panel', 'Lipid Panel',
             'Liver Panel', 'Thyroid Stimulating Hormone', 'Hemoglobin A1C', 'Urinalysis', 'Cultures']
cashed_collections = {}
cashed_entities = defaultdict(list)
cashed_cond_collections = {}


def get_collection(db: firestore, collection):
    if collection in cashed_collections:
        return cashed_collections[collection]
    docs = db.collection(collection).stream()
    arr = []
    for doc in docs:
        arr.append(doc.reference)
    cashed_collections[collection] = arr
    return arr


def get_entities(collection):
    # print(collection)
    if collection in cashed_entities:
        return cashed_entities[collection]
    else:
        return None


def cache_ref(ent):
    collection = ent.collection
    cashed_entities[collection].append(ent)
    # print(collection, len(cashed_entities[collection]))
    if collection in cashed_collections:
        cashed_collections[collection].append(ent.ref)
    else:
        cashed_collections[collection] = []
        cashed_collections[collection].append(ent.ref)


def get_dict_by_ref(collection, ref):
    entities = get_entities(collection)
    for ent in entities:
        if ent.id == ref.id:
            return ent.to_dict()
    return None


def get_by_condition(arr, collection, key, value):
    hash_str = collection + '.' + key + '.' + value
    if hash_str in cashed_cond_collections:
        return cashed_cond_collections[hash_str]

    entities = get_entities(collection)
    if entities is None:
        cashed_cond_collections[hash_str] = [ref for ref in arr if ref.get().to_dict()[key] == value]
        return cashed_cond_collections[hash_str]

    res = []
    for ref in arr:
        for ent in entities:
            if ref.id == ent.id and ent.to_dict()[key] == value:
                res.append(ref)
    cashed_cond_collections[hash_str] = res
    return res


class Patient(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'patients')

        profile = fake.simple_profile()
        self.name = profile['name']
        self.contactNumber = fake.phone_number()
        self.email = profile['mail']
        self.gender = profile['sex']
        self.address = profile['address']
        history = []
        for i in range(randint(0, 5)):
            row = {
                'date': get_fake_datetime(),
                'note': fake.paragraph(),
                'prescription': None,
            }
            history.append(row)
        self.medHistory = history

    def to_dict(self):
        return {
            u'name': self.name,
            u'address': self.address,
            u'contactNumber': self.contactNumber,
            u'gender': self.gender,
            u'email': self.email,
            u'medHistory': self.medHistory,
        }

    def post_action(self, batch=None):
        cache_ref(self)


class Medicine(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'medicines')

        self.expDate = get_fake_datetime(datetime.now(), datetime.now() + timedelta(days=120))
        self.sold = False
        self.name = choice(medNamed)
        self.price = medPrice[self.name]
        self.quantity = str(randint(10, 100)) + ' ' + choice(['ml', 'unit(s)'])

    def to_dict(self):
        return {
            u'expDate': self.expDate,
            u'sold': self.sold,
            u'name': self.name,
            u'price': self.price,
            u'quantity': self.quantity
        }

    def post_action(self, batch=None):
        cache_ref(self)


class Employee(Entity):
    def __init__(self, db, role="others"):
        super().__init__(db=db, collection=u'employees')

        profile = fake.simple_profile()
        self.name = profile['name']
        self.contactNumber = fake.phone_number()
        self.gender = profile['sex']
        self.address = profile['address']
        self.salary = randint(1200, 3600) * 10
        if role == "doctor":
            self.role = role
        elif role == "others":
            self.role = choice(empRole)
        if self.role == "doctor":
            self.status = "permanent"

    def to_dict(self):
        result = {
            u'name': self.name,
            u'address': self.address,
            u'contactNumber': self.contactNumber,
            u'gender': self.gender,
            u'salary': self.salary,
            u'role': self.role,
        }
        if self.role == "doctor":
            result[u'status'] = self.status
        return result

    def post_action(self, batch=None):
        cache_ref(self)


class Record(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'records')

        colPat = get_collection(db, "patients")
        patient = choice(colPat)
        self.patient = patient

        colDoc = get_collection(db, "employees")
        arr = get_by_condition(colDoc, "employees", "role", "doctor")
        doctor = choice(arr)
        self.doctor = doctor

        self.description = fake.paragraph()
        self.date = get_fake_datetime()
        self.status = choice(statusSlots)
        self.timeSlot = choice(timeSlots)

    def to_dict(self):
        return {
            u'patient': self.patient,
            u'doctor': self.doctor,
            u'description': self.description,
            u'date': self.date,
            u'status': self.status,
            u'timeSlot': self.timeSlot
        }

    def post_action(self, batch=None):
        cache_ref(self)


class Room(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'rooms')

        self.free = True
        self.roomType = choice(["basic", "luxury", "economic"])

        colNur = get_collection(db, "employees")
        arr = get_by_condition(colNur, "employees", "role", "nurse")
        nurse = choice(arr)
        self.nurse = nurse

        self.roomNumber = randint(1, 1000)

    def to_dict(self):
        return {
            u'free': self.free,
            u'roomType': self.roomType,
            u'nurse': self.nurse,
            u'roomNumber': self.roomNumber
        }

    def post_action(self, batch=None):
        cache_ref(self)


class Report(Entity):
    def __init__(self, db: firestore):
        super().__init__(db=db, collection=u'reports')
        self.date = get_fake_datetime()
        self.testResult = choice(["Positive: \n", "Negative: \n"]) + fake.paragraph()
        self.testType = choice(testTypes)

        colLab = get_collection(db, "employees")
        arr = get_by_condition(colLab, "employees", "role", "laboratorist")
        lab = choice(arr)
        self.laboratorist = lab

        colPat = get_collection(db, "patients")
        patient = choice(colPat)
        self.patient = patient

        colNur = get_collection(db, "employees")
        arr = get_by_condition(colNur, "employees", "role", "nurse")
        nurse = choice(arr)
        self.nurse = nurse

    def to_dict(self):
        return {
            u'date': self.date,
            u'testResult': self.testResult,
            u'testType': self.testType,
            u'laboratorist': self.laboratorist,
            u'patient': self.patient,
            u'requester': self.nurse,
        }

    def post_action(self, batch=None):
        cache_ref(self)


class Bill(Entity):
    def __init__(self, db: firestore, med_refs=None, buyer_ref=None):
        super().__init__(db=db, collection=u'bills')
        self.date = get_fake_datetime()

        if buyer_ref is None:
            colPat = get_collection(db, "patients")
            patient = choice(colPat)
            self.buyer = patient
        else:
            self.buyer = buyer_ref

        if med_refs is None:
            colRoom = get_collection(db, "medicines")
            meds = []
            for i in range(0, randint(1, 3)):
                meds.append(choice(colRoom))
            self.medList = meds
        else:
            self.medList = med_refs

    def to_dict(self):
        return {
            u'date': self.date,
            u'buyer': self.buyer,
            u'medList': self.medList,
        }

    def post_action(self, batch=None):
        cache_ref(self)


class Prescription(Entity):
    def __init__(self, db: firestore):
        super().__init__(db=db, collection=u'prescriptions')
        self.date = get_fake_datetime()
        self.description = fake.paragraph()

        colDoc = get_collection(db, "employees")
        arr = get_by_condition(colDoc, "employees", "role", "doctor")
        doctor = choice(arr)
        self.doctor = doctor

        colPat = get_collection(db, "patients")
        patient = choice(colPat)
        self.patient = patient

        medList = []
        self.med_objs = []
        colMed = get_collection(db, "medicines")
        self.med_objs = sample(colMed, k=randint(1, 3))

        for obj in self.med_objs:
            med = get_dict_by_ref("medicines", obj)
            obj = {
                'name': med['name'],
                'price': med['price'],
                'quantity': med['quantity'],
            }
            medList.append(obj)
        self.medList = medList
        self.bills = []

    def to_dict(self):
        return {
            u'date': self.date,
            u'description': self.description,
            u'doctor': self.doctor,
            u'patient': self.patient,
            u'bills': self.bills,
            u'medList': self.medList
        }

    def pre_action(self, batch=None):
        bill = Bill(db=self.db, med_refs=self.med_objs, buyer_ref=self.patient)
        doc = bill.save(self.db, batch)

        self.bills.append(doc)

        for med_obj in self.med_objs:
            batch.update(med_obj, {'sold': True})

    def post_action(self, batch=None):
        cache_ref(self)


class RoomAssign(Entity):
    def __init__(self, db: firestore):
        super().__init__(db=db, collection=u'room_assignment')
        self.dateAddmitted = get_fake_datetime()
        self.dateDischarged = self.dateAddmitted + timedelta(days=randint(1, 5))

        colPat = get_collection(db, "patients")
        patient = choice(colPat)
        self.patient = patient

        colRoom = get_collection(db, "rooms")
        room = choice(colRoom)
        self.room = room

    def to_dict(self):
        return {
            u'date_admitted': self.dateAddmitted,
            u'date_discharged': self.dateDischarged,
            u'patient': self.patient,
            u'room': self.room
        }

    def post_action(self, batch=None):
        cache_ref(self)


class Chat(Entity):
    def __init__(self, db: firestore):
        super().__init__(db=db, collection=u'chats')

        col = get_collection(db, "patients")
        patient = choice(col)
        self.patient = patient

        col = get_collection(db, "employees")
        arr = get_by_condition(col, "employees", "role", "doctor")
        doctor = choice(arr)
        self.doctor = doctor
        msg = []
        for i in range(1, randint(1, 15)):
            obj = {
                'data': get_fake_datetime(),
                'tex    t': fake.paragraph(),
                'sender': choice(["doctor", "patient"]),
            }
            msg.append(obj)
        self.messages = msg

    def to_dict(self):
        return {
            u'patient': self.patient,
            u'doctor': self.doctor,
            u'messages': self.messages,
        }

    def post_action(self, batch=None):
        cache_ref(self)
