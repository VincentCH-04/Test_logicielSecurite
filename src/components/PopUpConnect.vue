<template>
  <div class="modal" :class="{ 'is-active': isActive }">
    <div class="modal-background" @click="toggleModal"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Se connecter</p>
        <button class="delete" aria-label="close" @click="toggleModal"></button>
      </header>
      <section class="modal-card-body">
        <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input class="input" type="email" v-model="email" placeholder="Email">
            <span class="icon is-small is-left">
              <i class="fas fa-envelope"></i>
            </span>
          </p>
        </div>
        <div class="field">
          <p class="control has-icons-left">
            <input class="input" type="password" v-model="password" placeholder="Password">
            <span class="icon is-small is-left">
              <i class="fas fa-lock"></i>
            </span>
          </p>
        </div>
        <div class="field">
          <p class="control">
            <button class="button is-primary" @click="signIn">Log in</button>
          </p>
        </div>
        <p v-if="errorMessages" class="notification is-danger">{{ errorMessages }}</p>
      </section>
    </div>
  </div>
</template>

<script>
import { signInWithEmailAndPassword, signOut } from 'firebase/auth';
import { auth } from '../firebase';

export default {
  data() {
    return {
      isActive: false,
      email: '',
      password: '',
      errorMessages: ''
    };
  },
  methods: {
    toggleModal() {
      this.isActive = !this.isActive;
    },
    sanitizeEmail() {
      this.email = this.email.trim().toLowerCase();
    },
    async signIn() {
      this.sanitizeEmail();

      if (!this.email) {
        this.errorMessages = 'Veuillez entrer un email.';
        setTimeout(() => {
          this.errorMessages = '';
        }, 3000);
        return;
      }
      if (!this.password) {
        this.errorMessages = 'Veuillez entrer un mot de passe.';
        setTimeout(() => {
          this.errorMessages = '';
        }, 3000);
        return;
      }

      try {
        const userCredential = await signInWithEmailAndPassword(auth, this.email, this.password);
        this.toggleModal();
        this.$emit('login-success', userCredential.user);
        return userCredential.user;
      } catch (error) {
        switch (error.code) {
          case 'auth/user-not-found':
            this.errorMessages = 'Utilisateur non trouvé. Veuillez vérifier votre email.';
            break;
          case 'auth/invalid-email':
            this.errorMessages = 'Format de l’email invalide.';
            break;
          case 'auth/too-many-requests':
            this.errorMessages = 'Trop de tentatives infructueuses. Veuillez réessayer plus tard.';
            break;
          case 'auth/wrong-password':
            this.errorMessages = 'Mot de passe incorrect. Veuillez réessayer.';
            break;
          case 'auth/invalid-credential':
            this.errorMessages = 'Les informations d’identification sont incorrectes.';
            break;
          default:
            this.errorMessages = `Erreur inconnue : ${error.message}`;
        }

        setTimeout(() => {
          this.errorMessages = '';
        }, 3000);
      }
    },
    async logout() {
    try {
      await signOut(auth);
      this.user = null;
    } catch (error) {
      console.error("Error during sign out:", error);
    }
  }
  }
};
</script>