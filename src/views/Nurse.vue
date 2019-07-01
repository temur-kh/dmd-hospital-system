<template>
  <v-tabs color="blue" dark slider-color="yellow">
    <v-tab ripple>Rooms</v-tab>
    <v-tab ripple>Free Rooms</v-tab>
    <v-tab ripple>Reports</v-tab>
    <v-tab-item>
      <v-card flat>
        <v-card-title>
          Rooms allocation
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers" :items="rooms" :search="search">
          <template v-slot:items="props">
            <td>{{ props.item.roomId }}</td>
            <td>{{ props.item.roomType }}</td>
            <td>{{ props.item.patientId }}</td>
            <td>{{ props.item.patientName }}</td>
            <td>
              <v-btn v-on:click="remove(props.item.roomId)" round dark ripple>free</v-btn>
            </td>
          </template>
          <v-alert v-slot:no-results :value="true" color="error" icon="warning"
            >Your search for "{{ search }}" found no results.</v-alert
          >
        </v-data-table>
      </v-card>
    </v-tab-item>

    <v-tab-item>
      <v-card flat>
        <v-card-title>
          Room allocation
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers3" :items="rooms2" :search="search3">
          <template v-slot:items="props">
            <td>{{ props.item.roomId }}</td>
            <td>{{ props.item.roomType }}</td>
            <!-- <td>{{ props.item.patientId }}</td> -->
            <!-- <td>{{ props.item.patientName }}</td> -->
            <td>
              <v-btn v-on:click="openRoomDialog(props.item.roomId)" round dark ripple>Allocate</v-btn>
            </td>
          </template>
          <v-alert
            v-slot:no-results
            :value="true"
            color="error"
            icon="warning"
          >Your search for "{{ search }}" found no results.</v-alert>
        </v-data-table>
      </v-card>
    </v-tab-item>

    <v-tab-item>
      <v-card flat>
        <v-card-title>
          Reports
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers2" :items="reports" :search="search2">
          <template v-slot:items="props">
            <td>{{ props.item.testT }}</td>
            <td>{{ props.item.testR }}</td>
            <td>{{ props.item.laboratorist }}</td>
            <td>{{ props.item.laboratoristName }}</td>
            <td>{{ props.item.patient }}</td>
            <td>{{ props.item.patientName }}</td>
          </template>
          <v-alert
            v-slot:no-results
            :value="true"
            color="error"
            icon="warning"
          >Your search for "{{ search2 }}" found no results.</v-alert>
        </v-data-table>
      </v-card>
    </v-tab-item>


    <v-dialog
      v-model="roomDialog"
      persistent
      max-width="600px"
      v-if="freeRoom"
    >
      <v-card>
        <v-card-title>
          <span class="headline">RoomAllocation ID: {{freeRoom.roomId}}</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              
              <v-flex xs12 sm6>
                <v-autocomplete
                  v-model="freeRoom.patient"
                  :items="freeRoomsList"
                  label="Patient ID*"
                ></v-autocomplete>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="roomDialog = false"
            >Close</v-btn
          >
          <v-btn color="blue darken-1" flat v-on:click="allocate">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


  </v-tabs>
</template>

<script>
import firebase from 'firebase'

var db = firebase.firestore()
var nurse = this
var newT = this
var pName = ''
var names = []

var adjust = function(){
  nurse.rooms2 = []
  nurse.rooms = []
  db.collection('rooms').where("nurse", "==", firebase.auth().currentUser.uid).where("free", "==", false)
      .get().then(querySnapshot => {
        querySnapshot.forEach(doc2 => {
          
          var data = {
                'roomId': doc2.data().roomId,
                'roomType': doc2.data().roomType,
                'patientId': doc2.data().patient,
                'patientName': ''
          }
          db.collection('patients').where("PID", "==", doc2.data().patient).get()
            .then(querySnapshot2 =>{
              if(querySnapshot2.docs[0]){
                data.patientName = querySnapshot2.docs[0].data().name          
              }else{
                data.patientName = 'undefined'
              }
          })
          
          nurse.rooms.push(data)
        })
        
      });

      db.collection('rooms').where("free", "==", true).get().then(querySnapshot => {
        querySnapshot.forEach(doc2 => {
          var data = {
                'roomId': doc2.data().roomId,
                'roomType': doc2.data().roomType,
                
          }
          nurse.rooms2.push(data)
        })
        
      });
      
}

export default {
  data() {
    return {
      remove: function(id) {
        var deleteID = 0;
        db.collection('rooms').get().then(querySnapshot => {
          querySnapshot.forEach(doc => {
              if(doc.data().roomId === id){
                deleteID = doc.id
                db.collection('rooms').doc(deleteID).update({
                  free: true,
                  patient: null
                })
                adjust();                
                
              }
          })
        })
        
      },
      allocate: function() {
        
        nurse.roomDialog = false;
        nurse.freeRoom.free = false;
        db.collection('rooms').where("roomId", "==", nurse.freeRoom.roomId).get().then(snapshot =>{
          snapshot.forEach(doc => {
            console.log(nurse.freeRoom)
            db.collection('rooms').doc(doc.id).update(nurse.freeRoom)
            adjust();    
          })
          
        })
        

      },
      openRoomDialog: function(roomId) {
        db.collection('patients').get().then(snapshot =>{
          snapshot.forEach(doc =>{
            nurse.freeRoomsList.push(doc.id)
          })
        })
        nurse.freeRoom = nurse.rooms2.filter(x => x.roomId == roomId)[0];
        nurse.roomDialog = true;
      },
      roomDialog: false,
      search: "",
      freeRoomsList: [],
      headers: [
        {
          text: "Room ID",
          align: "left",
          sortable: true,
          value: "roomId"
        },
        { text: "Type of room", value: "roomType" },
        {
          text: "Patient ID",
          value: "patientId"
        },
        {text: "Patient Name", value: "patientName"},
        { text: "Edit Info", value: "edit" }
      ],
      freeRoom: null,
      temp: null,
      rooms: [],
      search2: "",
      headers2: [
        { text: "Test Type", value: "testT" },
        { text: "Test Result", value: "testR" },
        { text: "Laboratorist ID", value: "laboratorist" },
        { text: "Laboratorist name", value: "laboratoristName" },
        { text: "Patient ID", value: "patient" },
        { text: "Patient Name", value: "patientName" }
      ],
      headers3: [
        {
          text: "Room ID",
          align: "left",
          sortable: true,
          value: "roomId"
        },
        { text: "Type of room", value: "roomType" },
        { text: "Room allocation", value: "edit2" },
      ],
      rooms2: [],
      search3: "",
      reports: [],
    };
  },
  created () {
    nurse = this
    firebase.auth().onAuthStateChanged(function(user) {
      if(user){
      console.log(nurse.$route.name)
      adjust();
      
      db.collection('reports').get().then(querySnapshot =>{
        querySnapshot.forEach(doc => {
          
          const data = {
            'laboratorist': doc.data().laboratorist.id,
            'patient': doc.data().patient.id,
            'testT': doc.data().testT,
            'testR': doc.data().testR,
            'patientName': '',
            'laboratoristName': ''
          }

          db.collection('patients').where("PID", "==", doc.data().patient.id).get()
            .then(querySnapshot2 =>{
              if(querySnapshot2.docs[0]){
                data.patientName = querySnapshot2.docs[0].data().name          
              }else{
                data.patientName = 'undefined'
              }
          })

          var refDoc = db.collection('employees').doc(doc.data().laboratorist.id)
          if(refDoc){
            refDoc.get().then(snapshot =>{
              data.laboratoristName = snapshot.data().name;  
            })
          }else{
            data.laboratoristName = 'undefined'
          }

          nurse.reports.push(data)
        })
      }) 
      }
    });
  },

  
};
</script>

<style></style>
