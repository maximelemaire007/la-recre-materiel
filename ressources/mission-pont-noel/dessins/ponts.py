import cairosvg
INK='#1E1E1E'
DX,DY=56,-34
TOP=110
def books(x0):
    s=''
    for i,(y,dx,w) in enumerate([(TOP,0,96),(TOP+28,6,88),(TOP+56,-2,100)]):
        x=x0+dx
        s+=f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="4" fill="#fff"/>'
        s+=f'<path d="M{x+10} {y+14} H{x+w-30}" fill="none" stroke-width="3"/>'
    return s
L,R=40,330
W=R-L
def sheet(y0=TOP, depth=1.0):
    return f'<path d="M{L} {y0} H{R} L{R+DX*depth} {y0+DY*depth} H{L+DX*depth} Z" fill="#fff"/>'
def flat():
    return sheet()
def edges():
    h=16
    s=f'<path d="M{L+DX} {TOP+DY} H{R+DX} V{TOP+DY-h} H{L+DX} Z" fill="#fff"/>'  # back lip
    s+=sheet()
    s+=f'<path d="M{L} {TOP} H{R} V{TOP-h} H{L} Z" fill="#fff"/>'  # front lip
    s+=f'<path d="M{L} {TOP-h} L{L+DX} {TOP+DY-h} M{R} {TOP-h} L{R+DX} {TOP+DY-h}" fill="none" stroke-width="2.5"/>'
    return s
def accordion():
    n=6; amp=22
    pts=[(L+DX*k/n, TOP+DY*k/n-(amp if k%2 else 0)) for k in range(n+1)]
    s='<path d="M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)+' L'+' L'.join(f'{x+W:.1f} {y:.1f}' for x,y in reversed(pts))+' Z" fill="#fff"/>'
    s+='<path d="M'+' L'.join(f'{x+W:.1f} {y:.1f}' for x,y in pts)+'" fill="none"/>'
    for x,y in pts[1:-1]:
        s+=f'<path d="M{x:.1f} {y:.1f} H{x+W:.1f}" fill="none" stroke-width="3"/>'
    return s
def svg(paper):
    body=books(L-56)+books(R-40)+paper()
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-30 40 440 160" width="1320" height="480"><g stroke="{INK}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round">{body}</g></svg>'
for name,f in [('plat',flat),('bords-releves',edges),('accordeon',accordion)]:
    s=svg(f); open(name+'.svg','w').write(s)
    cairosvg.svg2png(bytestring=s.encode(),write_to=name+'.png')
from PIL import Image
ims=[Image.open(n+'.png').convert('RGBA') for n in ['plat','bords-releves','accordeon']]
m=Image.new('RGB',(ims[0].width,sum(i.height for i in ims)+40),'white'); y=0
for i in ims: m.paste(i,(0,y),i); y+=i.height+20
m.save('_planche.png')
