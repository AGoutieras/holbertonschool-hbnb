# HBnB Part 4 - Simple Web Client

HBnB Part 4 is the front-end of the HBnB project. It provides a simple web client built with HTML5, CSS3 and JavaScript ES6, and it connects to the Flask API contained in the nested `hbnb/` directory.

The application lets a user:

- log in with email and password
- store the JWT token in a cookie
- browse the list of places
- filter places by maximum price
- open a detailed view for each place
- read the reviews for a place
- add a review when authenticated
- switch between light and dark themes

## Project Structure

```text
part4/
├── index.html         # Main page with the list of places
├── login.html         # Login page
├── place.html         # Place details page
├── styles.css         # Shared styling for the whole client
├── scripts.js         # Client-side logic, auth and API calls
├── assets/            # Logos, icons and other static files
└── hbnb/              # Flask API used by the client
```

## Main Features

### Login

The login form sends a POST request to the API login endpoint. When the request succeeds, the returned JWT token is saved in a cookie and the user is redirected to the last requested page or to `index.html`.

### Places list

The home page fetches all places from the API and renders them as cards. Each card shows the place name, the price per night and a button to open the place details page.

### Price filter

The list page includes a client-side filter with the following values:

- All
- 10
- 50
- 100

The page hides or shows place cards without reloading.

### Place details

The details page loads a single place by ID from the URL query string. It shows:

- the place title
- the host name
- the price per night
- the description
- the amenities
- the reviews, when available

### Add review

Authenticated users can submit a review directly from the place details page. The form sends the review text and rating to the API before displaying a success or error message.

### Theme toggle

The client also includes a light/dark theme switch that persists the selected theme in localStorage.

## API Endpoints Used

The client expects a backend available at `http://localhost:5000/api/v1` by default.

- `POST /auth/login`
- `GET /places/`
- `GET /places/<place_id>`
- `POST /reviews/`
- `GET /amenities/`

If your backend runs on another host or port, update the base URL used in `scripts.js`.

## Setup

### 1. Start the backend API

From the `part4/hbnb/` directory:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

The API should be available at `http://localhost:5000`.

### 2. Start the front-end

Serve the `part4/` directory with a local web server. For example:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/index.html
```

You can also use VS Code Live Server or Five Server if you prefer.

## Usage Flow

1. Open `login.html` and authenticate.
2. Go to `index.html` to browse the places.
3. Click `View Details` to open `place.html?id=<place_id>`.
4. If you are logged in, submit a review directly from the form displayed on the place details page.

## Notes

- The client uses cookies to store the JWT token.
- The pages rely on fetch requests, so the API must allow CORS from the client origin.
- The seed script can help populate test data before testing the interface.

## Technologies

- HTML5
- CSS3
- JavaScript ES6
- Fetch API
- Flask backend
- JWT authentication

## Author

Project developed as part of the Holberton School HBnB curriculum by [Anthony Goutieras](https://github.com/AGoutieras)
