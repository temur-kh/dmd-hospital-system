<template>
  <div>
    <h1 class="title">
      Employees
      <v-btn small class="info" @click="addEmployee">Add Employee</v-btn>
    </h1>
    <div v-for="employee in employees" :key="employee.name">
      {{ employee.id }} {{ employee.name }} {{ employee.role }}
      <v-btn small class="warning" @click="openEmployeeDialog(employee.id)"
        >Edit</v-btn
      >
      <v-btn small class="error" @click="deleteEmployee(employee.id)"
        >Delete</v-btn
      >
    </div>
    <hr />
    <h1 class="title">
      Patients <v-btn small class="info" @click="addPatient">Add Patient</v-btn>
    </h1>
    <div v-for="(patient, index) in patients" :key="index">
      {{ patient.id }} {{ patient.name }}
      <v-btn small class="warning" @click="openPatientDialog(patient.id)"
        >Edit</v-btn
      >
      <v-btn small class="error" @click="deletePatient(patient.id)"
        >Delete</v-btn
      >
    </div>

    <v-dialog
      v-model="employeeDialog"
      persistent
      max-width="600px"
      v-if="employee"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Employee Profile</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm6>
                <v-text-field
                  label="Name*"
                  required
                  v-model="employee.name"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 sm6>
                <v-text-field
                  label="Address*"
                  required
                  v-model="employee.address"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 sm6>
                <v-text-field
                  label="Contact Number*"
                  required
                  v-model="employee.contactNumber"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-select
                  v-model="employee.gender"
                  :items="['Male', 'Female']"
                  label="Gender*"
                  required
                ></v-select>
              </v-flex>
              <v-flex xs12 sm6>
                <v-text-field
                  label="Salary*"
                  required
                  v-model="employee.salary"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 sm6>
                <v-autocomplete
                  v-model="employee.role"
                  :items="[
                    'Doctor',
                    'Laboratorist',
                    'Nurse',
                    'Patient',
                    'Pharmacist',
                    'Receptionist'
                  ]"
                  label="Role"
                ></v-autocomplete>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="employeeDialog = false"
            >Close</v-btn
          >
          <v-btn color="blue darken-1" flat @click="updateEmployee">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="patientDialog"
      persistent
      max-width="600px"
      v-if="patient"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Patient Profile</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm6>
                <v-text-field
                  label="Name*"
                  required
                  v-model="patient.name"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 sm6>
                <v-text-field
                  label="Address*"
                  required
                  v-model="patient.address"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 sm6>
                <v-text-field
                  label="Contact Number*"
                  required
                  v-model="patient.contactNumber"
                ></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-select
                  v-model="patient.gender"
                  :items="['Male', 'Female']"
                  label="Gender*"
                  required
                ></v-select>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="patientDialog = false"
            >Close</v-btn
          >
          <v-btn color="blue darken-1" flat @click="updatePatient">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import firebase from "firebase";

var app, db;

export default {
  data: function() {
    return {
      employees: [{ name: "Loading...", id: "" }],
      patients: [{ name: "Loading...", id: "" }],
      employeeDialog: false,
      patientDialog: false,
      employee: null,
      patient: null
    };
  },
  created() {
    app = this;
    db = firebase.firestore();

    db.collection("employees").onSnapshot(function(querySnapshot) {
      app.employees = [];
      querySnapshot.forEach(function(doc) {
        // doc.data() is never undefined for query doc snapshots
        //console.log(doc.id, " => ", doc.data());
        app.employees.push({
          id: doc.id,
          ...doc.data()
        });
      });
    });

    db.collection("patients").onSnapshot(function(querySnapshot) {
      app.patients = [];
      querySnapshot.forEach(function(doc) {
        app.patients.push({
          id: doc.id,
          ...doc.data()
        });
      });
    });
  },
  methods: {
    deleteEmployee(emplyeeId) {
      db.collection("employees")
        .doc(emplyeeId)
        .delete();
    },
    deletePatient(patientId) {
      db.collection("patients")
        .doc(patientId)
        .delete();
    },
    openEmployeeDialog(emplyeeId) {
      app.employee = app.employees.filter(x => x.id == emplyeeId)[0];
      app.employeeDialog = true;
    },
    openPatientDialog(patientId) {
      app.patient = app.patients.filter(x => x.id == patientId)[0];
      app.patientDialog = true;
    },
    updateEmployee() {
      app.employeeDialog = false;
      return db
        .collection("employees")
        .doc(app.employee.id)
        .update({
          ...app.employee
        });
    },
    updatePatient() {
      app.patientDialog = false;
      return db
        .collection("patients")
        .doc(app.patient.id)
        .update({
          ...app.patient
        });
    },
    addEmployee() {
      db.collection("employees").add({
        name: "Unnammed"
      });
    },
    addPatient() {
      db.collection("patients").add({
        name: "Unnammed"
      });
    }
  }
};
</script>
