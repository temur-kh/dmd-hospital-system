from .classes import *
from random import choice


class SampleDatabase:
    def __init__(self, db, patients=1, medicines=5, doctors=5, others=10, records=10, rooms=4, reports=1,
                 prescriptions=3, roomAssigns=1, bills=7, chats=1):
        self.db = db

        # initialize sample collection objects
        self.collections = []

        self.collections.append(SampleCollection(self, 'employees', doctors, Employee, context={'role': 'doctor'}))
        self.collections.append(SampleCollection(self, 'employees', others, Employee))
        self.collections.append(SampleCollection(self, 'patients', patients, Patient))
        self.collections.append(SampleCollection(self, 'medicines', medicines, Medicine))
        self.collections.append(SampleCollection(self, 'records', records, Record))
        self.collections.append(SampleCollection(self, 'rooms', rooms, Room))
        self.collections.append(SampleCollection(self, 'reports', reports, Report))
        self.collections.append(SampleCollection(self, 'prescriptions', prescriptions, Prescription))
        self.collections.append(SampleCollection(self, 'room_assignment', roomAssigns, RoomAssign))
        self.collections.append(SampleCollection(self, 'chats', chats, Chat))

    def generate(self):
        for collection in self.collections:
            collection.generate()
            print("The Data for the Collection '{}' is Generated".format(collection.name))


class SampleCollection:
    def __init__(self, database: SampleDatabase, name, no_of_records, entity_model, context=None):
        self.database = database
        self.name = name
        self.no_of_records = no_of_records
        self.records = []
        self.entity_model = entity_model
        self.context = context

    def create_data(self):
        for i in range(self.no_of_records):
            if self.context is not None:
                attributes = self.__create_attr_dict()
                record = self.entity_model(self.database.db, **attributes)
            else:
                record = self.entity_model(self.database.db)
            self.records.append(record)

    def __create_attr_dict(self):
        # attributes = dict()
        # for key, val in self.context.items():
        #     try:
        #         ref_collection = [col for col in self.database.collections if col.name == val][0]
        #     except IndexError as e:
        #         raise KeyError("The key reference to the collection does not exist!\n" + e.__str__())
        #     if self.no_of_records == ref_collection.no_of_records:
        #         attributes[key] = ref_collection.records[len(self.records)]  # in case of one-to-one relationship
        #     else:
        #         attributes[key] = choice(ref_collection.records)
        # return attributes
        return self.context

    def upload(self):
        counter = 0
        batch = self.database.db.batch()
        for record in self.records:
            record.save(self.database.db, batch)
            counter += 1
            if counter == 100:
                # print("batch commited!")
                batch.commit()
                batch = self.database.db.batch()
                counter = 0
        batch.commit()

    def generate(self):
        self.create_data()
        self.upload()
