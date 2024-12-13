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
              required
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label control" for="stock">Stock</label>
            <div class="control">
              <input class="input" type="number" id="stock" v-model="material.stock"
                placeholder="Quantité en stock" required />
            </div>
        </div>
  
        <div class="field">
          <label class="label" for="dateDispo">Date de Disponibilité</label>
          <div class="control">
            <input
              class="input"
              type="date"
              id="dateDispo"
              v-model="material.dateDispo"
              required
            />
          </div>
        </div>
  
        <div class="field">
          <label class="label" for="prix">Prix</label>
          <div class="control">
            <input
              class="input"
              type="number"
              id="prix"
              step="0.01"
              v-model="material.prix"
              placeholder="Prix du matériel"
              required
            />
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
import { collection, addDoc } from "firebase/firestore"; // Import Firestore
import { db } from "../firebase"; // Importez l'instance Firestore

export default {
  data() {
    return {
      material: {
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
    async createMaterial() {
      try {
        // Ajouter un nouveau document dans la collection "materials"
        await addDoc(collection(db, "materials"), {
          name: this.material.name,
          stock: this.material.stock,
          dateDispo: this.material.dateDispo,
          prix: this.material.prix,
        });

        // Afficher un message de succès
        this.message = "Matériel créé avec succès !";
        this.success = true;

        // Réinitialiser le formulaire
        this.material = {
          name: "",
          stock: 0,
          dateDispo: "",
          prix: 0,
        };
      } catch (error) {
        console.error("Erreur lors de la création :", error);
        this.message = "Erreur lors de la création du matériel.";
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
