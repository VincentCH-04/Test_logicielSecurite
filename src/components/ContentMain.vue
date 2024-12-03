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
              <button class="button is-primary is-small" @click="reserveItem(item)">BP RESERVER</button>
              <button class="button is-danger is-small" @click="deleteItem(item)">BP SUPPRIMER</button>
            </td>
          </tr>
      </tbody>
    </table>
    <div class="pagination">
      <button class="button" @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="button" @click="nextPage" :disabled="currentPage === totalPages">Next</button>
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
      currentPage: 1,
      itemsPerPage: 4
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
    reserveItem(item) {
      //Exemple de modification
      if(item.stock === 0) {
        alert(`Stock épuisé pour: ${item.name}`);
        //Dans 2jours
        const twoDaysInMilliseconds = 2 * 24 * 60 * 60 * 1000;
        item.dateDispo = new Date(Date.now() + twoDaysInMilliseconds).toISOString().split('T')[0];
        return;
      }
      else{
        alert(`Réservation pour: ${item.name}`);
        item.stock -= 1;
      }
    },
    deleteItem(item) {
      alert(`Suppression de: ${item.name}`);
      this.items = this.items.filter(i => i !== item); // Exemple de suppression
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

.table-container {
  width: calc(100vw - 20px);
  height: 100vh; /* Full viewport height */
  margin: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.full-page-table {
  width: 100%; /* Adjust the width as needed */
  height: 80%;
  table-layout: fixed;
}

/* Center the table and not the content */
.is-center {
  text-align: center;
}

</style>
