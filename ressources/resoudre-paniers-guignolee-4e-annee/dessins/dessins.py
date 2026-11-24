"""Dessins du résoudre « Les paniers de la guignolée » (style maison : encre #1E1E1E, gris pâle, fond blanc).

Polices : Nunito et Lilita One (installées localement, voir BRAND.md).
Usage : python3 dessins.py  (produit les fichiers .svg et .png dans ce dossier)
"""
import math
import cairosvg

INK = '#1E1E1E'
GRIS = '#D9D9D9'
GRIS_PALE = '#EFEFEF'
F = "font-family='Nunito'"
T = "font-family='Lilita One'"
KG = "font-family='KG Perfect Penmanship'"  # police de la créatrice (non versionnée, licence)


def save(name, w, h, body, scale=3):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
         f'<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')
    open(name + '.svg', 'w', encoding='utf-8').write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to=name + '.png', scale=scale)


def txt(x, y, t, size=16, anchor='middle', weight=400, font=F, fill=INK, extra=''):
    return (f"<text x='{x}' y='{y}' {font} font-size='{size}' font-weight='{weight}' "
            f"text-anchor='{anchor}' fill='{fill}' {extra}>{t}</text>")


# ---------- 1. Diagramme à bandes ----------
def diagramme():
    W, H = 640, 430
    x0, y0, x1, ytop = 90, 360, 610, 50          # axes
    vmax = 70
    sy = (y0 - ytop) / vmax
    b = txt(W / 2, 32, 'Denrées amassées par classe', 26, font=KG)
    for v in range(0, vmax + 1, 2):
        y = y0 - v * sy
        fort = v % 10 == 0
        b += f"<line x1='{x0}' y1='{y}' x2='{x1}' y2='{y}' stroke='{'#9A9A9A' if fort else '#D4D4D4'}' stroke-width='{1.4 if fort else 0.8}'/>"
        b += f"<line x1='{x0-(9 if fort else 5)}' y1='{y}' x2='{x0}' y2='{y}' stroke='{INK}' stroke-width='1.4'/>"
        if fort:
            b += txt(x0 - 14, y + 6, str(v), 17, 'end', font=KG)
    data = [('3e année A', 48), ('3e année B', 62), ('4e année A', 56), ('4e année B', 58)]
    bw = 70
    step = (x1 - x0) / len(data)
    for i, (lab, v) in enumerate(data):
        cx = x0 + step * (i + .5)
        b += (f"<rect x='{cx-bw/2}' y='{y0-v*sy}' width='{bw}' height='{v*sy}' fill='{GRIS}' "
              f"stroke='{INK}' stroke-width='2'/>")
        b += txt(cx, y0 + 28, lab, 18, font=KG)
    b += f"<line x1='{x0}' y1='{ytop-8}' x2='{x0}' y2='{y0}' stroke='{INK}' stroke-width='2.5'/>"
    b += f"<line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y0}' stroke='{INK}' stroke-width='2.5'/>"
    b += txt(30, (y0 + ytop) / 2, 'Nombre de denrées', 18, font=KG,
             extra=f"transform='rotate(-90 30 {(y0+ytop)/2})'")
    b += txt((x0 + x1) / 2, y0 + 60, 'Classes', 18, font=KG)
    save('diagramme-denrees', W, H, b)


# ---------- 2. Boîtes des fournisseurs ----------
def boite(x, y, w=46, h=30, d=14, sw=2):
    """Boîte (prisme) en perspective, (x, y) = coin avant bas gauche."""
    return (f"<path d='M{x} {y} h{w} v{-h} h{-w} Z' fill='#fff' stroke='{INK}' stroke-width='{sw}' stroke-linejoin='round'/>"
            f"<path d='M{x} {y-h} l{d} {-d*.7} h{w} l{-d} {d*.7} Z' fill='{GRIS_PALE}' stroke='{INK}' stroke-width='{sw}' stroke-linejoin='round'/>"
            f"<path d='M{x+w} {y} l{d} {-d*.7} v{-h} l{-d} {d*.7} Z' fill='{GRIS}' stroke='{INK}' stroke-width='{sw}' stroke-linejoin='round'/>")


def pile(cx, base, n, cols):
    s = ''
    w, h = 40, 26
    rows = math.ceil(n / cols)
    k = 0
    for r in range(rows):
        nb = min(cols, n - k)
        x0 = cx - (nb * w) / 2 - 6
        for c in range(nb):
            s += boite(x0 + c * w + r * 6, base - r * (h + 2), w - 6, h - 6, 10)
            k += 1
    return s


def fournisseurs():
    W, H = 690, 300
    cartes = [('A', 'Carton Plus', 1, 1, '2 $', 'la boîte'),
              ('B', 'Emballo', 5, 3, '8 $', 'le paquet de 5 boîtes'),
              ('C', 'Boîtes en vrac', 10, 4, '19 $', 'le paquet de 10 boîtes')]
    b = ''
    cw = 210
    for i, (let, nom, n, cols, prix, unite) in enumerate(cartes):
        x = 10 + i * (cw + 20)
        b += f"<rect x='{x}' y='10' width='{cw}' height='280' rx='18' fill='#fff' stroke='{INK}' stroke-width='3'/>"
        b += f"<circle cx='{x+30}' cy='40' r='18' fill='{INK}'/>" + txt(x + 30, 47, let, 20, font=T, fill='#fff')
        b += txt(x + cw / 2 + 20, 47, nom, 18, weight=800)
        b += pile(x + cw / 2, 175, n, cols)
        b += f"<line x1='{x+20}' y1='200' x2='{x+cw-20}' y2='200' stroke='{GRIS}' stroke-width='2'/>"
        b += txt(x + cw / 2, 245, prix, 34, font=T)
        b += txt(x + cw / 2, 274, unite, 16, weight=700)
    save('fournisseurs-boites', W, H, b)


# ---------- 3. Le ruban ----------
def ruban():
    W, H = 640, 330
    # dessus de la boîte vu de haut (rectangle 30 cm x 20 cm), à l'échelle
    k = 8
    x, y = 90, 70
    w, h = 30 * k, 20 * k
    b = txt(x + w / 2, 40, 'Le dessus de la boîte', 18, weight=800)
    b += f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{GRIS_PALE}' stroke='{INK}' stroke-width='3'/>"
    # ruban qui fait le tour du dessus (en pointillé gras sur le contour)
    b += f"<rect x='{x}' y='{y}' width='{w}' height='{h}' fill='none' stroke='{INK}' stroke-width='7' stroke-dasharray='14 8'/>"
    # boucle
    bx, by = x + w, y
    b += (f"<path d='M{bx} {by} c 30 -40 70 -20 40 10 c -20 18 -40 0 -40 -10 c -10 -30 30 -60 46 -30' "
          f"fill='none' stroke='{INK}' stroke-width='5' stroke-linecap='round'/>")
    b += txt(x + w / 2, y + h + 34, '30 cm', 18, weight=800)
    b += txt(x - 14, y + h / 2 + 6, '20 cm', 18, 'end', weight=800)
    # légende
    lx = 400
    b += f"<line x1='{lx}' y1='120' x2='{lx+44}' y2='120' stroke='{INK}' stroke-width='7' stroke-dasharray='14 8'/>"
    b += txt(lx + 56, 126, 'le ruban fait', 17, 'start', 700) + txt(lx + 56, 148, 'le tour du dessus', 17, 'start', 700)
    b += (f"<path d='M{lx+4} 196 c 18 -24 42 -12 24 6 c -12 11 -24 0 -24 -6' fill='none' stroke='{INK}' "
          f"stroke-width='4' stroke-linecap='round'/>")
    b += txt(lx + 56, 194, '+ 50 cm pour', 17, 'start', 700) + txt(lx + 56, 216, 'faire la boucle', 17, 'start', 700)
    # rouleau
    rx, ry = 420, 262
    b += f"<ellipse cx='{rx}' cy='{ry}' rx='16' ry='30' fill='{GRIS}' stroke='{INK}' stroke-width='3'/>"
    b += f"<ellipse cx='{rx}' cy='{ry}' rx='6' ry='11' fill='#fff' stroke='{INK}' stroke-width='2'/>"
    b += txt(rx + 34, ry - 4, 'Rouleau de 5 m', 18, 'start', 800) + txt(rx + 34, ry + 24, '3 $', 22, 'start', font=T)
    save('ruban', W, H, b)


# ---------- 4. Les étiquettes ----------
def etiquettes():
    u = 18                      # 1 unité de la grille
    W, H = 700, 280
    fig = [  # (numéro, sommets en unités, prix)
        ('1', [(0, 0), (4, 0), (4, 4), (0, 4)], '3 $'),                 # carré
        ('2', [(0, 0), (6, 0), (6, 3), (0, 3)], '2 $'),                 # rectangle
        ('3', [(3, 0), (5, 3), (3, 6), (1, 3)], '2 $'),                 # losange (diagonales 4 et 6)
        ('4', [(2, 0), (7, 0), (5, 4), (0, 4)], '1 $'),                 # parallélogramme
        ('5', [(1, 0), (4, 0), (6, 4), (0, 4)], '3 $'),                 # trapèze
    ]
    b = ''
    zones = [(7 + i * 140, 20) for i in range(5)]
    for (num, pts, prix), (zx, zy) in zip(fig, zones):
        gw, gh = 7, 7
        ox, oy = zx, zy + 30
        for i in range(gw + 1):
            for j in range(gh + 1):
                b += f"<circle cx='{ox+i*u}' cy='{oy+j*u}' r='1.6' fill='#9A9A9A'/>"
        maxx = max(p[0] for p in pts); maxy = max(p[1] for p in pts)
        dx = (gw - maxx) // 2; dy = (gh - maxy) // 2
        d = 'M' + ' L'.join(f'{ox+(px+dx)*u} {oy+(py+dy)*u}' for px, py in pts) + ' Z'
        b += f"<path d='{d}' fill='{GRIS_PALE}' stroke='{INK}' stroke-width='3' stroke-linejoin='round'/>"
        cx = ox + (sum(p[0] for p in pts) / len(pts) + dx) * u
        cy = oy + (sum(p[1] for p in pts) / len(pts) + dy) * u
        b += f"<circle cx='{cx}' cy='{cy}' r='5' fill='#fff' stroke='{INK}' stroke-width='2'/>"   # trou de l'étiquette
        b += f"<circle cx='{zx+gw*u/2}' cy='{zy+8}' r='15' fill='{INK}'/>" + txt(zx + gw * u / 2, zy + 15, num, 18, font=T, fill='#fff')
        b += txt(zx + gw * u / 2, oy + gh * u + 40, prix, 28, font=T)
        b += txt(zx + gw * u / 2, oy + gh * u + 62, 'le paquet de 6', 14, weight=700)
    save('etiquettes', W, H, b)


# ---------- 5. Quadrillage pour la démarche ----------
def quadrillage(cols=34, rows=40, u=20):
    W, H = cols * u + 2, rows * u + 2
    b = ''
    for i in range(cols + 1):
        b += f"<line x1='{1+i*u}' y1='1' x2='{1+i*u}' y2='{H-1}' stroke='#C8C8C8' stroke-width='1'/>"
    for j in range(rows + 1):
        b += f"<line x1='1' y1='{1+j*u}' x2='{W-1}' y2='{1+j*u}' stroke='#C8C8C8' stroke-width='1'/>"
    b += f"<rect x='1' y='1' width='{W-2}' height='{H-2}' fill='none' stroke='#9A9A9A' stroke-width='2'/>"
    save('quadrillage', W, H, b, scale=3)


# ---------- 6. Icônes au trait pour les bandeaux ----------
def icone_panier():
    b = (f"<g fill='none' stroke='{INK}' stroke-width='5' stroke-linejoin='round' stroke-linecap='round'>"
         "<path d='M20 70 h140 l-14 70 h-112 Z'/>"
         "<path d='M44 70 c0 -46 92 -46 92 0'/>"
         "<path d='M50 84 l6 44 M80 84 v44 M110 84 v44 M140 84 l-6 44'/>"
         "<rect x='58' y='36' width='30' height='36' rx='4'/>"
         "<path d='M96 70 v-26 h26 v26'/>"
         "<path d='M104 30 c4 -14 22 -14 18 4'/></g>")
    save('icone-panier', 180, 160, b)


def icone_boite():
    b = (f"<g fill='none' stroke='{INK}' stroke-width='5' stroke-linejoin='round' stroke-linecap='round'>"
         "<path d='M30 60 h90 v80 h-90 Z'/><path d='M30 60 l26 -24 h90 l-26 24'/><path d='M120 140 l26 -24 v-80'/>"
         "<path d='M75 60 v80 M75 60 l26 -24'/>"
         "<path d='M75 60 c-20 -26 -40 -10 -24 2 c10 8 24 -2 24 -2 c0 0 14 10 24 2 c16 -12 -4 -28 -24 -2'/></g>")
    save('icone-boite', 170, 160, b)


def icone_etiquette():
    b = (f"<g fill='none' stroke='{INK}' stroke-width='5' stroke-linejoin='round' stroke-linecap='round'>"
         "<path d='M30 40 h80 l40 40 l-40 40 h-80 Z'/><circle cx='112' cy='80' r='8'/>"
         "<path d='M120 80 c20 0 26 30 10 50'/><path d='M48 70 h40 M48 90 h30'/></g>")
    save('icone-etiquette', 170, 160, b)


def icone_calcul():
    b = (f"<g fill='none' stroke='{INK}' stroke-width='5' stroke-linejoin='round' stroke-linecap='round'>"
         "<rect x='40' y='20' width='90' height='124' rx='12'/><rect x='54' y='34' width='62' height='26' rx='4'/>"
         "<path d='M62 82 h14 M69 75 v14'/><path d='M96 82 h14'/>"
         "<path d='M63 108 l12 12 M75 108 l-12 12'/><path d='M96 108 h14 M103 102 v0 M103 122 v0'/></g>")
    save('icone-calcul', 170, 160, b)


if __name__ == '__main__':
    diagramme(); fournisseurs(); ruban(); etiquettes(); quadrillage()
    icone_panier(); icone_boite(); icone_etiquette(); icone_calcul()


# ---------- 7. Illustration de la couverture (panier de Noël en couleur) ----------
def st(c=INK, w=5):
    return f"stroke='{c}' stroke-width='{w}' stroke-linejoin='round' stroke-linecap='round'"


def couverture():
    W, H = 600, 470
    b = ''
    # anse
    b += f"<path d='M140 245 C 150 20, 450 20, 460 245' fill='none' {st(w=14)}/>"
    b += f"<path d='M140 245 C 150 20, 450 20, 460 245' fill='none' {st('#E4B47A', 6)}/>"
    # denrées derrière le panier
    b += f"<rect x='150' y='120' width='90' height='150' rx='8' fill='#F5D06F' {st()}/>"                 # boîte de céréales
    b += f"<path d='M168 150 h54 M168 172 h40' fill='none' {st()}/>"
    b += f"<circle cx='195' cy='225' r='18' fill='#fff' {st()}/>"
    b += f"<rect x='255' y='170' width='70' height='100' rx='10' fill='#F49FA6' {st()}/>"                # conserve
    b += f"<path d='M255 200 h70 M255 240 h70' fill='none' {st()}/>"
    b += f"<path d='M345 110 h60 v30 l14 20 v110 h-88 v-110 l14 -20 Z' fill='#7FD6C8' {st()}/>"          # pot
    b += f"<rect x='345' y='95' width='60' height='20' rx='5' fill='#2E8A5A' {st()}/>"
    b += f"<rect x='420' y='160' width='70' height='110' rx='8' fill='#FDE0C8' {st()}/>"                # pâtes
    b += f"<path d='M432 190 l46 30 M478 190 l-46 30' fill='none' {st()}/>"
    # panier
    b += f"<path d='M110 255 h380 l-34 175 h-312 Z' fill='#E4B47A' {st()}/>"
    b += "<clipPath id='corps'><path d='M110 255 h380 l-34 175 h-312 Z'/></clipPath><g clip-path='url(#corps)'>"
    for x in range(150, 470, 40):
        b += f"<path d='M{x} 262 l{(x-300)*0.09:.1f} 170' fill='none' {st(w=3)}/>"
    b += f"<path d='M100 310 h400 M100 360 h400' fill='none' {st(w=3)}/></g>"
    b += f"<path d='M110 255 h380 l-34 175 h-312 Z' fill='none' {st()}/>"
    b += f"<rect x='96' y='240' width='408' height='34' rx='12' fill='#C98B4E' {st()}/>"
    # boucle rouge
    b += (f"<path d='M300 262 l -24 60 M300 262 l 24 60' fill='none' {st('#D9443A', 10)}/>"
          f"<path d='M300 262 c -60 -50 -90 10 -30 20 Z' fill='#D9443A' {st()}/>"
          f"<path d='M300 262 c 60 -50 90 10 30 20 Z' fill='#D9443A' {st()}/>"
          f"<circle cx='300' cy='264' r='14' fill='#D9443A' {st()}/>")
    # branche de sapin
    b += f"<path d='M470 250 q40 -10 70 -50' fill='none' {st('#2E8A5A', 6)}/>"
    for i in range(6):
        x, y = 480 + i * 10, 246 - i * 9
        b += f"<path d='M{x} {y} l14 10 M{x} {y} l-4 -16' fill='none' {st('#2E8A5A', 5)}/>"
    b += f"<circle cx='506' cy='238' r='9' fill='#D9443A' {st(w=3)}/><circle cx='522' cy='250' r='9' fill='#D9443A' {st(w=3)}/>"
    save('couverture-panier', W, H, b)


if __name__ == '__main__':
    couverture()


# ---------- 8. Grille d'évaluation de l'enseignant (critères et niveaux A à E) ----------
def wrap(t, n):
    mots, lignes, cur = t.split(), [], ''
    for m in mots:
        if len(cur) + len(m) + 1 > n and cur:
            lignes.append(cur); cur = m
        else:
            cur = (cur + ' ' + m).strip()
    lignes.append(cur)
    return lignes


def grille():
    crit = [
        ('Compréhension de la situation-problème', [40, 32, 24, 16, 8], [
            "Effectue toutes les étapes. Tient compte de l’ensemble des contraintes et des données. Interventions mineures.",
            "Effectue la majorité des étapes. Tient compte des données et de la plupart des contraintes. Interventions pour certains aspects.",
            "Effectue la majorité des étapes. Tient compte des données importantes et de certaines contraintes. Interventions pour plusieurs aspects.",
            "Effectue quelques étapes. Tient compte des données importantes et de peu de contraintes. Interventions pour la plupart des aspects.",
            "Effectue quelques étapes sans les compléter. Tient compte de peu ou d’aucune contrainte. Interventions majeures."]),
        ('Mobilisation des concepts et des processus appropriés', [40, 32, 24, 16, 8], [
            "Fait appel aux concepts et aux processus adéquats. Commet peu d’erreurs mineures.",
            "Fait appel à la majorité des concepts et des processus adéquats. Commet quelques erreurs mineures ou peu d’erreurs conceptuelles ou procédurales.",
            "Fait appel aux concepts et aux processus principaux. Commet plusieurs erreurs mineures ou quelques erreurs conceptuelles ou procédurales.",
            "Fait appel à certains concepts et processus adéquats. Commet plusieurs erreurs conceptuelles ou procédurales. Réalise une partie de la solution.",
            "Fait appel à des concepts et processus inadéquats. Commet plusieurs erreurs conceptuelles ou procédurales. Solution inadéquate."]),
        ('Explicitation de la solution (traces écrites ou orales)', [20, 16, 12, 8, 4], [
            "Laisse des traces claires de sa démarche.",
            "Laisse des traces adéquates de sa démarche.",
            "Laisse quelques traces de sa démarche.",
            "Laisse peu de traces de sa démarche.",
            "Ne laisse pas de traces de sa démarche."]),
    ]
    W = 1000
    c0 = 190                     # largeur de la colonne des critères
    cw = (W - c0) / 5
    fs, lh = 14, 18
    b = ''
    y = 0
    hh = 44
    b += f"<rect x='0' y='0' width='{W}' height='{hh}' fill='{GRIS}' stroke='{INK}' stroke-width='2'/>"
    b += txt(c0 / 2, 28, 'Critères', 18, weight=800)
    for i, L in enumerate('ABCDE'):
        x = c0 + i * cw
        b += f"<line x1='{x}' y1='0' x2='{x}' y2='{hh}' stroke='{INK}' stroke-width='2'/>"
        b += txt(x + cw / 2, 30, L, 22, font=T)
    y = hh
    for nom, pts, desc in crit:
        lignes = [wrap(d, 19) for d in desc]
        nl = max(len(l) for l in lignes)
        h = max(nl * lh + 62, 120)
        b += f"<rect x='0' y='{y}' width='{W}' height='{h}' fill='#fff' stroke='{INK}' stroke-width='2'/>"
        b += f"<rect x='0' y='{y}' width='{c0}' height='{h}' fill='{GRIS_PALE}' stroke='{INK}' stroke-width='2'/>"
        nomL = wrap(nom, 16)
        y0 = y + h / 2 - (len(nomL) - 1) * 11
        for k, l in enumerate(nomL):
            b += txt(c0 / 2, y0 + k * 22 + 6, l, 16, weight=800)
        for i in range(5):
            x = c0 + i * cw
            b += f"<line x1='{x}' y1='{y}' x2='{x}' y2='{y+h}' stroke='{INK}' stroke-width='2'/>"
            for k, l in enumerate(lignes[i]):
                b += txt(x + 10, y + 24 + k * lh, l, fs, 'start')
            # case de points
            b += f"<rect x='{x+cw/2-28}' y='{y+h-38}' width='56' height='28' rx='6' fill='{GRIS_PALE}' stroke='{INK}' stroke-width='1.5'/>"
            b += txt(x + cw / 2, y + h - 18, str(pts[i]), 17, weight=800)
        y += h
    H = y + 2
    save('grille-evaluation', W + 2, H, f"<g transform='translate(1 1)'>{b}</g>", scale=3)


if __name__ == '__main__':
    grille()
