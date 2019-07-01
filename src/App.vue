<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>Hospital management system</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>

      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn flat>{{ this.$route.name }}</v-btn>
        <v-btn flat v-if="this.$route.name == 'home' && !loggedIn" to="/login"
          >Log in</v-btn
        >
        <v-btn
          flat
          v-if="this.$route.name != 'login' && loggedIn"
          @click="logOut"
          >Log out</v-btn
        >
      </v-toolbar-items>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>
    <v-footer app></v-footer>
  </v-app>
</template>

<script>
import firebase from "firebase";

export default {
  name: "app",
  methods: {
    logOut() {
      firebase.auth().signOut();
    },
    loggedIn() {
      return firebase.auth().currentUser != null;
    }
  },
  computed: {}
};
</script>
