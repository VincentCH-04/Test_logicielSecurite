<template>
    <div class="create-user-container">
      <h1 class="title">Créer un Compte Utilisateur</h1>
      <form @submit.prevent="createUser">
        <!-- Champ Nom -->
        <div class="field">
          <label class="label" for="name">Nom</label>
          <div class="control">
            <input class="input" type="text" id="name" v-model="user.name" placeholder="Nom complet"/>
          </div>
          <p v-if="errors.name" class="help is-danger">{{ errors.name }}</p>
        </div>

        <!-- Champ Prénom -->
        <div class="field">
          <label class="label" for="firstName">Prenom</label>
          <div class="control">
            <input class="input" type="text" id="firstName" v-model="user.firstName" placeholder="Prénom complet"/>
          </div>
          <p v-if="errors.firstName" class="help is-danger">{{ errors.firstName }}</p>
        </div>
  
        <!-- Champ Email -->
        <div class="field">
          <label class="label" for="email">Email</label>
          <div class="control">
            <input class="input" type="email" id="email" v-model="user.email" placeholder="Adresse email"/>
          </div>
          <p v-if="errors.email" class="help is-danger">{{ errors.email }}</p>
        </div>
  
        <!-- Champ Mot de Passe -->
        <div class="field">
          <label class="label" for="password">Mot de Passe</label>
          <div class="control">
            <input class="input" type="password" id="password" v-model="user.password" placeholder="Mot de passe"/>
          </div>
          <p v-if="errors.password" class="help is-danger">{{ errors.password }}</p>
        </div>
  
        <!-- Champ Rôle -->
        <div class="field">
          <label class="label" for="role">Rôle</label>
          <div class="control">
            <div class="select">
              <select id="role" v-model="user.role">
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
import { doc, setDoc } from "firebase/firestore"; // Utilisation de setDoc pour définir un ID spécifique
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
        firstName: null,
        email: null,
        password: null,
        role: null,
      };

      // Validation de chaque champ
      if (!this.user.name) {
        this.errors.name = "Le nom est requis.";
      }
      if (!this.user.firstName) {
        this.errors.firstName = "Le prenom est requis.";
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
        const userCredential = await createUserWithEmailAndPassword(
            auth,
            this.user.email,
            this.user.password
        );

        const userId = userCredential.user.uid; // ID généré par Firebase Auth
        await setDoc(doc(db, "Utilisateurs", userId), {
          id: userId,
          name: this.user.name,
          firstName: this.user.firstName,
          email: this.user.email,
          role: this.user.role,
          createdAt: new Date().toISOString(), // Date d'ajout automatique
        });

        // Message de succès
        this.message = "Compte utilisateur créé avec succès !";
        setTimeout(() => (this.message = null), 3000);
        this.success = true;

        // Réinitialisation du formulaire
        this.user = {
          name: "",
          firstName: "",
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

