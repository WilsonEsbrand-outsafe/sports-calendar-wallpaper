"""노을 진 잠실구장 전경 일러스트(SVG)를 만든다.

    python3 tools/jamsil/make_svg.py > tools/jamsil/jamsil.svg
    node tools/jamsil/render.js            # → assets/stadium/jamsil.jpg

홈플레이트 뒤 2층에서 외야를 바라본 구도. 멀리 롯데월드타워가 보인다.
"""
import random

W, H = 2560, 1440
HORIZON = 700          # 외야 관중석 꼭대기 높이
rnd = random.Random(1982)  # 결과가 매번 같도록 고정
out = []
add = out.append


def poly(pts, fill, extra=''):
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    add(f'<polygon points="{d}" fill="{fill}" {extra}/>')


# ── 정의: 하늘, 빛, 질감 ──────────────────────────
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('''<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"    stop-color="#1b2246"/>
    <stop offset="0.28" stop-color="#3d3a6e"/>
    <stop offset="0.50" stop-color="#8a5279"/>
    <stop offset="0.66" stop-color="#e07a5f"/>
    <stop offset="0.78" stop-color="#f6b26b"/>
    <stop offset="0.86" stop-color="#ffd59a"/>
  </linearGradient>
  <radialGradient id="sun" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0"   stop-color="#fff4d6" stop-opacity="1"/>
    <stop offset="0.12" stop-color="#ffe2a8" stop-opacity="0.95"/>
    <stop offset="0.4" stop-color="#ffb070" stop-opacity="0.35"/>
    <stop offset="1"   stop-color="#ff9060" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="lamp" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0"   stop-color="#fffbe8" stop-opacity="0.9"/>
    <stop offset="0.25" stop-color="#fff1c4" stop-opacity="0.35"/>
    <stop offset="1"   stop-color="#ffe7a8" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="grass" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#3f6b3a"/>
    <stop offset="1" stop-color="#2d5a2c"/>
  </linearGradient>
  <linearGradient id="haze" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffc58a" stop-opacity="0"/>
    <stop offset="1" stop-color="#ffc58a" stop-opacity="0.35"/>
  </linearGradient>
  <linearGradient id="fieldglow" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffb46e" stop-opacity="0.22"/>
    <stop offset="0.5" stop-color="#ffb46e" stop-opacity="0.05"/>
    <stop offset="1" stop-color="#ffb46e" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="vignette" cx="0.5" cy="0.48" r="0.75">
    <stop offset="0.55" stop-color="#000" stop-opacity="0"/>
    <stop offset="1"    stop-color="#0a0614" stop-opacity="0.55"/>
  </radialGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="n"/>
    <feColorMatrix type="saturate" values="0"/>
    <feComponentTransfer><feFuncA type="table" tableValues="0 0.10"/></feComponentTransfer>
  </filter>
  <filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="blur2"><feGaussianBlur stdDeviation="2"/></filter>
</defs>''')

# ── 하늘 ──────────────────────────────────────
add(f'<rect width="{W}" height="{HORIZON+40}" fill="url(#sky)"/>')
# 해: 외야 왼쪽 너머로 지는 중
SUN_X, SUN_Y = 700, 565
add(f'<circle cx="{SUN_X}" cy="{SUN_Y}" r="520" fill="url(#sun)"/>')
add(f'<circle cx="{SUN_X}" cy="{SUN_Y}" r="46" fill="#fff3d0"/>')

# 구름: 해 쪽은 밝게, 위쪽은 보랏빛
for _ in range(26):
    y = rnd.uniform(120, 520)
    x = rnd.uniform(-200, W)
    w = rnd.uniform(260, 760)
    h = rnd.uniform(10, 26)
    t = (y - 120) / 400
    near = max(0, 1 - abs(x - SUN_X) / 1400)
    col = ['#6b4f86', '#a8607e', '#e8896a', '#f7b27a'][min(3, int(t * 3 + near))]
    add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{w/2:.0f}" ry="{h:.0f}" fill="{col}" opacity="{0.35+0.3*t:.2f}" filter="url(#blur6)"/>')

# ── 서울 스카이라인 ────────────────────────────
def skyline(base, hmin, hmax, col, lit, seed):
    r = random.Random(seed)
    x = -20
    while x < W:
        bw = r.uniform(40, 120)
        bh = r.uniform(hmin, hmax)
        add(f'<rect x="{x:.0f}" y="{base-bh:.0f}" width="{bw:.0f}" height="{bh+60:.0f}" fill="{col}"/>')
        if lit:
            for _ in range(int(bw * bh / 900)):
                wx = x + r.uniform(4, bw - 6)
                wy = base - bh + r.uniform(6, bh)
                add(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="3" height="4" fill="#ffd89a" opacity="{r.uniform(.35,.9):.2f}"/>')
        x += bw + r.uniform(-10, 14)

skyline(HORIZON - 40, 30, 110, '#6d4a6e', False, 3)

# 롯데월드타워: 위로 갈수록 가늘어지고 꼭대기가 살짝 갈라진다
TX, TB, TT = 1800, HORIZON - 40, 170
left, right = [], []
for k in range(21):
    t = k / 20                      # 0 = 바닥, 1 = 꼭대기
    y = TB - (TB - TT) * t
    half = 34 * (1 - t) ** 1.2 + 6  # 붓 끝처럼 완만하게 좁아진다
    left.append((TX - half, y)); right.append((TX + half, y))
poly(left + [(TX - 4, TT - 30), (TX - 1, TT + 8), (TX + 1, TT + 8), (TX + 4, TT - 30)] + right[::-1], '#5b4060')
# 해가 비치는 왼쪽 면
poly(left + [(TX - 4, TT - 30), (TX - 1, TT + 8)] + [(TX - h * 0.15 - 1, y) for (x, y), h in zip(left[::-1], [TX - x for x, _ in left[::-1]])], '#f2a878', 'opacity="0.35"')
add(f'<circle cx="{TX-4}" cy="{TT-34}" r="4" fill="#ff5a4a"/>')

skyline(HORIZON - 10, 20, 70, '#4a3352', True, 11)
add(f'<rect y="{HORIZON-200}" width="{W}" height="220" fill="url(#haze)"/>')

# ── 외야 관중석 ────────────────────────────────
def crowd(pts_top_y, y0, y1, x0, x1, density, seed, dark=False):
    r = random.Random(seed)
    cols = ['#2a2f55', '#c9cbe0', '#1d2140', '#8a2a3a', '#e9e6f2', '#3a3f6c', '#f2c94c']
    n = int((x1 - x0) * (y1 - y0) / density)
    for _ in range(n):
        x = r.uniform(x0, x1)
        y = r.uniform(y0, y1)
        if y < pts_top_y(x):
            continue
        c = r.choice(cols)
        add(f'<rect x="{x:.0f}" y="{y:.0f}" width="3" height="3" fill="{c}" opacity="{0.45 if dark else 0.7}"/>')

BLEACH_TOP = HORIZON
FENCE_C = 805            # 가운데 펜스 높이(화면 y)

def fence_y(x):
    # 외야 펜스: 양 끝이 아래로 휘는 호
    u = (x - W / 2) / (W / 2)
    return FENCE_C + 150 * u * u

poly([(0, BLEACH_TOP + 70), (W / 2, BLEACH_TOP), (W, BLEACH_TOP + 70), (W, fence_y(W)), (W / 2, FENCE_C), (0, fence_y(0))], '#2b2442')
crowd(lambda x: BLEACH_TOP + 70 * abs(x - W / 2) / (W / 2), BLEACH_TOP, FENCE_C + 150, 0, W, 60, 5, dark=True)

# 전광판
add(f'<rect x="1130" y="{BLEACH_TOP-150}" width="300" height="150" rx="4" fill="#15132a"/>')
add(f'<rect x="1142" y="{BLEACH_TOP-138}" width="276" height="96" fill="#1f2a55"/>')
for i in range(9):
    add(f'<rect x="{1150+i*30}" y="{BLEACH_TOP-128}" width="22" height="16" fill="#ffe28a" opacity="{0.5+0.4*((i*7)%3)/2:.2f}"/>')
    add(f'<rect x="{1150+i*30}" y="{BLEACH_TOP-104}" width="22" height="16" fill="#9fd3ff" opacity="0.55"/>')
add(f'<rect x="1270" y="{BLEACH_TOP}" width="20" height="{FENCE_C-BLEACH_TOP}" fill="#15132a"/>')

# ── 외야 펜스(두산 남색) ───────────────────────
fence = [(x, fence_y(x)) for x in range(0, W + 1, 40)]
poly([(x, y - 34) for x, y in fence] + [(x, y) for x, y in reversed(fence)], '#13234f')
poly([(x, y - 34) for x, y in fence] + [(x, y - 30) for x, y in reversed(fence)], '#c9314a')

# ── 그라운드 ──────────────────────────────────
field_pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in fence + [(W, H), (0, H)])
add(f'<clipPath id="field"><polygon points="{field_pts}"/></clipPath>')
poly(fence + [(W, H), (0, H)], 'url(#grass)')
add('<g clip-path="url(#field)">')
# 잔디 깎은 줄무늬: 홈에서 퍼지는 부채꼴
HOME = (W / 2, H + 260)
for i in range(-12, 13):
    if i % 2:
        continue
    a0, a1 = i * 0.075, (i + 1) * 0.075
    def edge(a):
        import math
        return (HOME[0] + math.sin(a) * 3000, HOME[1] - math.cos(a) * 3000)
    poly([HOME, edge(a0), edge(a1)], '#ffffff', 'opacity="0.045"')
add('</g>')
# 외야 경고 트랙
track = [(x, y + 2) for x, y in fence]
poly(track + [(x, y + 26 + 10 * abs(x - W / 2) / (W / 2)) for x, y in reversed(fence)], '#9a6a4a')

# 내야: 흙 부채꼴 + 잔디 다이아몬드
IF = 1060  # 내야 흙 바깥 호의 꼭대기
poly([(HOME[0] - 1050, H + 40), (HOME[0] - 520, IF + 40), (HOME[0], IF), (HOME[0] + 520, IF + 40), (HOME[0] + 1050, H + 40)], '#b0764d')
poly([(HOME[0], 1150), (HOME[0] + 330, 1300), (HOME[0], 1500), (HOME[0] - 330, 1300)], '#3b6a37')
add(f'<ellipse cx="{HOME[0]}" cy="1290" rx="60" ry="22" fill="#b98057"/>')
add(f'<rect x="{HOME[0]-10}" y="1284" width="20" height="5" fill="#f3efe6"/>')
for bx, by in [(HOME[0] + 330, 1300), (HOME[0], 1150), (HOME[0] - 330, 1300)]:
    add(f'<rect x="{bx-9}" y="{by-6}" width="18" height="12" fill="#f3efe6" transform="rotate(0 {bx} {by})"/>')
# 파울 라인
add(f'<line x1="{HOME[0]}" y1="1500" x2="40" y2="{fence_y(40)}" stroke="#f3efe6" stroke-width="5" opacity="0.85"/>')
add(f'<line x1="{HOME[0]}" y1="1500" x2="{W-40}" y2="{fence_y(W-40)}" stroke="#f3efe6" stroke-width="5" opacity="0.85"/>')
# 해 쪽에서 비치는 따뜻한 빛
add(f'<rect y="{FENCE_C-40}" width="{W}" height="{H-FENCE_C+40}" fill="url(#fieldglow)"/>')

# ── 양쪽 내야 관중석과 지붕 ─────────────────────
def side_stand(sign):
    cx = W / 2
    def X(x):
        return cx + sign * (x - cx)
    stand = [(X(-10), 430), (X(430), 700), (X(700), H + 40), (X(-10), H + 40)]
    # 관중석 앞면 (그라운드 쪽 벽)
    poly([(X(80), fence_y(80) - 20), (X(430), 700), (X(700), H + 40), (X(-10), H + 40)], '#241d38')
    poly([(X(80), fence_y(80) - 20), (X(430), 700), (X(700), H + 40), (X(-10), H + 40)], '#13234f', 'opacity="0.0"')
    # 관중석 앞 펜스(남색 띠)
    add(f'<line x1="{X(430)}" y1="702" x2="{X(712)}" y2="{H+50}" stroke="#13234f" stroke-width="22"/>')
    poly(stand, '#2c2442')
    r = random.Random(40 + sign)
    cols = ['#1c2350', '#e7e4f0', '#2b3166', '#c4314a', '#f0d36a', '#121636']
    for _ in range(4200):
        x = r.uniform(0, 720)
        y = r.uniform(430, H)
        # 관중석 안쪽만: 앞면 선 (430,700)-(700,H) 바깥쪽
        lim = 430 + (y - 700) * (270 / (H - 700)) if y > 700 else 430 * (y - 430) / 270
        if x > lim:
            continue
        add(f'<rect x="{X(x):.0f}" y="{y:.0f}" width="4" height="4" fill="{r.choice(cols)}" opacity="0.75"/>')
    # 지붕 차양: 화면 위쪽 모서리를 덮는다
    poly([(X(-10), 0), (X(760), 0), (X(640), 110), (X(400), 250), (X(-10), 400)], '#140f22')
    poly([(X(640), 110), (X(400), 250), (X(-10), 400), (X(-10), 424), (X(412), 266), (X(656), 124)], '#3a2c4e')
    # 조명탑: 차양 끝 위의 조명 뭉치
    for lx, ly in [(560, 160), (230, 330)]:
        add(f'<circle cx="{X(lx)}" cy="{ly}" r="230" fill="url(#lamp)"/>')
        for i in range(4):
            for j in range(3):
                add(f'<rect x="{X(lx)-40+i*20}" y="{ly-20+j*14}" width="15" height="10" fill="#fffbe6"/>')

side_stand(-1)
side_stand(1)

# 외야 쪽 조명탑 두 개 (멀리 작게)
for lx in (420, W - 420):
    ly = BLEACH_TOP - 120
    add(f'<rect x="{lx-3}" y="{ly}" width="6" height="{fence_y(lx)-ly-30}" fill="#1a1530"/>')
    add(f'<circle cx="{lx}" cy="{ly}" r="110" fill="url(#lamp)"/>')
    add(f'<rect x="{lx-30}" y="{ly-16}" width="60" height="26" fill="#fffbe6"/>')

# ── 마감: 비네팅 + 필름 그레인 ─────────────────
add(f'<rect width="{W}" height="{H}" fill="url(#vignette)"/>')
add(f'<rect width="{W}" height="{H}" filter="url(#grain)"/>')
add('</svg>')
print('\n'.join(out))
