<template>
  <div id="app">
    <HeadNavBar @change-view="changeView" @update-is-admin="updateIsAdmin" @update-is-connected="updateIsConnected"/>
    <ContentMain v-if="currentView === 'ContentMain'" :isAdmin="isAdmin" :isConnected="isConnected"/>
    <div v-if="isConnected && isAdmin">
      <CreationCompte v-if="currentView === 'CreationCompte'"/>
      <CreationMateriel v-if="currentView === 'CreationMateriel'"/>
      <ModificationMateriel v-if="currentView === 'ModificationMateriel'"/>
      <ModificationCompte v-if="currentView === 'ModificationCompte'"/>
    </div>
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

export default {
  name: 'App',
  components: {
    ContentMain,
    HeadNavBar,
    CreationCompte,
    CreationMateriel,
    ModificationMateriel,
    ModificationCompte,
    FooterBar
  },
  data() {
    return {
      currentView: 'ContentMain', //Retourne l'état actuel de la vue
      isAdmin: false, // Changer en vrai pour avoir accès aux vues d'administration
      isConnected: false
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
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

.custom-navbar {
  height: 50px; /* Ajustez cette valeur selon vos besoins */
}
</style>
