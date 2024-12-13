// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth } from "firebase/auth";
//import { getStorage } from "firebase/storage";
//import { getMessaging } from "firebase/messaging";
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDAacX1f-MhIP2jLtVowTMgtpfnhB7R5JM",
  authDomain: "test-logiciel-vincent.firebaseapp.com",
  projectId: "test-logiciel-vincent",
  storageBucket: "test-logiciel-vincent.firebasestorage.app",
  messagingSenderId: "917926047092",
  appId: "1:917926047092:web:cdbdde616442bf75701021"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Export the database for components to use.
const db = getFirestore(app);

// Export the auth for components to use.
const auth = getAuth(app);

export { db, auth };