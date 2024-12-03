<template>
    <div class="edit-material-container">
      <h1 class="title">Modifier un Matériel</h1>
      <form @submit.prevent="updateMaterial">
        <div class="field">
          <label class="label">Nom du Matériel</label>
          <div class="control">
            <input
              class="input"
              type="text"
              v-model="material.name"
              placeholder="Nom du matériel"
              required
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label">Stock</label>
          <div class="control">
            <input
              class="input"
              type="number"
              v-model="material.stock"
              placeholder="Quantité en stock"
              required
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label">Date de Disponibilité</label>
          <div class="control">
            <input
              class="input"
              type="date"
              v-model="material.dateDispo"
              required
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label">Prix</label>
          <div class="control">
            <input
              class="input"
              type="number"
              step="0.01"
              v-model="material.prix"
              placeholder="Prix du matériel"
              required
            />
          </div>
        </div>
  
        <div class="field">
          <div class="control">
            <button class="button is-primary" type="submit">Modifier</button>
          </div>
        </div>
      </form>
  
      <div v-if="message" class="notification" :class="{ 'is-success': success, 'is-danger': !success }">
        {{ message }}
      </div>
    </div>
  </template>

<script>
import { doc, getDoc, updateDoc } from "firebase/firestore"; // Import Firestore méthodes
import { db } from "../firebase"; // Importez votre instance Firestore

export default {
  data() {
    return {
      material: {
        id: null,
        name: "",
        stock: 0,
        dateDispo: "",
        prix: 0,
      },
      message: null,
      success: false,
    };
  },
  methods: {
    async fetchMaterial(id) {
      try {
        const docRef = doc(db, "materials", id); // Référence au document
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
          this.material = { id, ...docSnap.data() }; // Charge les données
        } else {
          this.message = "Le matériel n'existe pas.";
          this.success = false;
        }
      } catch (error) {
        console.error("Erreur lors du chargement :", error);
        this.message = "Erreur lors du chargement du matériel.";
        this.success = false;
      }
    },
    async updateMaterial() {
      try {
        const docRef = doc(db, "materials", this.material.id); // Référence au document
        await updateDoc(docRef, {
          name: this.material.name,
          stock: this.material.stock,
          dateDispo: this.material.dateDispo,
          prix: this.material.prix,
        });

        this.message = "Matériel mis à jour avec succès !";
        this.success = true;
      } catch (error) {
        console.error("Erreur lors de la mise à jour :", error);
        this.message = "Erreur lors de la mise à jour du matériel.";
        this.success = false;
      }
    },
  },
  mounted() {
    const materialId = "idDuMateriel"; // Remplacez par un identifiant dynamique ou paramètre de route
    this.fetchMaterial(materialId);
  },
};
</script>


<style scoped>
.edit-material-container {
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
