#!/usr/bin/env python3
"""Generate FunDrivenDev org-profile README proposals, SVG assets, logos and preview.html."""
import base64, html, re, pathlib

# Writes every proposal under design/out/ (ignored); preview.html is copied to design/ by hand.
OUT = pathlib.Path(__file__).resolve().parent / 'out'

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
SPARK = "M0-10C1-3 3-1 10 0C3 1 1 3 0 10C-1 3-3 1-10 0C-3-1-1-3 0-10Z"
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


def spark(x, y, s, c, cls='', style=''):
    return (f'<g transform="translate({n(x)} {n(y)}) scale({n(s)})"><path d="{SPARK}" fill="{c}"'
            + (f' class="{cls}"' if cls else '') + (f' style="{style}"' if style else '') + '/></g>')


# ---------------------------------------------------------------- A: night shift
def banner_a(p, dark):
    top, bot = (p['crust'], p['base']) if dark else ('#dfe3ee', p['base'])
    star = p['text'] if dark else p['o0']
    stars = [(40, 30, 1.4), (150, 58, 1), (260, 24, 1.2), (380, 46, .9), (470, 20, 1.5), (560, 56, 1),
             (650, 110, 1.3), (690, 36, 1), (760, 84, 1.6), (850, 26, 1.1), (930, 64, 1), (990, 122, 1.2),
             (1172, 150, 1.1), (1040, 30, .9), (1180, 40, 1), (612, 26, 1)]
    defs = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bot}"/></linearGradient>'
            f'<linearGradient id="cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p["yellow"]}" stop-opacity="{".42" if dark else ".5"}"/>'
            f'<stop offset="1" stop-color="{p["yellow"]}" stop-opacity="0"/></linearGradient>'
            '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>'
            '<mask id="moon"><rect x="1060" y="20" width="100" height="100" fill="#fff"/>'
            '<circle cx="1124" cy="54" r="27" fill="#000"/></mask>')
    css = ('.tw{animation:tw 4s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.9}50%{opacity:.2}}'
           '.sp{transform-box:fill-box;transform-origin:center;opacity:.9;animation:sp 6s ease-in-out infinite}'
           '@keyframes sp{0%{transform:translate(0,16px) scale(.3) rotate(0);opacity:0}25%{opacity:1}'
           '75%{opacity:.85}100%{transform:translate(-8px,-48px) scale(1) rotate(90deg);opacity:0}}'
           '.ln{transform-box:fill-box;transform-origin:left center;animation:ln 7s steps(9,end) infinite}'
           '@keyframes ln{0%{transform:scaleX(0)}25%,100%{transform:scaleX(1)}}'
           '.bu{animation:bu 3s ease-in-out infinite}@keyframes bu{0%,100%{opacity:1}50%{opacity:.75}}'
           '.st{animation:st 3.5s ease-in-out infinite;opacity:.6}'
           '@keyframes st{0%{transform:translateY(4px);opacity:0}40%{opacity:.7}100%{transform:translateY(-10px);opacity:0}}')
    b = [f'<rect width="1200" height="300" rx="16" fill="url(#sky)"/>']
    b += [f'<circle class="tw" style="animation-delay:-{(i*0.7) % 4:.1f}s" cx="{x}" cy="{y}" r="{r}" fill="{star}"/>'
          for i, (x, y, r) in enumerate(stars)]
    b.append(f'<circle cx="1110" cy="64" r="30" fill="{p["yellow"]}" mask="url(#moon)"/>')
    # title block
    b.append(f'<text class="t" x="64" y="150" font-size="64" font-weight="800" letter-spacing="-1.5" fill="{p["text"]}">'
             f'<tspan fill="{p["mauve"]}">Fun</tspan>DrivenDev</text>')
    b.append(f'<text class="t" x="66" y="194" font-size="22" fill="{p["sub1"]}">A one-person workshop with a night shift of agents.</text>')
    b.append(f'<text class="m" x="66" y="238" font-size="15" fill="{p["o2"]}">Nantes, France · fundriven.dev · @rlvdx</text>')
    # desk scene
    b.append(f'<polygon points="816,190 860,182 1012,264 790,264" fill="url(#cone)"/>')
    b.append(f'<rect x="660" y="264" width="520" height="4" rx="2" fill="{p["s1"]}"/>')
    b.append(f'<ellipse cx="740" cy="261" rx="30" ry="6" fill="{p["s2"]}"/>')
    b.append(f'<polyline points="740,258 762,196 812,166" fill="none" stroke="{p["s2"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(f'<circle cx="762" cy="196" r="5" fill="{p["s2"]}"/>')
    b.append(f'<path d="M796 156L842 146L860 182L816 190Z" fill="{p["peach"]}"/>')
    b.append(f'<circle class="bu" cx="838" cy="186" r="6" fill="{p["yellow"]}"/>')
    b.append(f'<rect x="905" y="172" width="140" height="80" rx="8" fill="{p["blue"]}" opacity="{".35" if dark else ".25"}" filter="url(#blur)"/>')
    b.append(f'<rect x="900" y="168" width="150" height="90" rx="7" fill="{p["mantle"] if dark else "#ffffff"}" stroke="{p["s2"]}" stroke-width="3"/>')
    for i, (w, c) in enumerate([(70, 'mauve'), (104, 'blue'), (56, 'green'), (90, 'peach'), (38, 'text')]):
        x0 = 914 + (14 if i in (1, 2, 3) else 0)
        b.append(f'<rect class="ln" style="animation-delay:-{n(i*1.3)}s" x="{x0}" y="{182 + i*14}" width="{w}" height="6" rx="3" fill="{p[c]}"/>')
    b.append(f'<path d="M884 258H1066L1078 266H872Z" fill="{p["s2"]}"/>')
    b.append(f'<rect x="1100" y="238" width="24" height="26" rx="4" fill="{p["mauve"]}"/>')
    b.append(f'<path d="M1124 244h4a6 6 0 0 1 0 12h-4" fill="none" stroke="{p["mauve"]}" stroke-width="3"/>')
    for i, x in enumerate((1107, 1116)):
        b.append(f'<path class="st" style="animation-delay:-{n(i*1.6)}s" d="M{x} 230q-5-6 0-12q5-6 0-12" fill="none" stroke="{p["o1"]}" stroke-width="2" stroke-linecap="round"/>')
    sparks = [(930, 150, .9, 'mauve'), (985, 136, 1.2, 'yellow'), (1040, 152, .8, 'teal'),
              (960, 118, .7, 'pink'), (1015, 108, 1, 'blue'), (880, 168, .7, 'green')]
    for i, (x, y, s, c) in enumerate(sparks):
        b.append(spark(x, y, s, p[c], 'sp', f'animation-delay:-{i}s'))
    return svg(1200, 300, 'FunDrivenDev: a one-person workshop with a night shift of agents', defs, css, ''.join(b))


# ---------------------------------------------------------------- B: terminal
def banner_b(p, dark):
    body = p['base'] if dark else p['base']
    bar = p['mantle'] if dark else p['crust']
    D = 16
    W = 238
    css = [f'.cv{{opacity:0;animation:cv {D}s linear infinite}}'
           '@keyframes cv{0%,4%{transform:translateX(0);opacity:1;animation-timing-function:steps(22,end)}'
           f'18%{{transform:translateX({W}px);opacity:1}}23%,100%{{transform:translateX({W}px);opacity:0}}}}'
           '.bl{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}'
           f'.l0{{animation:l0 {D}s linear infinite}}@keyframes l0{{0%,94%{{opacity:1}}98%,100%{{opacity:0}}}}']
    times = [22, 28, 34, 40, 46, 52, 58]
    for i, t in enumerate(times, 1):
        css.append(f'.l{i}{{animation:l{i} {D}s linear infinite}}'
                   f'@keyframes l{i}{{0%,{t}%{{opacity:0}}{t+1}%,94%{{opacity:1}}98%,100%{{opacity:0}}}}')
    x0, y0, lh = 56, 98, 34
    b = [f'<rect x="20" y="16" width="1160" height="348" rx="12" fill="{body}" stroke="{p["s0"] if dark else p["s1"]}"/>',
         f'<path d="M20 28a12 12 0 0 1 12-12h1136a12 12 0 0 1 12 12v28H20Z" fill="{bar}"/>']
    for i, c in enumerate(('red', 'yellow', 'green')):
        b.append(f'<circle cx="{46 + i*22}" cy="36" r="7" fill="{p[c]}"/>')
    b.append(f'<text class="m" x="600" y="41" font-size="14" text-anchor="middle" fill="{p["o1"]}">rlvdx@workshop: ~/fundrivendev</text>')
    fs = 'font-size="18"'
    b.append(f'<g class="l0"><text class="m" {fs} x="{x0}" y="{y0}" fill="{p["green"]}">$</text>'
             f'<text class="m" {fs} x="80" y="{y0}" fill="{p["text"]}">claude --afk <tspan fill="{p["yellow"]}">"ship it"</tspan></text></g>')
    b.append(f'<g class="cv"><rect x="78" y="{y0-20}" width="{W+16}" height="28" fill="{body}"/>'
             f'<rect x="80" y="{y0-17}" width="10" height="22" fill="{p["text"]}"/></g>')
    rows = [
        ('◆', 'mauve', None, None, 'night shift on duty: agents picked up the backlog', 'sub1'),
        ('✓', 'green', 'claude-plugins', 'blue', 'handover · session-panel', 'sub0'),
        ('✓', 'green', 'homebrew-tap', 'blue', 'brew install fundrivendev/tap/memo', 'sub0'),
        ('✓', 'green', 'everything-as-code', 'blue', 'DNS · the org itself · servers · dotfiles', 'sub0'),
        ('✓', 'green', 'merged', 'blue', '289 PRs in ~3 weeks, many while you slept', 'sub0'),
        ('☾', 'yellow', None, None, 'see you in the morning, Raphaël.', 'yellow'),
    ]
    for i, (sym, sc, name, nc, txt, tc) in enumerate(rows, 1):
        y = y0 + lh * i
        g = [f'<text class="m" {fs} x="80" y="{y}" fill="{p[sc]}">{sym}</text>']
        if name:
            g.append(f'<text class="m" {fs} x="108" y="{y}" fill="{p[nc]}">{name}</text>')
            g.append(f'<text class="m" {fs} x="330" y="{y}" fill="{p[tc]}">{html.escape(txt)}</text>')
        else:
            g.append(f'<text class="m" {fs} x="108" y="{y}" fill="{p[tc]}">{html.escape(txt)}</text>')
        b.append(f'<g class="l{i}">' + ''.join(g) + '</g>')
    y = y0 + lh * 7
    b.append(f'<g class="l7"><text class="m" {fs} x="{x0}" y="{y}" fill="{p["green"]}">$</text>'
             f'<rect class="bl" x="80" y="{y-17}" width="10" height="22" fill="{p["text"]}"/></g>')
    return svg(1200, 380, 'Terminal: claude --afk "ship it", a night shift at FunDrivenDev, 289 PRs merged', '', ''.join(css), ''.join(b))


# ---------------------------------------------------------------- C: assembly line
def banner_c(p, dark):
    panel = p['mantle'] if dark else p['base']
    card = p['s0'] if dark else '#ffffff'
    D, travel, x_start, cw = 10.0, 1060, 40, 70
    stations = [('Detective', 260, 'blue'), ('Architect', 450, 'mauve'), ('Worker', 640, 'peach'), ('Judge', 830, 'green')]
    css = [f'.cd{{animation:mv {D:g}s linear infinite}}'
           f'@keyframes mv{{0%{{transform:translateX(0);opacity:0}}3%,96%{{opacity:1}}100%{{transform:translateX({travel}px);opacity:0}}}}'
           f'.is{{animation:is {D:g}s linear infinite}}@keyframes is{{0%,78%{{opacity:1}}80%,100%{{opacity:0}}}}'
           f'.mg{{opacity:0;animation:mg {D:g}s linear infinite}}@keyframes mg{{0%,78%{{opacity:0}}80%,100%{{opacity:1}}}}'
           '.bt{animation:bt .226s linear infinite}@keyframes bt{to{stroke-dashoffset:-24}}'
           '.lp{opacity:.3;animation:lp 2s ease-out infinite}@keyframes lp{0%{opacity:1}35%,100%{opacity:.3}}']
    rm_static = [0, 190, 380, 570, 940]
    extra = ''.join(f'.k{k} .cd{{transform:translateX({x}px)}}' for k, x in enumerate(rm_static))
    extra += '.k4 .mg{opacity:1}.k4 .is{opacity:0}'
    b = [f'<rect width="1200" height="290" rx="16" fill="{panel}"/>',
         f'<text class="t" x="32" y="54" font-size="30" font-weight="800" letter-spacing="-.5" fill="{p["text"]}">'
         f'<tspan fill="{p["mauve"]}">Fun</tspan>DrivenDev</text>',
         f'<text class="m" x="1168" y="52" font-size="15" text-anchor="end" fill="{p["o1"]}">the orchestrator is never an LLM</text>']
    for idx, (name, xs, c) in enumerate(stations):
        t_s = (xs - cw/2 - x_start) / travel * D
        delay = (t_s % 2) - 2
        b.append(f'<rect x="{xs-75}" y="92" width="150" height="58" rx="10" fill="{card}" stroke="{p["s1"]}"/>')
        b.append(f'<text class="m" x="{xs-62}" y="110" font-size="11" fill="{p["o1"]}">0{idx+1}</text>')
        b.append(f'<circle class="lp" style="animation-delay:{delay:.2f}s" cx="{xs+60}" cy="106" r="5" fill="{p[c]}"/>')
        b.append(f'<text class="t" x="{xs}" y="131" font-size="17" font-weight="600" text-anchor="middle" fill="{p["text"]}">{name}</text>')
        b.append(f'<path d="M{xs-10} 151L{xs+10} 151L{xs} 162Z" fill="{p["s1"]}"/>')
    b.append(f'<rect x="24" y="206" width="1120" height="20" rx="10" fill="{p["s0"]}" stroke="{p["s1"]}"/>')
    b.append(f'<line class="bt" x1="40" y1="216" x2="1128" y2="216" stroke="{p["s2"]}" stroke-width="3" stroke-dasharray="10 14"/>')
    for cx in (34, 1134):
        b.append(f'<circle cx="{cx}" cy="216" r="13" fill="{p["s1"]}" stroke="{p["s2"]}" stroke-width="2"/>')
    nums = [214, 237, 251, 268, 289]
    on_mauve = p['crust'] if dark else '#ffffff'
    for k, num in enumerate(nums):
        st = f'animation-delay:-{2*k}s'
        b.append(
            f'<g class="k{k}" transform="translate({x_start} 174)"><g class="cd" style="{st}">'
            f'<g class="is" style="{st}"><rect width="{cw}" height="30" rx="7" fill="{card}" stroke="{p["s2"]}"/>'
            f'<circle cx="16" cy="15" r="7" fill="none" stroke="{p["green"]}" stroke-width="2"/><circle cx="16" cy="15" r="2" fill="{p["green"]}"/>'
            f'<text class="m" x="29" y="20" font-size="13" fill="{p["text"]}">#{num}</text></g>'
            f'<g class="mg" style="{st}"><rect width="{cw}" height="30" rx="7" fill="{p["mauve"]}"/>'
            f'<g fill="none" stroke="{on_mauve}" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="8.5" r="2.5"/><circle cx="12" cy="21.5" r="2.5"/>'
            f'<circle cx="23" cy="17" r="2.5"/><path d="M12 11v8M12 11c0 4 3 6 8.5 6"/></g>'
            f'<text class="m" x="30" y="20" font-size="13" font-weight="700" fill="{on_mauve}">#{num}</text></g>'
            f'</g></g>')
    b.append(f'<text class="m" x="32" y="262" font-size="14" fill="{p["o1"]}">issues in →</text>')
    b.append(f'<text class="m" x="600" y="262" font-size="14" text-anchor="middle" fill="{p["sub0"]}">deterministic line · Claude Code at every station</text>')
    b.append(f'<text class="m" x="1168" y="262" font-size="14" text-anchor="end" fill="{p["o1"]}">→ merged PRs out</text>')
    return svg(1200, 290, 'Assembly line: issues travel through Detective, Architect, Worker and Judge and come out as merged PRs',
               '', ''.join(css), ''.join(b), extra)


# ---------------------------------------------------------------- D: XP light
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
    b.append(f'<text class="x" x="216" y="190" font-size="15" font-style="italic" fill="{p["o2"]}">Built for fun, kept for good.'
             f'</text><rect class="bl" x="424" y="178" width="2" height="15" fill="{p["o2"]}"/>')
    b.append(f'<path d="M10 214h980v20a10 10 0 0 1-10 10H20a10 10 0 0 1-10-10Z" fill="{status}"/>')
    b.append(f'<line x1="10" y1="214" x2="990" y2="214" stroke="{p["s0"] if dark else "#d6d3c8"}"/>')
    b.append(f'<text class="x" x="24" y="234" font-size="12" fill="{p["sub0"]}">Nantes, France</text>')
    b.append(f'<text class="x" x="976" y="234" font-size="12" text-anchor="end" fill="{p["sub0"]}">289 PRs merged in ~3 weeks</text>')
    return svg(1000, 256, 'FunDrivenDev window: a one-person workshop with a night shift of agents', defs, css, ''.join(b))


def start_button():
    defs = ('<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#96dd45"/>'
            '<stop offset=".5" stop-color="#7fca22"/><stop offset="1" stop-color="#5c9e14"/></linearGradient>')
    b = ['<path d="M4 0H210A22 22 0 0 1 210 44H4A4 4 0 0 1 0 40V4A4 4 0 0 1 4 0Z" fill="url(#g)"/>',
         '<path d="M6 2H208A20 20 0 0 1 226 12H6Z" fill="#fff" opacity=".22"/>',
         flag(14, 13, 8, 2, 1.5),
         '<text class="x" x="45" y="30" font-size="20" font-weight="700" font-style="italic" fill="#000" opacity=".28">start</text>',
         '<text class="x" x="44" y="29" font-size="20" font-weight="700" font-style="italic" fill="#fff">start</text>',
         '<line x1="104" y1="10" x2="104" y2="34" stroke="#fff" stroke-opacity=".45"/>',
         '<text class="x" x="114" y="27" font-size="13" fill="#fff">fundriven.dev</text>']
    return svg(232, 44, 'start: fundriven.dev', defs, '', ''.join(b))


# ---------------------------------------------------------------- logos
def logo_fd():
    p = FR
    return svg(512, 512, 'FunDrivenDev logo: fd spark', '', '',
               f'<rect width="512" height="512" fill="{p["base"]}"/>'
               f'<g fill="none" stroke-width="46" stroke-linecap="round" stroke-linejoin="round" transform="translate(-14 6)">'
               f'<path d="M178 392V214a72 72 0 0 1 72-72h12" stroke="{p["mauve"]}"/>'
               f'<path d="M126 252H232" stroke="{p["mauve"]}"/>'
               f'<circle cx="324" cy="326" r="66" stroke="{p["blue"]}"/>'
               f'<path d="M390 160V392" stroke="{p["blue"]}"/></g>'
               + spark(400, 98, 3.3, p['yellow']))


def logo_moon():
    p = FR
    return svg(512, 512, 'FunDrivenDev logo: night-shift moon',
               '<mask id="m"><rect width="512" height="512" fill="#fff"/><circle cx="306" cy="212" r="128" fill="#000"/></mask>', '',
               f'<rect width="512" height="512" fill="{p["crust"]}"/>'
               f'<circle cx="236" cy="262" r="150" fill="{p["yellow"]}" mask="url(#m)"/>'
               + spark(318, 222, 5.4, p['mauve']) +
               f'<rect x="290" y="292" width="54" height="16" rx="5" fill="{p["green"]}"/>'
               f'<circle cx="392" cy="128" r="8" fill="{p["text"]}"/><circle cx="420" cy="326" r="6" fill="{p["text"]}" opacity=".7"/>'
               f'<circle cx="118" cy="120" r="5" fill="{p["text"]}" opacity=".6"/>')


def logo_line():
    p = FR
    return svg(512, 512, 'FunDrivenDev logo: line of stations ending in a merge', '', '',
               f'<rect width="512" height="512" fill="{p["base"]}"/>'
               f'<path d="M100 256H330" stroke="{p["s2"]}" stroke-width="22" stroke-linecap="round"/>'
               f'<circle cx="100" cy="256" r="28" fill="{p["blue"]}"/><circle cx="180" cy="256" r="28" fill="{p["teal"]}"/>'
               f'<circle cx="260" cy="256" r="28" fill="{p["yellow"]}"/>'
               f'<circle cx="384" cy="256" r="82" fill="{p["mauve"]}"/>'
               f'<g fill="none" stroke="{p["crust"]}" stroke-width="16" stroke-linecap="round">'
               f'<circle cx="360" cy="214" r="13"/><circle cx="360" cy="298" r="13"/><circle cx="414" cy="268" r="13"/>'
               f'<path d="M360 228v56M360 230c0 22 14 38 40 38"/></g>')


def logo_xp():
    mask = ('<mask id="f"><rect width="512" height="512" fill="#fff"/>'
            '<g fill="none" stroke="#000" stroke-width="40" stroke-linecap="round">'
            '<path d="M226 440V236a74 74 0 0 1 74-74h40"/><path d="M164 272H300"/></g></mask>')
    return svg(512, 512, 'FunDrivenDev logo: XP flag remix', mask, '',
               '<rect width="512" height="512" fill="#ffffff"/>'
               f'<g mask="url(#f)">{flag(110, 118, 140, 8, 16)}</g>')


# ---------------------------------------------------------------- READMEs
GH = 'https://github.com/FunDrivenDev'
STACK = 'Rust · Go · TypeScript/Deno · Svelte 5 · Tauri 2 · Python · Terraform · Ansible · mise · just · Claude Code'


def picture(dark, light, alt, extra='width="100%"'):
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="../assets/{dark}">\n'
            f'  <img alt="{alt}" src="../assets/{light}" {extra}>\n</picture>')


README_A = f'''<p align="center">
{picture("banner-dark.svg", "banner-light.svg", "FunDrivenDev: a one-person workshop with a night shift of agents")}
</p>

I'm **Raphaël** ([@rlvdx](https://github.com/rlvdx)), a DevOps/back-end dev in Nantes, France, by day at Guest Suite. I care about two things and refuse to pick one: **happy users** and **calm developers**.

This org is where the things I build with Claude Code grow up and go public. One human on the day shift, agents on the night shift.

### Agent tooling that keeps sessions in their smart zone

**[claude-plugins]({GH}/claude-plugins)** is my Claude Code plugin marketplace. `handover` passes a session to a fresh one before its context fills up, instead of auto-compacting it. `session-panel` comes along too.

```text
/plugin marketplace add FunDrivenDev/claude-plugins
```

<details>
<summary>Still in the workshop</summary>

- **defactory**: a predictable line around non-deterministic workers. Claude Code sessions work the Stations (Detective, Architect, Worker, Judge…), deterministic Rust code runs the line, because *the orchestrator is never an LLM*.
- **wesh**: a macOS pro tool to steer several Claude Code sessions at once against Linear issues.
- **fundrivenOS**: how we work, as Markdown for agents.
- **linear-triage-bench**: LLM triage of issues, benchmarked. Models judged by models.

</details>

### Small keyboard-driven macOS apps, one stack

**MOSST** stands for macOS, Svelte, Tauri. The apps ship as the "Fun Driven Stuff" casks of **[homebrew-tap]({GH}/homebrew-tap)**, and **memo**, a reader for the plans, handoffs and reports Claude Code writes, is on tap:

```sh
brew install fundrivendev/tap/memo
```

<details>
<summary>Still in the workshop</summary>

- **wipinpeace**: *WIP in peace*. Four priority topics, one per slot, each with its issues, PRs, notes and Claude sessions.
- **okarina**: a zoomable canvas for vision, strategy, OKRs and metrics, linked to Linear and assisted by Claude.
- **focustube**: YouTube, filtered into a learning-oriented feed.
- **mosst-template**: the starting point of every MOSST app.

</details>

### Everything as code

DNS (Terraform on Cloudflare), this GitHub org itself (Terraform), the VPS (Ansible) and my dotfiles (chezmoi). Even the shop window: **[fundriven.dev](https://fundriven.dev)** is a Windows XP-style desktop, *FunDriven XP: eXtra Puns*, with zero dependencies.

---

<p align="center">
<b>289 PRs merged in ~3 weeks, many while I slept.</b><br>
Built for fun, kept for good.
</p>

<p align="center"><sub>{STACK}<br>Catppuccin Frappé, everywhere</sub></p>
'''

README_B = f'''<p align="center">
{picture("terminal-dark.svg", "terminal-light.svg", "Terminal: claude --afk ship it. Agents on the night shift, 289 PRs merged in about 3 weeks, see you in the morning.")}
</p>

**FunDrivenDev** is a one-person workshop with a night shift of agents. I'm [Raphaël](https://github.com/rlvdx), a DevOps/back-end dev in Nantes, France (day job at Guest Suite), and I refuse to pick between happy users and calm developers. What I build with Claude Code grows up here, then goes public.

| | Project | What it does |
|:-:|---|---|
| ● | [**claude-plugins**]({GH}/claude-plugins) | Claude Code plugins: `handover` (a fresh session before the context fills up, no auto-compaction) and `session-panel` |
| ● | [**homebrew-tap**]({GH}/homebrew-tap) | Casks for the Fun Driven Stuff apps: `brew install fundrivendev/tap/memo` |
| ○ | **memo** | Keyboard-driven macOS reader for the plans, handoffs and reports Claude Code writes |
| ○ | **wipinpeace** | WIP in peace: four priority topics, one per slot, with their issues, PRs, notes and sessions |
| ○ | **okarina** | Zoomable canvas for vision, strategy, OKRs and metrics, linked to Linear |
| ○ | **focustube** | YouTube, filtered into a learning-oriented feed |
| ○ | **mosst-template** | The starting point of every MOSST app (macOS, Svelte, Tauri) |
| ○ | **defactory** | Rust: a predictable line around non-deterministic workers; the orchestrator is never an LLM |
| ○ | **wesh** | Steer several Claude Code sessions at once against Linear issues |
| ○ | **fundrivenOS** | How we work, as Markdown for agents |
| ○ | **linear-triage-bench** | LLM issue triage, benchmarked: models judged by models |
| ○ | **everything as code** | Terraform for DNS and this org, Ansible for the VPS, chezmoi for dotfiles |

<sub>● public &nbsp; ○ in the workshop, out when it's ready</sub>

Also on the desk: [fundriven.dev](https://fundriven.dev), my site, a Windows XP-style desktop (*FunDriven XP: eXtra Puns*) with zero dependencies.

**289 PRs merged in ~3 weeks, many while I slept.** Built for fun, kept for good.

`Rust` `Go` `TypeScript/Deno` `Svelte 5` `Tauri 2` `Python` `Terraform` `Ansible` `mise` `just` `Claude Code` <sub>· Catppuccin Frappé</sub>
'''

README_C = f'''<p align="center">
{picture("line-dark.svg", "line-light.svg", "Assembly line: issue cards pass Detective, Architect, Worker and Judge and come out as merged PRs")}
</p>

<p align="center"><b>A one-person workshop with a night shift of agents.</b><br>
Issues go in, merged PRs come out: 289 in ~3 weeks, many while I slept.</p>

I'm [Raphaël](https://github.com/rlvdx), DevOps/back-end dev in Nantes, France (day job at Guest Suite). I care about two things and refuse to pick one: happy users and calm developers. This is where what I build with Claude Code grows up and goes public.

<table>
<tr>
<th width="33%">Agent tooling</th>
<th width="33%">macOS apps (MOSST)</th>
<th width="33%">Everything as code</th>
</tr>
<tr valign="top">
<td>

- [**claude-plugins**]({GH}/claude-plugins): `handover`, `session-panel`
- **defactory**: the line above. Stations worked by Claude Code, run by plain Rust
- **wesh**: steer several Claude Code sessions against Linear issues
- **fundrivenOS**: how we work, as Markdown for agents
- **linear-triage-bench**: models triage, models judge

</td>
<td>

- [**homebrew-tap**]({GH}/homebrew-tap): the Fun Driven Stuff casks
- **memo**: reader for Claude Code's plans, handoffs, reports
- **wipinpeace**: WIP in peace, four slots
- **okarina**: vision to metrics, on one zoomable canvas
- **focustube**: YouTube, for learning
- **mosst-template**: where every app starts

</td>
<td>

- DNS on Cloudflare, with Terraform
- This GitHub org, with Terraform
- The VPS, with Ansible
- Dotfiles, with chezmoi
- [**fundriven.dev**](https://fundriven.dev): FunDriven XP, eXtra Puns

</td>
</tr>
</table>

<sub>Linked means public. The rest is still on the line.</sub>

```sh
# in Claude Code
/plugin marketplace add FunDrivenDev/claude-plugins
# in a terminal
brew install fundrivendev/tap/memo
```

<p align="center">Built for fun, kept for good.<br><sub>{STACK} · Catppuccin Frappé</sub></p>
'''

README_D = f'''<p align="center">
{picture("window-dark.svg", "window-light.svg", "FunDrivenDev: a one-person workshop with a night shift of agents")}
</p>

Hi, I'm [Raphaël](https://github.com/rlvdx), a DevOps/back-end dev in Nantes, France (day job at Guest Suite). I care about happy users and calm developers, and refuse to pick one. FunDrivenDev is where what I build with Claude Code grows up and goes public.

#### Agent tooling

[**claude-plugins**]({GH}/claude-plugins): `handover` (hands a session to a fresh one before its context fills up) and `session-panel`, for Claude Code. `/plugin marketplace add FunDrivenDev/claude-plugins`

#### macOS apps on MOSST (macOS, Svelte, Tauri)

[**homebrew-tap**]({GH}/homebrew-tap): the Fun Driven Stuff casks. `brew install fundrivendev/tap/memo`

#### Everything as code

DNS and this org with Terraform, the VPS with Ansible, dotfiles with chezmoi.

<details>
<summary>Still in the workshop</summary>

- **memo**: keyboard-driven reader for the plans, handoffs and reports Claude Code writes
- **wipinpeace**: WIP in peace, four priority topics, one per slot
- **okarina**: zoomable canvas for vision, strategy, OKRs and metrics, linked to Linear
- **focustube**: YouTube, filtered into a learning-oriented feed
- **mosst-template**: the starting point of every MOSST app
- **defactory**: a predictable line around non-deterministic workers, in Rust
- **wesh**: steer several Claude Code sessions at once against Linear issues
- **fundrivenOS**: how we work, as Markdown for agents
- **linear-triage-bench**: LLM issue triage, models judged by models

</details>

<p align="center">
<a href="https://fundriven.dev"><img src="../assets/start.svg" alt="start: open fundriven.dev" height="44"></a><br>
<sub>Boots <a href="https://fundriven.dev">fundriven.dev</a>: FunDriven XP, eXtra Puns. Zero dependencies.</sub>
</p>

<p align="center"><sub>289 PRs merged in ~3 weeks, many while I slept. Built for fun, kept for good.<br>{STACK}</sub></p>
'''

VERSIONS = {
    'a': dict(name='A · Night shift', readme=README_A,
              desc='Lead option. A quiet night workshop: moon, desk lamp over a laptop that types by itself, agent sparks drifting up. Three themed sections; private projects folded into "Still in the workshop".',
              assets={'banner-dark.svg': banner_a(FR, True), 'banner-light.svg': banner_a(LA, False)}),
    'b': dict(name='B · Terminal', readme=README_B,
              desc='An animated terminal types claude --afk "ship it" and plays a short night-shift log. Below, one compact table of every project, public or still in the workshop.',
              assets={'terminal-dark.svg': banner_b(FR, True), 'terminal-light.svg': banner_b(LA, False)}),
    'c': dict(name='C · Assembly line', readme=README_C,
              desc='Issue cards ride a conveyor through Detective, Architect, Worker and Judge and leave as merged PRs. Then a three-column table: Agent tooling | macOS apps | Everything as code.',
              assets={'line-dark.svg': banner_c(FR, True), 'line-light.svg': banner_c(LA, False)}),
    'd': dict(name='D · XP light', readme=README_D,
              desc='A light nod to fundriven.dev: one XP-style window card in the four flag colors, a waving flag, and a start button that opens the site. Everything else stays plain.',
              assets={'window-dark.svg': banner_d(FR, True), 'window-light.svg': banner_d(LA, False), 'start.svg': start_button()}),
}

LOGOS = [
    ('fd-spark', '1 · fd spark', 'An f and d drawn with one round stroke weight in mauve and blue, with a yellow four-point spark on the d. Frappé base square, safe inside a circle crop.', logo_fd()),
    ('night-shift-moon', '2 · Night-shift moon', 'A yellow crescent holding a mauve spark and a green prompt cursor: the agent working while the moon is up. Pairs with version A.', logo_moon()),
    ('line', '3 · Line', 'Three station dots on a track running into a mauve merge disc. Pairs with version C.', logo_line()),
    ('xp-flag', '4 · XP flag remix', 'The four wavy panes of the fundriven.dev flag with a white "f" cut through them. Pairs with version D and the site desktop.', logo_xp()),
]


# ---------------------------------------------------------------- tiny markdown renderer (subset used above)
def inline(s):
    codes = []

    def keep(m):
        codes.append(html.escape(m.group(1)))
        return f'\x00{len(codes)-1}\x00'
    s = re.sub(r'`([^`]+)`', keep, s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])', r'<em>\1</em>', s)
    return re.sub(r'\x00(\d+)\x00', lambda m: f'<code>{codes[int(m.group(1))]}</code>', s)


def md(text):
    lines, out, i = text.split('\n'), [], 0
    starts = ('#', '- ', '|', '```', '<p', '<pic', '<det', '<tab', '<tr', '<td', '<th', '> ')
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1
            continue
        if l.startswith('```'):
            j, buf = i + 1, []
            while not lines[j].startswith('```'):
                buf.append(lines[j]); j += 1
            out.append('<pre><code>' + html.escape('\n'.join(buf)) + '</code></pre>')
            i = j + 1
        elif re.match(r'</?(p|picture|details|summary|table|tr|td|th|div)[\s>]', l):
            buf = []
            while i < len(lines) and lines[i].strip():
                buf.append(lines[i]); i += 1
            out.append('\n'.join(buf))
        elif m := re.match(r'(#{1,6}) (.*)', l):
            k = len(m.group(1))
            out.append(f'<h{k}>{inline(m.group(2))}</h{k}>'); i += 1
        elif l.strip() == '---':
            out.append('<hr>'); i += 1
        elif l.startswith('- '):
            items = []
            while i < len(lines) and (lines[i].startswith('- ') or (lines[i].startswith('  ') and items)):
                if lines[i].startswith('- '):
                    items.append(lines[i][2:])
                else:
                    items[-1] += ' ' + lines[i].strip()
                i += 1
            out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>')
        elif l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            al = ['center' if c.startswith(':') and c.endswith(':') else '' for c in rows[1]]

            def cell(tag, c, a):
                return f'<{tag}' + (f' align="{a}"' if a else '') + f'>{inline(c)}</{tag}>'
            h = '<tr>' + ''.join(cell('th', c, al[k]) for k, c in enumerate(rows[0])) + '</tr>'
            body = ''.join('<tr>' + ''.join(cell('td', c, al[k]) for k, c in enumerate(r)) + '</tr>' for r in rows[2:])
            out.append(f'<table><thead>{h}</thead><tbody>{body}</tbody></table>')
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(starts):
                buf.append(lines[i]); i += 1
            out.append('<p>' + inline('\n'.join(buf)) + '</p>')
    return '\n'.join(out)


def data_uri(svg_text):
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg_text.encode()).decode()


def render_for_preview(readme, assets):
    h = md(readme)

    def pic(m):
        dark, attrs = m.group(1), m.group(2)
        dattrs = re.sub(r'src="[^"]+"', f'src="{dark}"', attrs)
        return f'<img class="pv pv-dark" {dattrs}><img class="pv pv-light" {attrs}>'
    h = re.sub(r'<picture>\s*<source media="\(prefers-color-scheme: dark\)" srcset="([^"]+)">\s*<img ([^>]*)>\s*</picture>', pic, h)
    return re.sub(r'="\.\./assets/([^"]+)"', lambda m: f'="{data_uri(assets[m.group(1)])}"', h)


# ---------------------------------------------------------------- preview page
CSS = r'''
:root{--bg:#f3f4f7;--surface:#ffffff;--fg:#1f2330;--muted:#5c6170;--border:#dde1e8;--accent:#8839ef;--focus:#1e66f5;--chip:#eceef3}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#232634;--surface:#292c3c;--fg:#c6d0f5;--muted:#a5adce;--border:#414559;--accent:#ca9ee6;--focus:#8caaee;--chip:#303446}}
:root[data-theme="dark"]{--bg:#232634;--surface:#292c3c;--fg:#c6d0f5;--muted:#a5adce;--border:#414559;--accent:#ca9ee6;--focus:#8caaee;--chip:#303446}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--fg)}
body{font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;overflow-x:hidden}
.wrap{max-width:1120px;margin:0 auto;padding:24px 16px 64px}
.top h1{font-size:22px;margin:0 0 4px;letter-spacing:-.2px}
.top p{margin:0 0 18px;color:var(--muted);max-width:70ch}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px}
.tabs button,.seg button,.copy{font:inherit;font-size:13.5px;color:var(--fg);background:var(--chip);border:1px solid var(--border);border-radius:999px;padding:6px 14px;cursor:pointer}
.tabs button[aria-selected="true"]{background:var(--accent);border-color:var(--accent);color:var(--surface);font-weight:600}
.seg{display:inline-flex;border:1px solid var(--border);border-radius:999px;padding:2px;background:var(--chip)}
.seg button{border:0;background:transparent;padding:4px 12px}
.seg button[aria-pressed="true"]{background:var(--surface);box-shadow:0 0 0 1px var(--border);font-weight:600}
button:focus-visible,a:focus-visible,summary:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.vhead{display:flex;flex-wrap:wrap;gap:10px 20px;align-items:flex-end;justify-content:space-between;margin-bottom:12px}
.vhead h2{margin:0;font-size:18px}.vhead p{margin:2px 0 0;color:var(--muted);max-width:72ch;font-size:14px}
.mock{overflow-x:auto;border:1px solid var(--border);border-radius:12px;background:var(--surface)}
.src{margin-top:14px;border:1px solid var(--border);border-radius:10px;background:var(--surface)}
.src summary{cursor:pointer;padding:10px 14px;font-weight:600;font-size:14px}
.src .bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between;padding:0 14px 8px;color:var(--muted);font-size:12.5px}
.src pre{margin:0;padding:14px;overflow:auto;max-height:480px;font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;border-top:1px solid var(--border);white-space:pre}
/* GitHub mock */
.gh{--gbg:#0d1117;--gfg:#f0f6fc;--gmu:#9198a1;--gbo:#3d444d;--gln:#4493f8;--gcode:rgba(101,108,118,.2);--gsub:#151b23;color:var(--gfg);background:var(--gbg);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif;padding:24px;min-width:340px}
.gh.gh-light{--gbg:#ffffff;--gfg:#1f2328;--gmu:#59636e;--gbo:#d1d9e0;--gln:#0969da;--gcode:rgba(129,139,152,.12);--gsub:#f6f8fa}
.gh-dark .pv-light,.gh-light .pv-dark{display:none}
.gh a{color:var(--gln);text-decoration:none}.gh a:hover{text-decoration:underline}
.gh-org{display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.gh-ava{width:88px;height:88px;border-radius:8px;border:1px solid var(--gbo)}
.gh-name{font-size:24px;font-weight:600;margin:0;line-height:1.25}
.gh-login{color:var(--gmu);font-size:15px}
.gh-meta{display:flex;gap:14px;flex-wrap:wrap;color:var(--gmu);font-size:13px;margin-top:4px}
.gh-nav{display:flex;gap:4px;flex-wrap:wrap;border-bottom:1px solid var(--gbo);margin:18px -24px 24px;padding:0 24px;font-size:14px}
.gh-nav span{padding:8px 10px;color:var(--gfg)}
.gh-nav .on{border-bottom:2px solid #fd8c73;font-weight:600}
.gh-card{border:1px solid var(--gbo);border-radius:6px}
.gh-card-h{padding:8px 16px;font-size:12px;color:var(--gmu);font-family:ui-monospace,SFMono-Regular,Menlo,monospace;border-bottom:1px solid var(--gbo)}
.markdown-body{padding:24px;font-size:16px;line-height:1.5;word-wrap:break-word}
.markdown-body>*:first-child{margin-top:0}.markdown-body>*:last-child{margin-bottom:0}
.markdown-body p,.markdown-body ul,.markdown-body table,.markdown-body pre,.markdown-body details{margin:0 0 16px}
.markdown-body h1,.markdown-body h2,.markdown-body h3,.markdown-body h4{margin:24px 0 16px;font-weight:600;line-height:1.25}
.markdown-body h3{font-size:1.25em}.markdown-body h4{font-size:1em}
.markdown-body ul{padding-left:2em}.markdown-body li+li{margin-top:.25em}
.markdown-body img{max-width:100%;box-sizing:content-box;vertical-align:middle}
.markdown-body code{padding:.2em .4em;font-size:85%;background:var(--gcode);border-radius:6px;font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;white-space:break-spaces}
.markdown-body pre{padding:16px;overflow:auto;font-size:85%;line-height:1.45;background:var(--gsub);border-radius:6px}
.markdown-body pre code{padding:0;background:transparent;font-size:100%;white-space:pre}
.markdown-body hr{height:.25em;padding:0;margin:24px 0;background:var(--gbo);border:0}
.markdown-body table{border-collapse:collapse;display:block;width:max-content;max-width:100%;overflow:auto}
.markdown-body th,.markdown-body td{padding:6px 13px;border:1px solid var(--gbo)}
.markdown-body th{font-weight:600}
.markdown-body tr{background:var(--gbg);border-top:1px solid var(--gbo)}
.markdown-body tbody tr:nth-child(2n){background:var(--gsub)}
.markdown-body td>*:first-child{margin-top:0}.markdown-body td>*:last-child{margin-bottom:0}
.markdown-body summary{cursor:pointer}
.markdown-body sub{font-size:75%}
.gh-pinh{font-size:16px;font-weight:400;margin:24px 0 8px}
.gh-pins{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.gh-pin{border:1px solid var(--gbo);border-radius:6px;padding:16px;font-size:12px;color:var(--gmu)}
.gh-pin b{font-size:14px;color:var(--gln);font-weight:600}
.gh-pin .pub{border:1px solid var(--gbo);border-radius:2em;padding:0 7px;margin-left:6px;font-size:12px}
.gh-pin p{margin:8px 0 0}
/* logos */
.logo{display:grid;grid-template-columns:minmax(0,220px) minmax(0,1fr);gap:20px;align-items:start;padding:20px;border:1px solid var(--border);border-radius:12px;background:var(--surface);margin-bottom:16px}
.logo>img{width:100%;max-width:220px;height:auto;border-radius:14px;border:1px solid var(--border)}
.logo h3{margin:0 0 4px;font-size:17px}.logo p{margin:0 0 12px;color:var(--muted);font-size:14px}
.grounds{display:flex;flex-wrap:wrap;gap:10px}
.ground{border-radius:10px;padding:12px;display:flex;flex-direction:column;gap:8px;border:1px solid var(--border)}
.ground.lt{background:#ffffff;color:#59636e}.ground.dk{background:#0d1117;color:#9198a1}
.ground .lbl{font-size:11px;text-transform:uppercase;letter-spacing:.06em}
.ground .row{display:flex;align-items:center;gap:12px}
.c{border-radius:50%}.s{border-radius:12%}
.desk{border-radius:12px;overflow:hidden;border:1px solid var(--border);background:radial-gradient(120% 60% at 30% 110%,#7fca22 0 38%,transparent 39%),linear-gradient(#5aa9ec,#2f74d0);min-height:260px;position:relative;padding:18px 18px 60px}
.desk .icons{display:flex;flex-wrap:wrap;gap:18px 26px}
.dicon{width:86px;text-align:center;font:12px/1.3 Tahoma,Verdana,"Segoe UI",sans-serif;color:#fff}
.dicon img{width:48px;height:48px;display:block;margin:0 auto 6px;filter:drop-shadow(1px 2px 1px rgba(0,0,0,.35))}
.dicon span{padding:1px 3px;text-shadow:1px 1px 1px #000}
.dicon.sel img{filter:drop-shadow(1px 2px 1px rgba(0,0,0,.35)) brightness(.8) sepia(.3) hue-rotate(180deg)}
.dicon.sel span{background:#2b62c9;text-shadow:none;outline:1px dotted #fff}
.taskbar{position:absolute;left:0;right:0;bottom:0;height:40px;background:linear-gradient(#3a7af0,#2457cf);border-top:1px solid #6aa0ff;display:flex;align-items:center}
.taskbar img{height:40px;width:auto}
.note{color:var(--muted);font-size:13px;margin:6px 0 0}
@media (max-width:640px){.logo{grid-template-columns:1fr}.gh{padding:16px}.gh-nav{margin:14px -16px 18px;padding:0 16px}.markdown-body{padding:16px}}
@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}
'''

JS = r'''
(function(){
  var ids=['a','b','c','d','logos'];
  var tabs=[].slice.call(document.querySelectorAll('[role="tab"]'));
  function show(id,focus){
    if(ids.indexOf(id)<0) id='a';
    tabs.forEach(function(t){var on=t.dataset.id===id;t.setAttribute('aria-selected',on?'true':'false');t.tabIndex=on?0:-1;if(on&&focus)t.focus();});
    [].forEach.call(document.querySelectorAll('[role="tabpanel"]'),function(p){p.hidden=p.id!=='p-'+id;});
    try{localStorage.setItem('fdd-tab',id);}catch(e){}
    if(location.hash!=='#'+id){try{history.replaceState(null,'','#'+id);}catch(e){try{location.hash=id;}catch(_){}}}
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){show(t.dataset.id);});
    t.addEventListener('keydown',function(e){
      var k=e.key,j=-1;
      if(k==='ArrowRight')j=(i+1)%tabs.length; else if(k==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;
      else if(k==='Home')j=0; else if(k==='End')j=tabs.length-1;
      if(j>=0){e.preventDefault();show(tabs[j].dataset.id,true);}
    });
  });
  window.addEventListener('hashchange',function(){show(location.hash.slice(1));});
  var init=location.hash.slice(1);
  if(ids.indexOf(init)<0){try{init=localStorage.getItem('fdd-tab')||'a';}catch(e){init='a';}}
  show(init);
  [].forEach.call(document.querySelectorAll('.seg'),function(seg){
    var mock=document.getElementById(seg.dataset.target);
    [].forEach.call(seg.querySelectorAll('button'),function(b){
      b.addEventListener('click',function(){
        var dark=b.dataset.gh==='dark';
        mock.classList.toggle('gh-dark',dark);mock.classList.toggle('gh-light',!dark);
        [].forEach.call(seg.querySelectorAll('button'),function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});
      });
    });
  });
  [].forEach.call(document.querySelectorAll('.copy'),function(btn){
    btn.addEventListener('click',function(){
      var txt=document.getElementById(btn.dataset.src).textContent;
      var done=function(m){btn.textContent=m;setTimeout(function(){btn.textContent='Copy';},1800);};
      try{
        navigator.clipboard.writeText(txt).then(function(){done('Copied');}).catch(function(){done('Copy blocked: select the text');});
      }catch(e){done('Copy blocked: select the text');}
    });
  });
})();
'''


def esc(s):
    return html.escape(s, quote=True)


def build_preview():
    logo1 = data_uri(LOGOS[0][3])
    tab_btns = ''.join(
        f'<button role="tab" id="t-{k}" data-id="{k}" aria-controls="p-{k}">{esc(v["name"])}</button>' for k, v in VERSIONS.items())
    tab_btns += '<button role="tab" id="t-logos" data-id="logos" aria-controls="p-logos">Logos</button>'
    panels = []
    for k, v in VERSIONS.items():
        sizes = ', '.join(f'{name} ({len(s.encode())/1024:.1f} KB)' for name, s in v['assets'].items())
        body = render_for_preview(v['readme'], v['assets'])
        panels.append(f'''<section role="tabpanel" id="p-{k}" aria-labelledby="t-{k}" hidden>
<div class="vhead"><div><h2>{esc(v["name"])}</h2><p>{esc(v["desc"])}</p></div>
<div class="seg" role="group" aria-label="GitHub theme" data-target="gh-{k}"><button data-gh="light" aria-pressed="false">GitHub light</button><button data-gh="dark" aria-pressed="true">GitHub dark</button></div></div>
<div class="mock"><div class="gh gh-dark" id="gh-{k}">
<div class="gh-org"><img class="gh-ava" src="{logo1}" alt="FunDrivenDev avatar (logo 1)"><div><h3 class="gh-name">Fun driven dev</h3><div class="gh-login">FunDrivenDev</div>
<div class="gh-meta"><span>Nantes, France</span><a href="https://fundriven.dev">https://fundriven.dev</a></div></div></div>
<nav class="gh-nav" aria-label="Mock GitHub org tabs"><span class="on">Overview</span><span>Repositories</span><span>Projects</span><span>Packages</span><span>People</span></nav>
<div class="gh-card"><div class="gh-card-h">.github / profile / README.md</div><div class="markdown-body">
{body}
</div></div>
<h3 class="gh-pinh">Pinned</h3>
<div class="gh-pins">
<div class="gh-pin"><b>claude-plugins</b><span class="pub">Public</span><p>Claude Code plugin marketplace: handover, session-panel</p></div>
<div class="gh-pin"><b>homebrew-tap</b><span class="pub">Public</span><p>Casks for the Fun Driven Stuff apps</p></div>
</div>
</div></div>
<details class="src"><summary>README.md source</summary>
<div class="bar"><span>versions/{k}/profile/README.md · assets: {esc(sizes)}</span><button class="copy" data-src="src-{k}">Copy</button></div>
<pre id="src-{k}">{esc(v["readme"])}</pre></details>
</section>''')
    # logos
    items = []
    for slug, title, desc, s in LOGOS:
        u = data_uri(s)

        def ground(cls, label):
            row = lambda shape: ''.join(f'<img class="{shape}" src="{u}" width="{px}" height="{px}" alt="">' for px in (96, 40, 20))
            return (f'<div class="ground {cls}"><span class="lbl">{label} · circle</span><div class="row">{row("c")}</div>'
                    f'<span class="lbl">{label} · rounded square</span><div class="row">{row("s")}</div></div>')
        items.append(f'''<article class="logo"><img src="{u}" width="220" height="220" alt="{esc(title)}">
<div><h3>{esc(title)}</h3><p>{esc(desc)}</p><div class="grounds">{ground("lt", "light")}{ground("dk", "dark")}</div>
<p class="note">logos/{slug}.svg · {len(s.encode())/1024:.1f} KB</p></div></article>''')
    icons = ''.join(f'<div class="dicon{" sel" if i == 0 else ""}"><img src="{data_uri(s)}" alt=""><span>FunDrivenDev</span></div>'
                    for i, (_, _, _, s) in enumerate(LOGOS))
    start = data_uri(VERSIONS['d']['assets']['start.svg'])
    panels.append(f'''<section role="tabpanel" id="p-logos" aria-labelledby="t-logos" hidden>
<div class="vhead"><div><h2>Logos</h2><p>Four avatar concepts. Each fills its square, with the mark kept inside the circle so both the GitHub org crop (rounded square) and a circle crop work.</p></div></div>
{''.join(items)}
<h3 style="margin:24px 0 8px;font-size:16px">On the fundriven.dev desktop</h3>
<div class="desk"><div class="icons">{icons}</div><div class="taskbar"><img src="{start}" alt="start"></div></div>
<p class="note">Mock of a desktop icon with its label; the first one is shown selected. The real site's wallpaper may differ.</p>
</section>''')
    page = (f'<title>FunDrivenDev Org Profile</title>\n<style>{CSS}</style>\n<div class="wrap">'
            '<header class="top"><h1>FunDrivenDev org profile</h1><p>Four README directions and four logo concepts. Each mock renders the real profile/README.md as GitHub would; switch GitHub light/dark to see both banner variants.</p></header>'
            f'<div class="tabs" role="tablist" aria-label="Proposals">{tab_btns}</div>{"".join(panels)}</div>\n<script>{JS}</script>\n')
    return page


def main():
    for k, v in VERSIONS.items():
        d = OUT / 'versions' / k
        (d / 'profile').mkdir(parents=True, exist_ok=True)
        (d / 'assets').mkdir(parents=True, exist_ok=True)
        (d / 'profile' / 'README.md').write_text(v['readme'])
        for name, s in v['assets'].items():
            (d / 'assets' / name).write_text(s)
    (OUT / 'logos').mkdir(parents=True, exist_ok=True)
    for slug, _, _, s in LOGOS:
        (OUT / 'logos' / f'{slug}.svg').write_text(s)
    (OUT / 'preview.html').write_text(build_preview())


if __name__ == '__main__':
    main()
