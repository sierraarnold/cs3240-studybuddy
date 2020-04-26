importScripts('https://www.gstatic.com/firebasejs/7.8.2/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.8.2/firebase-messaging.js');

//Firebase notifications configuration
var firebaseConfig = {
  apiKey: "AIzaSyAbKG0p096vmi75oPf2ZA5gkOfhTSpOIjk",
  authDomain: "study-buddy-103.firebaseapp.com",
  databaseURL: "https://study-buddy-103.firebaseio.com",
  projectId: "study-buddy-103",
  storageBucket: "study-buddy-103.appspot.com",
  messagingSenderId: "803195332373",
  appId: "1:803195332373:web:3c9c5b1a4fc27d1f562b1c",
};
firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

//When website is in background show a browser notification
messaging.setBackgroundMessageHandler(function(payload) {
  const notificationTitle = 'Background Message Title';
  const notificationOptions = {
    body: payload.body,
    icon: 'static/login/images/favicon.ico',
    title: payload.title
  };

  return self.registration.showNotification(notificationTitle,
      notificationOptions);
});
