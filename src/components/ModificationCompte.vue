<template>
    <div class="edit-account-container">
      <h1 class="title">Modifier un Compte</h1>
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
            <button class="button is-primary" type="submit" @click="updateAccount">Modifier</button>
          </div>
        </div>
  
      <div v-if="message" class="notification" :class="{ 'is-success': success, 'is-danger': !success }">
        {{ message }}
      </div>
    </div>
  </template>

<script>
import { doc, getDoc, updateDoc } from "firebase/firestore"; // Import Firestore
import { db } from "../firebase"; // Importez votre instance Firestore

export default {
  data() {
    return {
      user: {
        id: null,
        name: "",
        email: "",
        role: "user",
      },
      message: null,
      success: false,
    };
  },
  methods: {
    async fetchUser(userId) {
      try {
        const docRef = doc(db, "users", userId); // Référence au document utilisateur
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
          this.user = { id: userId, ...docSnap.data() }; // Charger les données utilisateur
        } else {
          this.message = "Le compte utilisateur n'existe pas.";
          this.success = false;
        }
      } catch (error) {
        console.error("Erreur lors du chargement de l'utilisateur :", error);
        this.message = "Erreur lors du chargement des données utilisateur.";
        this.success = false;
      }
    },
    async updateAccount() {
      try {
        const docRef = doc(db, "users", this.user.id); // Référence au document utilisateur
        await updateDoc(docRef, {
          name: this.user.name,
          email: this.user.email,
          role: this.user.role,
        });

        this.message = "Compte utilisateur mis à jour avec succès !";
        this.success = true;
      } catch (error) {
        console.error("Erreur lors de la mise à jour :", error);
        this.message = "Erreur lors de la mise à jour du compte.";
        this.success = false;
      }
      setTimeout(() => {
        this.message = null;
      }, 3000);
      setTimeout(() => {
        this.success = false;
      }, 3000);
    },
  }
};
</script>

<style scoped>
.edit-account-container {
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
