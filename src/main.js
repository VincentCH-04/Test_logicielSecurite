import { createApp } from 'vue'
import App from './App.vue'

//import librairies bulma
import 'bulma/css/bulma.css'
import { db, auth } from './firebase.js';

const app = createApp(App);

//Ajouter Firebase à l'application
app.config.globalProperties.$db = db;
app.config.globalProperties.$auth = auth;

app.mount('#app');

