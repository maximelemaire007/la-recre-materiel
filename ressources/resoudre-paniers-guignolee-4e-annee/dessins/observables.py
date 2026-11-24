"""Grille « Éléments observables » (modèle de la créatrice) pour Les paniers de la guignolée.
Usage : python3 observables.py  -> observables-1.png, observables-2.png (format d'une page Lettre)
"""
from PIL import ImageFont
import cairosvg

INK = '#1E1E1E'
FR = '/root/.fonts/KGPerfectPenmanship.ttf'  # police de la créatrice (non versionnée, licence)
FB = FR
W = 720                 # largeur du tableau (px Canva)
C0 = 190                # colonne des critères
PAD = 14
FS = 14.5               # taille du texte
LH = 21                 # interligne
fr = ImageFont.truetype(FR, 100); fb = ImageFont.truetype(FB, 100)


def largeur(t, bold=False):
    f = fb if bold else fr
    return f.getlength(t) * FS / 100


def couper(t, maxw, bold=False):
    mots, out, cur = t.split(' '), [], ''
    for m in mots:
        essai = (cur + ' ' + m).strip()
        if largeur(essai, bold) > maxw and cur:
            out.append(cur); cur = m
        else:
            cur = essai
    out.append(cur)
    return out


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;')


# Contenu : (critère, [lignes]) ; une ligne = (type, texte)
#   'it' italique, 'b' gras, 'sec' sous-titre avec flèche, 'cb' case à cocher, 'sp' espace
COMP = ('Compréhension de la situation-problème', [
    ('it', 'L’élève comprend qu’elle, qu’il…'), ('sp', ''),
    ('b', 'doit déterminer le nombre de paniers à préparer en tenant compte :'),
    ('cb', 'du nombre de denrées amassées par chaque classe (diagramme à bandes)'),
    ('cb', 'du quart des denrées qui sont périmées et qu’il faut retirer'),
    ('cb', 'des 8 denrées par panier'),
    ('cb', 'des paniers complets seulement'), ('sp', ''),
    ('b', 'doit déterminer le coût de la préparation des paniers en tenant compte :'),
    ('sec', 'Les boîtes'),
    ('cb', 'd’une boîte par panier'),
    ('cb', 'des prix des trois fournisseurs (à l’unité, paquets de 5, paquets de 10)'),
    ('sec', 'Le ruban'),
    ('cb', 'de la taille de la boîte (30 cm × 20 cm)'),
    ('cb', 'des 50 cm de plus pour la boucle et d’un ruban d’un seul morceau'),
    ('cb', 'des rouleaux de 5 m à 3 $'),
    ('sec', 'Les étiquettes'),
    ('cb', 'des contraintes : un quadrilatère, 4 côtés de même longueur, aucun angle droit'),
    ('cb', 'd’une étiquette par panier et des paquets de 6'),
])
MOB = ('Mobilisation des concepts et processus', [
    ('it', 'L’élève…'), ('sp', ''),
    ('b', 'établit le bon nombre de paniers :'),
    ('cb', 'denrées amassées (lecture du diagramme. Ex. : 48 + 62 + 56 + 58 = 224)'),
    ('cb', 'denrées périmées (à l’aide de processus personnels. Ex. : 224 à séparer en 4 = 56)'),
    ('cb', 'denrées à donner (Ex. : 224 – 56 = 168)'),
    ('cb', 'paniers (à l’aide de processus personnels. Ex. : 168 à séparer en paquets de 8 = 21)'),
    ('sp', ''),
    ('b', 'établit le coût de la préparation :'),
    ('sec', 'Les boîtes'),
    ('cb', 'fournisseur A : 21 × 2 $ = 42 $'),
    ('cb', 'fournisseur B : 5 paquets de 5 (25 boîtes) × 8 $ = 40 $'),
    ('cb', 'fournisseur C : 3 paquets de 10 (30 boîtes) × 19 $ = 57 $'),
    ('cb', 'choix du fournisseur le moins cher : B, 40 $'),
    ('sec', 'Le ruban'),
    ('cb', 'périmètre du dessus de la boîte (Ex. : 30 + 20 + 30 + 20 = 100 cm)'),
    ('cb', 'ruban pour une boîte (Ex. : 100 cm + 50 cm = 150 cm)'),
    ('cb', 'boîtes par rouleau (5 m = 500 cm; 150 + 150 + 150 = 450 cm, donc 3 boîtes)'),
    ('cb', 'rouleaux (Ex. : 21 ÷ 3 = 7 rouleaux; 7 × 3 $ = 21 $)'),
    ('sec', 'Les étiquettes'),
    ('cb', 'choix de l’étiquette 3, le losange (4 côtés de même longueur, aucun angle droit)'),
    ('cb', 'paquets (Ex. : 21 ÷ 6 = 3 reste 3, donc 4 paquets; 4 × 2 $ = 8 $)'),
    ('sp', ''),
    ('b', 'établit le coût total :'),
    ('cb', 'coût de la préparation (Ex. : 40 $ + 21 $ + 8 $ = 69 $)'),
])
EXP = ('Explicitation des éléments pertinents de la solution', [
    ('cb', 'Laisse des traces de chacune des étapes'),
    ('cb', 'La solution comprend le nombre de paniers (21) et le coût de la préparation des paniers (69 $)'),
])


def bloc(crit, lignes, y):
    """Retourne (svg, hauteur) d'une rangée du tableau."""
    x1 = C0 + PAD
    maxw = W - x1 - PAD
    s = ''
    yy = y + PAD + 4
    for typ, t in lignes:
        if typ == 'sp':
            yy += LH * 0.5; continue
        if typ == 'cb':
            parts = couper(t, maxw - 22)
            s += f"<rect x='{x1}' y='{yy-11}' width='11' height='11' fill='#fff' stroke='{INK}' stroke-width='1.2'/>"
            for k, p in enumerate(parts):
                s += f"<text x='{x1+20}' y='{yy+k*LH}' font-family='KG Perfect Penmanship' font-size='{FS}' fill='{INK}'>{esc(p)}</text>"
            yy += LH * len(parts) + 2
        elif typ == 'sec':
            yy += 6
            s += (f"<path d='M{x1} {yy-11} L{x1+12} {yy-5.5} L{x1} {yy} L{x1+3.5} {yy-5.5} Z' fill='{INK}'/>"
                  f"<text x='{x1+20}' y='{yy}' font-family='KG Perfect Penmanship' stroke='#1E1E1E' stroke-width='0.7' font-size='{FS}' fill='{INK}'>{esc(t)}</text>")
            yy += LH + 3
        else:
            bold = typ == 'b'
            parts = couper(t, maxw, bold)
            for k, p in enumerate(parts):
                s += (f"<text x='{x1}' y='{yy+k*LH}' font-family='KG Perfect Penmanship' font-size='{FS}' fill='{INK}' "
                      f"{'stroke=\"#1E1E1E\" stroke-width=\"0.7\"' if bold else ''} {'font-style=\"italic\"' if typ == 'it' else ''}>{esc(p)}</text>")
            yy += LH * len(parts) + 2
    h = yy - y + PAD - 6
    # critère centré verticalement
    cl = couper(crit, C0 - 2 * PAD, True)
    cy = y + h / 2 - (len(cl) - 1) * 11 + 5
    for k, p in enumerate(cl):
        s += f"<text x='{C0/2}' y='{cy+k*22}' font-family='KG Perfect Penmanship' stroke='#1E1E1E' stroke-width='0.7' font-size='16' text-anchor='middle' fill='{INK}'>{esc(p)}</text>"
    s = (f"<rect x='0' y='{y}' width='{W}' height='{h}' fill='#fff' stroke='{INK}' stroke-width='1.5'/>"
         f"<line x1='{C0}' y1='{y}' x2='{C0}' y2='{y+h}' stroke='{INK}' stroke-width='1.5'/>") + s
    return s, h


def entete():
    s = (f"<rect x='0' y='0' width='{W}' height='86' fill='#fff' stroke='{INK}' stroke-width='1.5'/>"
         f"<rect x='0' y='0' width='{W}' height='18' fill='{INK}'/>"
         f"<text x='{W-10}' y='14' font-family='KG Perfect Penmanship' font-size='13' text-anchor='end' fill='#fff' stroke='#fff' stroke-width='0.5'>4e année</text>"
         f"<text x='{W/2}' y='42' font-family='KG Perfect Penmanship' stroke='#1E1E1E' stroke-width='0.7' font-size='15' text-anchor='middle' fill='{INK}'>Éléments observables</text>"
         f"<text x='{W/2}' y='72' font-family='KG Perfect Penmanship' stroke='#1E1E1E' stroke-width='1' font-size='24' text-anchor='middle' fill='{INK}'>Les paniers de la guignolée</text>")
    return s, 86


def page(nom, parts):
    s, y = '', 0
    for p in parts:
        if p == 'entete':
            b, h = entete()
        elif p == 'gap':
            y += 16; continue
        else:
            b, h = bloc(*p, y)
        s += b; y += h
    H = y + 2
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{W+2}' height='{H}' viewBox='-1 -1 {W+2} {H}'>"
           f"<rect x='-1' y='-1' width='{W+2}' height='{H}' fill='#fff'/>{s}</svg>")
    open(nom + '.svg', 'w', encoding='utf-8').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=nom + '.png', scale=3)
    return H


if __name__ == '__main__':
    print('p1', page('observables-1', ['entete', COMP]))
    print('p2', page('observables-2', [MOB, 'gap', EXP]))
