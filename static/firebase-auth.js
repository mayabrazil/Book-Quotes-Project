import { initializeApp } from "https://www.gstatic.com/firebasejs/12.1.0/firebase-app.js";

import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/12.1.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyDwbnwK1fndBoWASC28xxbeQc-C9Z3vLgA",
  authDomain: "bookquotes-app.firebaseapp.com",
  projectId: "bookquotes-app",
  storageBucket: "bookquotes-app.firebasestorage.app",
  messagingSenderId: "836802010083",
  appId: "1:836802010083:web:6196e040fac55f56e51ed6"
};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);

const provider = new GoogleAuthProvider();


// LOGIN
window.login = async () => {

  try {

    const result = await signInWithPopup(auth, provider);

    const token = await result.user.getIdToken();

    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        token: token
      })
    });

    const data = await response.json();

    console.log(data);
    alert(JSON.stringify(data));

    if (data.success) {

      document.getElementById('login-status')
        .textContent = `Logged in as ${result.user.email}`;

      alert('Successfully logged in!');

    } else {

      alert('Login failed.');

    }

  } catch (err) {

    console.error(err);
    alert(err.message);

    alert(err.message);
  }
};


// LOGOUT
window.logoutUser = async () => {

  try {

    await signOut(auth);

    await fetch('/logout', {
      method: 'POST'
    });

    document.getElementById('login-status')
      .textContent = 'Not logged in';

    alert('Logged out');

  } catch (err) {

    console.error(err);

  }
};


// KEEP LOGIN STATE
onAuthStateChanged(auth, (user) => {

  const status = document.getElementById('login-status');

  if (!status) return;

  if (user) {

    status.textContent =
      `Logged in as ${user.email}`;

  } else {

    status.textContent =
      'Not logged in';
  }
});