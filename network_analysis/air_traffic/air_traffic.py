import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
#from matplotlib.colors import Normalize
#from matplotlib.cm import ScalarMappable
#import matplotlib.ticker as ticker
from collections import Counter
import warnings
import community as community_louvain
#from networkx.algorithms.community import greedy_modularity_communities, girvan_newman
from pyvis.network import Network
from scipy.stats import pearsonr
import folium

warnings.filterwarnings("ignore")

plt.rcParams.update({
    "figure.facecolor":  "#0d1117",
    "axes.facecolor":    "#0d1117",
    "axes.edgecolor":    "#30363d",
    "axes.labelcolor":   "#e6edf3",
    "xtick.color":       "#8b949e",
    "ytick.color":       "#8b949e",
    "text.color":        "#e6edf3",
    "grid.color":        "#21262d",
    "grid.linewidth":    0.6,
    "font.family":       "monospace",
    "figure.dpi":        130,
})

ACCENT   = "#58a6ff"
ACCENT2  = "#f78166"
ACCENT3  = "#3fb950"
ACCENT4  = "#d2a8ff"
BG       = "#0d1117"
PANEL    = "#161b22"

def section(title):
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print(f"{'═'*60}")

section("1. DATA LOADING & PREPARATION (Weighted)")

routes_df = pd.read_parquet("./data/routes.parquet")
airports = pd.read_parquet("./data/airports.parquet")

routes_df = routes_df[(routes_df["source"] != "\\N") & (routes_df["dest"] != "\\N")]
routes_df = routes_df.dropna(subset=["source", "dest"])

routes_weighted = routes_df.groupby(["source", "dest"]).size().reset_index(name='weight')

print(f"Original routes count : {len(routes_df):,}")
print(f"Unique routes (weighted): {len(routes_weighted):,}")
print(f"Airports count        : {airports.shape[0]:,}")

section("2. GRAPH CONSTRUCTION")

G = nx.from_pandas_edgelist(routes_weighted, source="source", target="dest",
                             edge_attr="weight", create_using=nx.DiGraph())
UG = G.to_undirected()

print(f"Nodes  : {G.number_of_nodes():,}")
print(f"Edges  : {G.number_of_edges():,}")
print(f"Density: {nx.density(G):.6f}")
print(f"Avg degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")

section("3. CENTRALITY METRICS")

deg_c   = nx.degree_centrality(G)
in_deg  = nx.in_degree_centrality(G)
out_deg = nx.out_degree_centrality(G)
bet_c   = nx.betweenness_centrality(G, normalized=True)
clo_c   = nx.closeness_centrality(G)
eig_c   = nx.eigenvector_centrality(G, max_iter=500)
pr      = nx.pagerank(G, alpha=0.85, weight='weight')

def top10(d, label):
    top = sorted(d.items(), key=lambda x: x[1], reverse=True)[:10]
    print(f"\n▶ Top 10 — {label}")
    for i, (n, v) in enumerate(top, 1):
        bar = "█" * int(v * 300)
        print(f"  {i:2}. {n:6}  {v:.4f}  {bar}")
    return [n for n, _ in top]

top_deg = top10(deg_c,  "Degree Centrality")
top_bet = top10(bet_c,  "Betweenness Centrality")
top_pr  = top10(pr,     "PageRank (Weighted)")

section("4. SMALL-WORLD PHENOMENON (Watts–Strogatz)")

largest_cc = max(nx.connected_components(UG), key=len)
SG = UG.subgraph(largest_cc).copy()
n, m = SG.number_of_nodes(), SG.number_of_edges()
k_avg = int(2 * m / n)

avg_path = nx.average_shortest_path_length(SG)
clust_coeff = nx.average_clustering(SG)

ER = nx.erdos_renyi_graph(n=n, p=nx.density(SG), seed=42)
er_path = nx.average_shortest_path_length(ER.subgraph(max(nx.connected_components(ER), key=len)))
er_clust = nx.average_clustering(ER)

WS = nx.watts_strogatz_graph(n=n, k=max(k_avg, 2), p=0.1, seed=42)
ws_path = nx.average_shortest_path_length(WS)
ws_clust = nx.average_clustering(WS)

sigma = (clust_coeff / er_clust) / (avg_path / er_path)

print(f"\n  Real graph  — L={avg_path:.3f}, C={clust_coeff:.4f}")
print(f"  ✦ Small-World Index (σ) = {sigma:.2f}  (σ >> 1 → small-world!)")
print(f"  ✦ Diameter             = {nx.diameter(SG)}")

section("5. ECCENTRICITY & DIAMETER")

ecc = nx.eccentricity(SG)
radius = nx.radius(SG)
diam = nx.diameter(SG)

print(f"  Radius   : {radius}")
print(f"  Diameter : {diam}")

section("6. COMMUNITY DETECTION")

louvain_part = community_louvain.best_partition(UG)
louvain_mod = community_louvain.modularity(louvain_part, UG)
n_louvain = max(louvain_part.values()) + 1

print(f"  Louvain communities count : {n_louvain}")
print(f"  Louvain modularity        : {louvain_mod:.4f}")

section("7. ROBUSTNESS TEST")

def robustness_test(G_orig, strategy="betweenness", steps=40):
    G_c = G_orig.to_undirected().copy()
    sizes = []
    for i in range(steps):
        sizes.append(nx.number_connected_components(G_c))
        scores = nx.betweenness_centrality(G_c) if strategy == "betweenness" else dict(G_c.degree())
        if not scores: break
        top = max(scores, key=scores.get)
        G_c.remove_node(top)
    return sizes

rob_bet = robustness_test(G, "betweenness")
rob_deg = robustness_test(G, "degree")
critical = list(nx.articulation_points(UG))
print(f"  Critical nodes count: {len(critical)}")

section("8. VISUALIZATIONS GENERATION...")

fig = plt.figure(figsize=(22, 16), facecolor=BG)
fig.suptitle("✈  GLOBAL FLIGHT NETWORK — Graph Analytics Dashboard", fontsize=20, color=ACCENT, fontweight="bold", y=0.98)
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.55, wspace=0.45, left=0.06, right=0.97, top=0.93, bottom=0.06)

def styled_ax(ax, title):
    ax.set_facecolor(PANEL)
    ax.set_title(title, color=ACCENT, fontsize=10, pad=8, fontweight="bold")
    ax.spines[:].set_color("#30363d")
    ax.tick_params(colors="#8b949e", labelsize=8)
    ax.grid(True, alpha=0.3)

ax1 = fig.add_subplot(gs[0, 0]); styled_ax(ax1, "① Degree Distribution (log–log)")
deg_vals = sorted([d for _, d in G.degree()], reverse=True)
cnt = Counter(deg_vals); xs, ys = zip(*sorted(cnt.items()))
ax1.scatter(xs, ys, color=ACCENT, s=12, alpha=0.7); ax1.set_xscale("log"); ax1.set_yscale("log")
log_x, log_y = np.log(np.array(xs, dtype=float)), np.log(np.array(ys, dtype=float))
coeffs = np.polyfit(log_x[np.isfinite(log_x) & np.isfinite(log_y)], log_y[np.isfinite(log_x) & np.isfinite(log_y)], 1)
ax1.plot(xs, np.exp(coeffs[1]) * np.array(xs)**coeffs[0], color=ACCENT2, lw=1.5, label=f"γ≈{-coeffs[0]:.2f}")
ax1.legend(fontsize=8, facecolor=PANEL)

ax2 = fig.add_subplot(gs[0, 1]); styled_ax(ax2, "② Top 10 — Degree Centrality")
top10_d = sorted(deg_c.items(), key=lambda x: x[1], reverse=True)[:10]
ax2.barh([x[0] for x in top10_d][::-1], [x[1] for x in top10_d][::-1], color=ACCENT)

ax3 = fig.add_subplot(gs[0, 2]); styled_ax(ax3, "③ PageRank vs Betweenness")
common = list(G.nodes()); pr_v = [pr[n] for n in common]; bet_v = [bet_c[n] for n in common]
ax3.scatter(pr_v, bet_v, s=8, alpha=0.4, color=ACCENT4)
r, _ = pearsonr(pr_v, bet_v); ax3.text(0.05, 0.92, f"r = {r:.3f}", transform=ax3.transAxes, color=ACCENT3)

ax4 = fig.add_subplot(gs[1, 0]); styled_ax(ax4, "④ Small-World Comparison")
ax4.bar(["Real", "ER", "WS"], [avg_path, er_path, ws_path], color=[ACCENT, "#30363d", "#555"])
ax4.text(0.5, 0.1, f"σ = {sigma:.2f}", transform=ax4.transAxes, ha="center", color=ACCENT2, fontweight="bold")

ax5 = fig.add_subplot(gs[1, 1]); styled_ax(ax5, "⑤ Robustness Test")
ax5.plot(rob_bet, color=ACCENT2, label="Betweenness"); ax5.plot(rob_deg, color=ACCENT3, label="Degree")
ax5.legend(fontsize=7, facecolor=PANEL)

ax6 = fig.add_subplot(gs[1, 2]); styled_ax(ax6, "⑥ Eccentricity Distribution")
ax6.hist(list(ecc.values()), bins=10, color=ACCENT4, alpha=0.7)

ax7 = fig.add_subplot(gs[2, 0]); styled_ax(ax7, "⑦ Louvain Community Sizes")
comm_counts = Counter(louvain_part.values()); ax7.bar(range(len(comm_counts)), sorted(comm_counts.values(), reverse=True), color=ACCENT3)

ax8 = fig.add_subplot(gs[2, 1]); styled_ax(ax8, "⑧ In-degree vs Out-degree")
ax8.scatter(list(in_deg.values()), list(out_deg.values()), s=8, alpha=0.3, color=ACCENT)

ax9 = fig.add_subplot(gs[2, 2]); ax9.axis("off")
sum_txt = [f"Nodes: {G.number_of_nodes()}", f"Edges: {G.number_of_edges()}", f"L: {avg_path:.3f}", f"C: {clust_coeff:.4f}", f"σ: {sigma:.2f}", f"Modularity: {louvain_mod:.3f}"]
for i, t in enumerate(sum_txt): ax9.text(0.1, 0.85 - i*0.12, t, fontsize=10, color=ACCENT)

plt.savefig("viz1_dashboard.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("  ✓ viz1_dashboard.png")

section("9. GEOGRAPHIC MAP GENERATION")

airports_clean = airports.dropna(subset=['lat', 'lon', 'iata']).drop_duplicates(subset=['iata'])
coords = airports_clean.set_index('iata')[['lat', 'lon']].to_dict('index')

m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")

top_routes = routes_weighted.sort_values('weight', ascending=False).head(700)

for _, row in top_routes.iterrows():
    if row['source'] in coords and row['dest'] in coords:
        p1 = [coords[row['source']]['lat'], coords[row['source']]['lon']]
        p2 = [coords[row['dest']]['lat'], coords[row['dest']]['lon']]
        folium.PolyLine(locations=[p1, p2], weight=row['weight'] * 0.4, color=ACCENT, opacity=0.15).add_to(m)

top_nodes_150 = sorted(deg_c, key=deg_c.get, reverse=True)[:150]
for iata in top_nodes_150:
    if iata in coords:
        folium.CircleMarker(location=[coords[iata]['lat'], coords[iata]['lon']], radius=deg_c[iata] * 120, color=ACCENT2, fill=True, popup=f"<b>{iata}</b>").add_to(m)

m.save("viz5_geography_map.html")
print(" ✓ viz5_geography_map.html saved!")

section("10. INTERACTIVE NETWORK (PYVIS)")

net = Network(height="800px", width="100%", bgcolor=BG, font_color="white", directed=True)
top_nodes_300 = sorted(deg_c, key=deg_c.get, reverse=True)[:300]
vis_set = set(top_nodes_300)
colors = ["#58a6ff", "#f78166", "#3fb950", "#d2a8ff", "#e3b341", "#f06292"]

for n in top_nodes_300:
    net.add_node(n, label=n, size=deg_c[n]*600, color=colors[louvain_part.get(n, 0) % len(colors)])

for u, v, d in G.edges(data=True):
    if u in vis_set and v in vis_set:
        net.add_edge(u, v, value=d['weight'], color="#ffffff22")

net.write_html("viz4_interactive.html")
print(" ✓ viz4_interactive.html")

print(f"""
┌───────────────────────────────────────────────────────────────┐
│        FLIGHT NETWORK — COMPLETE GRAPH ANALYSIS               │
├───────────────────────────────────────────────────────────────┤
│ Nodes                : {G.number_of_nodes():>8,}              │
│ Edges                : {G.number_of_edges():>8,}              │
│ Density              : {nx.density(G):.6f}                    │
│ Avg Path Length (L)  : {avg_path:.3f}                         │
│ Clustering Coeff (C) : {clust_coeff:.4f}                      │
│ Small-World (σ)      : {sigma:.2f}   (σ >> 1 → SMALL-WORLD)   │
│ Diameter             : {diam}                                 │
│ Radius               : {radius}                               │
│ Louvain Modularity   : {louvain_mod:.4f}  ({n_louvain} comm.) │
│ Critical Nodes       : {len(critical):>8,}                    │
│ Power-law Exponent γ : {-coeffs[0]:.2f}  (scale-free)         │
├───────────────────────────────────────────────────────────────┤
│ Output Files:                                                 │
│  - dashboard.png              → analytics dashboard           │
│  - viz2_community_graph.png   → Louvain community graph       │
│  - ba_vs_real.png             → degree distribution compare   │
│  - interactive_network.html   → interactive network           │
│  - flight_map.html            → geographic route map          │
└───────────────────────────────────────────────────────────────┘
""")