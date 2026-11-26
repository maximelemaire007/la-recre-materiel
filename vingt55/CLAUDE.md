# Vingt55 — consignes pour Claude

Ce dossier contient l'identité visuelle de la Communauté Vingt55 (média d'information locale,
Drummondville, Centre-du-Québec) et le système de publications Instagram.
La personne qui gère le compte Instagram @communautevingt55 communique en français : répondre en français.

## Identité (ne pas modifier sans demande explicite)

- Couleurs uniquement : marine `#131A2E`, rouge `#E5303A`, crème `#F7F5F1`.
  Pas de blanc pur ni de noir dans les designs (le blanc est permis seulement comme fond de page d'un document).
- Police : Outfit (copie locale dans `instagram/fonts/`).
- Logo : « vingt » minuscule + « 55 » rouge décalé ; point du « i » rouge avec deux ondes « en direct »,
  centré sur la tige du « i ».
  - Signature « COMMUNAUTÉ » sous « vingt » (gras 800) : logo principal, bannières, photos de profil.
  - Signature « MÉDIA » au-dessus du 55, alignée à gauche du 55 (gras 800) : remplace l'ancien « Journal web ».
    Ne jamais remplacer « Communauté » par « Média » ailleurs.
- Fichiers finaux (PDF/SVG vectoriels, PNG) dans `identite/`.

## Publication Instagram à partir d'un article

La personne envoie une photo d'article et un lien (souvent `https://shrlnk.ca/s/...`).

1. **Titre de l'article** : `curl -sS URL` sur le lien court ; le titre est dans la page de redirection
   (« … – Vingt55 Redirecting… »). Le site vingt55.ca a une protection anti-robot : ne pas la contourner.
   Si le texte de l'article est nécessaire, le demander (capture d'écran ou copier-coller).
2. **Sujet** : pas d'accidents de la route, de faits divers ou de sujets pouvant choquer le public.
   Si l'article est de ce type, le signaler au lieu de produire la publication.
3. **Générer l'image** (depuis `vingt55/instagram/`) :
   ```
   node generer.js --photo PHOTO --titre "TITRE avec <em>mot-clé</em>" \
     --etiquette "Catégorie · Ville" --theme creme|marine [--position "X% Y%"] --sortie FICHIER.png
   ```
   - Thème `creme` : nouvelles positives (culture, commerce, fierté, événements). `marine` : actualité plus sérieuse.
   - Titre : court, accrocheur, fidèle à l'article ; un ou deux mots-clés en rouge avec `<em>`.
   - `--position` si un élément important (enseigne, visage) est coupé par le cadrage.
   - Le script retire la bande rouge des visuels Facebook et améliore automatiquement les petites photos.
   - Toujours regarder le résultat avant de l'envoyer.
4. **Description** : même structure que `instagram/exemples/descriptions.md` :
   émoji + accroche, 2 phrases de contexte, une question ou une invitation, « 📲 … lien dans la bio »,
   puis 6-8 mots-clics dont #Vingt55 #Drummondville #CentreDuQuébec.
5. **Faits** : ne rien inventer (noms, prix, chiffres, dates). Utiliser seulement le titre de l'article,
   le texte fourni ou ce qui est lisible dans la photo, et signaler ce qui doit être vérifié.
6. Envoyer l'image (et une variante crème/marine si utile) avec la description prête à copier.
