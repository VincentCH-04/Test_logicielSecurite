<script>
import PopUpConnect from './PopUpConnect.vue';

export default {
  components: {
    PopUpConnect
  },
  data() {
    return {
      user: null
    };
  },
  methods: {
    PopUpConnect() {
      this.$refs.popupConnect.toggleModal();
    },
    handleLoginSuccess(user) {
      this.user = user;
    },
    logout() {
      this.user = null;
      // Add Firebase sign out logic here if needed
    }
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>

<template>
    <nav class="navbar custom-navbar" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a class="navbar-item" href="http://localhost:8080/">
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