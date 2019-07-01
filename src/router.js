import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/About.vue")
    },
    {
      path: "/login",
      name: "login",
      component: () => import("./views/Login.vue")
    },
    {
      path: "/loginSuccess",
      name: "Logged In",
      component: () => import("./views/LoginSuccess.vue")
    },
    {
      path: "/admin",
      name: "admin",
      component: () => import("./views/Admin.vue")
    },
    {
      path: "/doctor",
      name: "doctor",
      component: () => import("./views/Doctor.vue")
    },
    {
      path: "/patient",
      name: "patient",
      component: () => import("./views/Patient.vue")
    },
    {
      path: "/nurse",
      name: "nurse",
      component: () => import("./views/Nurse.vue")
    },
    {
      path: "/receptionist",
      name: "receptionist",
      component: () => import("./views/Receptionist.vue")
    },
    {
      path: "/pharmacist",
      name: "pharmacist",
      component: () => import("./views/Pharmacist.vue")
    },
    {
      path: "/accountant",
      name: "accountant",
      component: () => import("./views/Accountant.vue")
    },
    {
      path: "/laboratorist",
      name: "laboratorist",
      component: () => import("./views/Laboratorist.vue")
    },
    {
      path: "/new_report",
      name: "New Report",
      component: () => import("./views/NewReport.vue")
    },
    {
      path: "/edit_report/:report_id",
      name: "Edit Report",
      component: () => import("./views/EditReport.vue")
    }
  ]
});
