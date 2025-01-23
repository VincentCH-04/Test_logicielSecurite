<template>
  <div class="edit-account-container">
    <h1 class="title" style="color: white;">Rechercher et Modifier un Compte</h1>

    <!-- Formulaire de recherche -->
    <div v-if="!user.id" class="search-form">
      <div class="field">
        <div class="control is-flex is-align-items-center">
          <label class="label mr-5" for="searchFirstName">Prénom</label>
          <input
              class="input"
              type="text"
              id="searchFirstName"
              v-model="search.firstName"
              placeholder="Rechercher par Prénom"
          />
        </div>
      </div>

      <div class="field">
        <div class="control is-flex is-align-items-center">
          <label class="label mr-3" for="searchLastName">Nom</label>
          <input
              class="input"
              type="text"
              id="searchLastName"
              v-model="search.lastName"
              placeholder="Rechercher par Nom"
          />
        </div>
      </div>

      <div class="field">
        <div class="control is-flex is-align-items-center">
          <label class="label mr-5" for="searchEmail">Email</label>
          <input
              class="input"
              type="email"
              id="searchEmail"
              v-model="search.email"
              placeholder="Rechercher par email"
          />
        </div>
      </div>

      <div class="field is-grouped is-grouped-centered is-flex is-align-items-flex-end">
        <div class="control">
          <label class="label mr-3" for="searchRole">Rôle</label>
          <div class="select">
            <select v-model="search.role" id="searchRole">
              <option value="">Tous</option>
              <option value="admin">Admin</option>
              <option value="user">Utilisateur</option>
            </select>
          </div>
        </div>
        <div class="is-flex is-align-items-flex-end">
          <button class="button is-info" @click="searchAccounts">Rechercher</button>
        </div>
      </div>
    </div>


    <!-- Formulaire de modification -->
    <div v-if="user.id" class="edit-form">
      <h2 class="subtitle" style="color: whitesmoke">Modifier le Compte</h2>

      <div class="field">
        <div class="control is-flex is-align-items-center">
          <label class="label mr-5" for="firstName">Prénom</label>
          <input
            class="input"
            type="text"
            id="firstName"
            v-model="user.firstName"
            placeholder="Nom complet"
          />
        </div>
      </div>

      <div class="field">
        <div class="control is-flex is-align-items-center">
          <label class="label mr-3" for="lastName">Nom</label>
          <input
              class="input"
              type="text"
              id="lastName"
              v-model="user.lastName"
              placeholder="Prénom complet"
          />
        </div>
      </div>

      <div class="field">
        <div class="control is-flex is-align-items-center">
          <label class="label mr-5" for="email">Email</label>
          <input
            class="input"
            type="email"
            id="email"
            v-model="user.email"
            placeholder="Adresse email"
          />
        </div>
      </div>

      <div class="field is-grouped is-grouped-centered">
        <div class="control">
          <label class="label" for="role">Rôle</label>
          <div class="select">
            <select v-model="user.role" id="role">
              <option value="admin">Admin</option>
              <option value="user">Utilisateur</option>
            </select>
          </div>
        </div>
        <div class="buttons is-flex is-align-items-flex-end">
          <button class="button is-primary" @click="updateAccount">Modifier</button>
          <button class="button is-danger" @click="deleteUser">Supprimer</button>
          <button class="button is-light" @click="resetSelection">Retour</button>
        </div>
      </div>

      <div v-if="message" class="notification" :class="{ 'is-success': success, 'is-danger': !success }">
        {{ message }}
      </div>
    </div>

    <!-- Résultats de la recherche avec pagination -->
    <div v-if="results.length > 0" class="results">
      <h2 class="subtitle" style="color: whitesmoke">Résultats :</h2>
      <ul>
        <li v-for="(user, index) in paginatedResults" :key="user.id" @click="selectUser(user)" class="result-item">
          {{ index + 1 + (currentPage - 1) * itemsPerPage }} : {{ user.firstName }} {{ user.lastName }} ({{ user.email }}) - {{ user.role }}
        </li>
      </ul>

      <!-- Pagination -->
      <div class="pagination">
        <button
          class="button is-light"
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
        >
          Précédent
        </button>
        <span class="page-info">Page {{ currentPage }} / {{ totalPages }}</span>
        <button
          class="button is-light"
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
        >
          Suivant
        </button>
      </div>
    </div>

    <div v-else-if="searchCompleted" class="no-results">
      Aucun compte trouvé.
    </div>
  </div>
</template>

<script>
import { collection, query, where, getDocs, doc, updateDoc, deleteDoc } from "firebase/firestore";
import { db } from "../firebase";

export default {
  data() {
    return {
      search: {
        lastName: "",
        firstName:"",
        email: "",
        role: ""
      },
      results: [], // Liste complète des résultats
      paginatedResults: [], // Résultats de la page courante
      currentPage: 1, // Page actuelle
      itemsPerPage: 5, // Nombre d'utilisateurs par page
      user: {
        id: null,
        lastName: "",
        firstName:"",
        email: "",
        role: "",
      },
      message: null,
      success: false,
      searchCompleted: false,
      userExists: false,
    };
  },
  computed: {
    // Calcule le nombre total de pages
    totalPages() {
      return Math.ceil(this.results.length / this.itemsPerPage);
    },
  },
  methods: {
    // Méthode pour réinitialiser le formulaire de modification
    resetSelection() {
      this.user = {
        id: null,
        lastName: "",
        firstName:"",
        email: "",
        role: "",
      };
      this.results = [];
      this.searchCompleted = false;
    },
    async deleteUser() {
      try {
        // Supprimer l'item de la base de données
        await deleteDoc(doc(db, "Utilisateurs", this.user.id));

        this.success = true;
        this.message = "Suppression de l'utilisateur : "+ this.user.firstName +" effectuée.";
        setTimeout(() => (this.message = null), 3000);
        setTimeout(() => (this.success = false), 3000);

      } catch (error) {
        console.error("Erreur lors de la suppression :", error);
        this.message = "Une erreur est survenue lors de la suppression.";
        setTimeout(() => (this.message = null), 3000);
      }
    },

    // Recherche des utilisateurs
    async searchAccounts() {
      this.results = [];
      this.paginatedResults = [];
      this.currentPage = 1;
      this.searchCompleted = false;

      try {
        const usersRef = collection(db, "Utilisateurs");
        const filters = [];

        // Ajout dynamique des filtres
        if (this.search.firstName) filters.push(...this.buildPartialQuery("firstName", this.search.firstName));
        if (this.search.lastName) filters.push(...this.buildPartialQuery("lastName", this.search.lastName));
        if (this.search.email) filters.push(...this.buildPartialQuery("email", this.search.email));
        if (this.search.role) filters.push(where("role", "==", this.search.role));

        const q = filters.length > 0 ? query(usersRef, ...filters) : query(usersRef);

        const querySnapshot = await getDocs(q);
        querySnapshot.forEach((doc) => {
          this.results.push({ id: doc.id, ...doc.data() });
        });

        this.updatePagination();
        this.searchCompleted = true;
      } catch (error) {
        console.error("Erreur lors de la recherche :", error);
        this.message = `Erreur : ${error.message}`;
        this.success = false;
        setTimeout(() => (this.message = null), 3000);
      }
    },
    buildPartialQuery(field, value) {
      const start = value;
      const end = value + "\uf8ff";
      return [where(field, ">=", start), where(field, "<", end)];
    },
    // Met à jour les résultats affichés en fonction de la page actuelle
    updatePagination() {
      const startIndex = (this.currentPage - 1) * this.itemsPerPage;
      const endIndex = startIndex + this.itemsPerPage;
      this.paginatedResults = this.results.slice(startIndex, endIndex);
    },

    // Change la page courante et met à jour les résultats
    changePage(newPage) {
      if (newPage > 0 && newPage <= this.totalPages) {
        this.currentPage = newPage;
        this.updatePagination();
      }
    },

    // Sélectionner un utilisateur pour modification
    selectUser(user) {
      this.user = { ...user };
    },

    // Mettre à jour les informations du compte
    async updateAccount() {
      try {
        const docRef = doc(db, "Utilisateurs", this.user.id);

        // Rechercher si un utilisateur a déjà cette adresse mail
        const usersRef = collection(db, "Utilisateurs");
        const q = query(usersRef, where("email", "==", this.user.email));
        const querySnapshot = await getDocs(q);
        querySnapshot.forEach((doc) => {
          if (doc.id !== this.user.id) {
            this.message = "Un utilisateur avec cette adresse email existe déjà.";
            this.success = false;
            this.userExists = true;
            setTimeout(() => (this.message = null), 3000);
          }
          else this.userExists = false;
        });

        // Rechercher si un utilisateur avec le même Nom et Prénom existe déjà
        const q2 = query(usersRef, where("lastName", "==", this.user.lastName), where("firstName", "==", this.user.firstName));
        const querySnapshot2 = await getDocs(q2);
        querySnapshot2.forEach((doc) => {
          if (doc.id !== this.user.id) {
            this.message = "Un utilisateur avec ce Nom et Prénom existe déjà.";
            this.success = false;
            this.userExists = true;
            setTimeout(() => (this.message = null), 3000);
          }
          else this.userExists = false;
        });
        
        if(this.userExists) return;


        await updateDoc(docRef, {
          lastName: this.user.lastName,
          firstName: this.user.firstName,
          email: this.user.email,
          role: this.user.role,
        });

        this.message = "Compte utilisateur mis à jour avec succès !";
        this.success = true;

        setTimeout(() => (this.message = null), 3000);
      } catch (error) {
        console.error("Erreur lors de la mise à jour :", error);
        this.message = "Erreur lors de la mise à jour du compte.";
        this.success = false;

        setTimeout(() => (this.message = null), 3000);
      }
    },
  },
};
</script>

<style scoped>

.edit-account-container {
  max-width: 1000px;
  margin: auto;
  padding: 20px;
}

.title{
  margin: 50px auto;
  text-align: center;
  margin-bottom: 20px;
}

.subtitle {
  text-align: center;
}

.field {
  margin-bottom: 15px;
}

.results {
  margin-top: 20px;
}

.result-item {
  cursor: pointer;
  padding: 10px;
  border: 1px solid #ccc;
  color: white;
  margin: 5px 0;
  border-radius: 5px;
}

.result-item:hover {
  background-color: #3d3939;
}

.notification {
  margin-top: 20px;
  text-align: center;
}

.no-results {
  text-align: center;
  color: #e74c3c;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.button {
  margin: 0 10px;
}

.page-info {
  font-weight: bold;
  color: white;
  margin: 0 10px;
}

.field label{
  color: #ffffff;
}

</style>
