/* global localStorage, alert */

// ============ UTILS ============

function getCookie (name) {
  const cookies = document.cookie.split('; ');
  for (const cookie of cookies) {
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
}

function buildLoginHref () {
  const currentPath = `${window.location.pathname}${window.location.search}${window.location.hash}`;
  const nextPath = currentPath.includes('login.html') ? 'index.html' : currentPath;
  return `login.html?next=${encodeURIComponent(nextPath)}`;
}

function getSafePostLoginPath () {
  const params = new URLSearchParams(window.location.search);
  const next = params.get('next');

  if (!next) return 'index.html';
  if (next.startsWith('http://') || next.startsWith('https://') || next.startsWith('//')) {
    return 'index.html';
  }
  if (next.includes('login.html')) return 'index.html';

  return next;
}

// ============ THEME ============

const storageKey = 'theme-preference';

const getColorPreference = () => {
  if (localStorage.getItem(storageKey)) {
    return localStorage.getItem(storageKey);
  } else {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
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
  document.firstElementChild.setAttribute('data-theme', theme.value);

  document.querySelector('#theme-toggle')?.setAttribute('aria-label', theme.value);

  const logo = document.querySelector('.logo');
  if (logo) {
    logo.src = theme.value === 'dark' ? 'assets/logo2.png' : 'assets/logo.png';
  }

  const footerHolbertonLogo = document.querySelector('.footer-holberton-logo');
  if (footerHolbertonLogo) {
    footerHolbertonLogo.src = theme.value === 'dark'
      ? 'assets/footer_holberton2.svg'
      : 'assets/footer_holberton1.svg';
  }

  const footerGithubLogo = document.querySelector('.footer-github-logo');
  if (footerGithubLogo) {
    footerGithubLogo.src = theme.value === 'dark'
      ? 'assets/footer_github2.svg'
      : 'assets/footer_github1.svg';
  }

  const footerLinkedinLogo = document.querySelector('.footer-linkedin-logo');
  if (footerLinkedinLogo) {
    footerLinkedinLogo.src = theme.value === 'dark'
      ? 'assets/footer_linkedin2.svg'
      : 'assets/footer_linkedin1.svg';
  }
};

// Appel unique ici pour éviter le flash de thème au chargement
reflectPreference();

const onClick = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light';
  setPreference();
};

// ============ AUTH ============

async function loginUser (email, password) {
  const response = await fetch('http://localhost:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = getSafePostLoginPath();
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
    const loginHref = buildLoginHref();

    loginLink.href = loginHref;
    loginLink.className = 'login-button-icon';
    loginLink.innerHTML = '<img src="assets/icons/icon-login.png" alt="Login" width="20" height="20">';

    if (addReview) {
      addReview.classList.add('auth-locked');

      const reviewTitle = addReview.querySelector('h2');
      const reviewForm = addReview.querySelector('#review-form');

      if (reviewTitle) reviewTitle.hidden = true;
      if (reviewForm) reviewForm.hidden = true;

      if (!addReview.querySelector('.login-message')) {
        const message = document.createElement('p');
        message.className = 'login-message';
        message.innerHTML = `Please <a href="${loginHref}">login</a> to add a review.`;
        addReview.prepend(message);
      }
    }
  } else {
    loginLink.href = '#';
    loginLink.className = 'login-button';
    loginLink.textContent = 'Logout';
    loginLink.onclick = logoutUser;

    if (addReview) {
      addReview.classList.remove('auth-locked');

      const reviewTitle = addReview.querySelector('h2');
      const reviewForm = addReview.querySelector('#review-form');

      if (reviewTitle) reviewTitle.hidden = false;
      if (reviewForm) reviewForm.hidden = false;

      const message = addReview.querySelector('.login-message');
      if (message) message.remove();
    }
  }

  const placesList = document.getElementById('places-list');
  if (placesList) {
    fetchPlaces(token || null);
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
    const placeCard = document.createElement('div');
    placeCard.dataset.price = place.price;
    placeCard.className = 'place-card';
    placeCard.innerHTML = `
    <div>
      <h4>${place.title}</h4>
      <p>Price per night: $${place.price}</p>
    </div>
    <a href="place.html?id=${place.id}" class="details-button" target="_blank">View Details</a>`;
    placesList.appendChild(placeCard);
  }
}

function getPlaceIdFromURL () {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
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

  const renderStar = (filled, className) => `
    <span class="star-button ${filled ? 'is-filled' : ''} ${className}" aria-hidden="true">
      <svg class="star-icon" viewBox="0 0 24 24" focusable="false">
        <path d="M12 2.7 14.9 8.6 21.4 9.5 16.7 14.1 17.8 20.7 12 17.6 6.2 20.7 7.3 14.1 2.6 9.5 9.1 8.6 12 2.7Z" />
      </svg>
    </span>`;

  const placeTitle = document.createElement('div');
  placeTitle.className = 'place-title';
  placeTitle.innerHTML = `<h1>${place.title}</h1>`;
  placeDetails.appendChild(placeTitle);

  const placeDetail = document.createElement('div');
  placeDetail.dataset.price = place.price;
  placeDetail.className = 'place-details place-info';
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
  reviewsSection.innerHTML = `
    <h2 class="reviews-heading">
      Reviews
      <span class="star-button is-filled review-title-star" aria-hidden="true">
        <svg class="star-icon" viewBox="0 0 24 24" focusable="false">
          <path d="M12 2.7 14.9 8.6 21.4 9.5 16.7 14.1 17.8 20.7 12 17.6 6.2 20.7 7.3 14.1 2.6 9.5 9.1 8.6 12 2.7Z" />
        </svg>
      </span>
      <span class="average-rating">${average.toFixed(1)}</span>
    </h2>
  `;
  for (const review of place.reviews) {
    const reviewCard = document.createElement('div');
    reviewCard.className = 'review-card';
    reviewCard.innerHTML = `
        <p><b>${review.author_first_name} ${review.author_last_name}</b></p>
        <p>${review.text}</p>
        <p class="review-rating">
          Rating:
          <span class="review-stars" aria-label="${review.rating} out of 5 stars">
            ${Array.from({ length: 5 }, (_, index) => renderStar(index < review.rating, 'review-star')).join('')}
          </span>
        </p>
      `;
    reviewsSection.appendChild(reviewCard);
  }
}

async function submitReview (token, placeId, reviewText, reviewRating) {
  if (!token) {
    alert('You must be logged in to submit a review.');
    return;
  }

  let userId;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    userId = payload.sub;
  } catch (e) {
    alert('Invalid session. Please log in again.');
    return;
  }

  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`
  };

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
    document.getElementById('review-text').value = '';
    resetStarRating();
    await fetchPlaceDetails(token, placeId);
  } else {
    const err = await response.json().catch(() => ({}));
    alert('Failed to submit review: ' + (err.error || response.statusText));
  }
}

// ============ STAR RATING ============

function initStarRating () {
  const ratingSelect = document.getElementById('rating');
  if (!ratingSelect || ratingSelect.dataset.enhanced === 'true') return;

  ratingSelect.dataset.enhanced = 'true';
  ratingSelect.classList.add('rating-select-hidden');

  const starRating = document.createElement('div');
  starRating.className = 'star-rating';
  starRating.setAttribute('role', 'radiogroup');
  starRating.setAttribute('aria-label', 'Rating');

  const stars = [];

  const paintStars = (activeValue) => {
    for (const star of stars) {
      const value = Number(star.dataset.value);
      star.classList.toggle('is-filled', value <= activeValue);
      star.setAttribute('aria-checked', String(value === activeValue));
    }
  };

  const setRating = (value) => {
    ratingSelect.value = String(value);
    paintStars(value);
  };

  for (let i = 1; i <= 5; i++) {
    const star = document.createElement('button');
    star.type = 'button';
    star.className = 'star-button';
    star.dataset.value = String(i);
    star.setAttribute('role', 'radio');
    star.setAttribute('aria-label', `${i} star${i > 1 ? 's' : ''}`);
    star.innerHTML = '<svg class="star-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2.7 14.9 8.6 21.4 9.5 16.7 14.1 17.8 20.7 12 17.6 6.2 20.7 7.3 14.1 2.6 9.5 9.1 8.6 12 2.7Z" /></svg>';

    star.addEventListener('mouseenter', () => paintStars(i));
    star.addEventListener('focus', () => paintStars(i));
    star.addEventListener('click', () => setRating(i));

    stars.push(star);
    starRating.appendChild(star);
  }

  starRating.addEventListener('mouseleave', () => {
    paintStars(Number(ratingSelect.value || 1));
  });

  starRating.addEventListener('keydown', (event) => {
    const current = Number(ratingSelect.value || 1);
    if (event.key === 'ArrowRight' || event.key === 'ArrowUp') {
      event.preventDefault();
      setRating(Math.min(5, current + 1));
      stars[Math.min(4, current)].focus();
    }
    if (event.key === 'ArrowLeft' || event.key === 'ArrowDown') {
      event.preventDefault();
      setRating(Math.max(1, current - 1));
      stars[Math.max(0, current - 2)].focus();
    }
  });

  ratingSelect.insertAdjacentElement('afterend', starRating);
  setRating(Number(ratingSelect.value || 1));
}

function resetStarRating () {
  const ratingSelect = document.getElementById('rating');
  if (!ratingSelect) return;

  ratingSelect.value = '1';

  const stars = document.querySelectorAll('.star-rating .star-button');
  stars.forEach(star => {
    const value = Number(star.dataset.value);
    star.classList.toggle('is-filled', value <= 1);
    star.setAttribute('aria-checked', String(value === 1));
  });
}

// ============ INIT ============

document.addEventListener('DOMContentLoaded', () => {
  // Attacher le theme toggle ici, plus besoin de window.onload
  document.querySelector('#theme-toggle')?.addEventListener('click', onClick);

  const token = checkAuthentication();

  // Un seul appel, disponible pour fetchPlaceDetails ET submitReview
  const placeId = getPlaceIdFromURL();

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
    fetchPlaceDetails(token, placeId);
  }

  initStarRating();

  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewTextField = document.getElementById('review-text');
      if (!reviewTextField) return;

      const reviewText = reviewTextField.value;
      const reviewRating = document.getElementById('rating').value;
      await submitReview(token, placeId, reviewText, reviewRating);
    });
  }
});