<template>
    <nav class="navbar custom-navbar" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a class="navbar-item" href="http://localhost:8080/" @click="$emit('change-view', 'ContentMain')">
                <img fill="none" src="../assets/logo_1.png" alt="LOGO">
                <img/>
            </a>
            <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div>
        <div class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item" @click="$emit('change-view', 'CreationMateriel')">
            Création Matériel
          </a>
          <a class="navbar-item" @click="$emit('change-view', 'ModificationMateriel')">
            Modification Matériel
          </a>
          <a class="navbar-item" @click="$emit('change-view', 'CreationCompte')">
            Création Compte utilisateur
          </a>
          <a class="navbar-item" @click="$emit('change-view', 'ModificationCompte')">
            Modification Compte
          </a>
        </div>
      </div>    
        <div class="navbar-end">
            <div class="navbar-item">
                <div class="output">
                    <a v-if="user" class="connecté">
                        <strong>Bienvenue, {{ user.email }}</strong>
                    </a>
                    <a v-else class="Pas connecté">
                        <strong>Veuillez vous connecter</strong>
                    </a>
                </div>
            </div>
            <div class="buttons">
                <a v-if="!user" class="button is-light" @click="PopUpConnect">
                Log in
                </a>
                <a v-else class="button is-light" @click="logout">
                Log out
                </a>
            </div>
        </div>
    </nav>

    <!-- Include the PopUpConnect component with a ref -->
  <PopUpConnect ref="popupConnect" @login-success="handleLoginSuccess"/>
</template>

<script>
import PopUpConnect from './PopUpConnect.vue';

export default {
  name: 'HeadNavBar',
  components: {
    PopUpConnect
  },
  data() {
    return {
      user: null,
      isAdmin: false
    };
  },
  methods: {
    PopUpConnect() {
      this.$refs.popupConnect.toggleModal();
    },
    handleLoginSuccess(user) {
      this.user = user;
      // Si l'utilisateur est un administrateur, affichez les vues d'administration
      if (user.role === 'admin') {
        this.isAdmin = true;
      }
      else {
        this.isAdmin = false;
      }
      return this.user, this.isAdmin;
    },
    logout() {
      this.user = null;
      return this.user;
    }
  }
};
</script>

<style scoped>

</style>