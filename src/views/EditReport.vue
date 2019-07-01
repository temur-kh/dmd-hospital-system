<template>
    <v-form
    ref="form"
    v-model="valid"
    lazy-validation
    >
        <v-select
        v-model="laboratorist"
        :items="laboratorists"
        :rules="[v => !!v || 'Laboratorist is required']"
        label="Laboratorist"
        required
        ></v-select>

        <v-select
        v-model="patient"
        :items="patients"
        :rules="[v => !!v || 'Patient is required']"
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

        <v-btn @click="update" color="success">edit</v-btn>
        <v-btn @click="remove" color="error">delete</v-btn>
        <v-btn @click="back">back</v-btn>
    </v-form>  
</template>

<script>
import firebase from 'firebase'
var db = firebase.firestore()
export default {
  name: 'edit-employee',
  data () { 
        return {
            valid: true,
            report_id: '',
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
  beforeRouteEnter (to, from, next) {
    db.collection('reports').doc(to.params.report_id).get().then(doc => {
        next(function(vm) {
            vm.report_id = doc.id
            doc.data().patient.get().then(res => {
              vm.patient = res.id
            })
            doc.data().laboratorist.get().then(res => {
              vm.laboratorist = res.id
            })
            vm.laboratorists = []
            vm.patients = []
            db.collection('patients').get().then(querySnapshot => {
                querySnapshot.forEach(doc => {
                    let data = doc.id;
                    vm.patients.push(data);
                })
            })
            db.collection('employees').where("role", "==", "Laboratorist")
            .get().then(querySnapshot => {
                querySnapshot.forEach(doc => {
                    let data = doc.id;
                    vm.laboratorists.push(data);
                })
            })
            vm.testR = doc.data().testR
            vm.testT = doc.data().testT
          
      })
      })
  },
  methods: {
    update () {
      db.collection('reports').doc(this.report_id).update({
            laboratorist: db.doc("employees/"+this.laboratorist),
            patient: db.doc("patients/"+this.patient),
            testT: this.testT,
            testR: this.testR
          })
          .then(() => {
            this.$router.push('/laboratorist')
          });
    },
    remove() {
      if (confirm("Are you sure?")) {
        db.collection('reports').doc(this.report_id).delete();
        this.$router.push('/laboratorist');
      }
    },
    back () {
      this.$router.push('/laboratorist');
    }
  }
}
</script>