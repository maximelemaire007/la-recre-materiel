"""Pages dessinées du cahier « La catastrophe au village des lutins » (KG Perfect Penmanship, encre #1E1E1E, gris).
Usage : python3 cahier.py -> plan-1.png, plan-2.png, choix.png, banque.png, lignes.png (+ .svg)
Toutes les lignes sont pleines.
"""
from PIL import ImageFont
import cairosvg

INK = '#1E1E1E'; GRIS = '#D9D9D9'; GRIS_P = '#F2F2F2'; LIGNE = '#8C8C8C'
KG = "font-family='KG Perfect Penmanship'"
GRAS = f"stroke='{INK}' stroke-width='0.7'"
f100 = ImageFont.truetype('/root/.fonts/KGPerfectPenmanship.ttf', 100)
W = 720


def larg(t, fs): return f100.getlength(t) * fs / 100
def esc(t): return t.replace('&', '&amp;')


def txt(x, y, t, fs=15, anchor='start', gras=False, fill=INK):
    return (f"<text x='{x}' y='{y}' {KG} font-size='{fs}' text-anchor='{anchor}' fill='{fill}' "
            f"{GRAS if gras else ''}>{esc(t)}</text>")


def lignes(x, y, w, n, pas=30):
    return ''.join(f"<line x1='{x}' y1='{y+i*pas}' x2='{x+w}' y2='{y+i*pas}' stroke='{LIGNE}' stroke-width='1.2'/>"
                   for i in range(1, n + 1))


def save(nom, h, body):
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{h}' viewBox='0 0 {W} {h}'>"
           f"<rect width='{W}' height='{h}' fill='#fff'/>{body}</svg>")
    open(nom + '.svg', 'w', encoding='utf-8').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=nom + '.png', scale=3)


def section(y, num, titre, partie, blocs):
    """Encadré d'une partie du schéma narratif : bandeau gris, puis des blocs (questions guides, nb de lignes pleines)."""
    corps = sum(20 * len(q) + n * 30 + 8 for q, n in blocs)
    h = 44 + corps + 10
    s = f"<rect x='1' y='{y}' width='{W-2}' height='{h}' rx='14' fill='#fff' stroke='{INK}' stroke-width='2.2'/>"
    s += f"<path d='M1 {y+14} a14 14 0 0 1 14 -14 H{W-15} a14 14 0 0 1 14 14 V{y+36} H1 Z' fill='{GRIS}' stroke='{INK}' stroke-width='2.2'/>"
    s += f"<circle cx='26' cy='{y+18}' r='13' fill='{INK}'/>" + txt(26, y + 24, str(num), 16, 'middle', fill='#fff')
    s += txt(48, y + 25, titre, 18, gras=True)
    s += txt(W - 16, y + 25, partie, 15, 'end')
    yy = y + 58
    for questions, n in blocs:
        for q in questions:
            s += f"<circle cx='22' cy='{yy-5}' r='2.6' fill='{INK}'/>" + txt(32, yy, q, 14)
            yy += 20
        s += lignes(16, yy - 22, W - 32, n)
        yy += n * 30 + 8
    return s, h


def plans():
    s, y = '', 0
    b, h = section(y, 1, 'Situation initiale', 'le début', [([
        'Où se passe ton histoire?', 'Qui sont les personnages?',
        'Que font-ils avant la catastrophe?'], 6)]); s += b; y += h + 14
    b, h = section(y, 2, 'Élément déclencheur', 'le début', [([
        'Quelle catastrophe arrive?', 'Comment les personnages la découvrent-ils?',
        'Comment réagissent-ils?'], 6)]); s += b; y += h + 14
    save('plan-1', y - 14, s)
    s, y = '', 0
    b, h = section(y, 3, 'Péripéties', 'le milieu', [
        (['Péripétie 1 : Que font les personnages pour régler le problème?'], 3),
        (['Péripétie 2 : Que se passe-t-il ensuite? Une nouvelle difficulté arrive-t-elle?'], 3)]); s += b; y += h + 14
    b, h = section(y, 4, 'Dénouement et situation finale', 'la fin', [(
        ['Comment les personnages règlent-ils le problème?',
         'Que se passe-t-il après? Comment se termine ton histoire?'], 4)]); s += b; y += h + 14
    # approbation par l'enseignant ou l'enseignante
    ha = 74
    s += f"<rect x='1' y='{y}' width='{W-2}' height='{ha}' rx='14' fill='{GRIS_P}' stroke='{INK}' stroke-width='2.2' stroke-dasharray='0'/>"
    s += txt(18, y + 28, 'Mon plan est accepté par mon enseignant ou mon enseignante :', 15, gras=True)
    bx = 18
    for lab in ['Oui, tu peux écrire ton brouillon!', 'À retravailler']:
        s += f"<rect x='{bx}' y='{y+42}' width='16' height='16' fill='#fff' stroke='{INK}' stroke-width='1.6'/>"
        s += txt(bx + 24, y + 56, lab, 14); bx += larg(lab, 14) + 60
    s += txt(W - 170, y + 56, 'Initiales :', 14)
    s += f"<line x1='{W-100}' y1='{y+58}' x2='{W-18}' y2='{y+58}' stroke='{INK}' stroke-width='1.4'/>"
    y += ha
    save('plan-2', y, s)


def choix():
    s = ''
    cw = (W - 24) / 2
    items = [('Choix 1', 'Les cadeaux ont disparu!',
              ['Un matin, les lutins découvrent', 'que tous les cadeaux préparés', 'pour Noël ont mystérieusement', 'disparu!']),
             ('Choix 2', 'La machine à jouets est brisée!',
              ['À quelques jours de Noël,', 'la machine qui fabrique tous', 'les jouets tombe soudainement', 'en panne!'])]
    h = 210
    for i, (c, t, lignes_) in enumerate(items):
        x = 1 + i * (cw + 22)
        s += f"<rect x='{x}' y='1' width='{cw}' height='{h}' rx='16' fill='#fff' stroke='{INK}' stroke-width='2.4'/>"
        s += f"<rect x='{x+16}' y='18' width='22' height='22' fill='#fff' stroke='{INK}' stroke-width='2'/>"
        s += txt(x + 48, 37, c, 18, gras=True)
        s += txt(x + cw / 2, 78, t, 17, 'middle', gras=True)
        for k, l in enumerate(lignes_):
            s += txt(x + cw / 2, 116 + k * 24, l, 15, 'middle')
    save('choix', h + 2, s)


def banque():
    rows = [('Personnages', 'lutin, lutine, père Noël, mère Noël, renne, apprenti, chef des lutins'),
            ('Lieux', 'atelier, village, forêt enneigée, entrepôt, traîneau, pôle Nord'),
            ('Verbes', 'fabriquer, découvrir, réparer, chercher, courir, cacher, emballer'),
            ('Adjectifs', 'mystérieux, immense, minuscule, inquiet, magique, brillant'),
            ('Émotions', 'paniqué, surpris, découragé, soulagé, heureux, fier'),
            ('Marqueurs de relation', 'soudain, ensuite, quelques minutes plus tard, pendant ce temps, finalement')]
    c0 = 190; rh = 66
    s = f"<rect x='1' y='1' width='{W-2}' height='{38+rh*len(rows)}' fill='#fff' stroke='{INK}' stroke-width='2'/>"
    s += f"<rect x='1' y='1' width='{W-2}' height='38' fill='{GRIS}' stroke='{INK}' stroke-width='2'/>"
    s += txt(c0 / 2, 27, 'Catégorie', 17, 'middle', True) + txt(c0 + (W - c0) / 2, 27, 'Exemples', 17, 'middle', True)
    y = 39
    for cat, ex in rows:
        s += f"<line x1='1' y1='{y}' x2='{W-1}' y2='{y}' stroke='{INK}' stroke-width='1.4'/>"
        s += txt(16, y + rh / 2 + 6, cat, 15, gras=True)
        # retour à la ligne des exemples
        mots, cur, out = ex.split(' '), '', []
        for m in mots:
            e = (cur + ' ' + m).strip()
            if larg(e, 15) > W - c0 - 30 and cur: out.append(cur); cur = m
            else: cur = e
        out.append(cur)
        y0 = y + rh / 2 + 6 - (len(out) - 1) * 10
        for k, l in enumerate(out):
            s += txt(c0 + 14, y0 + k * 20, l, 15)
        y += rh
    s += f"<line x1='{c0}' y1='1' x2='{c0}' y2='{y}' stroke='{INK}' stroke-width='1.4'/>"
    save('banque', y + 2, s)


def page_lignee(n=24, pas=31):
    save('lignes', n * pas + 4, lignes(0, 0, W, n, pas))


if __name__ == '__main__':
    plans(); choix(); banque(); page_lignee()


def lettre():
    """La lettre du chef des lutins, encadrée, en KG Perfect Penmanship."""
    paras = ['Chers élèves,',
             'J’ai besoin de votre aide!',
             'Une terrible catastrophe vient de se produire au village des lutins. Les préparatifs de Noël sont complètement bouleversés et nous avons très peu de temps pour régler la situation.',
             'J’ai entendu dire que vous étiez de bons écrivains et que vous aviez beaucoup d’imagination. Je vous confie donc une mission très importante : inventer une histoire pour raconter cette catastrophe et expliquer comment les lutins réussiront à sauver Noël!',
             'Attention, votre histoire devra avoir un début, un milieu et une fin.',
             'J’ai confiance en vous!']
    fs, lh, x0, maxw = 19, 30, 44, W - 88
    s, y = '', 70
    for p in paras:
        cur, out = '', []
        for m in p.split(' '):
            e = (cur + ' ' + m).strip()
            if larg(e, fs) > maxw and cur: out.append(cur); cur = m
            else: cur = e
        out.append(cur)
        for l in out:
            s += txt(x0, y, l, fs); y += lh
        y += 14
    s += txt(W - x0, y + 10, 'Le chef des lutins', 22, 'end', gras=True)
    h = y + 50
    cadre = (f"<rect x='3' y='3' width='{W-6}' height='{h-6}' rx='22' fill='#fff' stroke='{INK}' stroke-width='3'/>"
             f"<rect x='14' y='14' width='{W-28}' height='{h-28}' rx='14' fill='none' stroke='{GRIS}' stroke-width='3'/>")
    save('lettre', h, cadre + s)


if __name__ == '__main__':
    lettre()


def zone(nom, titre, n, pas=34):
    """Une consigne courte suivie de n lignes pleines."""
    save(nom, 30 + n * pas + 4, txt(0, 20, titre, 17, gras=True) + lignes(0, 26, W, n, pas))


def relis():
    """Liste de vérification de l'élève (une case à cocher par énoncé)."""
    items = ['J’ai donné un titre à mon histoire.',
             'J’ai présenté mes personnages et le lieu.',
             'J’ai expliqué clairement la catastrophe.',
             'J’ai écrit au moins deux péripéties.',
             'J’ai expliqué comment le problème est réglé.',
             'J’ai organisé mon histoire en paragraphes.',
             'J’ai utilisé des marqueurs de relation.',
             'Mes phrases commencent par une majuscule et se terminent par une ponctuation.',
             'J’ai vérifié les accords dans mes groupes du nom.',
             'J’ai vérifié les accords entre le sujet et le verbe.',
             'J’ai vérifié l’orthographe des mots.']
    pas, y0 = 50, 22
    s = ''
    for i, t in enumerate(items):
        y = y0 + i * pas
        if i % 2 == 0:
            s += f"<rect x='12' y='{y-4}' width='{W-24}' height='{pas}' rx='8' fill='{GRIS_P}'/>"
        s += f"<rect x='28' y='{y+8}' width='24' height='24' rx='3' fill='#fff' stroke='{INK}' stroke-width='2'/>"
        s += txt(68, y + 28, t, 17)
    h = y0 + len(items) * pas + 14
    cadre = f"<rect x='1.5' y='1.5' width='{W-3}' height='{h-3}' rx='16' fill='none' stroke='{INK}' stroke-width='2.4'/>"
    save('relis', h, cadre + s)


def titre():
    s = txt(0, 26, 'Titre :', 20, gras=True)
    s += f"<line x1='{larg('Titre :', 20) + 12}' y1='30' x2='{W}' y2='30' stroke='{INK}' stroke-width='1.6'/>"
    save('titre', 38, s)


if __name__ == '__main__':
    zone('mission-mots', 'Ma mission, dans mes mots :', 3)
    zone('choix-pourquoi', 'J’ai choisi cette catastrophe parce que…', 3)
    zone('mes-mots', 'Mes mots à moi :', 5)
    relis(); titre()
