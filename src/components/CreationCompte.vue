<template>
    <div class="create-user-container">
      <h1 class="title">Créer un Compte Utilisateur</h1>
      <form @submit.prevent="createUser">
        <!-- Champ Prénom -->
        <div class="field">
          <label class="label" for="firstName">Prenom</label>
          <div class="control">
            <input class="input" type="text" id="firstName" v-model="user.firstName" placeholder="Prénom complet"/>
          </div>
          <p v-if="errors.firstName" class="help is-danger">{{ errors.firstName }}</p>
        </div>

        <!-- Champ Nom -->
        <div class="field">
          <label class="label" for="lastName">Nom</label>
          <div class="control">
            <input class="input" type="text" id="lastName" v-model="user.lastName" placeholder="Nom complet"/>
          </div>
          <p v-if="errors.lastName" class="help is-danger">{{ errors.lastName }}</p>
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
import { doc, setDoc, getDocs, where, collection, query} from "firebase/firestore"; // Utilisation de setDoc pour définir un ID spécifique
import { createUserWithEmailAndPassword } from "firebase/auth";
import { db, auth } from "../firebase";

export default {
  data() {
    return {
      user: {
        firstName: "",
        email: "",
        password: "",
        role: "user",
      },
      errors: {
        firstName: null,
        email: null,
        password: null,
        role: null,
      },
      message: null,
      success: false,
    };
  },
  methods: {
    sanitizeEmail() {
      if(this.user.email) {
        this.user.email = this.user.email.trim().toLowerCase();
      }
    },
    sanitizeFirstName() {
      if(this.user.firstName) {
        this.user.firstName = this.user.firstName.trim().toLowerCase().replace(/^\w/, (c) => c.toUpperCase());
      }
    },
    sanitizeLastName() {
      if(this.user.lastName) {
        this.user.lastName = this.user.lastName.trim().toLowerCase().replace(/^\w/, (c) => c.toUpperCase());
      }
    },
    isEmailValid(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    },
    async isEmailExists() {
      const q = query(collection(db, "Utilisateurs"), where("email", "==", this.user.email));
      const querySnapshot = await getDocs(q);
      return !querySnapshot.empty;
    },
    async isUserExists() {
      const q = query(
        collection(db, "Utilisateurs"),
        where("firstName", "==", this.user.firstName),
        where("lastName", "==", this.user.lastName)
      );
      const querySnapshot = await getDocs(q);
      return !querySnapshot.empty;
    },
    validateFields() {
      // Réinitialisation des erreurs
      this.errors = {
        firstName: null,
        lastName: null,
        email: null,
        password: null,
        role: null,
      };

      // Validation de chaque champ
      if (!this.user.lastName) {
        this.errors.lastName = "Le nom est requis.";
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
      // Nettoyage de l'adresse email
      this.sanitizeEmail();
      this.sanitizeFirstName();
      this.sanitizeLastName();

      // Validation des champs avant soumission
      if (!this.validateFields()) {
        this.message = "Veuillez corriger les erreurs ci-dessus.";
        this.success = false;
        setTimeout(() => (this.message = null), 3000);
        setTimeout(() => {
        this.errors = {
          firstName: null,
          lastName: null,
          email: null,
          password: null,
          role: null,
        };
      }, 5000);
        return;
      }

      try {
        const userExists = await this.isUserExists();
        if (userExists) {
          this.message = "Erreur : nom et prénom déjà existants.";
          setTimeout(() => (this.message = null), 3000);
          this.success = false;
          return;
        }

        const emailExists = await this.isEmailExists();
        if (emailExists) {
          this.message = "Erreur : email déjà existant.";
          setTimeout(() => (this.message = null), 3000);
          this.success = false;
          return;
        }

        const userCredential = await createUserWithEmailAndPassword(
            auth,
            this.user.email,
            this.user.password
        );

        const userId = userCredential.user.uid; // ID généré par Firebase Auth
        await setDoc(doc(db, "Utilisateurs", userId), {
          id: userId,
          firstName: this.user.firstName,
          lastName: this.user.lastName,
          email: this.user.email,
          role: this.user.role,
          createdAt: new Date().toISOString(), // Date d'ajout automatique
        });

        // Message de succès
        this.message = "Compte utilisateur créé avec succès !";
        setTimeout(() => (this.message = null), 3000);
        this.success = true;
        setTimeout(() => this.success = false, 3000);

        // Réinitialisation du formulaire
        this.user = {
          firstName: "",
          lastName: "",
          email: "",
          password: "",
          role: "user",
        };
      } catch (error) {
        console.error("Erreur lors de la création de l'utilisateur :", error);

        // Gestion des erreurs Firebase
        if (error.code === "auth/email-already-in-use") {
          this.errors.email = "Cette adresse email est déjà utilisée.";
        } else if (error.code === "auth/weak-password") {
          this.errors.password = "Le mot de passe est trop faible.";
        } else {
          this.message = "Une erreur est survenue lors de la création du compte utilisateur.";
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

