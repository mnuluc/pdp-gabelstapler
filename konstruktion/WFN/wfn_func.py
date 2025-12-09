import math

### Funktionen für dynamischen Wellenfestigkeitsnachweis

## Sicherheit Dauerfestigkeit
def sicherheit_D(sig_zda, sig_zdak, sig_ba, sig_bak, tau_ta, tau_tak):
    zdb = sig_zda / sig_zdak + sig_ba / sig_bak
    t = tau_ta / tau_tak
    return 1 / math.sqrt(zdb**2 + t**2)

## BEANSPRUCHUNG
#   Amplitude
def sig_zda(f_zda, d):
    a = math.pi/4 * d * d
    return f_zda/a

def sig_ba(m_ba, d):
    wb = math.pi/32 * d * d * d
    return m_ba/wb

def tau_ta(m_ta, d):
    wt = math.pi/16 * d * d * d
    return m_ta/wt

#   Mittelwert
def sig_zdm(f_zdm, d):
    a = math.pi/4 * d * d
    return f_zdm/a

def sig_bm(m_bm, d):
    wb = math.pi/32 * d * d * d
    return m_bm/wb

def tau_tm(m_tm, d):
    wt = math.pi/16 * d * d * d
    return m_tm/wt


## BEANSPRUCHBARKEIT
#   Ausschlagfestigkeit
def sig_zdak(sig_zdwk, psi_zdw, sig_vm):
    return sig_zdwk - psi_zdw * sig_vm

def sig_bak(sig_bwk, psi_bw, sig_vm):
    return sig_bwk - psi_bw * sig_vm

def tau_tak(tau_twk, psi_tw, tau_vm):
    return tau_twk - psi_tw * tau_vm

#   Vergleichsmittelspannung
def sig_vm(sig_zdm, sig_bm, tau_m):
    return math.sqrt((sig_zdm + sig_bm)**2 + 3 * tau_m**2)

def tau_vm(sig_vm):
    return sig_vm/math.sqrt(3)

#   Mittelspannungsempfindlichkiet
def psi_zdw(sig_zdwk, k_t, r_m):
    return sig_zdwk / (2*k_t * r_m - sig_zdwk)

def psi_bw(sig_bwk, k_t, r_m):
    return sig_bwk / (2*k_t * r_m - sig_bwk)

def psi_tw(tau_twk, k_t, r_m):
    return tau_twk / (2*k_t * r_m - tau_twk)

#   Wechselfestigkeit
def sig_zdwk(sig_zdw, k_t, k_gzd):
    return sig_zdw * k_t / k_gzd

def sig_bwk(sig_bw, k_t, k_gb):
    return sig_bw * k_t / k_gb

def tau_twk(tau_tw, k_t, k_gt):
    return tau_tw * k_t / k_gt

# Einflussfaktoren
#   Gesamteinflussfaktoren
def k_gzd(bet_kzd, k_fs, k_v):
    return (bet_kzd + (1 / k_fs) - 1) / k_v

def k_gb(bet_kb, k_e, k_fs, k_v):
    return (bet_kb / k_e + 1 / k_fs - 1) / k_v

def k_gt(bet_kt, k_e, k_ft, k_v):
    return (bet_kt / k_e + 1 / k_ft - 1) / k_v

def k_g(bet_k, k_e, k_fs, k_v):
    bet_kzd, bet_kb, bet_kt = bet_k
    k_zd = k_gzd(bet_kzd, k_fs, k_v)
    k_b = k_gb(bet_kb, k_e, k_fs, k_v)
    k_t = k_gt(bet_kt, k_e, k_ft(k_fs), k_v)

    return (k_zd, k_b, k_t)

#   Geometrischer Einflussfaktor
def k_e(d_eff):
    if d_eff >= 0.150:
        return 0.8
    else:
        return 1 - 0.2 * (math.log(d_eff/0.0075)/math.log(20))

#   Oberflächenrauheit Einflussfaktoren
def k_fs(r_z, r_m, k_t):
    return 1 - 0.22 * math.log(r_z/1e-6) * (math.log(r_m * k_t / 20e6) -1)

def k_ft(k_fs):
    return 0.575 * k_fs + 0.425

def k_2f(vollwelle, harte_randschicht):
    if harte_randschicht:
        if vollwelle:
            return [1 , 1.1, 1.1]
        else:
            return [1, 1, 1]
    else:
        if vollwelle:
            return [1, 1.2, 1.2]
        else:
            return [1, 1.1, 1]

# Kerbwirkungszahlen
#   Konstanten für Formzahl
a_zd = 0.62
b_zd = 3.5
c_zd = 0
z_zd = 0

a_b = 0.62
b_b = 5.8
c_b = 0.2
z_b = 3

a_t = 3.4
b_t = 19
c_t = 1
z_t = 2

gamma_f_zdb = [
    1,
    1.05,
    1.1,
    1.15
]

def alp_k(a, b, c, z, d_k, d_g, r):
    t = (d_g-d_k)/2
    calc = a * r/t + 2 * b * r/d_k * (1 + 2 * r / d_k)**2 + c * (r/t)**z * d_k/d_g
    return 1 + 1/calc

def n_hat(g_dash, r_e):
    power = - (0.33 + r_e / 712e6)
    return 1 + math.sqrt(g_dash) * math.pow(10, power)

def phi(d_k, d_g, r):
    t = (d_g-d_k)/2
    return 1 / (4 * math.sqrt(t/r) + 2)

def bet_k(d_k, d_g, r, r_m):
    ph = phi(d_k, d_g, r)

    g_dash_zd = 2 * (1 + ph)/r
    g_dash_b = 2 * (1 + ph)/r
    g_dash_t = 1/r

    n_hat_zd = n_hat(g_dash_zd, r_m)
    n_hat_b = n_hat(g_dash_b, r_m)
    n_hat_t = n_hat(g_dash_t, r_m)

    alp_k_zd = alp_k(a_zd, b_zd, c_zd, z_zd, d_k, d_g, r)
    alp_k_b = alp_k(a_b, b_b, c_b, z_b, d_k, d_g, r)
    alp_k_t = alp_k(a_t, b_t, c_t, z_t, d_k, d_g, r)

    return (alp_k_zd/n_hat_zd, alp_k_b/n_hat_b, alp_k_t/n_hat_t)

def gamma_f(bet_k):
    gamma_f = [None, None, 1]
    # zd
    if bet_k[0] < 1.5 : gamma_f[0] = gamma_f_zdb[0]
    if bet_k[0] >= 1.5 and bet_k[0] < 2: gamma_f[0] = gamma_f_zdb[1]
    if bet_k[0] >= 2 and bet_k[0] < 3: gamma_f[0] = gamma_f_zdb[2]
    else: gamma_f[0] = gamma_f_zdb[3]
    # b
    if bet_k[1] < 1.5 : gamma_f[1] = gamma_f_zdb[0]
    if bet_k[1] >= 1.5 and bet_k[1] < 2: gamma_f[1] = gamma_f_zdb[1]
    if bet_k[1] >= 2 and bet_k[1] < 3: gamma_f[1] = gamma_f_zdb[2]
    else: gamma_f[1] = gamma_f_zdb[3]

    return gamma_f # tupel enthält: [gamma_f (für zd), gamma_f (für b), gamma_f (für t)]

### Funktionen für den statischen Wellenfestigkeitsnachweis
#   Maximal
def sig_zdmax(f_zdmax, d):
    a = math.pi/4 * d * d
    return f_zdmax/a

def sig_bmax(m_bmax, d):
    wb = math.pi/32 * d * d * d
    return m_bmax/wb

def tau_tmax(m_tmax, d):
    wt = math.pi/16 * d * d * d
    return m_tmax/wt

#   Fließgrenzen Bauteil Kerbe
def sig_zdfk(r_e, bet_k, k_Fzd, k_t):
    gamma_fzd = gamma_f(bet_k)[0]
    return k_t * k_Fzd * gamma_fzd * r_e

def sig_bfk(r_e, bet_k, k_Fb, k_t):
    gamma_fb = gamma_f(bet_k)[1]
    return k_t * k_Fb * gamma_fb * r_e

def tau_tfk(r_e, bet_k, k_Ft, k_t):
    gamma_fb = gamma_f(bet_k)[2]
    return k_t * k_Ft * gamma_fb * r_e


## Sicherheit Fließen
def sicherheit_F(sig_zda, sig_zdfk, sig_ba, sig_bfk, tau_ta, tau_tfk):
    sig_zdb = sig_zda / sig_zdfk + sig_ba / sig_bfk
    t = tau_ta / tau_tfk
    return 1 / math.sqrt(sig_zdb ** 2 + t ** 2)
