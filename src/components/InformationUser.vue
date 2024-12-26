<template>
    <div class="user-widget">
        <div v-if="isConnected">
            <p class="information">Bienvenue, <strong>{{ currentUser.name }}</strong>!</p>
            <div class="information-details">
                <p><em>Email :</em> {{ currentUser.email }}</p>
                <p><em>Rôle :</em> {{ currentUser.role }}</p>
                <p><em>Membre depuis :</em> {{ formatDate(currentUser.createdAt) }}</p>
            </div>
        </div>
        <div v-else>
            <p>Vous n'êtes pas connecté.</p>
            <button class="button is-small is-primary" >Vous n'êtes pas connecté</button>
        </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "ActiveUser",
    props: {
      isConnected: { type: Boolean, required: true },
      currentUser: { 
        type: Object, 
        required: true, 
      },
    },
    methods: {
        formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('fr-FR', options);
        }    
    },
  };
  </script>

  <style scoped>
    .user-widget {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 1rem;
        padding: 2rem;
        border: 1px solid #ccc;
        border-radius: 5px;
        color: #b3b3b3;
    }

    .information {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        line-height: 1.5;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .information-details {
        margin-top: 3rem;
        align-items: left;
        justify-content: left;
        font-size: 20px;
    }
    </style>