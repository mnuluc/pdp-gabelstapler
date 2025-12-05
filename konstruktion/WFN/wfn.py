import wfn_lib as wl

## PARAMETER

f_zd = 0 #Zug-/Druckkraft 0 Nm
m_ta = 30000 #Torsionsmoment Amplitude 30 kNm
m_tm = 0 #Torsionsmoment Mittelwert 0 Nm
m_ba = 1164 #Biegemoment Amplitude 1164 Nm
m_bm = 4332 #Biegemoment Mittelwert 4332 Nm
d_k = 0.155 #Kleiner Durchmesser Welle 155 mm
d_g = 0.160 #Großer Druchmesser Welle 160 mm
r = 0.002 #Radius Kerbe 2mm
k_t = 0.75 #Technologischer Größenfaktor 0.75
k_v = 1 #Einflussfaktor Oberflächenverfestigung
r_z = 3.2e-6 #Oberflächenrauheit 3.2um
r_m = 800e6 #Zugfestigkeit 800N/mm²


## BERECHNUNG

# Wechselfestigkeiten
sig_zdw = 0.4 * r_m
sig_bw = 0.5 * r_m
tau_tw = 0.3 * r_m

# Nennspannungen

sig_zda = wl.sig_zda(f_zd, d_k)
sig_ba = wl.sig_ba(m_ba, d_k)
tau_ta = wl.tau_ta(m_ta, d_k)

sig_zdm = wl.sig_zdm(f_zd, d_k)
sig_bm = wl.sig_bm(m_bm, d_k)
tau_tm = wl.tau_tm(m_tm, d_k)

# Berechnung Einflussfaktoren

k_e = wl.k_e(d_k)
k_fs = wl.k_fs(r_z, r_m, k_t)

bet_k = wl.bet_k(d_k, d_g, r, r_m)

k_gzd, k_gb, k_gt = wl.k_g(bet_k, k_e, k_fs, k_v)

sig_zdwk = wl.sig_zdwk(sig_zdw, k_t, k_gzd)
sig_bwk = wl.sig_bwk(sig_bw, k_t, k_gb)
tau_twk = wl.tau_twk(tau_tw, k_t, k_gt)

psi_zdw = wl.psi_zdw(sig_zdwk, k_t, r_m)
psi_bw = wl.psi_bw(sig_bwk, k_t, r_m)
psi_tw = wl.psi_tw(tau_twk, k_t, r_m)

sig_vm = wl.sig_vm(sig_zdm, sig_bm, tau_tm)
tau_vm = wl.tau_vm(sig_vm)

sig_zdak = wl.sig_zdak(sig_zdwk, psi_zdw, sig_vm)
sig_bak = wl.sig_bak(sig_bwk, psi_bw, sig_vm)
tau_tak = wl.tau_tak(tau_twk, psi_tw, tau_vm)

# Sicherheit
sicherheit = wl.sicherheit(sig_zda,sig_zdak, sig_ba, sig_bak, tau_ta, tau_tak)


## AUSGABE
print(f"S: {sicherheit}")
print(f"sig_zdm: {sig_zdm}")
print(f"sig_bm: {sig_bm}")
print(f"tau_tm: {tau_tm}")
print(f"sig_zda: {sig_zda}")
print(f"sig_ba: {sig_ba}")
print(f"tau_ta: {tau_ta}")
print(f"sig_zdak: {sig_zdak}")
print(f"sig_bak: {sig_bak}")
print(f"tau_tak: {tau_tak}")