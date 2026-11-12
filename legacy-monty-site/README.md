
# Monty Site (Static)

A fast, static website for Monty — psychotherapist, educator, mental fitness coach.

## Structure
- `index.html` — Home
- `about.html` — About
- `blog/` — Blog index and posts
- `contact.html` — Contact form (Formspree placeholder)
- `thank-you.html` — Thank-you page
- `assets/` — CSS, JS, images

## Replace Profile Photo
Put your photo at `assets/img/profile.jpg` and update `<img src="assets/img/profile.jpg">` where needed
(or replace the existing `profile.svg` filename in the HTML with `profile.jpg`).

## Contact Form
- Create a free Formspree form and replace the `action` in `contact.html` (e.g., `https://formspree.io/f/xxxx`).
- Update the `_redirect` hidden input to your deployed domain `https://your-domain/thank-you.html`.

## Local Preview
Open `index.html` in your browser, or run a tiny server:
```bash
python3 -m http.server 8080
```

## Deploy (Vercel)
1. Add this project to a GitHub repo.
2. On Vercel, "New Project" → import the repo.
3. Framework preset: **Other** (static).
4. Build command: **None**. Output directory: **/**.
5. Ensure `index.html` is root. Vercel will serve it as static.

## Deploy (GitHub Pages)
- Create repo, push, then enable Pages in **Settings → Pages** with root `/`.
