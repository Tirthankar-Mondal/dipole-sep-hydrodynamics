"""Generate every figure used in progress.pdf, from the raw data on disk.

Usage:
    python scripts/make_progress_figures.py

Writes vector PDFs to numerics/results/figures/final/ and a machine-readable
dump of every number quoted in the document to
numerics/data/processed/progress_numbers.json.

Note on the project convention: CLAUDE.md asks for one regenerating script
per final figure, named to match. This single generator produces the whole
coordinated figure set for one document instead; each figure's source data
and construction is in the correspondingly named function below
(fig_h1_overview() -> fig_h1_overview.pdf, and so on).
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator
from scipy.optimize import curve_fit
from scipy import stats

REPO = Path(__file__).resolve().parent.parent.parent
RAW = REPO / "numerics" / "data" / "raw"
ARCH = REPO / "numerics" / "data" / "archive"
FIGS = REPO / "numerics" / "results" / "figures" / "final"
PROC = REPO / "numerics" / "data" / "processed"
FIGS.mkdir(parents=True, exist_ok=True)
PROC.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9.5,
    "legend.fontsize": 7.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.dpi": 160,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linewidth": 0.5,
    "lines.linewidth": 1.2,
    "legend.frameon": True,
    "legend.framealpha": 0.9,
    "legend.edgecolor": "0.8",
    "savefig.bbox": "tight",
})

NUMBERS = {}


# ----------------------------------------------------------------- loading
def load_summary(path, key="frozen_fraction_mean", sekey="frozen_fraction_se"):
    rows = sorted(json.load(open(Path(path) / "summary.json")), key=lambda r: r["L"])
    return (np.array([r["L"] for r in rows], float),
            np.array([r[key] for r in rows], float),
            np.array([r[sekey] for r in rows], float))


def newest(pattern, root=RAW):
    """Newest run directory matching `pattern` that actually finished
    (summary.json present) -- an in-progress run is skipped, not half-read."""
    hits = [h for h in sorted(root.glob(pattern)) if (h / "summary.json").exists()]
    return hits[-1] if hits else None


DEFA_PROD = ARCH / "frozen_fraction_production_20260912T074229Z"
DEFA_FIT = ARCH / "frozen_fraction_fitting_range_20260912T102036Z"
DEFB5_TEST = RAW / "frozen_fraction_test_20260913T062809Z"
DEFB5_PROD = RAW / "frozen_fraction_production_intermediate_20260913T064716Z"
DEFB10_PROD = RAW / "frozen_fraction_production_intermediate_20260913T084452Z"
GAP_PROD = RAW / "gap_length_gap_length_production_20260914T045549Z"
GAP_L = [100, 200, 400, 800, 1600, 3200, 6400, 12800]


def def_a_combined():
    L1, f1, s1 = load_summary(DEFA_PROD)
    L2, f2, s2 = load_summary(DEFA_FIT)
    L = np.concatenate([L1, L2]); f = np.concatenate([f1, f2]); s = np.concatenate([s1, s2])
    o = np.argsort(L)
    return L[o], f[o], s[o]


def def_b5_combined():
    L1, f1, s1 = load_summary(DEFB5_TEST)
    L2, f2, s2 = load_summary(DEFB5_PROD)
    L = np.concatenate([L1, L2]); f = np.concatenate([f1, f2]); s = np.concatenate([s1, s2])
    o = np.argsort(L)
    return L[o], f[o], s[o]


def wmean(f, se):
    w = 1.0 / se ** 2
    return float(np.sum(w * f) / np.sum(w)), float(np.sqrt(1.0 / np.sum(w)))


# ------------------------------------------------------------------- fits
def fit_models(N, f, se):
    out = {}
    w = 1 / se ** 2
    fc, fc_se = wmean(f, se)
    chi = float(np.sum(((f - fc) / se) ** 2)); dof = len(N) - 1
    out["M1"] = dict(f_inf=fc, f_inf_se=fc_se, chi2=chi, dof=dof, red=chi / dof,
                     pvalue=float(stats.chi2.sf(chi, dof)))
    try:
        p, cov = curve_fit(lambda N, f0, a, al: f0 + a * N ** (-al), N, f,
                           p0=[0.36, -1.0, 1.0], sigma=se, absolute_sigma=True, maxfev=400000)
        r = (f - (p[0] + p[1] * N ** (-p[2]))) / se
        chi = float(np.sum(r ** 2)); dof = len(N) - 3; pe = np.sqrt(np.diag(cov))
        out["M2"] = dict(f_inf=p[0], f_inf_se=pe[0], a=p[1], a_se=pe[1],
                         alpha=p[2], alpha_se=pe[2], chi2=chi, dof=dof, red=chi / dof)
    except Exception as e:
        out["M2"] = dict(error=str(e))
    try:
        p, cov = curve_fit(lambda N, c, al: c * N ** (-al), N, f, p0=[0.36, 0.0],
                           sigma=se, absolute_sigma=True, maxfev=400000)
        r = (f - p[0] * N ** (-p[1])) / se
        chi = float(np.sum(r ** 2)); dof = len(N) - 2; pe = np.sqrt(np.diag(cov))
        out["H1b"] = dict(c=p[0], c_se=pe[0], alpha=p[1], alpha_se=pe[1],
                          chi2=chi, dof=dof, red=chi / dof,
                          ci95_lo=p[1] - 1.96 * pe[1], ci95_hi=p[1] + 1.96 * pe[1])
    except Exception as e:
        out["H1b"] = dict(error=str(e))
    c_ln = float(np.sum(w * f / np.log(N)) / np.sum(w / np.log(N) ** 2))
    chi = float(np.sum(((f - c_ln / np.log(N)) / se) ** 2)); dof = len(N) - 1
    out["H1c"] = dict(c=c_ln, chi2=chi, dof=dof, red=chi / dof)
    lr = stats.linregress(np.log(N), np.log(f))
    out["slope"] = dict(alpha=-lr.slope, se=lr.stderr,
                        alpha_95_upper=-lr.slope + 1.96 * lr.stderr)
    return out


# ---------------------------------------------------------------- figures
def fig_h1_overview():
    La, fa, sa = def_a_combined()
    Lb, fb, sb = def_b5_combined()
    Lc, fc_, sc = load_summary(DEFB10_PROD)

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    ax = axes[0]
    ax.errorbar(La, fa, yerr=sa, fmt="o", ms=3, color="#1f4e79", capsize=1.5,
                label=r"definition A (cumulative), $N \leq 3 \times 10^5$")
    ax.errorbar(Lb, fb, yerr=sb, fmt="s", ms=3.4, color="#c0392b", capsize=1.5,
                label=r"definition B, $W=5L$")
    ax.errorbar(Lc, fc_, yerr=sc, fmt="^", ms=3.4, color="#e08214", capsize=1.5,
                label=r"definition B, $W=10L$")
    for f_, s_, col in [(wmean(fa, sa), None, "#1f4e79"),
                        (wmean(fb, sb), None, "#c0392b"),
                        (wmean(fc_, sc), None, "#e08214")]:
        ax.axhline(f_[0], color=col, lw=0.7, ls="--", alpha=0.7)
    ax.set_xscale("log")
    ax.set_xlabel(r"system size $N$")
    ax.set_ylabel(r"frozen fraction $f_N$")
    ax.set_ylim(0.335, 0.40)
    ax.legend(loc="lower right")
    ax.set_title("(a) all frozen-fraction data")

    ax = axes[1]
    ma, mae = wmean(fa, sa); mb, mbe = wmean(fb, sb); mc, mce = wmean(fc_, sc)
    ax.errorbar(La, fa - ma, yerr=sa, fmt="o", ms=3, color="#1f4e79", capsize=1.5)
    ax.errorbar(Lb, fb - mb, yerr=sb, fmt="s", ms=3.4, color="#c0392b", capsize=1.5)
    ax.errorbar(Lc, fc_ - mc, yerr=sc, fmt="^", ms=3.4, color="#e08214", capsize=1.5)
    ax.axhline(0, color="k", lw=0.7)
    ax.set_xscale("log")
    ax.set_xlabel(r"system size $N$")
    ax.set_ylabel(r"$f_N-\langle f\rangle$  (per definition)")
    ax.set_title("(b) residual from own constant fit")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_h1_overview.pdf")
    plt.close(fig)

    NUMBERS["h1"] = {
        "defA": dict(zip(["wmean", "wmean_se"], wmean(fa, sa))),
        "defB5": dict(zip(["wmean", "wmean_se"], wmean(fb, sb))),
        "defB10": dict(zip(["wmean", "wmean_se"], wmean(fc_, sc))),
        "defA_fits": fit_models(La, fa, sa),
        "defB5_fits": fit_models(Lb, fb, sb),
        "defB10_fits": fit_models(Lc, fc_, sc),
        "defA_npts": len(La), "defB5_npts": len(Lb), "defB10_npts": len(Lc),
        "defA_Nrange": [float(La.min()), float(La.max())],
        "defB5_Nrange": [float(Lb.min()), float(Lb.max())],
    }


def fig_h1_models():
    N, f, se = def_a_combined()
    fits = fit_models(N, f, se)
    grid = np.logspace(np.log10(N.min()), np.log10(N.max()), 400)

    fig, axes = plt.subplots(2, 1, figsize=(5.0, 4.3), sharex=True,
                             gridspec_kw={"height_ratios": [2.1, 1]})
    ax = axes[0]
    ax.errorbar(N, f, yerr=se, fmt="o", ms=3.2, color="k", capsize=1.5,
                zorder=5, label="data (definition A, 31 points)")
    ax.plot(grid, np.full_like(grid, fits["M1"]["f_inf"]), color="#1f4e79",
            label=r"H1a: $f_\infty$ (const.), $\chi^2_\nu=%.2f$" % fits["M1"]["red"])
    m = fits["M2"]
    ax.plot(grid, m["f_inf"] + m["a"] * grid ** (-m["alpha"]), color="#27ae60", ls="-.",
            label=r"H1a+corr.: $f_\infty+aN^{-\alpha}$, $\chi^2_\nu=%.2f$" % m["red"])
    m = fits["H1b"]
    ax.plot(grid, m["c"] * grid ** (-m["alpha"]), color="#c0392b", ls="--",
            label=r"H1b: $cN^{-\alpha}$, $\alpha=%+.5f$, $\chi^2_\nu=%.2f$" % (m["alpha"], m["red"]))
    m = fits["H1c"]
    ax.plot(grid, m["c"] / np.log(grid), color="#8e44ad", ls=":",
            label=r"H1c: $c/\ln N$, $\chi^2_\nu=%.0f$" % m["red"])
    ax.set_xscale("log")
    ax.set_ylim(0.30, 0.40)
    ax.set_ylabel(r"$f_N$")
    ax.legend(loc="lower left")
    ax.set_title("Model comparison, definition A (cumulative), $N = 100$ to $3 \\times 10^5$")

    ax = axes[1]
    ax.errorbar(N, (f - fits["M1"]["f_inf"]) / se, yerr=1, fmt="o", ms=3.2,
                color="#1f4e79", capsize=1.5, label="vs constant")
    m = fits["M2"]
    ax.errorbar(N, (f - (m["f_inf"] + m["a"] * N ** (-m["alpha"]))) / se, yerr=1,
                fmt="s", ms=3.0, color="#27ae60", capsize=1.5, alpha=0.8,
                label=r"vs $f_\infty+aN^{-\alpha}$")
    ax.axhline(0, color="k", lw=0.7)
    ax.set_xscale("log")
    ax.set_xlabel(r"system size $N$")
    ax.set_ylabel(r"residual / $\sigma$")
    ax.legend(ncol=2, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_h1_models.pdf")
    plt.close(fig)


def fig_h1_settings():
    L5, f5, s5 = load_summary(DEFB5_PROD)
    L10, f10, s10 = load_summary(DEFB10_PROD)
    assert np.array_equal(L5, L10)
    d = f10 - f5
    sd = np.hypot(s5, s10)
    w = 1 / sd ** 2
    dm = float(np.sum(w * d) / np.sum(w)); dse = float(np.sqrt(1 / np.sum(w)))
    lr = stats.linregress(np.log(L5), d)

    fig, axes = plt.subplots(2, 1, figsize=(5.0, 4.1), sharex=True,
                             gridspec_kw={"height_ratios": [2, 1]})
    ax = axes[0]
    ax.errorbar(L5, f5, yerr=s5, fmt="s-", ms=3.4, lw=0.8, color="#c0392b",
                capsize=1.5, label=r"$W=5L$, $M=10$, $c=5$, $n_{\min}=20$")
    ax.errorbar(L10, f10, yerr=s10, fmt="^-", ms=3.4, lw=0.8, color="#e08214",
                capsize=1.5, label=r"$W=10L$, $M=20$, $c=10$, $n_{\min}=40$")
    ax.set_ylabel(r"$f_N$")
    ax.legend(loc="lower right")
    ax.set_title("Same $N$ grid, two estimator settings (four parameters changed at once)")

    ax = axes[1]
    ax.errorbar(L5, d, yerr=sd, fmt="o", ms=3.2, color="0.25", capsize=1.5)
    ax.axhline(0, color="k", lw=0.7)
    ax.axhline(dm, color="#c0392b", ls="--", lw=0.9,
               label=r"weighted mean $=%+.5f\pm%.5f$ (%.1f$\sigma$)" % (dm, dse, abs(dm / dse)))
    ax.fill_between([L5.min(), L5.max()], dm - dse, dm + dse, color="#c0392b", alpha=0.15)
    ax.set_xlabel(r"system size $N$")
    ax.set_ylabel(r"$f_N(10L)-f_N(5L)$")
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_h1_settings.pdf")
    plt.close(fig)

    NUMBERS["settings"] = dict(shift_mean=dm, shift_se=dse, sigma=abs(dm / dse),
                               n_down=int(np.sum(d < 0)), n_total=len(d),
                               slope_vs_lnN=float(lr.slope), slope_se=float(lr.stderr),
                               slope_p=float(lr.pvalue))


def fig_h2_pmf():
    gaps = {L: np.load(GAP_PROD / f"L{L}_gaps.npy") for L in GAP_L}
    cmap = plt.cm.viridis(np.linspace(0, 0.92, len(GAP_L)))
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))

    for ax, logx, title in [(axes[0], False, r"(a) semi-log: straight $\Rightarrow$ exponential"),
                            (axes[1], True, r"(b) log-log: straight $\Rightarrow$ power law")]:
        for L, c in zip(GAP_L, cmap):
            v, n = np.unique(gaps[L], return_counts=True)
            ax.plot(v, n / len(gaps[L]), "o", ms=2.2, color=c, alpha=0.85, label=f"$L={L}$")
        if logx:
            ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(r"active-region length $\ell$ (sites)")
        ax.set_ylabel(r"$P_L(\ell)$")
        ax.set_title(title)
    # exponential reference fitted on the largest L, full range
    L = 12800
    v, n = np.unique(gaps[L], return_counts=True)
    p = n / len(gaps[L])
    lr = stats.linregress(v, np.log(p))
    lam = -1 / lr.slope
    xs = np.linspace(4, v.max(), 200)
    axes[0].plot(xs, np.exp(lr.intercept + lr.slope * xs), "k--", lw=1.0,
                 label=r"exp. fit $L{=}12800$: $\lambda=%.1f$" % lam)
    axes[0].legend(ncol=2, fontsize=6.4, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_h2_pmf.pdf")
    plt.close(fig)


def fig_h2_collapse():
    gaps = {L: np.load(GAP_PROD / f"L{L}_gaps.npy") for L in GAP_L}
    cmap = plt.cm.viridis(np.linspace(0, 0.92, len(GAP_L)))
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    for L, c in zip(GAP_L, cmap):
        a = gaps[L]; m = a.mean()
        v, n = np.unique(a, return_counts=True)
        ax.plot(v / m, m * n / len(a), "o", ms=2.4, color=c, alpha=0.85, label=f"$L={L}$")
    xs = np.linspace(0.25, 8, 200)
    ax.plot(xs, np.exp(-xs) / (1 - np.exp(-1)) * 0 + np.exp(-xs), "k--", lw=1.0,
            label=r"$e^{-x}$ (memoryless reference)")
    ax.set_yscale("log")
    ax.set_xlabel(r"$\ell/\langle\ell\rangle_L$")
    ax.set_ylabel(r"$\langle\ell\rangle_L\,P_L(\ell)$")
    ax.set_ylim(1e-4, 1)
    ax.legend(ncol=2, fontsize=6.6)
    ax.set_title("Rescaled active-region-length distribution")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_h2_collapse.pdf")
    plt.close(fig)


def fig_h2_forbidden():
    gaps = {L: np.load(GAP_PROD / f"L{L}_gaps.npy") for L in GAP_L}
    cmap = plt.cm.viridis(np.linspace(0, 0.92, len(GAP_L)))
    ells = np.arange(0, 15)
    fig, ax = plt.subplots(figsize=(5.4, 3.0))
    width = 0.105
    for k, (L, c) in enumerate(zip(GAP_L, cmap)):
        cnt = np.array([np.sum(gaps[L] == e) for e in ells], float)
        ax.bar(ells + (k - 3.5) * width, np.maximum(cnt, 0.4), width=width,
               color=c, label=f"$L={L}$", log=True)
    for e in [0, 1, 2, 3, 5]:
        ax.axvspan(e - 0.5, e + 0.5, color="#c0392b", alpha=0.10, zorder=0)
    ax.set_xticks(ells)
    ax.set_ylim(0.4, 4e3)
    ax.set_xlabel(r"active-region length $\ell$")
    ax.set_ylabel("pooled count (log scale)")
    ax.set_title(r"Shaded $\ell$: \textbf{zero} counts at every $L$ ($\ell=0$ discarded by construction)"
                 if plt.rcParams.get("text.usetex") else
                 "Shaded $\\ell$: zero counts at every $L$ ($\\ell=0$ discarded by construction)")
    ax.legend(ncol=4, fontsize=6.4, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_h2_forbidden.pdf")
    plt.close(fig)

    NUMBERS["forbidden"] = {
        str(L): {str(e): int(np.sum(gaps[L] == e)) for e in range(0, 13)} for L in GAP_L}


def fig_h2_vs_L():
    rows = sorted(json.load(open(GAP_PROD / "summary.json")), key=lambda r: r["L"])
    L = np.array([r["L"] for r in rows], float)
    mean = np.array([r["gap_length_mean"] for r in rows])
    std = np.array([r["gap_length_std"] for r in rows])
    npool = np.array([r["n_pooled_gaps"] for r in rows], float)
    zrate = np.array([r["zero_gap_rate"] for r in rows])
    gaps = {int(x): np.load(GAP_PROD / f"L{int(x)}_gaps.npy") for x in L}

    lam, alpha, r2e, r2p, lam_t, alpha_t = [], [], [], [], [], []
    for x in L:
        a = gaps[int(x)]
        v, n = np.unique(a, return_counts=True)
        p = n / len(a)
        fe = stats.linregress(v, np.log(p)); fp = stats.linregress(np.log(v), np.log(p))
        lam.append(-1 / fe.slope); alpha.append(-fp.slope)
        r2e.append(fe.rvalue ** 2); r2p.append(fp.rvalue ** 2)
        m = v >= 15
        fe2 = stats.linregress(v[m], np.log(p[m])); fp2 = stats.linregress(np.log(v[m]), np.log(p[m]))
        lam_t.append(-1 / fe2.slope); alpha_t.append(-fp2.slope)
    lam, alpha, r2e, r2p = map(np.array, (lam, alpha, r2e, r2p))

    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.5))
    ax = axes[0]
    ax.errorbar(L, mean, yerr=std / np.sqrt(npool), fmt="o-", ms=3.4, color="#1f4e79", capsize=1.5)
    ax.set_xscale("log"); ax.set_xlabel("$L$"); ax.set_ylabel(r"$\langle\ell\rangle_L$")
    ax.set_ylim(14.5, 17); ax.set_title("(a) mean nonzero gap")
    ax = axes[1]
    ax.plot(L, zrate, "o-", ms=3.4, color="#c0392b")
    ax.set_xscale("log"); ax.set_xlabel("$L$"); ax.set_ylabel(r"$P(\ell=0)$")
    ax.set_ylim(0.85, 0.92); ax.set_title("(b) zero-gap (adjacent-frozen) rate")
    ax = axes[2]
    ax.plot(L, lam, "o-", ms=3.4, color="#1f4e79", label=r"$\lambda$ (exp., full range)")
    ax.plot(L, alpha * 4, "s--", ms=3.4, color="#c0392b", label=r"$4\alpha$ (power law)")
    ax.set_xscale("log"); ax.set_xlabel("$L$"); ax.set_ylabel("fitted tail parameter")
    ax.legend(fontsize=6.6); ax.set_title("(c) fitted decay parameters")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_h2_vs_L.pdf")
    plt.close(fig)

    NUMBERS["h2"] = dict(
        L=L.tolist(), mean=mean.tolist(), std=std.tolist(), zero_rate=zrate.tolist(),
        n_pooled=npool.tolist(), lam_full=lam.tolist(), alpha_full=alpha.tolist(),
        r2_exp_full=r2e.tolist(), r2_pow_full=r2p.tolist(),
        lam_tail=lam_t, alpha_tail=alpha_t,
        snapshot_f=[r["frozen_fraction_snapshot_mean"] for r in rows],
        snapshot_f_se=[r["frozen_fraction_snapshot_se"] for r in rows],
        n_realizations=[r["n_realizations"] for r in rows])


def fig_wdep():
    d = newest("w_dependence_w_dependence_2*")
    if d is None:
        print("  [skip] no w_dependence run found")
        return
    rows = json.load(open(d / "summary.json"))
    Ls = sorted({r["L"] for r in rows})
    fig, ax = plt.subplots(figsize=(5.0, 3.3))
    cols = ["#1f4e79", "#c0392b", "#e08214", "#27ae60"]
    out = {}
    for L, c in zip(Ls, cols):
        rr = sorted([r for r in rows if r["L"] == L], key=lambda r: r["W_multiplier"])
        m = np.array([r["W_multiplier"] for r in rr], float)
        f = np.array([r["f_B_mean"] for r in rr])
        s = np.array([r["f_B_se"] for r in rr])
        ax.errorbar(m, f, yerr=s, fmt="o-", ms=3.6, color=c, capsize=1.5,
                    label=f"$L={L}$ ($n={rr[0]['n_samples']}$)")
        out[str(L)] = dict(W_mult=m.tolist(), f=f.tolist(), se=s.tolist())
    La, fa, sa = def_a_combined()
    ma, mae = wmean(fa, sa)
    ax.axhline(ma, color="k", ls="--", lw=0.9,
               label=r"definition A (cumulative), $\langle f\rangle=%.4f$" % ma)
    ax.axvline(5, color="0.5", lw=0.7, ls=":")
    ax.axvline(10, color="0.5", lw=0.7, ls=":")
    ax.text(5, ax.get_ylim()[1], " production\n $W=5L$", fontsize=6.2, va="top", color="0.35")
    ax.set_xscale("log")
    ax.set_xlabel(r"window multiplier $W/L$")
    ax.set_ylabel(r"$f_B(W)$")
    ax.legend(fontsize=7)
    ax.set_title(r"$W$-dependence of definition B (all $W$ from the same trajectories)")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_wdep.pdf")
    plt.close(fig)
    NUMBERS["wdep"] = out
    NUMBERS["wdep_dir"] = d.name


def fig_static_bfs():
    d = newest("static_frozen_*")
    if d is None:
        print("  [skip] no static_frozen run found")
        return
    rows = sorted(json.load(open(d / "summary.json")), key=lambda r: r["L"])
    L = np.array([r["L"] for r in rows], float)
    f_all = np.array([r["f_static_mean"] for r in rows])
    s_all = np.array([r["f_static_se"] for r in rows])
    med = np.array([r["sector_size_median"] for r in rows])

    # exact frozen fraction with fully-jammed configs removed (the dynamical
    # estimator structurally cannot sample those), and the jammed fraction
    f_ex, s_ex, jam = [], [], []
    for x in L:
        a = np.load(d / f"L{int(x)}_samples.npy")
        jam.append(float(np.mean(a == 1.0)))
        b = a[a < 1.0]
        f_ex.append(b.mean()); s_ex.append(b.std(ddof=1) / np.sqrt(len(b)))
    f_ex, s_ex, jam = np.array(f_ex), np.array(s_ex), np.array(jam)

    dw = newest("w_dependence_w_dependence_small_*")
    wl, wf, ws = [], [], []
    if dw is not None:
        wr = json.load(open(dw / "summary.json"))
        for r in sorted([q for q in wr if q["W_multiplier"] == 500], key=lambda q: q["L"]):
            wl.append(r["L"]); wf.append(r["f_B_mean"]); ws.append(r["f_B_se"])
    wl, wf, ws = np.array(wl, float), np.array(wf), np.array(ws)

    fig, axes = plt.subplots(1, 3, figsize=(7.4, 2.6))
    ax = axes[0]
    ax.errorbar(L, f_all, yerr=s_all, fmt="o-", ms=3.4, color="#8e44ad", capsize=1.5,
                label=r"exact $f_{\rm stat}$, all configs")
    ax.errorbar(L, f_ex, yerr=s_ex, fmt="s--", ms=3.2, color="#2c3e50", capsize=1.5,
                label=r"exact, jammed removed")
    if len(wl):
        ax.errorbar(wl, wf, yerr=ws, fmt="^", ms=4.0, color="#c0392b", capsize=1.5,
                    label=r"dynamical $f_B(W\!=\!500L)$".replace("\\!", ""))
    La, fa, sa = def_a_combined()
    ax.axhline(wmean(fa, sa)[0], color="k", ls=":", lw=0.9,
               label=r"def. A, $N\geq100$: %.3f" % wmean(fa, sa)[0])
    ax.set_xlabel(r"$L$"); ax.set_ylabel("frozen fraction")
    ax.legend(fontsize=5.8, loc="lower right")
    ax.set_title("(a) exact vs. dynamical estimator")

    ax = axes[1]
    ax.semilogy(L, np.maximum(jam, 1e-4), "o-", ms=3.4, color="#c0392b")
    ax.set_xlabel(r"$L$"); ax.set_ylabel("fraction fully jammed")
    ax.set_title("(b) jammed configs (sector $=1$)")

    ax = axes[2]
    from scipy.special import gammaln
    ax.semilogy(L, med, "o-", ms=3.4, color="#1f4e79", label="median Krylov sector")
    ax.semilogy(L, np.exp(gammaln(L + 1) - 2 * gammaln(L / 2 + 1)), "--", color="0.45",
                label=r"all half-filled states $\binom{L}{L/2}$")
    ax.set_xlabel(r"$L$"); ax.set_ylabel("number of states")
    ax.legend(fontsize=6.2, loc="upper left")
    ax.set_title("(c) strong fragmentation")
    fig.tight_layout()
    fig.savefig(FIGS / "fig_static_bfs.pdf")
    plt.close(fig)

    Bm = np.polyfit(L, np.log(med), 1)[0]
    Bc = np.polyfit(L, gammaln(L + 1) - 2 * gammaln(L / 2 + 1), 1)[0]
    val = []
    for x, y, e in zip(wl, wf, ws):
        i = int(np.where(L == x)[0][0])
        diff = y - f_ex[i]
        val.append(dict(L=float(x), exact_excl=float(f_ex[i]), exact_excl_se=float(s_ex[i]),
                        f_B500=float(y), f_B500_se=float(e), diff=float(diff),
                        sigma=float(diff / np.hypot(s_ex[i], e))))
    chi2 = float(sum(v["sigma"] ** 2 for v in val))
    NUMBERS["static"] = dict(L=L.tolist(), f_all=f_all.tolist(), se_all=s_all.tolist(),
                             f_excl=f_ex.tolist(), se_excl=s_ex.tolist(),
                             jammed_frac=jam.tolist(), median_sector=med.tolist(),
                             n_samples=[r["n_samples"] for r in rows],
                             n_over_cap=[r["n_over_cap"] for r in rows], dir=d.name,
                             sector_growth_base=float(np.exp(Bm)),
                             total_growth_base=float(np.exp(Bc)),
                             ratio_base=float(np.exp(Bm - Bc)),
                             validation=val, validation_chi2=chi2,
                             validation_red_chi2=chi2 / max(len(val), 1))


def cross_checks():
    Lg, fg, sg = load_summary(GAP_PROD, "frozen_fraction_snapshot_mean",
                              "frozen_fraction_snapshot_se")
    Lb, fb, sb = def_b5_combined()
    rows = []
    for L, f, s in zip(Lg, fg, sg):
        j = np.where(Lb == L)[0]
        if len(j):
            j = j[0]
            rows.append(dict(L=float(L), f_gap=float(f), se_gap=float(s),
                             f_h1=float(fb[j]), se_h1=float(sb[j]),
                             nsigma=float((f - fb[j]) / np.hypot(s, sb[j]))))
    NUMBERS["crosscheck_gap_vs_h1"] = rows

    # identity check <l>_nonzero vs frozen fraction, accounting for discarded zeros
    g = json.load(open(GAP_PROD / "summary.json"))
    ident = []
    for r in sorted(g, key=lambda r: r["L"]):
        fsnap = r["frozen_fraction_snapshot_mean"]
        # all gaps (incl. zeros): mean = (1-f)/f
        pred_all = (1 - fsnap) / fsnap
        got_all = r["n_raw_gaps"] and (r["gap_length_mean"] * r["n_pooled_gaps"]) / r["n_raw_gaps"]
        ident.append(dict(L=r["L"], pred_mean_all_gaps=pred_all, obs_mean_all_gaps=got_all,
                          ratio=got_all / pred_all))
    NUMBERS["identity_check"] = ident


def main():
    print("generating figures ->", FIGS)
    for fn in (fig_h1_overview, fig_h1_models, fig_h1_settings,
               fig_h2_pmf, fig_h2_collapse, fig_h2_forbidden, fig_h2_vs_L,
               fig_wdep, fig_static_bfs):
        print("  ", fn.__name__)
        fn()
    cross_checks()
    with open(PROC / "progress_numbers.json", "w") as f:
        json.dump(NUMBERS, f, indent=2, default=float)
    print("wrote", PROC / "progress_numbers.json")


if __name__ == "__main__":
    main()
