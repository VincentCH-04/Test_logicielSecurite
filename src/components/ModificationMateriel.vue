<template>
  <div>
    <h1 class="title">Modification de matériel</h1>
    <table class="table is-bordered full-page-table is-center">
      <thead>
        <tr>
          <th>NAME</th>
          <th>REFERENCE</th>
          <th>CONSTRUCTEUR</th>
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
            <td class="is-loading">
              <input
                class="input"
                v-model="editForm.name"
                type="text"
                placeholder="Nom"
              />
              <p v-if="errors.name" class="help is-danger">{{ errors.name }}</p>
            </td>
            <td class="is-loading">
              <input
                class="input"
                v-model="editForm.reference"
                type="text"
                placeholder="Reference"
              />
              <p v-if="errors.reference" class="help is-danger">{{ errors.reference }}</p>
            </td>
            <td class="is-loading">
              <input
                class="input"
                v-model="editForm.constructeur"
                type="text"
                placeholder="Constructeur"
              />
              <p v-if="errors.constructeur" class="help is-danger">{{ errors.constructeur }}</p>
            </td>
            <td class="is-loading">
              <input
                class="input"
                v-model.number="editForm.stock"
                type="number"
                placeholder="Stock"
              />
              <p v-if="errors.stock" class="help is-danger">{{ errors.stock }}</p>
            </td>
            <td class="is-center is-vcentered is-loading">
              <input
                type="date"
                v-model="editForm.dateDispo"
                @input="editForm.dateDispo = $event.target.value.split('-').reverse().join('-')"
              />
              <p v-if="errors.dateDispo" class="help is-danger">
                {{ errors.dateDispo }}
              </p>
            </td>
            <td class="is-loading">
              <input
                class="input"
                v-model.number="editForm.prix"
                type="number"
                placeholder="Prix"
              />
              <p v-if="errors.prix" class="help is-danger">{{ errors.prix }}</p>
            </td>
            <td>
              <button class="button is-success is-small rectangle" @click="saveItem(item)">VALIDER</button>
              <button class="button is-danger is-small rectangle" @click="cancelEdit">ANNULER</button>
            </td>
          </template>
          <template v-else>
            <!-- Affichage en lecture seule -->
            <td>{{ item.name }}</td>
            <td>{{ item.reference }}</td>
            <td>{{ item.constructeur }}</td>
            <td>{{ item.stock }}</td>
            <td>{{ item.dateDispo }}</td>
            <td>{{ item.prix }}</td>
            <td>
              <button class="button is-primary is-small rectangle" @click="editItem(item)">MODIFIER</button>
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
import { collection, getDocs, doc, updateDoc } from "firebase/firestore";
import { db } from "../firebase";

export default {
  data() {
    return {
      items: [], // Liste vide pour charger les données Firestore
      editableItem: null,
      editForm: {
        name: "",
        reference: "",
        constructeur: "",
        stock: 0,
        dateDispo: "",
        prix: 0,
      },
      errors: {
        name: null,
        reference: null,
        constructeur: null,
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
    async fetchItems() {
      try {
        const querySnapshot = await getDocs(collection(db, "Materiels"));
        this.items = querySnapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
        }));
      } catch (error) {
        console.error("Erreur lors du chargement des matériels :", error);
        this.errors.firebase = "Impossible de charger les données.";
      }
    },
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
        reference: null,
        constructeur: null,
        stock: null,
        dateDispo: null,
        prix: null,
        firebase: null,
      };

      if (!this.editForm.name) {
        this.errors.name = "Le nom est requis.";
      }
      if (!this.editForm.reference) {
        this.errors.reference = "La référence est requise.";
      }
      if (!this.editForm.constructeur) {
        this.errors.constructeur = "Le constructeur est requis.";
      }
      if (this.editForm.stock <= 0) {
        this.errors.stock = "Le stock doit être positif.";
      }
      if (!this.editForm.dateDispo) {
        this.errors.dateDispo = "La date est requise.";
      }
      if (this.editForm.prix <= 0) {
        this.errors.prix = "Le prix doit être positif.";
      }

      // Vérification de la référence en double
      const referenceExists = this.items.some(
        (existingItem) =>
          existingItem.reference === this.editForm.reference &&
          existingItem.id !== this.editableItem.id // Ignore l'élément en cours d'édition
      );

      if (referenceExists) {
        this.errors.reference = "Cette référence existe déjà.";
      }

      // Vérification du nom en double
      const nameExists = this.items.some(
        (existingItem) =>
          existingItem.name.toLowerCase() === this.editForm.name.toLowerCase() &&
          existingItem.id !== this.editableItem.id
      );

      if (nameExists) {
        this.errors.name = "Ce nom existe déjà.";
      }

      return !Object.values(this.errors).some((error) => error !== null);
    },
    async saveItem(item) {
      if (!this.validateFields()) return;

      try {
        const docRef = doc(db, "Materiels", item.id);
        await updateDoc(docRef, { ...this.editForm });
        Object.assign(item, this.editForm);
        this.editableItem = null;
      } catch (error) {
        console.error("Erreur Firebase :", error);
        this.errors.firebase = "Erreur de mise à jour.";
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('fr-FR', options);
    }
  },
  mounted() {
    this.fetchItems(); // Charger les matériels au montage du composant
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

.is-loading {
  background-color: rgb(0, 35, 148);
}

.rectangle {
  margin: 5px;
  width: 40%;
  font-size: 70%;
  align-content: baseline;
}
</style>
