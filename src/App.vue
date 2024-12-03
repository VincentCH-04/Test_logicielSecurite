<template>
  <div id="app">
    <HeadNavBar @change-view="changeView"/>
    <ContentMain v-if="currentView === 'ContentMain'"/>
    <CreationCompte v-if="currentView === 'CreationCompte'"/>
    <CreationMateriel v-if="currentView === 'CreationMateriel'"/>
    <ModificationMateriel v-if="currentView === 'ModificationMateriel'"/>
    <ModificationCompte v-if="currentView === 'ModificationCompte'"/>
  </div>
</template>

<script>
import ContentMain from './components/ContentMain.vue';
import HeadNavBar from './components/HeadNavBar.vue';
import CreationCompte from './components/CreationCompte.vue';
import CreationMateriel from './components/CreationMateriel.vue';
import ModificationMateriel from './components/ModificationMateriel.vue';
import ModificationCompte from './components/ModificationCompte.vue';

export default {
  name: 'App',
  components: {
    ContentMain,
    HeadNavBar,
    CreationCompte,
    CreationMateriel,
    ModificationMateriel,
    ModificationCompte
  },
  data() {
    return {
      //retourne l'état actuel de la vue
      currentView: 'ContentMain'
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
