<template>
  <div>
    <div v-if="isLoadingReservations">
      Chargement des données...
    </div>
    <table class="table is-bordered full-page-table is-center" v-else>
      <thead>
        <tr>
          <th>NAME</th>
          <th>REFERENCE</th>
          <th>CONSTRUCTEUR</th>
          <th>STOCK</th>
          <th>DATE DISPO</th>
          <th>PRIX</th>
          <th v-if="isConnected">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in paginatedItems" :key="index">
          <td>{{ item.name }}</td>
          <td>{{ item.reference }}</td>
          <td>{{ item.constructeur }}</td>
          <td>{{ item.stock }}</td>
          <td>{{ formatDate(item.dateDispo) }}</td>
          <td>{{ item.prix }}</td>
          <td v-if="isConnected">
            <button class="button is-primary rectangle" v-if="canReserve(item)" @click="showReservationPopup(item)">RESERVER</button>
            <button v-if="canReturn(item)" class="button is-warning rectangle" @click="returnMaterial(item)">RENDRE</button>
            <button v-if="isAdmin" class="button is-danger rectangle" @click="showDeletePopup(item)">SUPPRIMER</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Pagination -->
    <div class="pagination">
      <button class="button" @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="button" @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>

    <!-- Modal Suppression -->
    <div class="modal" :class="{ 'is-active': showDeleteModal }">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Confirmer la Suppression</p>
          <button class="delete" aria-label="close" @click="closeDeletePopup"></button>
        </header>
        <section class="modal-card-body">
          <p>Êtes-vous sûr de vouloir supprimer <strong>{{ itemToDelete?.name }}</strong> ?</p>
          <input class="input" type="number" v-model="suppression.quantity" placeholder="Entrez la quantité" required />
          <p v-if="successMessage" class="notification is-success">{{ successMessage }}</p>
          <p v-if="errorMessage" class="notification is-danger">{{ errorMessage }}</p>
        </section>
        <footer class="modal-card-foot">
          <button class="button is-danger" @click="deleteItem">Supprimer</button>
          <button class="button" @click="closeDeletePopup">Annuler</button>
        </footer>
      </div>
    </div>

    <!-- Modal Réservation -->
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
              <input id="reservation-quantity" class="input" type="number" v-model="reservation.quantity" required />
            </div>
            <div class="field">
              <label class="label" for="reservation-name">Nom du Réservant</label>
              <input id="reservation-name" class="input" type="text" v-model="reservation.name" :placeholder="this.currentUser?.firstName +' '+ this.currentUser?.lastName || ''" disabled/>
            </div>
            <div class="field">
              <label class="label" for="reservation-name">Date de la réservation</label>
              <input id="reservation-name" class="input" type="text" v-model="reservation.date" :placeholder="formatDate(Date.now())" disabled/>
            </div>
            <div class="field">
              <button class="button is-primary" type="submit">Confirmer</button>
              <button class="button" @click="closeReservationPopup" type="button">Annuler</button>
            </div>
            <p v-if="successMessage" class="notification is-success">{{ successMessage }}</p>
            <p v-if="errorMessage" class="notification is-danger">{{ errorMessage }}</p>
          </form>
        </section>
      </div>
    </div>
    <p v-if="!isConnected" class="demande-connexion">
      Pour pouvoir réserver, vous devez vous connecter.
    </p>
  </div>
</template>

<script>
import { collection, getDocs, doc, updateDoc, addDoc } from "firebase/firestore";
import { db } from "../firebase";

export default {
  name: "MainContent",
  props: {
    isAdmin: { type: Boolean, required: true },
    isConnected: { type: Boolean, required: true },
    currentUser: { type: Object, required: true },
  },
  data() {
    return {
      items: [],
      reservations: [],
      showDeleteModal: false,
      itemToDelete: null,
      suppression: { quantity: 1 },
      showReservationModal: false,
      itemToReserve: null,
      reservation: { quantity: 1 },
      currentPage: 1,
      itemsPerPage: 6,
      successMessage: null,
      errorMessage: null,
      isLoadingReservations: true,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.items.length / this.itemsPerPage);
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.items.slice(start, start + this.itemsPerPage);
    },
  },
  methods: {
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('fr-FR', options);
    },
    canReserve(item) {
      if(this.isLoadingReservations) return false;

      const userReservation = this.reservations.find(
        (reservation) =>
          reservation.itemId === item.id &&
          reservation.userId === this.currentUser.id &&
          !reservation.returned
      );
      return !userReservation && item.stock > 0;
    },
    canReturn(item) {
      if(this.isLoadingReservations) return false;

      return this.reservations.some(
        (reservation) =>
          reservation.itemId === item.id &&
          reservation.userId === this.currentUser.id &&
          !reservation.returned
      );
    },
    async fetchReservations() {
      this.isLoadingReservations = true; // Commence à charger les réservations
      try {
        const reservationSnapshot = await getDocs(collection(db, "Réservation"));
        this.reservations = reservationSnapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data(),
        }));
      } catch (error) {
        console.error("Erreur lors du chargement des réservations :", error);
        this.reservations = [];
      }
      finally {
        this.isLoadingReservations = false; // Fin du chargement des réservations
      }
    },
    async fetchItems() {
      const snapshot = await getDocs(collection(db, "Materiels"));
      this.items = snapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
    },
    async returnMaterial(item) {
      try {
        const reservation = this.reservations.find(
          (res) =>
            res.itemId === item.id &&
            res.userId === this.currentUser.id && // Vérifie que c'est la réservation de l'utilisateur connecté
            !res.returned
        );

        if (!reservation) {
          this.errorMessage = "Réservation introuvable pour cet utilisateur.";
          setTimeout(() => (this.errorMessage = null), 3000);
          return;
        }

        // Marquer la réservation comme retournée
        await updateDoc(doc(db, "Réservation", reservation.id), { returned: true });

        // Remettre à jour le stock
        item.stock += reservation.quantity;
        await updateDoc(doc(db, "Materiels", item.id), { stock: item.stock });

        this.successMessage = "Matériel rendu avec succès.";
        setTimeout(() => (this.successMessage = null), 3000);
        this.fetchReservations();
      } catch (error) {
        this.errorMessage = "Une erreur est survenue lors du retour du matériel.";
        setTimeout(() => (this.errorMessage = null), 3000);
      }
    },
    showReservationPopup(item) {
      this.itemToReserve = item;
      this.reservation.name = this.currentUser.firstName+' '+this.currentUser.lastName || "";
      this.reservation.date = this.formatDate(Date.now());
      this.showReservationModal = true;
    },
    closeReservationPopup() {
      this.showReservationModal = false;
      this.reservation = { quantity: 1 };
    },
    async reserveItem() {
      // Validation des entrées
      if (!this.itemToReserve) {
        this.errorMessage = "Aucun article sélectionné pour la réservation.";
        setTimeout(() => (this.errorMessage = null), 3000);
        return;
      }

      if (!this.reservation.quantity || this.reservation.quantity <= 0) {
        this.errorMessage = "Veuillez saisir une quantité valide.";
        setTimeout(() => (this.errorMessage = null), 3000);
        return;
      }

      if (this.itemToReserve.stock < this.reservation.quantity) {
        this.errorMessage = "Stock insuffisant pour effectuer cette réservation.";
        setTimeout(() => (this.errorMessage = null), 3000);
        return;
      }

      try {
        // Mettre à jour le stock
        this.itemToReserve.stock -= this.reservation.quantity;
        console.log("Mise à jour du stock :", this.itemToReserve.stock);

        try {
          await updateDoc(doc(db, "Materiels", this.itemToReserve.id), {
            stock: this.itemToReserve.stock,
          });
        } catch (updateError) {
          console.error("Erreur lors de la mise à jour du stock :", updateError);
          throw new Error("Impossible de mettre à jour le stock dans la base de données.");
        }

        // Ajouter la réservation
        try {
          await addDoc(collection(db, "Réservation"), {
            quantity: this.reservation.quantity,
            userId: this.currentUser.id,
            userName: this.currentUser.firstName + " " + this.currentUser.lastName,
            itemId: this.itemToReserve.id,
            date: this.formatDate(Date.now()),
          });
        } catch (addError) {
          console.error("Erreur lors de l'ajout de la réservation :", addError);
          throw new Error("Impossible d'ajouter la réservation dans la base de données.");
        }

        this.successMessage = "Réservation réussie.";
        setTimeout(() => (this.successMessage = null), 3000);
        this.fetchReservations();
        setTimeout(this.closeReservationPopup, 2000);
      } catch (error) {
        console.error("Erreur générale lors de la réservation :", error);
        this.errorMessage = error.message || "Une erreur inconnue est survenue.";
        setTimeout(() => (this.errorMessage = null), 3000);
      }
    },
    showDeletePopup(item) {
      this.itemToDelete = item;
      this.showDeleteModal = true;
    },
    closeDeletePopup() {
      this.showDeleteModal = false;
      this.suppression = { quantity: 1 };
    },
    deleteItem() {
      if (
        this.itemToDelete.stock < this.suppression.quantity ||
        this.suppression.quantity <= 0
      ) {
        this.errorMessage = "Quantité invalide.";
        setTimeout(() => (this.errorMessage = null), 3000);
        return;
      }
      this.itemToDelete.stock -= this.suppression.quantity;
      this.successMessage = "Suppression effectuée.";
      setTimeout(() => (this.successMessage = null), 3000);
      this.closeDeletePopup();
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++;
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--;
    },
  },
  mounted() {
    this.fetchItems();
    this.fetchReservations();
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.demande-connexion {
  text-align: center;
  align-content: center;
  margin: 20px auto;
  height: 10%;
  width: 40%;
  color: #ffffff;
  background-color: #ff0033;
  border-radius: 5px;
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

.rectangle {
  margin: 5px;
  width: 40%;
  font-size: 70%;
  align-content: baseline;
}

.full-page-table {
  margin: 20px auto;
  width: 100%;
  height: 80%;
  table-layout: fixed;
}

.is-center {
  text-align: center;
}

</style>
