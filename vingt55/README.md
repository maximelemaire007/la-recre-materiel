# Vingt55 — identité visuelle et publications Instagram

## Contenu

- `identite/` : logos, bannières Facebook, photos de profil et affiche « Avant / Après »,
  en PDF et SVG vectoriels et en PNG. Voir `identite/LISEZMOI.txt` pour les couleurs et la police.
  `identite/sources/` contient les fichiers qui ont servi à les produire.
- `instagram/` : le gabarit des publications Instagram (format 1080 × 1350).
  - `gabarit.html` : la mise en page (photo, étiquette rouge, titre, logo).
  - `generer.js` : crée une publication en une commande.
  - `fonts/`, `logos/` : police Outfit et logos, enregistrés localement.
  - `exemples/` : trois publications d'exemple et leurs descriptions.
- `CLAUDE.md` : la marche à suivre que Claude applique pour chaque nouvelle publication.

## Créer une publication

Envoyer à Claude la photo de l'article et son lien. Claude prépare l'image et la description.

Pour la générer soi-même (Node, Playwright et ImageMagick requis) :

```
cd vingt55/instagram
node generer.js --photo photo.jpg \
  --titre "Près de <em>800 visiteurs</em> pour l'ouverture de la Librairie Temps Libre" \
  --etiquette "Commerce local · Drummondville" \
  --theme creme --sortie publication.png
```

| Option | Rôle |
|---|---|
| `--photo` | Photo de l'article (JPG, PNG ou WEBP) |
| `--titre` | Titre affiché ; le texte entre `<em>` et `</em>` s'affiche en rouge |
| `--etiquette` | Catégorie · Ville, en haut du titre |
| `--theme` | `creme` (nouvelles légères) ou `marine` (actualité) ; `creme` par défaut |
| `--position` | Cadrage de la photo, ex. `"100% 50%"` pour garder la partie droite |
| `--sortie` | Nom du fichier PNG à créer |

La taille du titre s'ajuste toute seule et les lignes sont équilibrées.
