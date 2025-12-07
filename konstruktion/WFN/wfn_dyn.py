import konstruktion.WFN.wfn_dyn_func as f

""" Wellenfestigkeitsnachweis gegen Überschreiten der Dauerfestigkeit und Fließgrenze

    # Vorgehen gemäß "Maschinenelemente und Mechatronik II" von Eckhard Kirchner, sechste Auflage, 2023.
"""

## EINGABE PARAMETER
f_zd = 14.1 # [N] Zug-/Druckkraft Amplitude
f_zdm = 0 # [N] Zug-/Druckkraft Mittelwert
m_ta = 1.84 # [Nm] Torsionsmoment Amplitude
m_tm = 0 # [Nm] Torsionsmoment Mittelwert
m_ba = 0.420 # [Nm] Biegemoment Amplitude
m_bm = 0 # [Nm] Biegemoment Mittelwert
d_k = 0.010 # [m] Kleiner Durchmesser Welle
d_g = 0.015 # [m] Großer Druchmesser Welle
r = 0.001 # [m] Radius Kerbe
k_t = 1 # [] Technologischer Größeneinflussfaktor
k_v = 1 # [] Einflussfaktor Oberflächenverfestigung
r_z = 3.2e-6 # [m] Oberflächenrauheit
r_m = 750e6 # [Pa] Zugfestigkeit Wellenmaterial
sicherheit_min_D = 2 # [] geforderte Sicherheitszahl gegen Dauerbruch
sicherheit_min_F = 2 # [] geforderte Sicherheitszahl gegen Fließen


## BERECHNUNG
# Beanspruchung:
#   Ausschlag
sig_zda = f.sig_zda(f_zd, d_k)
sig_ba = f.sig_ba(m_ba, d_k)
tau_ta = f.tau_ta(m_ta, d_k)
#   Mittel
sig_zdm = f.sig_zdm(f_zd, d_k)
sig_bm = f.sig_bm(m_bm, d_k)
tau_tm = f.tau_tm(m_tm, d_k)
#   Vergleich
sig_vm = f.sig_vm(sig_zdm, sig_bm, tau_tm)
tau_vm = f.tau_vm(sig_vm)

# Beanspruchbarkeit:
#   Wechselfestigkeiten Material nach DIN 743-3 Gl. (1) bis (3)
sig_zdw = 0.4 * r_m
sig_bw = 0.5 * r_m
tau_tw = 0.3 * r_m
#   Einflussfaktoren
k_e = f.k_e(d_k)
k_fs = f.k_fs(r_z, r_m, k_t)
bet_k = f.bet_k(d_k, d_g, r, r_m)
k_gzd, k_gb, k_gt = f.k_g(bet_k, k_e, k_fs, k_v)
#   Wechselfestigkeiten Bauteil
sig_zdwk = f.sig_zdwk(sig_zdw, k_t, k_gzd)
sig_bwk = f.sig_bwk(sig_bw, k_t, k_gb)
tau_twk = f.tau_twk(tau_tw, k_t, k_gt)
#   Mittelspannungsempfindlichkeiten
psi_zdw = f.psi_zdw(sig_zdwk, k_t, r_m)
psi_bw = f.psi_bw(sig_bwk, k_t, r_m)
psi_tw = f.psi_tw(tau_twk, k_t, r_m)
#   Aussschlagsfestigkeit
sig_zdak = f.sig_zdak(sig_zdwk, psi_zdw, sig_vm)
sig_bak = f.sig_bak(sig_bwk, psi_bw, sig_vm)
tau_tak = f.tau_tak(tau_twk, psi_tw, tau_vm)

# Sicherheit:
sicherheit = f.sicherheit(sig_zda,sig_zdak, sig_ba, sig_bak, tau_ta, tau_tak)

# Festigkeitsnachweis:
nachweis = sicherheit >= sicherheit_min

## AUSGABE
print()
if nachweis: print("Der Festigkeitsnachweis ist gemäß der getroffenen Annahmen erfüllt.")
else: print("Der Festigkeitsnachweis ist gemäß der getroffenen Annahmen NICHT erfüllt!")
print("Errechnete Beanspruchung:")
print(f"    sig_zda: {sig_vm/1e6} N/mm²")
print(f"    sig_ba: {sig_ba/1e6} N/mm²")
print(f"    tau_ta: {tau_vm/1e6} N/mm²")
print("Errechnete Beanspruchbarkeit (Ausschlagsfestigkeiten):")
print(f"    sig_zdak: {sig_zdak/1e6} N/mm²")
print(f"    sig_bak: {sig_bak/1e6} N/mm²")
print(f"    tau_tak: {tau_tak/1e6} N/mm²")
print(f"Errechnete Sicherheit: {sicherheit}")
print()
