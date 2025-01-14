<template>
    <footer class="footer" :style="footerStyle">
        <div class="footer-container">
        <div class="footer-section">
            <a @click="toggleContact">Contact</a>
            <p v-if="contactVisu" class="footer-section">
                vincent.chaumette@etu.univ-tours.fr
            <br>ewen.lapaix@etu.univ-tours.fr
            <br>flavien.absolu@etu.univ-tours.fr
            <br>mehdi.sibous@etu.univ-tours.fr
            <br>timothee.debey@etu.univ-tours.fr
            <br>dimitri.britan@etu.univ-tours.fr
            </p>
        </div>
        <div v-if="isAdmin" class="footer-section">
            <a href="https://drive.google.com/drive/u/0/folders/1_zZupTXEe4kw6BTCLBjRtK7SQmZbKkkE">Drive</a>
        </div>
        <div class="footer-section">
            © Tous droits réservés 2024 Locomate
        </div>
        <div class="footer-section">
            Version {{ version }}
        </div>
        <div @click="toggleAPropos" class="footer-section">
            <a>À propos de Locomate</a>
            <div v-if="AProposVisu" class="footer-columns">
                <div class="footer-column">
                    <p>Vincent CHAUMETTE</p>
                    <p>Ewen LAPAIX</p>
                    <p>Flavien ABSOLU</p>
                </div>
                <div class="footer-column">
                    <p>Mehdi SIBOUS</p>
                    <p>Timothee DEBEY</p>
                    <p>Dimitri BRITAN</p>
                </div>
            </div>
        </div>
        </div>
    </footer>
</template>

<script>
import packageJson from '../../package.json';

export default {
    name: 'FooterBar',
    props: {
        isAdmin: {
            type: Boolean,
            required: true
        },
        footerStyle: {  
            type: Object,
            required: true,
        }
    },
    data() {
        return{
            contactVisu: false,
            AProposVisu: false,
            version: packageJson.version
        };
    },
    methods: {
        toggleContact() {
            this.contactVisu = !this.contactVisu;
        },
        toggleAPropos() {
            this.AProposVisu = !this.AProposVisu;
        }
    }
};
</script>

<style scoped>
.footer {
  width: 100%;
  background-color: #000000;
  padding: 10px 0;
  position: absolute;
  bottom: 0;
}

.footer-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  flex-wrap: wrap;
}

.footer-section {
    margin: 5px;
    color: white;
}

.footer-columns {
  display: flex;
  justify-content: space-between;
}

.footer-column {
  margin: 0 10px;
}
</style>