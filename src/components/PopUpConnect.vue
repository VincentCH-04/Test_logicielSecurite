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
      </section>
    </div>
  </div>
</template>

<script>
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';

export default {
  data() {
    return {
      isActive: false,
      email: '',
      password: ''
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
      } catch (error) {
        alert(error.message);
      }
    }
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>