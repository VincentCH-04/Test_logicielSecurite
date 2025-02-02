<template>
  <nav class="navbar custom-navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" @click="$emit('change-view', 'ContentMain')">
        HOME
        <img fill="none" src="../assets/logo_1.png" alt="LOGO" />
      </a>
      <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample" @keydown="handleKeydown">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div class="navbar-menu">
      <div class="navbar-start">
        <div class="buttons">
          <a v-if="localIsAdmin" class="navbar-item" @click="$emit('change-view', 'CreationCompte')">
            Créer un compte
          </a>
          <a v-if="localIsAdmin" class="navbar-item" @click="$emit('change-view', 'CreationMateriel')">
            Créer un matériel
          </a>
          <a v-if="localIsAdmin" class="navbar-item" @click="$emit('change-view', 'ModificationMateriel')">
            Modifier un matériel
          </a>
          <a v-if="localIsAdmin" class="navbar-item" @click="$emit('change-view', 'ModificationCompte')">
            Modifier un compte
          </a>
        </div>
      </div>
    </div>
    <div class="navbar-end">
      <div class="navbar-item has-dropdown is-hoverable is-align-items-center">
        <div class="output">
          <a v-if="localIsConnected" class="connecté navbar-link">
            <strong>{{ localUser?.email }}</strong>
          </a>
          <a v-else class="Pas connecté navbar-link">
            <strong>Veuillez vous connecter</strong>
          </a>
        </div>
        <div class="navbar-dropdown" v-if="localIsConnected">
          <a class="navbar-item" @click="$emit('change-view', 'InformationUser')">
            Information de mon compte
          </a>
          <a class="navbar-item" @click="$emit('change-view', 'OurReservation')">
            Mes réservations
          </a>
          <a class="navbar-item" @click="$emit('change-view', 'AllReservations')">
            Toutes les réservations
          </a>
        </div>
      </div>
      <div class="buttons">
        <a 
          class="button is-light" 
          @click="localIsConnected ? logout() : PopUpConnect()">
          {{ localIsConnected ? 'Déconnexion' : 'Connexion' }}
        </a>
      </div>
    </div>
  </nav>

  <PopUpConnect ref="popupConnect" @login-success="handleLoginSuccess" />
</template>

<script>
import PopUpConnect from './PopUpConnect.vue';
import { collection, query, where, getDocs } from "firebase/firestore";
import { db } from "../firebase";

export default {
  components: {
    PopUpConnect
  },
  props: {
    isAdmin: {
      type: Boolean,
      required: true
    },
    isConnected: {
      type: Boolean,
      required: true
    },
    user: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localIsAdmin: this.isAdmin,
      localIsConnected: this.isConnected,
      localUser: { ...this.user }
    };
  },
  watch: {
    isAdmin(newVal) {
      this.localIsAdmin = newVal;
    },
    isConnected(newVal) {
      this.localIsConnected = newVal;
    },
    user(newVal) {
      this.localUser = { ...newVal };
    }
  },
  methods: {
    PopUpConnect() {
      this.$refs.popupConnect.toggleModal();
    },
    async handleLoginSuccess(user) {
      try {
        const usersRef = collection(db, "Utilisateurs");
        const q = query(usersRef, where("email", "==", user.email));
        const querySnapshot = await getDocs(q);

        if (!querySnapshot.empty) {
          querySnapshot.forEach(async (doc) => {
            const userData = doc.data();
            this.updateUser(userData);
            this.updateAdminStatus(userData.role === 'admin');
            this.updateConnectionStatus(true);
          });
        } else {
          console.error("Utilisateur non trouvé.");
        }
      } catch (error) {
        console.error("Erreur lors de la connexion :", error);
      }
    },
    updateUser(newUser) {
      this.localUser = newUser;
      this.$emit("update-user", newUser);
    },
    updateAdminStatus(isAdmin) {
      this.localIsAdmin = isAdmin;
      this.$emit("update-is-admin", isAdmin);
    },
    updateConnectionStatus(isConnected) {
      this.localIsConnected = isConnected;
      this.$emit("update-is-connected", isConnected);
    },
    logout() {
      this.localUser = null;
      this.localIsAdmin = false;
      this.localIsConnected = false;
      this.$emit("update-user", null);
      this.$emit("update-is-admin", false);
      this.$emit("update-is-connected", false);
      this.$emit('change-view', 'ContentMain');
    }
  }
};
</script>

<style scoped>

.custom-navbar {
  background-color: #000000;
  border-bottom: 1px solid #dbdbdb;
  width: 100%;
  display: flex;
  justify-content: baseline;
  padding: 0 20px;
  align-items: center;
}

.navbar-item {
  color: #ffffff;
  width: auto;
  font-variant: normal;
}
</style>

