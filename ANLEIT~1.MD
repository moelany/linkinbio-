# WNTI Link-in-Bio – Anleitung

Eine eigene Link-in-Bio-Seite ohne Wasserzeichen und ohne laufende Kosten.
Die neusten Artikel von wnti.ch erscheinen automatisch (alle 2 Stunden aktualisiert).

## So funktioniert es

1. Die Seite (`index.html`) zeigt Branding, Buttons und die neusten Artikel.
2. Eine GitHub Action (`.github/workflows/update-feed.yml`) holt alle 2 Stunden
   den RSS-Feed von `https://wnti.ch/api/rss-feed`, inkl. Artikelbild, und
   schreibt die neusten 4 Artikel in `posts.json`.
3. Die Seite liest `posts.json` – kein manueller Aufwand mehr.

Du postest also einfach wie gewohnt: Artikel auf wnti.ch publizieren,
Instagram-Post machen – die Bio-Seite aktualisiert sich von selbst.

## Einrichtung (einmalig, ca. 15 Minuten)

### 1. GitHub-Account und Repository

1. Auf [github.com](https://github.com) einloggen oder gratis registrieren.
2. Oben rechts **+** → **New repository**.
3. Name z.B. `wnti-links`, Sichtbarkeit **Public**, dann **Create repository**.

### 2. Dateien hochladen

1. Im neuen Repository: **uploading an existing file** anklicken
   (oder **Add file → Upload files**).
2. Den gesamten Inhalt dieses Ordners hineinziehen – wichtig: auch der
   versteckte Ordner `.github` muss mit. Falls der Upload per Drag & Drop den
   `.github`-Ordner nicht mitnimmt: die Datei `update-feed.yml` einzeln über
   **Add file → Create new file** anlegen und als Dateinamen
   `.github/workflows/update-feed.yml` eintippen (GitHub legt die Ordner
   automatisch an), dann den Inhalt hineinkopieren.
3. **Commit changes**.

### 3. GitHub Pages aktivieren

1. Im Repository: **Settings → Pages**.
2. Bei "Source": **Deploy from a branch**, Branch **main**, Ordner **/ (root)**.
3. **Save**. Nach 1–2 Minuten ist die Seite erreichbar unter:
   `https://DEIN-BENUTZERNAME.github.io/wnti-links/`

### 4. Action-Berechtigung setzen (wichtig!)

1. **Settings → Actions → General**.
2. Ganz unten bei "Workflow permissions": **Read and write permissions** wählen, **Save**.

### 5. Ersten Lauf starten

1. Tab **Actions** → Workflow "Artikel-Feed aktualisieren" → **Run workflow**.
2. Nach ca. 1 Minute ist `posts.json` mit den echten Artikeln gefüllt.

### 6. Link in die Instagram-Bio

Instagram-Profil → **Profil bearbeiten** → **Links** →
`https://DEIN-BENUTZERNAME.github.io/wnti-links/` eintragen. Fertig!

## Anpassungen

- **Buttons ändern/hinzufügen:** in `index.html` den Block `<nav class="links">` bearbeiten.
- **Anzahl Artikel:** in `scripts/update_feed.py` den Wert `MAX_POSTS` ändern
  (und in `index.html` das `.slice(0, 4)`).
- **Farben:** oben in `index.html` unter `:root` (z.B. `--bg` für den Hintergrund).
- **Teamfoto:** `assets/team.jpg` ersetzen (gleicher Dateiname).
- **Eigene Domain** (z.B. links.wnti.ch): Settings → Pages → Custom domain,
  plus ein CNAME-Eintrag bei eurem Domain-Anbieter. Kostenlos, optional.

## Gut zu wissen

- GitHub pausiert geplante Actions nach ca. 60 Tagen ohne manuelle Aktivität
  im Repository. Ihr bekommt dann eine E-Mail und könnt den Workflow mit einem
  Klick wieder aktivieren. Jede kleine Änderung am Repository setzt den Zähler zurück.
- Ändert sich die Feed-Adresse von wnti.ch, in `scripts/update_feed.py`
  die Zeile `FEED_URL` anpassen.
