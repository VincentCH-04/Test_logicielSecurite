<template>
    <div v-if="reservations.length > 0">
      <table class="table is-bordered full-page-table is-center">
        <thead>
          <tr>
            <th>NAME</th>
            <th>REFERENCE</th>
            <th>QUANTITE</th>
            <th>DATE EMPRUNT</th>
            <th>PRIX</th>
            <th v-if="isConnected">Actions</th>
          </tr>
        </thead>
        <tbody>
            <tr v-for="reservation in reservations" :key="reservation.id">
              <td>{{ reservation.material?.name || "Matériel introuvable" }}</td>
              <td>{{ reservation.material?.reference || "N/A" }}</td>
              <td>{{ reservation.quantity }}</td>
              <td>{{ reservation.date || "Non spécifiée" }}</td>
              <td>{{ reservation.material?.prix || "N/A" }} €</td>
              <td v-if="isConnected">
                <button v-if="!reservation.returned" class="button is-warning is-small" @click="returnMaterial(reservation.material)">RENDRE</button>
              </td>
            </tr>
        </tbody>
      </table>
  
      <!-- Pagination -->
      <div class="pagination">
        <button class="button" @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} sur {{ totalPages }}</span>
        <button class="button" @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      </div>

    </div>
    <div v-else>
      <p class="is-center no-material">Aucun matériel réservé</p>
    </div>
  </template>
  
  <script>
  import { collection, getDocs, doc, updateDoc } from "firebase/firestore";
  import { db } from "../firebase";
  
  export default {
    name: "MainContent",
    props: {
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
        itemsPerPage: 4,
        successMessage: null,
        errorMessage: null,
      };
    },
    computed: {
      totalPages() {
        return this.reservations.length > 0 ? Math.ceil(this.reservations.length / this.itemsPerPage) : 0;
      },
      paginatedItems() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        return this.reservations.slice(start, start + this.itemsPerPage);
      },
    },
    methods: {
      formatDate(timestamp) {
        if (!timestamp) return "Non spécifiée";
        const date = new Date(timestamp);
        return date.toLocaleDateString("fr-FR");
      },
      async fetchReservations() {
        try {
          const reservationSnapshot = await getDocs(collection(db, "Réservation"));
          const rawReservations = reservationSnapshot.docs.map((doc) => ({
            id: doc.id,
            ...doc.data(),
          }));

          // Récupérer tous les matériels pour enrichir les données
          const materialSnapshot = await getDocs(collection(db, "Materiels"));
          const materials = materialSnapshot.docs.reduce((acc, doc) => {
            acc[doc.id] = { id: doc.id, ...doc.data() };
            return acc;
          }, {});

          // Filtrer les réservations non retournées
          this.reservations = rawReservations
            .filter((reservation) => !reservation.returned) // Filtrer les réservations non retournées
            .map((reservation) => ({
              ...reservation,
              material: materials[reservation.itemId] || null,
            }));
        } catch (error) {
          console.error("Erreur lors du chargement des réservations :", error);
          this.reservations = [];
        }
      },
      async returnMaterial(item) {
        try {
          const reservation = this.reservations.find(
            (res) =>
              res.itemId=== item.id &&
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
      nextPage() {
        if (this.currentPage < this.totalPages) this.currentPage++;
      },
      prevPage() {
        if (this.currentPage > 1) this.currentPage--;
      },
    },
    mounted() {
      this.fetchReservations();
    },
  };
  </script>
  

  <style scoped>
  .no-material {
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    margin-top: 100px;
    color: #b3b3b3;
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
  