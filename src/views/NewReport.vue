<template>
    <v-form
    ref="form"
    v-model="valid"
    lazy-validation
    >
        <v-select
        v-model="laboratorist"
        :items="laboratorists"
        :rules="[v => !!v || 'Test Type is required']"
        label="Laboratorist"
        required
        ></v-select>

        <v-select
        v-model="patient"
        :items="patients"
        :rules="[v => !!v || 'Test Type is required']"
        label="Patient"
        required
        ></v-select>

        <v-select
        v-model="testT"
        :items="types"
        :rules="[v => !!v || 'Test Type is required']"
        label="Test Type"
        required
        ></v-select>

        <v-textarea
            v-model="testR"
            auto-grow
            label="Test Result"
            rows="2"
        ></v-textarea>

        <v-btn @click="submit" color="success">save</v-btn>
        <v-btn @click="back">back</v-btn>
    </v-form>  
</template>

<script>
import firebase from 'firebase'
var db = firebase.firestore()
  
  export default { 
    data () { 
        return {
            valid: true,
            laboratorist: '',
            patient: '',
            laboratorists: [],
            patients: [],
            testR: '',
            testT: '',
            types: [
                'Complete Blood Count',
                'Urinalysis',
                'Basic Metabolic Panel',
                'Comprehensive Metabolic Panel',
                'Hemoglobin A1C'
            ],
        };
    },

    created () {
        db.collection('patients').get().then(querySnapshot => {
            querySnapshot.forEach(doc => {
                let data = doc.id
                this.patients.push(data)
            })
        })
        db.collection('employees').where("role", "==", "Laboratorist")
        .get().then(querySnapshot => {
            querySnapshot.forEach(doc => {
                let data = doc.id
                this.laboratorists.push(data)
            })
        })

    },

    methods: {
      submit () {
        db.collection('reports').add({
            laboratorist: db.doc("employees/"+this.laboratorist),
            patient: db.doc("patients/"+this.patient),
            testT: this.testT,
            testR: this.testR
        })
        this.$router.push('/laboratorist');
      },
      back () {
        this.$router.push('/laboratorist');
      }
    }
  }
</script>