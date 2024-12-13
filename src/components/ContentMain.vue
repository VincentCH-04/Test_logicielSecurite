<template>
  <div>
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
      <tbody >
        <tr v-for="(item, index) in paginatedItems" :key="index">
            <td>{{ item.name }}</td>
            <td>{{ item.stock }}</td>
            <td>{{ item.dateDispo }}</td>
            <td>{{ item.prix }}</td>
            <td>
              <button class="button is-primary is-small" @click="showReservationPopup(item)">RESERVER</button>
              <button class="button is-danger is-small" @click="showDeletePopup(item)">SUPPRIMER</button>
            </td>
          </tr>
      </tbody>
    </table>
    <div class="pagination">
      <button class="button" @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="button" @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>

    <div class="modal" :class="{ 'is-active': showDeleteModal }">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirmer la Suppression</p>
          <button class="delete" aria-label="close" @click="closeDeletePopup"></button>
        </header>
        <section class="modal-card-body">
          <p style="color: green;">Êtes-vous sûr de vouloir supprimer <strong>{{ itemToDelete?.name }}</strong> ?</p>
          <input class="input" type="number" v-model="suppresion.quantity" placeholder="Entrez la quantité" required/>
          <p v-if="successMessage" class="notification is-success">{{ successMessage }}</p>
          <p v-if="errorMessage" class="notification is-danger">{{ errorMessage }}</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="deleteItem">Supprimer</button>
          <button class="button" @click="closeDeletePopup">Annuler</button>
        </footer>
      </div>
    </div>
    
    <div class="modal" :class="{ 'is-active': showReservationModal }">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Réserver {{ itemToReserve?.name }}</p>
          <button class="delete" aria-label="close" @click="closeReservationPopup"></button>
        </header>
        <section class="modal-card-body">
          <form @submit.prevent="reserveItem">
            <div class="field">
              <label class="label" for="reservation-quantity">Quantité</label>
              <div class="control">
                <input
                  class="input"
                  type="number"
                  id="reservation-quantity"
                  v-model="reservation.quantity"
                  placeholder="Entrez la quantité"
                  required
                />
              </div>
            </div>

            <div class="field">
              <label class="label" for="reservation-name">Nom du Réservant</label>
              <div class="control">
                <input
                  class="input"
                  type="text"
                  id="reservation-name"
                  v-model="reservation.name"
                  placeholder="Entrez votre nom"
                  required
                />
              </div>
            </div>

            <div class="field">
              <div class="control">
                <button class="button is-primary" type="submit">Confirmer</button>
                <button class="button" @click="closeReservationPopup" type="button">Annuler</button>
              </div>
            </div>
            <p v-if="successMessage" class="notification is-success">{{ successMessage }}</p>
            <p v-if="errorMessage" class="notification is-danger">{{ errorMessage }}</p>
          </form>
        </section>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'MainContent',
  data(){
    return {
      items: [
        { name: "Item 1", stock: 10, dateDispo: "2024-12-10", prix: 20 },
        { name: "Item 2", stock: 5, dateDispo: "2024-12-12", prix: 15 },
        { name: "Item 3", stock: 8, dateDispo: "2024-12-15", prix: 25 },
        { name: "Item 4", stock: 3, dateDispo: "2024-12-18", prix: 30 },
      ],
      showDeleteModal: false,
      itemToDelete: null,
      suppresion: {
        quantity: 1,
      },

      currentPage: 1,
      itemsPerPage: 4,

      showReservationModal: false,
      itemToReserve: null,
      reservation: {
        quantity: 1,
        name: "",
      },

      successMessage: null,
      errorMessage: null
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
    }
  },
  methods: {
    showReservationPopup(item) {
      this.itemToReserve = item; // Définit l'élément à réserver
      this.showReservationModal = true; // Affiche la popup
    },
    closeReservationPopup() {
      this.showReservationModal = false; // Cache la popup
      this.itemToReserve = null; // Réinitialise l'élément
      this.reservation = { quantity: 1, name: "" }; // Réinitialise le formulaire
    },
    reserveItem() {
      try{
        setTimeout(() => {
          this.successMessage = null;
          this.errorMessage = null;
          this.closeReservationPopup();
        }, 3000);
        if(this.itemToReserve.stock === 0) {
          this.errorMessage = "Stock épuisé pour cet article";
          return;
        }
        if(this.itemToReserve.stock < this.reservation.quantity) {
          this.errorMessage = "Stock insuffisant pour cette quantité";
          return this.errorMessage;
        }
        if(this.reservation.quantity <= 0) {
          this.errorMessage = "Quantité invalide";
          return this.errorMessage
        }
        else{
          this.itemToReserve.stock -= this.reservation.quantity;
        }

        this.successMessage = "Réservation effectuée avec succès !";
        this.errorMessage = null;
      }
      catch(error){
        console.error("Erreur lors de la réservation :", error);
        this.errorMessage = "Erreur lors de la réservation.";
        this.successMessage = null;
      }
    },
    showDeletePopup(item) {
      this.itemToDelete = item; // Définit l'élément à supprimer
      this.showDeleteModal = true; // Affiche la popup
    },
    closeDeletePopup() {
      this.showDeleteModal = false; // Cache la popup
      this.itemToDelete = null; // Réinitialise l'élément à supprimer
    },
    deleteItem() {
      try{
        setTimeout(() => {
          this.successMessage = null;
          this.errorMessage = null;
          this.closeDeletePopup();
        }, 3000);
        if (this.itemToDelete.stock === 0) {
          this.errorMessage = "Stock épuisé pour cet article";
          return;
        }
        if (this.itemToDelete.stock < this.suppresion.quantity) {
          this.errorMessage = "Stock insuffisant pour cette quantité";
          return;
        }
        if (this.suppresion.quantity <= 0) {
          this.errorMessage = "Quantité invalide";
          return;
        }
        else{
          this.itemToDelete.stock -= this.suppresion.quantity;
        }

        this.errorMessage = null;
        this.successMessage = "Suppression effectuée avec succès !";
      }
      catch(error){
        console.error("Erreur lors de la suppression :", error);
        this.errorMessage = "Erreur lors de la suppression.";
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
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination .button {
  margin: 0 5px;
}

.full-page-table {
  margin: 20px auto;
  width: 100%;
  height: 80%;
  table-layout: fixed;
}

/* Center the table and not the content */
.is-center {
  text-align: center;
}

</style>
