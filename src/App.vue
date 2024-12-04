<template>
  <div id="app">
    <HeadNavBar @change-view="changeView" :isadmin="isAdmin"/>
    <ContentMain v-if="currentView === 'ContentMain'"/>
    <CreationCompte v-if="isAdmin && currentView === 'CreationCompte'"/>
    <CreationMateriel v-if="isAdmin && currentView === 'CreationMateriel'"/>
    <ModificationMateriel v-if="isAdmin && currentView === 'ModificationMateriel'"/>
    <ModificationCompte v-if="isAdmin && currentView === 'ModificationCompte'"/>
    <FooterBar/>
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
      currentView: 'ContentMain', //retourne l'état actuel de la vue
      isAdmin: true // Changer en vrai pour avoir accès aux vues d'administration
    };
  },
  methods: {
    changeView(view) {
      if(view !== this.currentView) {
        this.currentView = view;
      }
      return this.currentView;
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
