<template>
  <div id="app">
    <div class="page-container">
      <HeadNavBar class="header" @change-view="changeView" @update-is-admin="updateIsAdmin" @update-is-connected="updateIsConnected" @update-user="updateCurrentUser"/>
      <div class="content">
        <ContentMain v-if="currentView === 'ContentMain'" :isAdmin="isAdmin" :isConnected="isConnected" :currentUser="currentUser"/>
        <div v-if="isConnected && isAdmin">
          <CreationCompte v-if="currentView === 'CreationCompte'"/>
          <CreationMateriel v-if="currentView === 'CreationMateriel'"/>
          <ModificationMateriel v-if="currentView === 'ModificationMateriel'"/>
          <ModificationCompte v-if="currentView === 'ModificationCompte'"/>
        </div>
        <InformationUser v-if="currentView === 'InformationUser'" :isConnected="isConnected" :currentUser="currentUser"/>
        <OurReservation v-if="currentView === 'OurReservation'" :isConnected="isConnected" :currentUser="currentUser"/>
        <AllReservations v-if="currentView === 'AllReservations'" :isConnected="isConnected"/>
      </div>
    </div>
  </div>
  <div id="footer">
    <FooterBar :isAdmin="isAdmin"/>
  </div>
</template>

<script>
import ContentMain from './components/ContentMain.vue';
import HeadNavBar from './components/HeadNavBar.vue';
import CreationCompte from './components/CreationCompte.vue';
import CreationMateriel from './components/CreationMateriel.vue';
import ModificationMateriel from './components/ModificationMateriel.vue';
import ModificationCompte from './components/ModificationCompte.vue';
import FooterBar from './components/FooterBar.vue';
import InformationUser from './components/InformationUser.vue';
import OurReservation from './components/OurReservation.vue';
import AllReservations from './components/AllReservations.vue';

export default {
  name: 'App',
  components: {
    ContentMain,
    HeadNavBar,
    CreationCompte,
    CreationMateriel,
    ModificationMateriel,
    ModificationCompte,
    FooterBar,
    InformationUser,
    OurReservation,
    AllReservations
  },
  data() {
    return {
      currentView: 'ContentMain', //Retourne l'état actuel de la vue
      isAdmin: false, // Changer en vrai pour avoir accès aux vues d'administration
      isConnected: false,
      currentUser: null
    };
  },
  methods: {
    changeView(view) {
      if(view !== this.currentView) {
        this.currentView = view;
      }
      return this.currentView;
    },
    updateIsAdmin(newVal) {
      this.isAdmin = newVal;
      return this.isAdmin;
    },
    updateIsConnected(status) {
      this.isConnected = status;
      return this.isConnected;
    },
    updateCurrentUser(status) {
      this.currentUser = status;
      return this.currentUser;
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  width: 100%;
  overflow-y: auto;
  overflow-x: hidden; 
  display: flex;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

.page-container {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.content {
  padding-bottom: 50px;
  overflow-y: auto;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

#footer {
  width: 100%;
  background-color: #000000;
  padding: 10px 0;
  position: fixed;
  bottom: 0;
  left: 0;
  z-index: 10;
}

</style>
