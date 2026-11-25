"""Grille d'évaluation en écriture, 2e cycle, en KG Perfect Penmanship (police de la créatrice, non versionnée).
Contenu repris de la grille du ministère (Précisions sur la grille d'évaluation, fin du 2e cycle, 2012).
Usage : python3 grille_ecriture.py  -> grille-ecriture.png / .svg (Lettre à l'horizontale, 792 × 612)
"""
from PIL import ImageFont
import cairosvg

INK = '#1E1E1E'
GRIS = '#D9D9D9'
KGP = '/root/.fonts/KGPerfectPenmanship.ttf'
KG = "font-family='KG Perfect Penmanship'"
GRAS = f"stroke='{INK}' stroke-width='0.6'"
f100 = ImageFont.truetype(KGP, 100)


def larg(t, fs):
    return f100.getlength(t) * fs / 100


def couper(t, maxw, fs):
    out = []
    for para in t.split('\n'):
        if para == '':
            out.append(''); continue
        cur = ''
        for m in para.split(' '):
            e = (cur + ' ' + m).strip()
            if larg(e, fs) > maxw and cur:
                out.append(cur); cur = m
            else:
                cur = e
        out.append(cur)
    return out


def esc(t):
    return t.replace('&', '&amp;')


def bloc(x, y, w, h, texte, fs, lh, anchor='middle', gras=False, valign='middle'):
    lignes = couper(texte, w - 12, fs)
    tot = len(lignes) * lh
    y0 = y + (h - tot) / 2 + lh * 0.78 if valign == 'middle' else y + 8 + lh * 0.78
    xx = x + w / 2 if anchor == 'middle' else x + 7
    s = ''
    for k, l in enumerate(lignes):
        if l:
            s += (f"<text x='{xx}' y='{y0 + k*lh}' {KG} font-size='{fs}' text-anchor='{anchor}' fill='{INK}' "
                  f"{GRAS if gras else ''}>{esc(l)}</text>")
    return s


W, H = 792, 612
X0, Y0 = 30, 76
CW = [150, 120, 120, 120, 120, 112]          # critères + A..E (total 742)
NIV = [('TRÈS SATISFAISANT', 'A', 20), ('SATISFAISANT', 'B', 16), ('ACCEPTABLE', 'C', 12),
       ('PEU SATISFAISANT', 'D', 8), ('INSATISFAISANT', 'E', 4)]
CRIT = [
    ('1. Adaptation à la situation d’écriture', [
        'Les idées, très bien développées, respectent particulièrement bien le projet d’écriture.',
        'Les idées, bien développées, respectent le projet d’écriture.',
        'Les idées, peu développées, respectent les principales exigences du projet d’écriture.',
        'Il manque un élément important pour que le projet d’écriture soit respecté.\nOU\nPlusieurs idées sont imprécises ou superflues.',
        'Les idées ont peu ou pas de liens avec le projet d’écriture.'], 66),
    ('2. Cohérence du texte', [
        'Les idées sont présentées dans un ordre logique.\nDes liens appropriés sont assez souvent établis entre les phrases.\nLe texte est divisé en paragraphes qui correspondent assez bien aux différentes parties.',
        'En général, les idées sont présentées dans un ordre logique.\nQuelques liens appropriés sont établis entre les phrases.\nLe texte est divisé en paragraphes qui correspondent un peu aux différentes parties.',
        'Les idées, présentées la plupart du temps selon un ordre logique, sont à certains moments décousues.\nLe texte comprend un ou plusieurs paragraphes.',
        'Les idées sont assez souvent décousues, malgré la présence d’une certaine organisation.',
        'Les idées sont décousues.'], 150),
    ('3. Utilisation d’un vocabulaire approprié', [
        'Les expressions et les mots sont souvent précis et variés.',
        'Les expressions et les mots sont corrects. À l’occasion, les termes utilisés sont précis et variés.',
        'Les expressions et les mots sont corrects.',
        'Les expressions et les mots sont parfois imprécis et souvent répétés.',
        'Les expressions et les mots sont souvent imprécis ou relèvent de la langue familière.'], 66),
    ('4. Construction des phrases et ponctuation appropriées', [
        'En général, les phrases sont bien structurées et bien ponctuées, malgré la présence de maladresses dans les phrases élaborées.',
        'Les phrases sont souvent bien structurées et bien ponctuées, malgré la présence de maladresses dans les phrases élaborées.\nQuelques phrases élaborées sont mal structurées ou mal ponctuées.',
        'Les phrases simples sont bien structurées. Elles sont généralement délimitées par la majuscule et le point.\nCertaines phrases élaborées sont bien structurées et bien ponctuées.',
        'Plusieurs phrases sont mal structurées ou mal ponctuées.',
        'La plupart des phrases sont mal structurées ou mal ponctuées.'], 120),
    ('5. Respect des normes relatives à l’orthographe d’usage et à l’orthographe grammaticale', [
        'Le texte présente moins de 4 % d’erreurs.',
        'Le texte présente de 4 % à 7 % d’erreurs.',
        'Le texte présente de 8 % à 10 % d’erreurs.',
        'Le texte présente de 11 % à 14 % d’erreurs.',
        'Le texte présente plus de 14 % d’erreurs.'], 62),
]
FS, LH = 8.6, 10.6

s = f"<rect width='{W}' height='{H}' fill='#fff'/>"
s += (f"<text x='{W/2}' y='34' {KG} font-size='22' text-anchor='middle' fill='{INK}' stroke='{INK}' stroke-width='0.9'>"
      f"Grille d’évaluation en écriture – 2e cycle</text>")
s += f"<text x='{X0}' y='62' {KG} font-size='13' fill='{INK}'>Nom de l’élève : ______________________________</text>"
s += f"<text x='{W-X0}' y='62' {KG} font-size='13' text-anchor='end' fill='{INK}'>Résultat : ________ / 100</text>"

xs = [X0]
for c in CW:
    xs.append(xs[-1] + c)
TW = xs[-1] - X0
# en-tête
h1, h2 = 22, 40
s += f"<rect x='{X0}' y='{Y0}' width='{TW}' height='{h1+h2}' fill='{GRIS}' stroke='{INK}' stroke-width='1.4'/>"
s += bloc(xs[0], Y0, CW[0], h1 + h2, 'CRITÈRES', 13, 14, gras=True)
s += bloc(xs[1], Y0, TW - CW[0], h1, 'CARACTÉRISTIQUES DU TEXTE', 12, 14, gras=True)
s += f"<line x1='{xs[1]}' y1='{Y0+h1}' x2='{xs[-1]}' y2='{Y0+h1}' stroke='{INK}' stroke-width='1'/>"
for i, (nom, let, pts) in enumerate(NIV):
    x = xs[i + 1]
    s += bloc(x, Y0 + h1, CW[i + 1], h2, f'{nom}\n{let}\n({pts} points)', 8.8, 11, gras=True)
y = Y0 + h1 + h2
for crit, cases, h in CRIT:
    h = max(max(len(couper(t, CW[i+1]-12, FS)) for i, t in enumerate(cases)) * LH + 12,
            len(couper(crit, CW[0]-12, 9.6)) * 11.6 + 26)
    s += f"<rect x='{X0}' y='{y}' width='{TW}' height='{h}' fill='#fff' stroke='{INK}' stroke-width='1.4'/>"
    s += bloc(xs[0], y, CW[0], h - 14, crit, 9.6, 11.6, anchor='start', gras=True, valign='top')
    s += f"<text x='{xs[0]+CW[0]/2}' y='{y+h-6}' {KG} font-size='9.6' text-anchor='middle' fill='{INK}' {GRAS}>20 %</text>"
    for i, t in enumerate(cases):
        s += bloc(xs[i + 1], y, CW[i + 1], h, t, FS, LH)
    y += h
for x in xs[1:-1]:
    s += f"<line x1='{x}' y1='{Y0 + (h1 if x != xs[1] else 0)}' x2='{x}' y2='{y}' stroke='{INK}' stroke-width='1'/>"
s += f"<line x1='{xs[1]}' y1='{Y0}' x2='{xs[1]}' y2='{y}' stroke='{INK}' stroke-width='1.4'/>"
s += f"<rect x='{X0}' y='{Y0}' width='{TW}' height='{y-Y0}' fill='none' stroke='{INK}' stroke-width='1.6'/>"
s += (f"<text x='{X0}' y='{y+16}' {KG} font-size='8' fill='#555'>Source : ministère de l’Éducation, du Loisir et du Sport, "
      f"Précisions sur la grille d’évaluation, fin du 2e cycle (2012).</text>")
print('bas du tableau :', y)
svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{s}</svg>"
open('grille-ecriture.svg', 'w', encoding='utf-8').write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to='grille-ecriture.png', scale=3)
