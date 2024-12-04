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
    async signIn() {
      try {
        const userCredential = await signInWithEmailAndPassword(auth, this.email, this.password);
        this.toggleModal();
        this.$emit('login-success', userCredential.user);
        return userCredential.user;
      } catch (error) {
        this.errorMessages = error.message;
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

<style scoped>
/* Add your styles here */
</style>