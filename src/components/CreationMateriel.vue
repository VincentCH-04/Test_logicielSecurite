<template>
  <div class="create-material-container">
    <h1 class="title">Créer un Nouveau Matériel</h1>
    <form @submit.prevent="createMaterial">
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
        <label class="label">ID de l'Utilisateur</label>
        <div class="control">
          <input
              class="input"
              type="text"
              v-model="material.userId"
              placeholder="ID de l'utilisateur"
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
import { collection, addDoc, doc, setDoc } from "firebase/firestore"; // Import Firestore
import { db } from "../firebase"; // Importez l'instance Firestore

export default {
  data() {
    return {
      material: {
        name: "",
        stock: 0,
        prix: 0,
        userId: "", // ID de l'utilisateur auquel le matériel sera attribué
      },
      message: null,
      success: false,
    };
  },
  methods: {
    async createMaterial() {
      if (!this.material.name || !this.material.userId) {
        this.message = "Le nom du matériel et l'ID utilisateur sont requis.";
        this.success = false;
        return;
      }

      try {
        // Ajouter le matériel principal dans la collection "Materiels"
        const materialRef = await addDoc(collection(db, "Materiels"), {
          name: this.material.name,
          stock: this.material.stock,
          prix: this.material.prix,
          userId: this.material.userId,
          dateAjout: new Date().toISOString(), // Date d'ajout automatique
        });

        // Ajouter les unités dans la sous-collection "Units"
        for (let i = 0; i < this.material.stock; i++) {
          const unitRef = doc(collection(materialRef, "Units"));
          await setDoc(unitRef, {
            materialId: materialRef.id,  // ID du matériel parent
            userId: this.material.userId, // ID de l'utilisateur
            status: "Disponible", // Statut initial de l'unité (ex : disponible)
            dateAjout: new Date().toISOString(), // Date d'ajout de l'unité
          });
        }

        // Message de succès
        this.message = "Matériel créé avec succès avec les unités associées.";
        this.success = true;

        // Réinitialiser le formulaire
        this.material = {
          name: "",
          stock: 0,
          prix: 0,
          userId: "",
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
