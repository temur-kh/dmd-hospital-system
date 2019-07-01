<template>
    <v-tabs color="blue" dark slider-color="yellow">
        <v-tab ripple>Bills</v-tab>
        <v-tab-item>
            <v-card flat>
                <v-card-title>
                    Bills information
                    <v-spacer></v-spacer>
                    <v-text-field
                            v-model="search"
                            append-icon="search"
                            label="Search"
                            single-line
                            hide-details
                    ></v-text-field>
                </v-card-title>
                <v-data-table :headers="header" :items="bills" :search="search">
                    <template v-slot:items="props">
                        <td>{{ props.item.bId }}</td>
                        <td>{{ props.item.bCost }}</td>
                        <td>{{ props.item.bQuantity }}</td>
                        <td>{{ props.item.bDate }}</td>
                        <!--<td>{{ props.item.bMedList }}</td>-->
                        <td>
                            <v-menu offset-y>
                                <template v-slot:activator="{ on }">
                                    <v-btn flat small
                                           light ripple
                                           v-on="on"
                                    >
                                        MedList
                                    </v-btn>
                                </template>
                                <v-list>
                                    <v-list-tile
                                            v-for="(item, index) in props.item.bMedList"
                                            :key="index"
                                            @click=""
                                    >
                                        <v-list-tile-title>{{ item }}</v-list-tile-title>
                                    </v-list-tile>
                                </v-list>
                            </v-menu>
                        </td><!-- MEDLIST BUTTON -->
                        <td>
                            <v-btn flat small light ripple v-on:click="remove(props.item.bId)">delete</v-btn>
                        </td><!-- DELETE BUTTON -->
                    </template>

                    <v-alert
                            v-slot:no-results
                            :value="true"
                            color="error"
                            icon="warning"
                    >Your search for "{{ search }}" found no results.
                    </v-alert>
                </v-data-table>
            </v-card>
        </v-tab-item>
    </v-tabs>

</template>


<script>
    import firebase from 'firebase'

    const db = firebase.firestore()

    export default {
        data() {
            return {
                remove: function(id){
                    db.collection('bills').doc(id).delete().then(function () {
                        console.log("DOCUMENT MUST BE DELETED");
                        this.$router.push("accountant/");
                    }).catch(function (error) {
                        console.error("ERROR: ", error);
                    });
                },
                search: "",
                header: [
                    {text: "ID", align: "left", value: "bId"},
                    {text: "cost", align: "left", sortable: true, value: "bCost"},
                    {text: "quantity", align: "left", sortable: true, value: "bQuantity"},
                    {text: "date", align: "left", value: "bDate"},
                    {text: "med list", value: "bMedList"},
                    {text: "Manager", value: "manage"},
                ],
                bills: [],
            };
        },
        created() {
            db.collection('bills').get().then(snapshot => {
                snapshot.forEach(doc => {
                    const data = {
                        bId: doc.id,
                        bCost: doc.data().cost,
                        bQuantity: doc.data().quantity,
                        bDate: doc.data().date.toDate(),
                        bMedList: doc.data().medList,
                    };
                    this.bills.push(data)
                })
            })
        }
    }
</script>
