<template>
    <div v-if="reservations.length > 0">
        <div class="filter-container" style="margin: 1% auto;">
            <div class="field is-grouped is-grouped-centered">
                <div class="control">
                    <label class="label" for="sortCriteria">Trier par :</label>
                    <div class="select is-rounded is-info" style="width: 100%;">
                        <select id="sortCriteria" v-model="sortCriteria" @change="fetchReservations">
                            <option value="date">Date d'emprunt</option>
                            <option value="material">Nom du matériel</option>
                            <option value="user">Nom du réservant</option>
                        </select>
                    </div>
                </div>
                <div class="control">
                    <button :class="['button', 'is-medium', isDescending ? 'is-danger' : 'is-success']" @click="toggleSortOrder" title="Inverser l'ordre du tri">
                        <span v-if="isDescending">
                            <i class="fas fa-arrow-down"></i>
                        </span>
                        <span v-else>
                            <i class="fas fa-arrow-up"></i>
                        </span>
                    </button>
                </div>
            </div>
        </div>
      <table class="table is-bordered full-page-table is-center">
        <thead>
          <tr>
            <th>NOM DU RÉSERVANT</th>
            <th>NOM DU MATÉRIEL</th>
            <th>RÉFÉRENCE</th>
            <th>QUANTITÉ</th>
            <th>DATE D'EMPRUNT</th>
            <th>ÉTAT</th>
            <th v-if="isConnected">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="reservation in paginatedItems" :key="reservation.id">
            <td>{{ reservation?.userName || "Utilisateur inconnu" }}</td>
            <td>{{ reservation.material?.name || "Matériel introuvable" }}</td>
            <td>{{ reservation.material?.reference || "N/A" }}</td>
            <td>{{ reservation.quantity }}</td>
            <td>{{ formatDate(reservation.date) || "Non spécifiée" }}</td>
            <td>{{ reservation.returned ? "Rendu" : "Non rendu" }}</td>
            <td v-if="isConnected">
              <button v-if="!reservation.returned" class="button is-warning is-small" @click="returnMaterial(reservation)">
                MARQUER COMME RENDU
              </button>
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
      <p class="is-center no-material">Aucune réservation effectuée</p>
    </div>
  </template>
  
  <script>
  import { collection, getDocs, doc, updateDoc } from "firebase/firestore";
  import { db } from "../firebase";
  
  export default {
    name: "MainContent",
    props: {
      isConnected: { type: Boolean, required: true },
    },
    data() {
      return {
        reservations: [],
        currentPage: 1,
        itemsPerPage: 5,
        isDescending: true,
        sortCriteria: "date",
        successMessage: null,
        errorMessage: null,
      };
    },
    computed: {
      totalPages() {
        return Math.ceil(this.reservations.length / this.itemsPerPage);
      },
      paginatedItems() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        return this.reservations.slice(start, start + this.itemsPerPage);
      },
    },
    methods: {
        formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString('fr-FR', options);
        },
        async fetchReservations() {
            try {
            const reservationSnapshot = await getDocs(collection(db, "Réservation"));
            const materialSnapshot = await getDocs(collection(db, "Materiels"));
            const userSnapshot = await getDocs(collection(db, "Utilisateurs"));
    
            const materials = materialSnapshot.docs.reduce((acc, doc) => {
                acc[doc.id] = { id: doc.id, ...doc.data() };
                return acc;
            }, {});
    
            const users = userSnapshot.docs.reduce((acc, doc) => {
                acc[doc.id] = { id: doc.id, ...doc.data() };
                return acc;
            }, {});
    
            this.reservations = reservationSnapshot.docs.map((doc) => {
                const data = doc.data();
                return {
                id: doc.id,
                ...data,
                material: materials[data.itemId] || null,
                user: users[data.userId] || null,
                date: new Date(data.date),
                };
            });

            this.reservations.sort((a, b) => {
                let comparison = 0;

                // Comparaison en fonction du critère choisi
                switch (this.sortCriteria) {
                case "date":
                    if(a.date == null) comparison = -1;
                    if(b.date == null) comparison = 1;
                    if(a.date < b.date) comparison = -1;
                    if(a.date > b.date) comparison = 1;
                    break;
                case "material":
                    comparison = a.material.name.localeCompare(b.material.name); // Tri par nom du matériel
                    break;
                case "user":
                    comparison = a.userName.localeCompare(b.userName); // Tri par nom du réservant
                    break;
                }

                // Inverser l'ordre si isDescending est true
                return this.isDescending ? -comparison : comparison;
            });
            } catch (error) {
            console.error("Erreur lors du chargement des réservations :", error);
            this.errorMessage = "Erreur lors du chargement des données.";
            setTimeout(() => (this.errorMessage = null), 3000);
            }
        },

        async returnMaterial(reservation) {
            try {
            const material = reservation.material;
            if (!material) throw new Error("Matériel introuvable.");
    
            // Marquer la réservation comme "rendu"
            await updateDoc(doc(db, "Réservation", reservation.id), { returned: true });
    
            // Remettre à jour le stock
            material.stock += reservation.quantity;
            await updateDoc(doc(db, "Materiels", material.id), { stock: material.stock });
    
            this.successMessage = "Matériel marqué comme rendu.";
            setTimeout(() => (this.successMessage = null), 3000);
            this.fetchReservations();
            } catch (error) {
            console.error("Erreur lors du retour :", error);
            this.errorMessage = "Erreur lors du retour du matériel.";
            setTimeout(() => (this.errorMessage = null), 3000);
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) this.currentPage++;
        },
        prevPage() {
            if (this.currentPage > 1) this.currentPage--;
        },
        toggleSortOrder() {
            this.isDescending = !this.isDescending;
            this.fetchReservations(); // Recharger les réservations après avoir inversé le tri
        },
        changeSortCriteria(criteria) {
            this.sortCriteria = criteria;
            this.fetchReservations(); // Recharger les réservations après avoir changé le critère
        },
    },
    mounted() {
        this.fetchReservations();
    },
};
  </script>
  
  <style scoped>

    .filter-container {
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .filter-container .label {
    font-size: 1.1rem;
    margin-right: 10px;
    }

    .table th {
    background-color: #0078d4;
    color: white;
    }

    .table td {
    text-align: center;
    }

    .button.is-small {
    border-radius: 20px;
    transition: all 0.3s;
    }

    .button.is-small:hover {
    background-color: #005fa3;
    color: white;
    transform: scale(1.05);
    }

    .is-rounded {
    border-radius: 30px;
    }

    .select.is-info {
    width: 180px;
    }

    .fas {
    font-size: 18px;
    }

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
  