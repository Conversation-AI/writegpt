// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyBY86PE6ZGDzAiQtGLQL0Gv4rItuEVweY0",
    authDomain: "writegpt-cai.firebaseapp.com",
    projectId: "writegpt-cai",
    storageBucket: "writegpt-cai.appspot.com",
    messagingSenderId: "1039449579705",
    appId: "1:1039449579705:web:1b9c110fef66b7f256bb68",
    measurementId: "G-MPDTFFR1QK",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
