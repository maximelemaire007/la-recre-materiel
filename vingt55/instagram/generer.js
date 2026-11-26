#!/usr/bin/env node
// Génère une publication Instagram Vingt55 (PNG 1080 x 1350) à partir d'une photo d'article.
//
// Utilisation :
//   node generer.js --photo PHOTO --titre "TITRE" --etiquette "ÉTIQUETTE" \
//                   [--theme creme|marine] [--position "50% 40%"] [--sortie fichier.png]
//
//   --titre      Titre affiché. Entourer le mot-clé de <em>...</em> pour le mettre en rouge.
//   --etiquette  Catégorie · Ville, ex. "Culture · Drummondville".
//   --theme      creme (nouvelles légères : culture, fierté, commerces) ou marine (actualité). Défaut : creme.
//   --position   Cadrage de la photo (CSS background-position), ex. "100% 50%" pour garder la droite.
//   --sortie     Fichier PNG à créer. Défaut : publication.png dans le dossier courant.
//
// Préparation automatique de la photo :
//   - retire une bande rouge unie en bas (ajoutée par les visuels Facebook) ;
//   - si la photo est petite (< 1600 px de large), l'agrandit et la rend plus nette ;
//   - sinon, ajoute seulement une légère netteté.
// Nécessite : Node + Playwright (Chromium) et ImageMagick (convert/identify).

const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

function args() {
  const a = process.argv.slice(2), o = { theme: 'creme', sortie: 'publication.png' };
  for (let i = 0; i < a.length; i += 2) {
    const k = a[i].replace(/^--/, ''), v = a[i + 1];
    if (v === undefined) throw new Error(`Valeur manquante pour ${a[i]}`);
    o[k] = v;
  }
  for (const k of ['photo', 'titre', 'etiquette']) if (!o[k]) throw new Error(`--${k} est obligatoire`);
  if (!['creme', 'marine'].includes(o.theme)) throw new Error('--theme doit être creme ou marine');
  return o;
}

function im(...a) { return execFileSync(a[0], a.slice(1), { encoding: 'utf8' }).trim(); }

// Hauteur utile de la photo : retire une bande rouge unie en bas, s'il y en a une.
function hauteurSansBande(photo) {
  const [w, h] = im('identify', '-format', '%w %h', photo + '[0]').split(' ').map(Number);
  const col = im('convert', photo + '[0]', '-crop', `1x${h}+${Math.floor(w / 2)}+0`, '+repage', '-depth', '8', 'txt:-');
  const px = col.split('\n').slice(1).map(l => {
    const m = l.match(/\((\d+),(\d+),(\d+)/); return m ? m.slice(1).map(Number) : null;
  }).filter(Boolean);
  let y = px.length;
  while (y > 0) { const [r, g, b] = px[y - 1]; if (r > 190 && g < 70 && b < 70) y--; else break; }
  const bande = px.length - y;
  return { w, h, utile: bande > 20 ? y - 4 : h, bande: bande > 20 ? bande : 0 };
}

function preparerPhoto(src, dest) {
  const { w, utile, bande } = hauteurSansBande(src);
  const a = ['convert', src + '[0]', '-crop', `${w}x${utile}+0+0`, '+repage'];
  if (w < 1600) a.push('-filter', 'Lanczos', '-resize', w < 1100 ? '200%' : '160%', '-enhance',
                       '-unsharp', '0x1.6+1.1+0.02', '-sigmoidal-contrast', '2.2x50%', '-modulate', '101,106,100');
  else a.push('-unsharp', '0x1+0.6+0.02', '-modulate', '100,104,100');
  a.push('-quality', '95', dest);
  im(...a);
  return { largeur: w, bandeRetiree: bande, ameliore: w < 1600 };
}

(async () => {
  const o = args();
  const ici = __dirname;
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'vingt55-'));
  const photo = path.join(tmp, 'photo.jpg');
  const info = preparerPhoto(path.resolve(o.photo), photo);

  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 2, viewport: { width: 1140, height: 1400 } });
  await p.addInitScript(post => { window.POST = post; }, {
    photo: 'file://' + photo, theme: o.theme, position: o.position,
    tag: o.etiquette, title: o.titre,
  });
  await p.goto('file://' + path.join(ici, 'gabarit.html'));
  await p.evaluate(() => window.READY);
  await p.waitForTimeout(300);
  const brut = path.join(tmp, 'rendu-2x.png');
  await (await p.$('#post')).screenshot({ path: brut });
  await b.close();

  // Rendu en double résolution, puis réduction soignée à la taille exacte d'Instagram.
  const sortie = path.resolve(o.sortie);
  im('convert', brut, '-filter', 'Lanczos', '-resize', '1080x1350', '-unsharp', '0x0.6+0.5+0.01', sortie);
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(`Publication créée : ${sortie}`);
  console.log(`Photo : ${info.largeur}px de large` +
    (info.bandeRetiree ? `, bande rouge de ${info.bandeRetiree}px retirée` : '') +
    (info.ameliore ? ', agrandie et rendue plus nette' : ', légère netteté'));
})().catch(e => { console.error('Erreur :', e.message); process.exit(1); });
