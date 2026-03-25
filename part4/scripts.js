/* global localStorage, alert */

// ============ UTILS ============

function getCookie (name) {
  const cookies = document.cookie.split('; ');
  for (const cookie of cookies) {
    if (cookie.startsWith(name + '=')) {
      return cookie.split('=')[1];
    }
  }
}

// ============ THEME ============

const storageKey = 'theme-preference';

const getColorPreference = () => {
  if (localStorage.getItem(storageKey)) { return localStorage.getItem(storageKey); } else {
    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }
};

const theme = {
  value: getColorPreference()
};

const setPreference = () => {
  localStorage.setItem(storageKey, theme.value);
  reflectPreference();
};

const reflectPreference = () => {
  document.firstElementChild
    .setAttribute('data-theme', theme.value);

  document
    .querySelector('#theme-toggle')
    ?.setAttribute('aria-label', theme.value);

  const logo = document.querySelector('.logo');
  if (logo) {
    logo.src = theme.value === 'dark' ? 'assets/logo2.png' : 'assets/logo.png';
  }
};

reflectPreference();

window.onload = () => {
  reflectPreference();

  document
    .querySelector('#theme-toggle')
    .addEventListener('click', onClick);
};

const onClick = () => {
  theme.value = theme.value === 'light'
    ? 'dark'
    : 'light';

  setPreference();
};

// ============ AUTH ============

async function loginUser (email, password) {
  const response = await fetch('http://localhost:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email,
      password
    })
  });
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

function logoutUser () {
  document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT';
  window.location.href = 'index.html';
}

function checkAuthentication () {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const addReview = document.getElementById('add-review');

  if (!token) {
    loginLink.href = 'login.html';
    loginLink.className = 'login-button-icon';
    loginLink.innerHTML = '<img src="assets/icons/icon-login.png" alt="Login" width="20" height="20">';

    if (addReview) {
      const textarea = addReview.querySelector('textarea');
      const submitBtn = addReview.querySelector('button[type="submit"]');

      if (textarea) textarea.style.display = 'none';
      if (submitBtn) submitBtn.style.display = 'none';

      if (!addReview.querySelector('.login-message')) {
        const message = document.createElement('p');
        message.className = 'login-message';
        message.innerHTML = 'Please <a href="login.html">login</a> to add a review.';
        addReview.prepend(message);
      }
    }
  } else {
    loginLink.href = '#';
    loginLink.className = 'login-button';
    loginLink.textContent = 'Logout';
    loginLink.onclick = logoutUser;

    if (addReview) {
      const textarea = addReview.querySelector('textarea');
      const submitBtn = addReview.querySelector('button[type="submit"]');

      if (textarea) textarea.style.display = 'block';
      if (submitBtn) submitBtn.style.display = 'block';

      const message = addReview.querySelector('.login-message');
      if (message) message.remove();
    }
  }
  const placesList = document.getElementById('places-list');
  if (placesList) {
    fetchPlaces(token);
  }

  return token;
}

// ============ PLACES ============

async function fetchPlaces (token) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch('http://localhost:5000/api/v1/places/', {
    method: 'GET',
    headers
  });
  if (response.ok) {
    const data = await response.json();
    displayPlaces(data);
  }
}

function displayPlaces (places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';
  for (const place of places) {
    console.log(place);
    const placeCard = document.createElement('div');
    placeCard.dataset.price = place.price;
    placeCard.className = 'place-card';
    placeCard.innerHTML = `
    <div>
      <h4>${place.title}</h4>
      <p>Price per night: $${place.price}</p>
    </div>
    <a href="place.html?id=${place.id}" class="details-button">View Details</a>`;
    placesList.appendChild(placeCard);
  }
}

function getPlaceIdFromURL () {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');
  return id;
}

async function fetchPlaceDetails (token, placeId) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
    method: 'GET',
    headers
  });
  if (response.ok) {
    const data = await response.json();
    displayPlaceDetails(data);
  }
}

function displayPlaceDetails (place) {
  const placeDetails = document.getElementById('place-details');
  placeDetails.innerHTML = '';

  const placeTitle = document.createElement('div');
  placeTitle.className = 'place-title';
  placeTitle.innerHTML = `
  <h1>${place.title}</h1>`;
  placeDetails.appendChild(placeTitle);

  const placeDetail = document.createElement('div');
  placeDetail.dataset.price = place.price;
  placeDetail.className = 'place-details';
  placeDetail.innerHTML = `
    <p><b>Host:</b> ${place.owner.first_name} ${place.owner.last_name}</p>
    <p><b>Price per night:</b> $${place.price}</p>
    <p><b>Description:</b> ${place.description}</p>
    `;
  placeDetails.appendChild(placeDetail);

  const amenities = document.createElement('div');
  amenities.className = 'amenities';
  amenities.innerHTML = `
    <h2>Amenities</h2>
    ${place.amenities.map(a => `<div class="amenity-item"><span class="amenity-icon" style="mask-image: url('./assets/icons/${a.name.toLowerCase().replace(/ /g, '-')}.svg')"></span> ${a.name}</div>`).join(' ')}
    `;
  placeDetails.appendChild(amenities);

  const reviewsSection = document.getElementById('reviews');
  const average = place.reviews.length > 0
    ? place.reviews.reduce((sum, r) => sum + r.rating, 0) / place.reviews.length
    : 0;
  reviewsSection.innerHTML = `<h2>Reviews ⭐ ${average.toFixed(1)}</h2>`;
  for (const review of place.reviews) {
    const reviewCard = document.createElement('div');
    reviewCard.className = 'review-card';
    reviewCard.innerHTML = `
        <p><b>${review.author_first_name} ${review.author_last_name}</b></p>
        <p>${review.text}</p>
        <p>Rating: ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
      `;
    reviewsSection.appendChild(reviewCard);
  }
}

async function submitReview (token, placeId, reviewText, reviewRating) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  const payload = JSON.parse(atob(token.split('.')[1]));
  const userId = payload.sub;

  const response = await fetch('http://localhost:5000/api/v1/reviews/', {
    method: 'POST',
    headers,
    body: JSON.stringify({
      text: reviewText,
      rating: parseInt(reviewRating),
      user_id: userId,
      place_id: placeId
    })
  });
  if (response.ok) {
    alert('Review submitted successfully!');
    // Clear the form
  } else {
    alert('Failed to submit review');
  }
}

// ============ INIT ============

document.addEventListener('DOMContentLoaded', () => {
  const token = checkAuthentication();
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await loginUser(email, password);
    });
  }
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
      const selectedPrice = event.target.value;
      const cards = document.querySelectorAll('.place-card');
      for (const card of cards) {
        const price = parseFloat(card.dataset.price);
        if (selectedPrice === 'All') {
          card.style.display = 'flex';
        } else {
          card.style.display = price <= parseFloat(selectedPrice) ? 'flex' : 'none';
        }
      }
    });
  }
  const placeDetails = document.getElementById('place-details');
  if (placeDetails) {
    const placeId = getPlaceIdFromURL();
    fetchPlaceDetails(token, placeId);
  }

  const reviewForm = document.getElementById('review-form');
  const placeId = getPlaceIdFromURL();

  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewText = document.getElementById('review-text').value;
      const reviewRating = document.getElementById('rating').value;
      await submitReview(token, placeId, reviewText, reviewRating);
    });
  }
});