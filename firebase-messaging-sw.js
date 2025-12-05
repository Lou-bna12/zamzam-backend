importScripts("https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyCV5Yz4_JDH5ruzYOSEHfqFNHaeQBTgRjc",
  authDomain: "zamzam-notifications.firebaseapp.com",
  projectId: "zamzam-notifications",
  storageBucket: "zamzam-notifications.firebasestorage.app",
  messagingSenderId: "994562800924",
  appId: "1:994562800924:web:26589b49ea0218ed804ed9"
});

const messaging = firebase.messaging();

// 🎉 Affichage de la notification reçue
messaging.onBackgroundMessage((payload) => {
  console.log("📩 Notification reçue :", payload);

  self.registration.showNotification(payload.notification.title, {
    body: payload.notification.body,
    icon: "/favicon.ico"
  });
});
