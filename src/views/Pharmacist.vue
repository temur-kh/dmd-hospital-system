<template>
  <v-container
    fluid
    grid-list-lg
  >
    <v-layout row wrap>
      <v-flex xs12>
        <v-card>
          <v-card-title>
            <v-toolbar-title> Medicine list </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="search"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>

          <v-data-table
            v-model="selected"
            :headers="headers"
            :items="medicines"
            :search="search"
            item-key="id"
            select-all
            class="elevation-1"
          >
            <template v-slot:items="props">
              <td>
                <v-checkbox
                  v-model="props.selected"
                  primary
                  hide-details
                ></v-checkbox>
              </td>

              <td hidden key="id">{{ props.item.id }}</td>

              <td>
                <v-text-field
                  v-model="props.item.name"
                  :value="props.item.name"
                  required
                ></v-text-field>
              </td>

              <td>
                <v-text-field 
                  v-model="props.item.quantity"
                  :value="props.item.quantity"
                  required
                ></v-text-field>
              </td>

              <td>
                <v-text-field
                  mask="#####"
                  v-model="props.item.price"
                  :value="props.item.price"
                  required
                  ></v-text-field>
              </td>

              <td>
                <v-select
                  v-model="props.item.sold"
                  :items="soldItems"
                ></v-select>
              </td>

              <td>
                <v-text-field
                  :v-model="props.item.expDate"
                  :value="formatDate(props.item.expDate)"
                  readonly                
                  ></v-text-field>
              </td>
            </template>

            <template v-slot:footer>
              <td :colspan="headers.length">
                <v-btn 
                  color="error" 
                  :disabled="drugsAreChosen" 
                  @click="deleteSelected()"
                >Delete Selected</v-btn>

                <v-btn 
                  color="info"
                  :disabled="drugsAreChosen"
                  @click="updateSelected()"
                >Update Selected</v-btn>
              </td>
            </template>
          </v-data-table>
        </v-card>
      </v-flex>

      <v-flex xs12>
        <v-card>
          <v-card-title>
            <v-toolbar-title>Add medicine</v-toolbar-title>
          </v-card-title>

          <v-container>
            <v-form ref="drugInfo">
              <v-layout row wrap>
                <v-flex>
                <v-text-field
                  name="drugName"
                  v-model="drugName"
                  label="Name"
                  required
                ></v-text-field>
                </v-flex>

                <v-flex xs3>
                  <v-text-field
                    name="drugQuantity"
                    v-model="drugQuantity"
                    label="Quantity"
                    required
                  ></v-text-field>
                </v-flex>


              </v-layout>

              <v-layout row wrap>
                <v-flex>
                  <v-text-field
                    name="drugPrice"
                    v-model="drugPrice"
                    label="Price"
                    mask="######"
                    required
                  ></v-text-field>
                </v-flex>

                <v-flex>
                  <v-select
                    name="drugIsSold"
                    v-model="drugIsSold"
                    label="Sold"
                    :items="soldItems"
                  ></v-select>
                </v-flex>

                <!-- <v-flex>
                  <v-text-field
                    name="drugExpDate"
                    v-model="drugExpDate"
                    label="Expiration date"
                    placeholder="dd/mm/yyyy"
                    required
                  ></v-text-field>
                </v-flex> -->

                <v-flex>
                  <v-dialog
                    ref="dialog"
                    v-model="modal"
                    :return-value.sync="date"
                    persistent
                    lazy
                    full-width
                    width="290px"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        v-model="drugExpDate"
                        label="Date"
                        prepend-icon="event"
                        readonly
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker v-model="drugExpDate" scrollable>
                      <v-spacer></v-spacer>
                      <v-btn flat color="primary" @click="modal = false">Cancel</v-btn>
                      <v-btn flat color="primary" @click="$refs.dialog.save(drugExpDate)">OK</v-btn>
                    </v-date-picker>
                  </v-dialog>
                </v-flex>
              </v-layout>

              <v-btn 
                color="success" 
                :disabled="!formIsValid" 
                @click="addMedicine()"
              >submit</v-btn>
            </v-form>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import firebase from 'firebase'

  var app, db

  export default {
    name: "Pharmacist",
    methods: {
      deleteSelected() {        
        for (let med of this.selected) {
          db.collection("medicines")
          .doc(med.id)
          .delete()
        }
      },
      updateSelected() { 
        for (let med of this.selected) {
          if (med.name != "") {
            db.collection("medicines").doc(med.id).update({
              name: med.name,
              price: Number(med.price),
              quantity: med.quantity,
              sold: Boolean(med.sold),
            });
          }
        }

        this.selected = []
      },
      addMedicine() {
        const [year, month, day] = this.drugExpDate.split('-');

        db.collection("medicines").add({
          name: this.drugName,
          price: this.drugPrice,
          quantity: this.drugQuantity,
          sold: Boolean(this.drugIsSold),
          expDate: new Date(year, month, day)
        });        

        this.$refs.drugInfo.reset()
      },
      formatDate(date) {
          if (date == null)
            return "Loading...";
          var t = new Date(1970, 0, 1);
          t.setSeconds(date.seconds);

          return t.getFullYear() + '-' + t.getMonth() + '-' + t.getDate();
        }
    },
    computed: {
      drugsAreChosen: function() {
        return !(this.selected.length > 0);
      },
      formIsValid: function() {
        return this.drugName != ""
            && this.drugQuantity != null
            && this.drugPrice != null
            && this.drugExpDate != null
            && this.drugIsSold != null;
      }
    },
    data() {
      return {
        search: "",
        date: null,
        selected: [],
        modal: false,
        soldItems: [true, false],
        headers: [
          {text: "Name", value: "name"},
          {text: "Quantity", value: "quantity"},
          {text: "Price", value: "price"},
          {text: "Sold", value: "sold"},
          {text: "Expiration date", value: "expDate"}
        ],
        medicines: [
          { 
            name: "Loading...",
            price: "Loading...",
            sold: "Loading...",
            quantity: "Loading...",
            expDate: null
          }
        ],
        drugName: "",
        drugQuantity: null,
        drugIsSold: null,
        drugPrice: null,
        drugExpDate: null
      }
    },
    created() {
      db = firebase.firestore();

      app = this;

      db.collection("medicines").get().then(function(querySnapshot) {
        app.medicines = [];

        querySnapshot.forEach(function(doc) {    
          var docData = doc.data();

          app.medicines.push(
            {
              id: doc.id,
              price: docData.price,
              quantity: docData.quantity,
              sold: docData.sold,
              name: docData.name,
              expDate: docData.expDate
            }
          );
        });
      });
    }
  }
</script>
