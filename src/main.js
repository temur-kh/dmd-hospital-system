import Vue from "vue";
import "./plugins/vuetify";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import firebase from "firebase";
import { config } from "./helpers/firebaseConfig";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  created() {
    firebase.initializeApp(config);
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        //this.$router.push('/loginSuccess')
      } else {
        this.$router.push("/login");
      }
    });
  },
  render: h => h(App)
}).$mount("#app");
