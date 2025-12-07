import wfn_func as fd

""" Wellenfestigkeitsnachweis gegen Überschreiten der Dauerfestigkeit und Fließgrenze

    # Vorgehen gemäß "Maschinenelemente und Mechatronik II" von Eckhard Kirchner, sechste Auflage, 2023.
    # HINWEIS: Nicht für Wellen mit hohen stationären Beanspruchungsanteilen geeignet!
"""

## EINGABE PARAMETER
f_zda = 14.1 # [N] Zug-/Druckkraft Amplitude
f_zdm = 0 # [N] Zug-/Druckkraft Mittelwert
m_ta = 1.84 # [Nm] Torsionsmoment Amplitude
m_tm = 0 # [Nm] Torsionsmoment Mittelwert
m_ba = 0.420 # [Nm] Biegemoment Amplitude
m_bm = 0 # [Nm] Biegemoment Mittelwert

f_zdmax = 100000 # [N] Zug-/Druckkraft Maximal
m_tmax = 0.1 # [Nm] Torsionsmoment Maximal
m_bmax = 0.1 # [Nm] Biegemoment Maximal

d_k = 0.010 # [m] Kleiner Durchmesser Welle
d_g = 0.015 # [m] Großer Druchmesser Welle
r = 0.001 # [m] Radius Kerbe
vollwelle = True
harte_randschicht = False

k_t = 1 # [] Technologischer Größeneinflussfaktor
k_v = 1 # [] Einflussfaktor Oberflächenverfestigung

r_z = 3.2e-6 # [m] Oberflächenrauheit

r_m = 750e6 # [Pa] Zugfestigkeit Wellenmaterial
r_e = 520e6 # [Pa] Streckgrenze Wellenmaterial

sicherheit_min_D = 2 # [] geforderte Sicherheitszahl gegen Dauerbruch
sicherheit_min_F = 2 # [] geforderte Sicherheitszahl gegen Fließen


## BERECHNUNG
# Beanspruchung:
#   Ausschlag
sig_zda = fd.sig_zda(f_zda, d_k)
sig_ba = fd.sig_ba(m_ba, d_k)
tau_ta = fd.tau_ta(m_ta, d_k)
#   Mittel
sig_zdm = fd.sig_zdm(f_zda, d_k)
sig_bm = fd.sig_bm(m_bm, d_k)
tau_tm = fd.tau_tm(m_tm, d_k)
#   Vergleich
sig_vm = fd.sig_vm(sig_zdm, sig_bm, tau_tm)
tau_vm = fd.tau_vm(sig_vm)
#   Maximal
sig_zdmax = fd.sig_zdmax(f_zdmax, d_k)
sig_bmax = fd.sig_bmax(m_bmax, d_k)
tau_tmax = fd.tau_tmax(m_tmax, d_k)

# Beanspruchbarkeit:
#   Wechselfestigkeiten Material nach DIN 743-3 Gl. (1) bis (3)
sig_zdw = 0.4 * r_m
sig_bw = 0.5 * r_m
tau_tw = 0.3 * r_m
#   Einflussfaktoren
k_e = fd.k_e(d_k)
k_fs = fd.k_fs(r_z, r_m, k_t)
bet_k = fd.bet_k(d_k, d_g, r, r_m)
k_gzd, k_gb, k_gt = fd.k_g(bet_k, k_e, k_fs, k_v)
k_Fzd, k_Fb, k_Ft = fd.k_2f(vollwelle, harte_randschicht)
#   Wechselfestigkeiten Bauteil
sig_zdwk = fd.sig_zdwk(sig_zdw, k_t, k_gzd)
sig_bwk = fd.sig_bwk(sig_bw, k_t, k_gb)
tau_twk = fd.tau_twk(tau_tw, k_t, k_gt)
#   Mittelspannungsempfindlichkeiten
psi_zdw = fd.psi_zdw(sig_zdwk, k_t, r_m)
psi_bw = fd.psi_bw(sig_bwk, k_t, r_m)
psi_tw = fd.psi_tw(tau_twk, k_t, r_m)
#   Aussschlagsfestigkeit
sig_zdak = fd.sig_zdak(sig_zdwk, psi_zdw, sig_vm)
sig_bak = fd.sig_bak(sig_bwk, psi_bw, sig_vm)
tau_tak = fd.tau_tak(tau_twk, psi_tw, tau_vm)
#   Fließgrenzen Bauteil
sig_zdfk = fd.sig_zdfk(r_e, bet_k, k_Fzd, k_t)
sig_bfk = fd.sig_bfk(r_e, bet_k, k_Fb, k_t)
tau_tfk = fd.tau_tfk(r_e, bet_k, k_Ft, k_t)

# Sicherheit:
sicherheit_D = fd.sicherheit_D(sig_zda,sig_zdak, sig_ba, sig_bak, tau_ta, tau_tak)
sicherheit_F = fd.sicherheit_F(sig_zdmax, sig_zdfk, sig_bmax, sig_bfk, tau_tmax, tau_tfk)

# Festigkeitsnachweis:
nachweis_D = sicherheit_D >= sicherheit_min_D
nachweis_F = sicherheit_F >= sicherheit_min_F

## AUSGABE
print()
if nachweis_D: print("Der dynamische Festigkeitsnachweis ist gemäß der getroffenen Annahmen erfüllt.")
else: print("Der dynamische Festigkeitsnachweis ist gemäß der getroffenen Annahmen NICHT erfüllt!")
print("Errechnete Beanspruchung:")
print(f"    sig_zda: {sig_zda/1e6} N/mm²")
print(f"    sig_ba: {sig_ba/1e6} N/mm²")
print(f"    tau_ta: {tau_ta/1e6} N/mm²")
print(f"    sig_zdm: {sig_zdm/1e6} N/mm²")
print(f"    sig_bm: {sig_bm/1e6} N/mm²")
print(f"    tau_tm: {tau_tm/1e6} N/mm²")
print("Errechnete Beanspruchbarkeit (Ausschlagsfestigkeiten):")
print(f"    sig_zdAK: {sig_zdak/1e6} N/mm²")
print(f"    sig_bAK: {sig_bak/1e6} N/mm²")
print(f"    tau_tAK: {tau_tak/1e6} N/mm²")
print(f"Errechnete Sicherheit gegen Dauerbruch: {sicherheit_D}")
print()
if nachweis_F: print("Der statische Festigkeitsnachweis ist gemäß der getroffenen Annahmen erfüllt.")
else: print("Der statische Festigkeitsnachweis ist gemäß der getroffenen Annahmen NICHT erfüllt!")
print("Errechnete Beanspruchung:")
print(f"    sig_zdmax: {sig_zdmax/1e6} N/mm²")
print(f"    sig_bmax: {sig_bmax/1e6} N/mm²")
print(f"    tau_tmax: {tau_tmax/1e6} N/mm²")
print("Errechnete Beanspruchbarkeit:")
print(f"    sig_zdFK: {sig_zdfk/1e6} N/mm²")
print(f"    sig_bFK: {sig_bfk/1e6} N/mm²")
print(f"    tau_tFK: {tau_tfk/1e6} N/mm²")
print(f"Errechnete Sicherheit gegen Dauerbruch: {sicherheit_F}")