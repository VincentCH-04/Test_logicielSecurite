<template>
    <div class="create-user-container">
      <h1 class="title">Créer un Compte Utilisateur</h1>
      <form @submit.prevent="createUser">
        <!-- Champ Nom -->
        <div class="field">
          <label class="label">Nom</label>
          <div class="control">
            <input class="input" type="text" v-model="user.name" placeholder="Nom complet"/>
          </div>
          <p v-if="errors.name" class="help is-danger">{{ errors.name }}</p>
        </div>
  
        <!-- Champ Email -->
        <div class="field">
          <label class="label">Email</label>
          <div class="control">
            <input class="input" type="email" v-model="user.email" placeholder="Adresse email"/>
          </div>
          <p v-if="errors.email" class="help is-danger">{{ errors.email }}</p>
        </div>
  
        <!-- Champ Mot de Passe -->
        <div class="field">
          <label class="label">Mot de Passe</label>
          <div class="control">
            <input class="input" type="password" v-model="user.password" placeholder="Mot de passe"/>
          </div>
          <p v-if="errors.password" class="help is-danger">{{ errors.password }}</p>
        </div>
  
        <!-- Champ Rôle -->
        <div class="field">
          <label class="label">Rôle</label>
          <div class="control">
            <div class="select">
              <select v-model="user.role">
                <option value="admin">Admin</option>
                <option value="user">Utilisateur</option>
              </select>
            </div>
          </div>
          <p v-if="errors.role" class="help is-danger">{{ errors.role }}</p>
        </div>
  
        <!-- Bouton de soumission -->
        <div class="field">
          <div class="control">
            <button class="button is-primary" type="submit">Créer</button>
          </div>
        </div>
      </form>
  
      <!-- Notification de succès ou d'erreur -->
      <div v-if="message" class="notification" :class="{ 'is-success': success, 'is-danger': !success }">
        {{ message }}
      </div>
    </div>
  </template>
  

  <script>
  import { collection, addDoc } from "firebase/firestore";
  import { createUserWithEmailAndPassword } from "firebase/auth";
  import { db, auth } from "../firebase";
  
  export default {
    data() {
      return {
        user: {
          name: "",
          email: "",
          password: "",
          role: "user",
        },
        errors: {
          name: null,
          email: null,
          password: null,
          role: null,
        },
        message: null,
        success: false,
      };
    },
    methods: {
      validateFields() {
        // Réinitialisation des erreurs
        this.errors = {
          name: null,
          email: null,
          password: null,
          role: null,
        };
  
        // Validation de chaque champ
        if (!this.user.name) {
          this.errors.name = "Le nom est requis.";
        }
        if (!this.user.email) {
          this.errors.email = "L'adresse email est requise.";
        } else if (!/\S+@\S+\.\S+/.test(this.user.email)) {
          this.errors.email = "L'adresse email est invalide.";
        }
        if (!this.user.password) {
          this.errors.password = "Le mot de passe est requis.";
        } else if (this.user.password.length < 6) {
          this.errors.password = "Le mot de passe doit contenir au moins 6 caractères.";
        }
        if (!this.user.role) {
          this.errors.role = "Le rôle est requis.";
        }
  
        // Retourne vrai si aucune erreur
        return !Object.values(this.errors).some((error) => error !== null);
      },
      async createUser() {
        // Validation des champs avant soumission
        if (!this.validateFields()) {
          this.message = "Veuillez corriger les erreurs ci-dessus.";
          this.success = false;
          return;
        }
  
        try {
          // Étape 1 : Créer l'utilisateur dans Firebase Authentication
          const userCredential = await createUserWithEmailAndPassword(
            auth,
            this.user.email,
            this.user.password
          );
  
          // Étape 2 : Ajouter les détails utilisateur dans Firestore
          const userId = userCredential.user.uid;
          await addDoc(collection(db, "users"), {
            id: userId,
            name: this.user.name,
            email: this.user.email,
            role: this.user.role,
            createdAt: new Date().toISOString(),
          });
  
          // Message de succès
          this.message = "Compte utilisateur créé avec succès !";
          this.success = true;
  
          // Réinitialisation du formulaire
          this.user = {
            name: "",
            email: "",
            password: "",
            role: "user",
          };
        } catch (error) {
          console.error("Erreur lors de la création de l'utilisateur :", error);
  
          // Gestion des erreurs Firebase
          if (error.code === "auth/email-already-in-use") {
            this.errors.email = "Cette adresse email est déjà utilisée.";
          } else {
            this.message = error.message;
          }
  
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

.help.is-danger {
  color: #ff3860; /* Rouge Bulma */
  font-size: 0.9em;
  margin-top: 5px;
}
</style>

