<template>
  <div>
    <h1 class="title">Modification de matériel</h1>
    <table class="table is-bordered full-page-table is-center">
      <thead>
        <tr>
          <th>NAME</th>
          <th>STOCK</th>
          <th>DATE DISPO</th>
          <th>PRIX</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in paginatedItems" :key="index">
          <template v-if="editableItem === item">
            <!-- Champs modifiables -->
            <td>
              <input
                class="input"
                v-model="editForm.name"
                type="text"
                placeholder="Nom"
              />
              <p v-if="errors.name" class="help is-danger">{{ errors.name }}</p>
            </td>
            <td>
              <input
                class="input"
                v-model.number="editForm.stock"
                type="number"
                placeholder="Stock"
              />
              <p v-if="errors.stock" class="help is-danger">{{ errors.stock }}</p>
            </td>
            <td>
              <input
                class="input"
                v-model="editForm.dateDispo"
                type="date"
              />
              <p v-if="errors.dateDispo" class="help is-danger">
                {{ errors.dateDispo }}
              </p>
            </td>
            <td>
              <input
                class="input"
                v-model.number="editForm.prix"
                type="number"
                placeholder="Prix"
              />
              <p v-if="errors.prix" class="help is-danger">{{ errors.prix }}</p>
            </td>
            <td>
              <button class="button is-success is-small" @click="saveItem(item)">VALIDER</button>
              <button class="button is-danger is-small" @click="cancelEdit">ANNULER</button>
            </td>
          </template>
          <template v-else>
            <!-- Affichage en lecture seule -->
            <td>{{ item.name }}</td>
            <td>{{ item.stock }}</td>
            <td>{{ item.dateDispo }}</td>
            <td>{{ item.prix }}</td>
            <td>
              <button class="button is-primary is-small" @click="editItem(item)">MODIFIER</button>
            </td>
          </template>
        </tr>
      </tbody>
    </table>

    <!-- Message d'erreur Firebase -->
    <p v-if="errors.firebase" class="notification is-danger">{{ errors.firebase }}</p>

    <div class="pagination">
      <button class="button" @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="button" @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>



<script>
import { doc, updateDoc, } from "firebase/firestore";
import { db } from "../firebase";

export default {
  data() {
    return {
      items: [
        { id: "id1", name: "Item 1", stock: 10, dateDispo: "2024-12-10", prix: 20 },
        { id: "id2", name: "Item 2", stock: 5, dateDispo: "2024-12-12", prix: 15 },
        { id: "id3", name: "Item 3", stock: 8, dateDispo: "2024-12-15", prix: 25 },
        { id: "id4", name: "Item 4", stock: 3, dateDispo: "2024-12-18", prix: 30 },
      ],
      editableItem: null,
      editForm: {
        name: "",
        stock: 0,
        dateDispo: "",
        prix: 0,
      },
      errors: {
        name: null,
        stock: null,
        dateDispo: null,
        prix: null,
        firebase: null,
      },
      currentPage: 1,
      itemsPerPage: 4,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.items.length / this.itemsPerPage);
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.items.slice(start, end);
    },
  },
  methods: {
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    editItem(item) {
      this.editableItem = item;
      this.editForm = { ...item }; // Crée une copie des données pour l'édition
    },
    cancelEdit() {
      this.editableItem = null;
      this.errors = {}; // Réinitialise les erreurs
    },
    validateFields() {
      this.errors = {
        name: null,
        stock: null,
        dateDispo: null,
        prix: null,
        firebase: null,
      };

      if (!this.editForm.name) {
        this.errors.name = "Le nom est requis.";
        setTimeout(() => {
          this.errors.name = null;
        }, 3000);
      }
      if (this.editForm.stock <= 0) {
        this.errors.stock = "Le stock doit être positif.";
        setTimeout(() => {
          this.errors.stock = null;
        }, 3000);
      }
      if (!this.editForm.dateDispo) {
        this.errors.dateDispo = "La date est requise.";
        setTimeout(() => {
          this.errors.dateDispo = null;
        }, 3000);
      }
      if (this.editForm.prix <= 0) {
        this.errors.prix = "Le prix doit être positif.";
        setTimeout(() => {
          this.errors.prix = null;
        }, 3000);
      }

      return !Object.values(this.errors).some((error) => error !== null);
    },
    async saveItem(item) {
      if (!this.validateFields()) return; // Valide les champs avant la sauvegarde

      try {
        // Met à jour l'élément dans Firestore
        const docRef = doc(db, "materials", item.id);
        await updateDoc(docRef, { ...this.editForm });

        // Met à jour les données locales
        Object.assign(item, this.editForm);

        // Réinitialise l'état d'édition
        this.editableItem = null;
        this.errors = {};
      } catch (error) {
        console.error("Erreur Firebase :", error);

        // Gestion des erreurs Firebase
        if (error.code === "permission-denied") {
          this.errors.firebase =
            "Vous n'avez pas la permission de modifier cet élément.";
        } else if (error.code === "not-found") {
          this.errors.firebase = "L'élément à modifier est introuvable.";
        } else if (error.code === "unavailable") {
          this.errors.firebase =
            "Le service est actuellement indisponible. Vérifiez votre connexion.";
        } else if (error.code === "deadline-exceeded") {
          this.errors.firebase =
            "La connexion avec la base de données a expiré. Réessayez plus tard.";
        } else {
          this.errors.firebase = "Une erreur inattendue s'est produite.";
        }
        setTimeout(() => {
          this.errors.firebase = null;
        }, 5000);
      }
    },
  },
};
</script>


<style scoped>
.title {
  margin: 80px auto;
  text-align: center;
  margin-bottom: 20px;
}

.full-page-table {
  width: 100%;
  height: 70%;
  table-layout: fixed;
}

.is-center {
  text-align: center;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination .button {
  margin: 0 5px;
}

.help.is-danger {
  color: #ff3860; /* Rouge Bulma */
  font-size: 0.85em;
  margin-top: 5px;
}
</style>
