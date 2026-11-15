"""Illustrations originales pour Mission glaçon (trait encre, couleurs douces)."""
import math, os
import cairosvg

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'png')
os.makedirs(OUT, exist_ok=True)
INK = '#1E1E1E'
ICE = '#D3ECF8'
ICE2 = '#8FCBE8'
RED = '#E0484B'
WHITE = '#FFFFFF'


def flake(cx, cy, r, sw=3):
    s = ''
    for k in range(6):
        a = math.radians(k * 60)
        x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
        s += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}"/>'
        for t in (0.55,):
            bx, by = cx + r * t * math.cos(a), cy + r * t * math.sin(a)
            for d in (-40, 40):
                b = a + math.radians(d)
                s += f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx + r*0.32*math.cos(b):.1f}" y2="{by + r*0.32*math.sin(b):.1f}"/>'
    return f'<g stroke="{INK}" stroke-width="{sw}" stroke-linecap="round" fill="none">{s}</g>'


def glacon(col=True):
    ice = ICE if col else WHITE
    ice2 = ICE2 if col else '#EDEDED'
    red = RED if col else WHITE
    blush = '#F7B6CD' if col else WHITE
    return f'''
<g stroke="{INK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">
  <!-- flaque -->
  <ellipse cx="200" cy="352" rx="120" ry="16" fill="{ice2}"/>
  <!-- cube : faces -->
  <path d="M110 150 L150 118 L310 118 L270 150 Z" fill="{WHITE}"/>
  <path d="M270 150 L310 118 L310 298 L270 334 Z" fill="{ice2}"/>
  <path d="M110 150 H270 V334 Q248 346 236 334 Q226 350 206 336 Q184 352 168 336 Q150 350 132 336 Q118 344 110 334 Z" fill="{ice}"/>
  <!-- reflets -->
  <path d="M128 172 V230" fill="none" stroke="{WHITE}" stroke-width="9"/>
  <path d="M128 248 V262" fill="none" stroke="{WHITE}" stroke-width="9"/>
  <!-- goutte -->
  <path d="M292 330 Q302 346 292 352 Q282 346 292 330 Z" fill="{ice}"/>
  <!-- visage -->
  <circle cx="162" cy="236" r="9" fill="{INK}" stroke="none"/>
  <circle cx="218" cy="236" r="9" fill="{INK}" stroke="none"/>
  <circle cx="165" cy="232" r="3" fill="{WHITE}" stroke="none"/>
  <circle cx="221" cy="232" r="3" fill="{WHITE}" stroke="none"/>
  <ellipse cx="146" cy="262" rx="12" ry="7" fill="{blush}" stroke="none"/>
  <ellipse cx="234" cy="262" rx="12" ry="7" fill="{blush}" stroke="none"/>
  <path d="M176 262 Q190 278 204 262" fill="none"/>
  <!-- tuque -->
  <path d="M120 128 Q150 40 236 30 Q300 26 318 74 Q290 58 262 70 Q290 92 286 120 Z" fill="{red}"/>
  <rect x="104" y="112" width="200" height="34" rx="17" fill="{WHITE}"/>
  <circle cx="320" cy="82" r="20" fill="{WHITE}"/>
</g>'''


def svg(body, w=400, h=380):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w*3}" height="{h*3}">{body}</svg>'


def couverture(col=True):
    body = glacon(col)
    body += flake(52, 92, 30) + flake(356, 210, 24) + flake(40, 262, 18) + flake(366, 330, 14)
    return svg(body, 400, 380)


def thermometre(col=True):
    red = RED if col else '#9A9A9A'
    return svg(f'''
<g stroke="{INK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">
  <path d="M84 40 A20 20 0 0 1 124 40 V170 A36 36 0 1 1 84 170 Z" fill="{WHITE}"/>
  <path d="M104 100 V196" stroke="{red}" stroke-width="14"/>
  <circle cx="104" cy="200" r="22" fill="{red}"/>
  <path d="M124 60 H138 M124 84 H138 M124 108 H138 M124 132 H138" fill="none"/>
</g>''', 210, 250)


def verre(col=True):
    ice = ICE if col else WHITE
    return svg(f'''
<g stroke="{INK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">
  <path d="M40 40 H180 L164 230 Q162 240 152 240 H68 Q58 240 56 230 Z" fill="{WHITE}"/>
  <path d="M58 170 H162 L156 230 Q155 236 148 236 H72 Q65 236 64 230 Z" fill="{ice}"/>
  <path d="M86 116 L130 106 L140 148 L96 158 Z" fill="{ice}"/>
  <path d="M60 80 H80 M62 110 H80 M64 140 H80" fill="none"/>
</g>''', 220, 270)


def cadeau(col=True):
    red = RED if col else WHITE
    grn = '#7CC078' if col else WHITE
    return svg(f'''
<g stroke="{INK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">
  <rect x="30" y="100" width="180" height="130" rx="6" fill="{grn}"/>
  <rect x="20" y="74" width="200" height="34" rx="6" fill="{grn}"/>
  <path d="M106 74 V230 M134 74 V230" fill="none"/>
  <rect x="106" y="74" width="28" height="156" fill="{red}"/>
  <path d="M120 74 Q70 20 66 52 Q66 74 120 74 Q174 74 174 52 Q170 20 120 74 Z" fill="{red}"/>
</g>''', 240, 250)


if __name__ == '__main__':
    for name, fn in [('glacon', couverture), ('thermometre', thermometre), ('verre', verre), ('cadeau', cadeau)]:
        for col in (True, False):
            s = fn(col)
            suf = '' if col else '-nb'
            open(f'{OUT}/{name}{suf}.svg', 'w').write(s)
            cairosvg.svg2png(bytestring=s.encode(), write_to=f'{OUT}/{name}{suf}.png')
    from PIL import Image
    ims = [Image.open(f'{OUT}/{n}.png').convert('RGBA') for n in ['glacon', 'thermometre', 'verre', 'cadeau']]
    W = sum(i.width for i in ims) + 40
    H = max(i.height for i in ims)
    m = Image.new('RGB', (W, H), 'white')
    x = 0
    for i in ims:
        m.paste(i, (x, 0), i); x += i.width + 10
    m.thumbnail((1400, 1400))
    m.save(f'{OUT}/_planche.png')
    print('ok')
