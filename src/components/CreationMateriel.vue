<template>
  <div class="create-material-container">
    <h1 class="title">Créer un Nouveau Matériel</h1>
    <form @submit.prevent="createMaterial">
      <div class="field">
        <label class="label" for="materialName">Nom du Matériel</label>
        <div class="control">
          <input
            class="input"
            type="text"
            id="materialName"
            v-model="material.name"
            placeholder="Nom du matériel"
            :class="{ 'is-danger': errors.name }"
          />
        </div>
        <p v-if="errors.name" class="error-message">{{ errors.name }}</p>
      </div>

      <div class="field">
        <label class="label" for="referenceName">Référence</label>
        <div class="control">
          <input
            class="input"
            type="text"
            id="referenceName"
            v-model="material.reference"
            placeholder="Référence"
            :class="{ 'is-danger': errors.reference }"
          />
        </div>
        <p v-if="errors.reference" class="error-message">{{ errors.reference }}</p>
      </div>

      <div class="field">
        <label class="label" for="constructeurName">Constructeur</label>
        <div class="control">
          <input
            class="input"
            type="text"
            id="constructeurName"
            v-model="material.constructeur"
            placeholder="Constructeur"
            :class="{ 'is-danger': errors.constructeur }"
          />
        </div>
        <p v-if="errors.constructeur" class="error-message">{{ errors.constructeur }}</p>
      </div>

      <div class="field">
        <label class="label" for="stock">Stock</label>
        <div class="control">
          <input
            class="input"
            type="number"
            id="stock"
            v-model.number="material.stock"
            placeholder="Quantité en stock"
            :class="{ 'is-danger': errors.stock }"
          />
        </div>
        <p v-if="errors.stock" class="error-message">{{ errors.stock }}</p>
      </div>

      <div class="field">
        <label class="label" for="dateDispo">Date de Disponibilité</label>
        <div class="control">
          <input
            class="input"
            type="date"
            id="dateDispo"
            v-model="material.dateDispo"
            :class="{ 'is-danger': errors.dateDispo }"
          />
        </div>
        <p v-if="errors.dateDispo" class="error-message">{{ errors.dateDispo }}</p>
      </div>

      <div class="field">
        <label class="label" for="prix">Prix</label>
        <div class="control">
          <input
            class="input"
            type="number"
            id="prix"
            step="0.01"
            v-model.number="material.prix"
            placeholder="Prix du matériel"
            :class="{ 'is-danger': errors.prix }"
          />
        </div>
        <p v-if="errors.prix" class="error-message">{{ errors.prix }}</p>
      </div>

      <div class="field">
        <div class="control">
          <button class="button is-primary" type="submit">Créer</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { collection, addDoc } from "firebase/firestore";
import { db } from "../firebase";

export default {
  data() {
    return {
      material: {
        name: "",
        reference: "",
        constructeur: "",
        stock: null,
        dateDispo: "",
        prix: null,
      },
      errors: {}, // Gestion des erreurs pour chaque champ
      message: null,
      success: false,
    };
  },
  methods: {
    validateForm() {
      setTimeout(() => {
        this.errors = {};
      }, 3000); // 3 secondes

      if (!this.material.name.trim()) this.errors.name = "Le nom du matériel est requis.";
      if (!this.material.reference.trim()) this.errors.reference = "La référence est requise.";
      if (!this.material.constructeur.trim()) this.errors.constructeur = "Le constructeur est requis.";
      if (this.material.stock === null || this.material.stock < 0)
        this.errors.stock = "Le stock doit être un nombre positif.";
      if (!this.material.dateDispo) this.errors.dateDispo = "La date de disponibilité est requise.";
      if (this.material.prix === null || this.material.prix < 0)
        this.errors.prix = "Le prix doit être un nombre positif.";

      return Object.keys(this.errors).length === 0; // Retourne true si aucune erreur
    },

    async createMaterial() {
      if (!this.validateForm()) {
        this.message = "Veuillez corriger les erreurs avant de soumettre.";
        this.success = false;
        return;
      }

      try {
        await addDoc(collection(db, "Materials"), {
          name: this.material.name,
          reference: this.material.reference,
          constructeur: this.material.constructeur,
          stock: this.material.stock,
          dateDispo: this.material.dateDispo,
          prix: this.material.prix,
        });

        this.message = "Matériel créé avec succès !";
        this.success = true;

        this.material = {
          name: "",
          reference: "",
          constructeur: "",
          stock: null,
          dateDispo: "",
          prix: null,
        };

      } catch (error) {
        console.error("Erreur Firebase :", error.code, error.message);
        this.message = "Erreur lors de la création du matériel : " + error.message;
        this.success = false;
      }
    },
  },
};
</script>

<style scoped>
.create-material-container {
  max-width: 1000px;
  margin: 30px auto;
  padding: 30px;
  color: #f5f5f5;
  border-radius: 8px;
}

.label {
  color: #f5f5f5;
}

.input.is-danger {
  border-color: #e74c3c;
}

.error-message {
  color: #e74c3c;
  font-size: 0.85em;
  margin-top: 5px;
}

.notification.is-success {
  background-color: #2ecc71;
}

.notification.is-danger {
  background-color: #e74c3c;
}
</style>
