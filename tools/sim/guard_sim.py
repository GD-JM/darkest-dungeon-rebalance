"""보호(수호자)의 가치: 파티 몬테카를로. 공격은 실제 편성(AI 가중치)에서 뽑는다."""
import sys, io, os, json, random, statistics as st
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
random.seed(7)
ATK = json.load(open(os.path.join(os.environ['TEMP'], 'mon_attacks.json')))   # (가중치, 명중, 최소, 최대, 치명타%, 광역)
W = [a[0] for a in ATK]
HP_OTHERS = [29, 35, 35, 36, 36, 36, 37, 38, 38, 43, 43, 44, 45, 46, 46, 47, 47, 61, 63]   # 중보병(55) 제외 5레벨 체력
MAA_HP, DODGE, DB_RESIST = 55, 25, 0.67
STRESS_HP = 1.30
COST_DD = (8 + 3 * 0.25 * 4) * STRESS_HP                 # 죽음의 문턱 진입: 본인 +8, 동료 각 25%로 +4
COST_DEATH = 43 + (3 * 0.5 * 12) * STRESS_HP              # 사망: 영웅 체력 한 명분 + 동료 각 50%로 +12
ATT_PER_ROUND = 2


def fight(guard, rounds, start_frac, prot):
    hp_max = [MAA_HP] + random.sample(HP_OTHERS, 3)
    hp = [m * start_frac for m in hp_max]
    dd = [False] * 4; dead = [False] * 4
    raw = 0.0; cost = 0.0
    guarded = None
    if guard:
        guarded = min(range(1, 4), key=lambda i: hp[i] / hp_max[i])
    for r in range(rounds):
        g_on = guard and r < 3
        for _ in range(ATT_PER_ROUND):
            a = random.choices(ATK, weights=W)[0]
            _, acc, lo, hi, crit, aoe = a
            alive = [i for i in range(4) if not dead[i]]
            if not alive:
                break
            targets = alive if aoe else [random.choice(alive)]
            if g_on and not aoe and targets[0] == guarded and not dead[0]:
                targets = [0]
            for i in targets:
                if random.random() > max(0.05, min(0.95, (acc - DODGE) / 100)):
                    continue
                c = random.random() < crit / 100
                d = hi * 1.5 if c else random.uniform(lo, hi)
                if i == 0 and g_on:
                    d *= (1 - prot)
                raw += d
                if dd[i]:
                    if random.random() > DB_RESIST:
                        dead[i] = True; cost += COST_DEATH
                    continue
                hp[i] -= d
                if hp[i] <= 0:
                    hp[i] = 0; dd[i] = True; cost += COST_DD
    return raw, cost


def run(rounds, start, N=60000):
    out = {}
    for g in (False, True):
        rs, cs = zip(*(fight(g, rounds, start, 0.30) for _ in range(N)))
        out[g] = (st.mean(rs), st.mean(cs))
    return out


print(f'비용 환산: 문턱 진입 {COST_DD:.1f} HP, 사망 {COST_DEATH:.1f} HP')
for rounds in (3, 6):
    for start in (1.0, 0.7, 0.5):
        o = run(rounds, start)
        d_raw = o[False][0] - o[True][0]; d_cost = o[False][1] - o[True][1]
        print(f'전투 {rounds}라운드, 시작 체력 {start*100:.0f}%: 보호 없음 문턱·사망 비용 {o[False][1]:.2f} -> 보호 {o[True][1]:.2f} '
              f'| 보호 가치 = 방어도로 줄인 피해 {d_raw:.2f} + 문턱·사망 방지 {d_cost:.2f} = {d_raw + d_cost:.2f} HP')
