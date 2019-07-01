<template>
  <div>
    <h1>Login succeeded. Redirecting...</h1>
  </div>
</template>

<script>
import firebase from "firebase";

let userRouting = [
  ["admin@gmail.com", "admin"],
  ["doctor@gmail.com", "doctor"],
  ["patient@gmail.com", "patient"],
  ["nurse@gmail.com", "nurse"],
  ["receptionist@gmail.com", "receptionist"],
  ["pharmacist@gmail.com", "pharmacist"],
  ["accountant@gmail.com", "accountant"],
  ["laboratorist@gmail.com", "laboratorist"]
];

export default {
  data() {
    return {
      photo: "",
      userId: "",
      name: "",
      email: "",
      user: {}
    };
  },
  created() {
    setTimeout(this.redirect, 1000);
  },
  methods: {
    redirect() {
      this.user = firebase.auth().currentUser;
      //console.log(this.user);
      if (this.user) {
        this.name = this.user.displayName;
        this.email = this.user.email;
        this.userId = this.user.uid;

        for (let i = 0; i < userRouting.length; i++) {
          if (this.user.email == userRouting[i][0])
            this.$router.push(userRouting[i][1]);
        }
      }
    }
  }
};
</script>
