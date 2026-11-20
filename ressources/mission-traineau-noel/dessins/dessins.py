"""Dessins au trait de Mission traîneau (style maison : encre #1E1E1E, fond blanc)."""
import cairosvg, random
INK='#1E1E1E'
def svg(vb,w,h,body,sw=4):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w}" height="{h}">'
            f'<g stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" fill="none">{body}</g></svg>')
def save(name,s):
    open(name+'.svg','w').write(s); cairosvg.svg2png(bytestring=s.encode(),write_to=name+'.png')

def sled(x,y,k=1.0,a=0,gifts=0,sw=4):
    """Traîneau vu de côté, tourné vers la droite; (x,y) = bas arrière du patin."""
    b=''
    for i in range(gifts):
        b+=gift(8+i*19,-30,13,sw)
    b+=(f'<path d="M8 -14 H60 L66 -34 H2 Z" fill="#fff" stroke-width="{sw}"/>'
       f'<path d="M16 -14 V-2 M52 -14 V-2" stroke-width="{sw}"/>'
       f'<path d="M-4 -2 Q-6 2 0 2 H70 C84 2 88 -12 80 -20 C76 -24 70 -20 74 -16" stroke-width="{sw*1.3}"/>')
    return f'<g transform="translate({x} {y}) rotate({a}) scale({k})">{b}</g>'
def gift(x,y,s,sw=3):
    d=s*0.35
    return (f'<path d="M{x} {y} V{y-s} H{x+s} V{y} Z" fill="#fff" stroke-width="{sw}"/>'
            f'<path d="M{x} {y-s} L{x+d} {y-s-d} H{x+s+d} L{x+s} {y-s} Z" fill="#fff" stroke-width="{sw}"/>'
            f'<path d="M{x+s+d} {y-s-d} V{y-d} L{x+s} {y}" fill="#fff" stroke-width="{sw}"/>'
            f'<path d="M{x+s/2} {y} V{y-s} L{x+s/2+d} {y-s-d}" stroke-width="{sw*0.8}"/>')

# --- Les 3 surfaces ---
def sheet(extra):
    return f'<rect x="20" y="20" width="200" height="140" rx="10" fill="#fff" stroke-width="5"/>{extra}'
random.seed(4)
alu=('<path d="M190 20 V56 H220" fill="#fff"/><path d="M190 20 L220 56"/>'
     '<path d="M50 130 L110 50 M75 135 L125 70 M140 140 L175 95" stroke-width="5"/>'
     '<path d="M40 60 l14 -14 M160 60 l10 -10" stroke-width="3"/>')
save('aluminium',svg('0 0 240 180',720,540,sheet(alu)))
fel=''.join(f'<path d="M{x} {y} q4 -6 8 0" stroke-width="2.5"/>' for x in range(40,200,20) for y in range(48,150,18) if (x//20+y//18)%2==0)
fel+='<rect x="32" y="32" width="176" height="116" rx="6" stroke-dasharray="8 8" stroke-width="3"/>'
save('feutrine',svg('0 0 240 180',720,540,sheet(fel)))
sab=''.join(f'<circle cx="{random.randint(32,208)}" cy="{random.randint(32,148)}" r="{random.choice([1.2,1.6,2.0])}" fill="{INK}" stroke="none"/>' for _ in range(380))
save('papier-sable',svg('0 0 240 180',720,540,sheet(sab)))

# --- Le montage : rampe sur des livres, zone d'arrivée ---
def books(x,y,n=3):
    s=''
    for i in range(n):
        yy=y-28*(i+1); dx=[0,5,-3][i%3]
        s+=f'<rect x="{x+dx}" y="{yy}" width="70" height="28" rx="4" fill="#fff"/><path d="M{x+dx+10} {yy+14} H{x+dx+44}" stroke-width="3"/>'
    return s
GROUND=200
RX0,RY0,RX1=40,GROUND-84,250   # haut de la rampe (sur les livres) et bas
def ramp(strip=True,start=True):
    s=books(26,GROUND)
    s+=f'<path d="M{RX0-10} {RY0-4} L{RX1} {GROUND-2} L{RX1} {GROUND+8} L{RX0-10} {RY0+8} Z" fill="#fff"/>'
    if strip:
        s+=f'<path d="M{RX0+40} {RY0+16} L{RX1-30} {GROUND-12}" stroke-width="9" stroke="#9a9a9a"/>'
        s+=f'<path d="M{RX0+36} {RY0+8} l-3 12 M{RX1-26} {GROUND-20} l-3 12" stroke-width="3"/>'
    if start:
        s+=f'<path d="M{RX0+34} {RY0+10} l-22 -34" stroke-width="3" stroke-dasharray="5 5"/>'
    return s
floor=f'<path d="M0 {GROUND+8} H560" stroke-width="4"/>'
def ruler(x0,x1,y):
    s=f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="26" rx="3" fill="#fff"/>'
    for i,x in enumerate(range(x0+8,x1-4,12)):
        s+=f'<path d="M{x} {y} v{14 if i%5==0 else 8}" stroke-width="2.5"/>'
    return s
# Étape 1 : je prépare la rampe (bande de matériau fixée avec du ruban)
save('etape1-rampe',svg('0 40 320 200',640,400,floor+ramp()+
    ''))
# Étape 2 : je laisse glisser le traîneau (sans pousser)
import math
ang=math.degrees(math.atan2(GROUND-RY0,RX1-RX0))
save('etape2-glisser',svg('0 40 320 200',640,400,floor+ramp(strip=True)+sled(RX0+38,RY0+6,0.9,ang)+
    f'<path d="M150 110 Q190 120 215 150 M203 149 l12 1 l-2 -12" stroke-width="4"/>'))
# Étape 3 : j'observe la distance (de la fin de la rampe à l'avant du traîneau)
save('etape3-distance',svg('0 40 560 230',1120,460,floor+ramp(strip=True,start=False)+sled(400,GROUND,0.9)+
    ruler(RX1,500,GROUND+20)+f'<path d="M{RX1} {GROUND+56} H476 M{RX1+10} {GROUND+48} l-10 8 l10 8 M466 {GROUND+48} l10 8 l-10 8" stroke-width="3.5"/>'))
# Schéma complet du montage (guide)
save('montage',svg('0 20 600 260',1200,520,
    '<path d="M0 208 H600"/>'+ramp()+sled(RX0+38,RY0+6,0.9,ang)+ruler(RX1,560,GROUND+22)+
    f'<path d="M{RX1} {GROUND-6} V{GROUND+60}" stroke-dasharray="6 6" stroke-width="3"/>'))
# Pictogrammes
save('traineau',svg('-12 -44 104 52',520,260,sled(0,0,1,sw=3)))
save('traineau-cadeaux',svg('-12 -54 104 62',520,310,sled(0,0,1,0,3,sw=3)))
save('cadeau',svg('0 -30 30 32',300,320,gift(4,0,18,1.8)))
save('traineau-glisse',svg('-60 -44 160 52',800,260,sled(0,0,1,0,0,sw=3)+
    '<path d="M-50 -22 H-14 M-44 -8 H-10 M-56 -34 H-24" stroke-width="3"/>'))
save('drapeau-depart',svg('0 0 80 100',320,400,'<path d="M20 92 V10" stroke-width="5"/><path d="M20 12 H64 L54 28 L64 44 H20" fill="#fff" stroke-width="5"/>'))
print('ok')

# Schéma annoté du montage (guide de l'enseignant)
def label(x,y,t,anchor='start'):
    return f'<text x="{x}" y="{y}" font-family="Inter" font-size="15" fill="{INK}" stroke="none" text-anchor="{anchor}">{t}</text>'
def lead(x1,y1,x2,y2):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke-width="1.6"/><circle cx="{x2}" cy="{y2}" r="2.5" fill="{INK}" stroke="none"/>'
body=('<path d="M0 208 H640"/>'+ramp()+sled(RX0+38,RY0+6,0.9,ang)+sled(430,GROUND,0.9)+
      f'<path d="M{RX1} {GROUND-30} V{GROUND+64}" stroke-dasharray="6 6" stroke-width="2.5"/>'+
      f'<path d="M507 {GROUND-30} V{GROUND+64}" stroke-dasharray="6 6" stroke-width="2.5"/>'+
      f'<path d="M{RX1+4} {GROUND+50} H503 M{RX1+14} {GROUND+42} l-10 8 l10 8 M493 {GROUND+42} l10 8 l-10 8" stroke-width="3"/>'+
      label(378,GROUND+78,'Distance mesurée (cm)','middle')+
      label(4,38,'Ligne de départ')+lead(60,42,RX0+30,RY0-12)+
      label(150,60,'Traîneau')+lead(175,64,RX0+80,RY0+6)+
      label(4,GROUND+40,'Support (livres)')+lead(40,GROUND+26,40,GROUND-20)+
      label(255,96,'Rampe d’environ 30 cm')+lead(300,100,190,GROUND-30)+
      label(250,150,'Surface testée')+lead(280,154,215,GROUND-14)+
      label(232,GROUND+100,'Fin de la rampe','middle')+
      label(470,120,'Zone d’arrivée plane')+lead(520,124,560,GROUND+6)+
      label(540,GROUND+100,'Avant du traîneau','middle'))
save('montage-annote',svg('0 20 640 300',1280,600,body))
