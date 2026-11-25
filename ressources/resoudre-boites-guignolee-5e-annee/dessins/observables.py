"""Grille « Éléments observables » (modèle de la créatrice) pour Les boîtes de la guignolée (5e année).
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
    ('b', 'doit déterminer le nombre de boîtes à préparer en tenant compte :'),
    ('cb', 'du nombre de denrées amassées par chaque classe (diagramme à bandes)'),
    ('cb', 'du 1/8 des denrées qui sont périmées et qu’il faut retirer'),
    ('cb', 'des 8 denrées par boîte et des boîtes complètes seulement'), ('sp', ''),
    ('b', 'doit déterminer le coût de la préparation des boîtes en tenant compte :'),
    ('sec', 'Les boîtes'),
    ('cb', 'des prix des trois fournisseurs (à l’unité, paquets de 5, paquets de 10)'),
    ('sec', 'Le ruban'),
    ('cb', 'de la taille de la boîte (35 cm × 25 cm) et des 45 cm pour la boucle'),
    ('cb', 'des rouleaux de 10 m à 5 $ et d’un ruban d’un seul morceau'),
    ('sec', 'Les étiquettes'),
    ('cb', 'des contraintes : un quadrilatère, une seule paire de côtés parallèles, une aire de 10 carrés ou plus'),
    ('cb', 'd’une étiquette par boîte et des paquets de 8'), ('sp', ''),
    ('b', 'doit déterminer l’argent qui restera en tenant compte :'),
    ('cb', 'des 200 $ donnés par les parents'),
])
MOB = ('Mobilisation des concepts et processus', [
    ('it', 'L’élève…'), ('sp', ''),
    ('b', 'établit le bon nombre de boîtes :'),
    ('cb', 'denrées amassées (lecture du diagramme. Ex. : 125 + 110 + 115 + 130 = 480)'),
    ('cb', 'denrées périmées (à l’aide de processus personnels. Ex. : 480 à séparer en 8 = 60)'),
    ('cb', 'denrées à donner (Ex. : 480 – 60 = 420)'),
    ('cb', 'boîtes (Ex. : 420 ÷ 8 = 52 reste 4, donc 52 boîtes complètes)'),
    ('sp', ''),
    ('b', 'établit le coût de la préparation :'),
    ('sec', 'Les boîtes'),
    ('cb', 'fournisseur A : 52 × 2 $ = 104 $'),
    ('cb', 'fournisseur B : 52 ÷ 5 = 10 reste 2, donc 11 paquets; 11 × 9 $ = 99 $'),
    ('cb', 'fournisseur C : 52 ÷ 10 = 5 reste 2, donc 6 paquets; 6 × 18 $ = 108 $'),
    ('cb', 'choix du fournisseur le moins cher : B, 99 $'),
    ('sec', 'Le ruban'),
    ('cb', 'ruban pour une boîte (Ex. : 35 + 25 + 35 + 25 = 120 cm; 120 + 45 = 165 cm = 1,65 m)'),
    ('cb', 'boîtes par rouleau (10 m = 1000 cm; 165 × 6 = 990 cm, donc 6 boîtes)'),
    ('cb', 'rouleaux (Ex. : 52 ÷ 6 = 8 reste 4, donc 9 rouleaux; 9 × 5 $ = 45 $)'),
    ('sec', 'Les étiquettes'),
    ('cb', 'choix de l’étiquette 4, le grand trapèze (une seule paire de côtés parallèles, aire de 12 carrés)'),
    ('cb', 'paquets (Ex. : 52 ÷ 8 = 6 reste 4, donc 7 paquets; 7 × 3 $ = 21 $)'),
    ('sp', ''),
    ('b', 'établit le coût total et l’argent qui reste :'),
    ('cb', 'coût de la préparation (Ex. : 99 $ + 45 $ + 21 $ = 165 $)'),
    ('cb', 'argent qui reste (Ex. : 200 $ – 165 $ = 35 $)'),
])
EXP = ('Explicitation des éléments pertinents de la solution', [
    ('cb', 'Laisse des traces de chacune des étapes'),
    ('cb', 'La solution comprend le nombre de boîtes (52), le coût de la préparation (165 $) et l’argent qui reste (35 $)'),
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
         f"<text x='{W-10}' y='14' font-family='KG Perfect Penmanship' font-size='13' text-anchor='end' fill='#fff' stroke='#fff' stroke-width='0.5'>5e année</text>"
         f"<text x='{W/2}' y='42' font-family='KG Perfect Penmanship' stroke='#1E1E1E' stroke-width='0.7' font-size='15' text-anchor='middle' fill='{INK}'>Éléments observables</text>"
         f"<text x='{W/2}' y='72' font-family='KG Perfect Penmanship' stroke='#1E1E1E' stroke-width='1' font-size='24' text-anchor='middle' fill='{INK}'>Les boîtes de la guignolée</text>")
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


def resultat(nom='grille-resultat'):
    """Grille-synthèse A à E (modèle de la créatrice), en gris selon BRAND.md."""
    GR = '#D9D9D9'
    KGF = "font-family='KG Perfect Penmanship'"
    B = f"stroke='{INK}' stroke-width='0.7'"
    Wt, x0 = 720, 0
    c1 = 330                       # colonne des critères
    cw = (Wt - c1) / 5             # colonnes A à E
    y0 = 48                        # sous le titre
    hH1, hH2, r1, r2, r3, rR = 60, 44, 76, 76, 56, 56
    H = y0 + hH1 + hH2 + r1 + r2 + r3 + rR
    sep = 4                        # filets blancs entre les cases
    s = f"<text x='0' y='32' {KGF} font-size='30' fill='{INK}' stroke='{INK}' stroke-width='1'>Résoudre une situation-problème</text>"
    # fond gris arrondi
    s += f"<rect x='0' y='{y0}' width='{Wt}' height='{H-y0}' rx='18' fill='{GR}'/>"
    def case(x, y, w, h):
        return f"<rect x='{x+sep/2}' y='{y+sep/2}' width='{w-sep}' height='{h-sep}' fill='#fff'/>"
    def t(x, y, txt, size=19, anchor='start', bold=False):
        return (f"<text x='{x}' y='{y}' {KGF} font-size='{size}' text-anchor='{anchor}' fill='{INK}' "
                f"{B if bold else ''}>{esc(txt)}</text>")
    # en-tête
    s += t(22, y0 + (hH1 + hH2) / 2 + 7, 'Critères d’évaluation', 21, bold=True)
    s += f"<line x1='{c1}' y1='{y0}' x2='{c1}' y2='{H}' stroke='#fff' stroke-width='{sep}'/>"
    s += f"<line x1='{c1}' y1='{y0+hH1}' x2='{Wt}' y2='{y0+hH1}' stroke='#fff' stroke-width='{sep}'/>"
    s += t(c1 + (Wt - c1) / 2, y0 + 26, 'Manifestations observables', 20, 'middle', True)
    s += t(c1 + (Wt - c1) / 2, y0 + 50, 'd’un niveau', 20, 'middle', True)
    for i, L in enumerate('ABCDE'):
        x = c1 + i * cw
        if i:
            s += f"<line x1='{x}' y1='{y0+hH1}' x2='{x}' y2='{y0+hH1+hH2}' stroke='#fff' stroke-width='{sep}'/>"
        s += t(x + cw / 2, y0 + hH1 + 30, L, 21, 'middle', True)
    # rangées
    y = y0 + hH1 + hH2
    rangs = [(['Compréhension de la', 'situation-problème'], r1, [40, 32, 24, 16, 8]),
             (['Mobilisation des concepts et des', 'processus appropriés à la situation'], r2, [40, 32, 24, 16, 8]),
             (['Explicitation de la solution (traces)'], r3, [20, 16, 12, 8, 4])]
    for lignes, h, pts in rangs:
        s += case(0, y, c1, h)
        for k, l in enumerate(lignes):
            s += t(22, y + h / 2 + 7 - (len(lignes) - 1) * 12 + k * 24, l, 18.5)
        for i, p in enumerate(pts):
            s += case(c1 + i * cw, y, cw, h)
            s += t(c1 + i * cw + cw / 2, y + h / 2 + 7, str(p), 20, 'middle')
        y += h
    # résultat
    s += t(c1 - 22, y + rR / 2 + 8, 'Résultat', 21, 'end', True)
    s += (f"<path d='M{c1+sep/2} {y+sep/2} H{Wt-sep/2} V{y+rR-18} "
          f"A{18-sep/2} {18-sep/2} 0 0 1 {Wt-18} {y+rR-sep/2} H{c1+sep/2} Z' fill='#fff'/>")
    s += t(c1 + (Wt - c1) / 2, y + rR / 2 + 8, '/100', 21, 'middle')
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{Wt+2}' height='{H+2}' viewBox='-1 -1 {Wt+2} {H+2}'>"
           f"<rect x='-1' y='-1' width='{Wt+2}' height='{H+2}' fill='#fff'/>{s}</svg>")
    open(nom + '.svg', 'w', encoding='utf-8').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=nom + '.png', scale=3)
    print('resultat', H + 2)


if __name__ == '__main__':
    resultat()
