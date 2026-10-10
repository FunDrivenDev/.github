#!/usr/bin/env python3
"""Draw the org profile images: the XP window banner (light and dark), the start button and the FDD avatar.

Run `just images` after an edit here; it rewrites assets/*.svg, logos/fdd.svg and logos/fdd.png.
"""
import html, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

FR = dict(crust='#232634', mantle='#292c3c', base='#303446', s0='#414559', s1='#51576d', s2='#626880',
          o0='#737994', o1='#838ba7', o2='#949cbb', sub0='#a5adce', sub1='#b5bfe2', text='#c6d0f5',
          mauve='#ca9ee6', blue='#8caaee', green='#a6d189', yellow='#e5c890', peach='#ef9f76', red='#e78284',
          teal='#81c8be', pink='#f4b8e4', sky='#99d1db', lavender='#babbf1')


LA = dict(crust='#dce0e8', mantle='#e6e9ef', base='#eff1f5', s0='#ccd0da', s1='#bcc0cc', s2='#acb0be',
          o0='#9ca0b0', o1='#8c8fa1', o2='#7c7f93', sub0='#6c6f85', sub1='#5c5f77', text='#4c4f69',
          mauve='#8839ef', blue='#1e66f5', green='#40a02b', yellow='#df8e1d', peach='#fe640b', red='#d20f39',
          teal='#179299', pink='#ea76cb', sky='#04a5e5', lavender='#7287fd')


SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


XPF = "Tahoma, Verdana, 'Segoe UI', Geneva, sans-serif"


FONTS = f".t{{font-family:{SANS}}}.m{{font-family:{MONO}}}.x{{font-family:{XPF}}}"


RM = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


FLAG = ['#ff5b24', '#7fca22', '#20a4f3', '#ffc21c']


def n(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def svg(w, h, title, defs, css, body, extra_rm=''):
    t = html.escape(title)
    rm = RM if not extra_rm else RM[:-1] + extra_rm + '}'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{t}"><title>{t}</title><defs>{defs}</defs>'
            f'<style>{FONTS}{css}{rm}</style>{body}</svg>\n')


def pane(x, y, w, h, c, a):
    return (f'<path d="M{n(x)} {n(y)}Q{n(x+w/2)} {n(y-a)} {n(x+w)} {n(y)}L{n(x+w)} {n(y+h)}'
            f'Q{n(x+w/2)} {n(y+h-a)} {n(x)} {n(y+h)}Z" fill="{c}"/>')


def flag(x, y, s, g, a):
    d = s * .06
    return (pane(x, y, s, s, FLAG[0], a) + pane(x+s+g, y-d, s, s, FLAG[1], a) +
            pane(x, y+s+g, s, s, FLAG[2], a) + pane(x+s+g, y+s+g-d, s, s, FLAG[3], a))


def banner_d(p, dark):
    body = p['base'] if dark else '#ffffff'
    status = p['mantle'] if dark else '#f4f4f0'
    defs = ('<linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3cb4f7"/>'
            '<stop offset=".55" stop-color="#20a4f3"/><stop offset="1" stop-color="#1689d4"/></linearGradient>'
            '<filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feGaussianBlur stdDeviation="5"/></filter>')
    css = ('.wv{transform-box:fill-box;transform-origin:left center;animation:wv 4.5s ease-in-out infinite}'
           '@keyframes wv{0%,100%{transform:skewY(0)}50%{transform:skewY(-3deg)}}'
           '.bl{animation:bl 1.1s steps(1) infinite}@keyframes bl{50%{opacity:0}}')
    b = [f'<rect x="14" y="16" width="972" height="232" rx="10" fill="#000" opacity="{".45" if dark else ".18"}" filter="url(#sh)"/>',
         f'<rect x="8" y="8" width="984" height="236" rx="10" fill="{body}" stroke="#1689d4" stroke-width="2"/>',
         '<path d="M8 18a10 10 0 0 1 10-10h964a10 10 0 0 1 10 10v26H8Z" fill="url(#tb)"/>',
         '<rect x="18" y="10" width="964" height="2" rx="1" fill="#fff" opacity=".35"/>',
         flag(20, 18, 7, 2, 1.5),
         f'<text class="x" x="44" y="31" font-size="15" font-weight="700" fill="#fff">FunDrivenDev</text>']
    for i, kind in enumerate(('min', 'max', 'close')):
        x = 902 + i * 28
        fill = '#ff5b24' if kind == 'close' else 'rgba(255,255,255,.18)'
        b.append(f'<rect x="{x}" y="14" width="24" height="22" rx="4" fill="{fill}" stroke="#fff" stroke-opacity=".8"/>')
        g = {'min': f'<path d="M{x+7} 29h10"/>', 'max': f'<rect x="{x+7}" y="19" width="10" height="10" fill="none"/>',
             'close': f'<path d="M{x+7.5} 20.5l9 9m0-9l-9 9"/>'}[kind]
        b.append(f'<g stroke="#fff" stroke-width="2.2" stroke-linecap="round">{g}</g>')
    b.append(f'<g class="wv">{flag(60, 78, 52, 8, 9)}</g>')
    b.append(f'<text class="x" x="214" y="124" font-size="44" font-weight="700" fill="{p["text"]}">FunDrivenDev</text>')
    b.append(f'<text class="x" x="216" y="160" font-size="18" fill="{p["sub1"]}">A one-person workshop with a night shift of agents.</text>')
    b.append(f'<text class="x" x="216" y="190" font-size="15" font-style="italic" fill="{p["o2"]}">Fun to use, seriously built software.'
             f'</text><rect class="bl" x="470" y="178" width="2" height="15" fill="{p["o2"]}"/>')
    b.append(f'<path d="M10 214h980v20a10 10 0 0 1-10 10H20a10 10 0 0 1-10-10Z" fill="{status}"/>')
    b.append(f'<line x1="10" y1="214" x2="990" y2="214" stroke="{p["s0"] if dark else "#d6d3c8"}"/>')
    b.append(f'<text class="x" x="24" y="234" font-size="12" fill="{p["sub0"]}">Nantes, France</text>')
    b.append(f'<text class="x" x="976" y="234" font-size="12" text-anchor="end" fill="{p["sub0"]}">289 PRs merged in ~3 weeks</text>')
    return svg(1000, 256, 'FunDrivenDev window: a one-person workshop with a night shift of agents', defs, css, ''.join(b))


def start_button():
    defs = ('<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#96dd45"/>'
            '<stop offset=".5" stop-color="#7fca22"/><stop offset="1" stop-color="#5c9e14"/></linearGradient>')
    defs += ('<linearGradient id="tk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a7af0"/>'
             '<stop offset=".12" stop-color="#2e6be6"/><stop offset="1" stop-color="#2457cf"/></linearGradient>')
    b = ['<path d="M80 0H228A4 4 0 0 1 232 4V40A4 4 0 0 1 228 44H80Z" fill="url(#tk)"/>',
         '<path d="M80 1H228" stroke="#6aa0ff"/>',
         '<path d="M4 0H90A22 22 0 0 1 90 44H4A4 4 0 0 1 0 40V4A4 4 0 0 1 4 0Z" fill="url(#g)"/>',
         '<path d="M6 2H88A20 20 0 0 1 106 12H6Z" fill="#fff" opacity=".22"/>',
         flag(14, 13, 8, 2, 1.5),
         '<text class="x" x="45" y="30" font-size="20" font-weight="700" font-style="italic" fill="#000" opacity=".28">start</text>',
         '<text class="x" x="44" y="29" font-size="20" font-weight="700" font-style="italic" fill="#fff">start</text>',
         '<text class="x" x="128" y="27" font-size="13" fill="#fff">fundriven.dev</text>']
    return svg(232, 44, 'start: fundriven.dev', defs, '', ''.join(b))


def fdd_paths(x0, y, h, wf, wd, gap, r, mid=.5, fbar=.82):
    """Centerlines of F, D, D starting at x0, cap height h; r is the D bowl radius."""
    f = f'M{n(x0)} {n(y+h)}V{n(y)}H{n(x0+wf)}M{n(x0)} {n(y+h*mid)}H{n(x0+wf*fbar)}'

    def d(x):
        return (f'M{n(x)} {n(y)}H{n(x+wd-r)}A{n(r)} {n(r)} 0 0 1 {n(x+wd)} {n(y+r)}V{n(y+h-r)}'
                f'A{n(r)} {n(r)} 0 0 1 {n(x+wd-r)} {n(y+h)}H{n(x)}Z')
    x1 = x0 + wf + gap
    x2 = x1 + wd + gap
    return f, d(x1), d(x2), (x0, x1, x2)


def fdd_width(wf, wd, gap):
    return wf + gap + wd + gap + wd


BLISS = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1957cf"/>'
         '<stop offset=".55" stop-color="#4b95ec"/><stop offset="1" stop-color="#a8d4fa"/></linearGradient>'
         '<linearGradient id="hill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7cc63a"/>'
         '<stop offset="1" stop-color="#2f7d10"/></linearGradient>'
         '<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>')


def bliss(hill_y=388):
    return ('<rect width="512" height="512" fill="url(#sky)"/>'
            '<g fill="#fff" opacity=".55" filter="url(#soft)"><ellipse cx="120" cy="92" rx="70" ry="16"/>'
            '<ellipse cx="380" cy="70" rx="90" ry="18"/><ellipse cx="420" cy="150" rx="50" ry="10"/></g>'
            f'<path d="M0 {hill_y+18}C110 {hill_y-40} 300 {hill_y-34} 512 {hill_y+6}V512H0Z" fill="url(#hill)"/>'
            f'<path d="M0 {hill_y+18}C110 {hill_y-40} 300 {hill_y-34} 512 {hill_y+6}" fill="none" stroke="#c4ef7e" stroke-width="3" opacity=".7"/>')


APPLE = ('M0-14C-8-22-26-20-28-2C-30 16-16 34-8 34C-3 34-2 31 0 31C2 31 3 34 8 34'
         'C16 34 30 16 28-2C26-20 8-22 0-14Z')


def apple(x, y, s):
    """A plain white apple, the fruit: whole, with its stem and a leaf (no bite)."""
    return (f'<g transform="translate({n(x)} {n(y)}) scale({n(s)})">'
            f'<path d="{APPLE}" fill="#0a3a96" opacity=".35" transform="translate(2 3)"/>'
            f'<path d="{APPLE}" fill="#fff"/>'
            '<path d="M0-14C0-21 2-27 6-31" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>'
            '<path d="M3-24C8-34 18-35 22-31C17-24 9-22 3-24Z" fill="#fff"/></g>')


def logo_xp_fdd():
    wf, wd, gap, h = 62, 80, 56, 112
    x0 = 256 - fdd_width(wf, wd, gap) / 2 + 2
    f, d1, d2, _ = fdd_paths(x0, 176, h, wf, wd, gap, 40)
    letters = f + d1 + d2
    sh = '<filter id="ds" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4"/></filter>'
    return svg(512, 512, 'FunDrivenDev logo: FDD on an XP hillside', BLISS + sh, '',
               bliss() +
               '<g transform="skewX(-9) translate(40 0)" fill="none" stroke-linecap="square" stroke-linejoin="round">'
               f'<path d="{letters}" stroke="#0a3a96" stroke-width="30" opacity=".55" transform="translate(5 8)" filter="url(#ds)"/>'
               f'<path d="{letters}" stroke="#fff" stroke-width="30"/></g>'
               + apple(256, 420, 1.05))

def main():
    out = {'assets/window-dark.svg': banner_d(FR, True), 'assets/window-light.svg': banner_d(LA, False),
           'assets/start.svg': start_button(), 'logos/fdd.svg': logo_xp_fdd()}
    for path, text in out.items():
        (ROOT / path).write_text(text)


if __name__ == '__main__':
    main()
