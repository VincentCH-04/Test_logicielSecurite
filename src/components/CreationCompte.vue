<template>
    <div class="create-user-container">
      <h1 class="title">Créer un Compte Utilisateur</h1>
      <form @submit.prevent="createUser">
        <div class="field">
          <label class="label">Nom</label>
          <div class="control">
            <input
              class="input"
              type="text"
              v-model="user.name"
              placeholder="Nom complet"
              required
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label">Email</label>
          <div class="control">
            <input
              class="input"
              type="email"
              v-model="user.email"
              placeholder="Adresse email"
              required
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label">Mot de Passe</label>
          <div class="control">
            <input
              class="input"
              type="password"
              v-model="user.password"
              placeholder="Mot de passe"
              required
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label">Rôle</label>
          <div class="control">
            <div class="select">
              <select v-model="user.role" required>
                <option value="admin">Admin</option>
                <option value="user">Utilisateur</option>
              </select>
            </div>
          </div>
        </div>
  
        <div class="field">
          <div class="control">
            <button class="button is-primary" type="submit">Créer</button>
          </div>
        </div>
      </form>
  
      <div v-if="message" class="notification" :class="{ 'is-success': success, 'is-danger': !success }">
        {{ message }}
      </div>
    </div>
  </template>

<script>
import { collection, addDoc } from "firebase/firestore"; // Pour enregistrer dans Firestore
import { createUserWithEmailAndPassword } from "firebase/auth"; // Pour créer un compte utilisateur Firebase Auth
import { db, auth } from "../firebase"; // Import des instances Firestore et Auth

export default {
  data() {
    return {
      user: {
        name: "",
        email: "",
        password: "",
        role: "user", // Par défaut, rôle utilisateur
      },
      message: null,
      success: false,
    };
  },
  methods: {
    async createUser() {
      try {
        // Étape 1 : Créer l'utilisateur dans Firebase Authentication
        const userCredential = await createUserWithEmailAndPassword(
          auth,
          this.user.email,
          this.user.password
        );

        // Étape 2 : Ajouter les détails utilisateur dans Firestore
        const userId = userCredential.user.uid; // Récupérer l'ID généré par Firebase Auth
        await addDoc(collection(db, "users"), {
          id: userId,
          name: this.user.name,
          email: this.user.email,
          role: this.user.role,
          createdAt: new Date().toISOString(),
        });

        // Afficher un message de succès
        this.message = "Compte utilisateur créé avec succès !";
        this.success = true;

        // Réinitialiser le formulaire
        this.user = {
          name: "",
          email: "",
          password: "",
          role: "user",
        };
      } catch (error) {
        console.error("Erreur lors de la création de l'utilisateur :", error);
        this.message = error.message;
        this.success = false;
      }
    },
  },
};
</script>

<style scoped>
.create-user-container {
  max-width: 1000px;
  margin: 30px auto;
  padding: 50px;
  border-radius: 8px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.notification {
  margin-top: 50px;
  text-align: center;
}
</style>
