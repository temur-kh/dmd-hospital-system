<template lang="html">
  <div id="firebaseui-auth-container"></div>
</template>
<script>
import firebase from "firebase";
import firebaseui from "firebaseui";
export default {
  name: "auth",
  mounted() {
    var uiConfig = {
      signInSuccessUrl: "/loginSuccess",
      signInOptions: [firebase.auth.EmailAuthProvider.PROVIDER_ID],
      // Terms of service url.
      tosUrl: "<your-tos-url>",
      // Privacy policy url.
      privacyPolicyUrl: "<your-privacy-policy-url>",
      credentialHelper: firebaseui.auth.CredentialHelper.NONE
    };
    var ui = new firebaseui.auth.AuthUI(firebase.auth());
    ui.start("#firebaseui-auth-container", uiConfig);
  }
};
</script>
