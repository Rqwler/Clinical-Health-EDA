"""
================================================================
  FITNESS DATASET — INTERACTIVE EXPLORATORY DATA ANALYSIS
  Charts displayed one by one in your browser / GUI window.
  Run:  python fitness_eda_interactive.py
================================================================
"""

# ── 0. IMPORTS ────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import warnings

warnings.filterwarnings("ignore")

# Plotly will open each chart in a new browser tab
pio.renderers.default = "browser"

# ── COLOUR PALETTE ────────────────────────────────────────────
PALETTE = {
    "primary" : "#00D4FF",   # cyan
    "accent1" : "#FF6B6B",   # coral
    "accent2" : "#FFD93D",   # yellow
    "accent3" : "#6BCB77",   # green
    "accent4" : "#9B59B6",   # purple
    "bg"      : "#0D1117",   # dark bg
    "card"    : "#161B22",   # card bg
    "text"    : "#E6EDF3",   # light text
}
LIFESTYLE_COLORS = {"Active": "#6BCB77", "Sedentary": "#FF6B6B", "Athlete": "#00D4FF"}
FITNESS_COLORS   = {"Fit": "#6BCB77",   "Moderate": "#FFD93D",  "Unfit": "#FF6B6B"}

# ── HELPER: pause between charts ──────────────────────────────
CHART_NUM = [0]

def show_plotly(fig, title=""):
    """Display a Plotly figure in the browser, then wait for Enter."""
    CHART_NUM[0] += 1
    print(f"\n{'─'*60}")
    print(f"  Chart {CHART_NUM[0]:02d}  │  {title}")
    print(f"{'─'*60}")
    fig.show()
    input("  ▶  Press  Enter  to continue to the next chart …\n")

def show_mpl(title=""):
    """Display the current matplotlib figure, then wait for Enter."""
    CHART_NUM[0] += 1
    print(f"\n{'─'*60}")
    print(f"  Chart {CHART_NUM[0]:02d}  │  {title}")
    print(f"{'─'*60}")
    plt.tight_layout()
    plt.show(block=False)
    input("  ▶  Press  Enter  to continue to the next chart …\n")
    plt.close("all")

# ── 1. LOAD DATA ──────────────────────────────────────────────
print("\n📂  Loading dataset …")
df = pd.read_csv("1779623154544_fitness_dataset.csv")   # ← adjust path if needed

# Derived columns
bins   = [17, 25, 35, 45, 55, 65]
labels = ["18-25", "26-35", "36-45", "46-55", "56-64"]
df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels)

df["stress_bin"] = pd.cut(df["stress_level"], bins=5,
                           labels=["1-3","3-5","5-6","6-8","8-10"])
df["sleep_bin"]  = pd.cut(df["sleep_quality"], bins=5,
                           labels=["Very Low","Low","Medium","High","Very High"])
df["workout_bin"] = df["workouts_per_week"].astype(str) + " days"
df["diet_bin"]    = pd.cut(df["diet_quality"], bins=[0,3,6,8,10],
                            labels=["Poor (1-3)","Fair (3-6)","Good (6-8)","Excellent (8-10)"])

# Representative sample for scatter / 3-D plots
SAMPLE = df.sample(20_000, random_state=42)

print(f"✅  Loaded {len(df):,} rows  —  {len(SAMPLE):,}-row sample for scatter plots.")
print(f"\n🗂   Total charts to display: 20")
print(f"     Each chart opens in your browser (Plotly) or a window (matplotlib).")
print(f"     Press Enter in this terminal to advance to the next chart.\n")
input("  ▶  Press  Enter  to start …\n")


# ═══════════════════════════════════════════════════════════════
# SECTION A — OVERVIEW DASHBOARD  (matplotlib)
# ═══════════════════════════════════════════════════════════════
num_cols = ["age","steps_per_day","active_minutes","sleep_hours",
            "sleep_quality","stress_level","bmi","heart_rate_resting",
            "heart_rate_avg","workouts_per_week","diet_quality",
            "hydration_liters","consistency_score"]

fig = plt.figure(figsize=(24, 28), facecolor=PALETTE["bg"])
fig.suptitle("FITNESS DATASET  •  OVERVIEW DASHBOARD",
             fontsize=26, color=PALETTE["primary"], fontweight="bold", y=0.98)

gs = gridspec.GridSpec(5, 4, figure=fig, hspace=0.55, wspace=0.38)

# KPI cards
stat_colors = [PALETTE["primary"], PALETTE["accent3"], PALETTE["accent2"], PALETTE["accent1"]]
stats = [
    ("1,000,000", "Total Records"),
    ("41 yrs",    "Avg Age"),
    ("7,006",     "Avg Steps / Day"),
    ("24.2",      "Avg BMI"),
]
for i, (val, label) in enumerate(stats):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor(PALETTE["card"])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    c = stat_colors[i]
    rect = FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                          boxstyle="round,pad=0.04",
                          linewidth=2, edgecolor=c, facecolor=PALETTE["card"])
    ax.add_patch(rect)
    ax.text(0.5, 0.65, val, ha="center", va="center", fontsize=28, color=c, fontweight="bold")
    ax.text(0.5, 0.28, label, ha="center", va="center", fontsize=11, color=PALETTE["text"])

# Lifestyle pie
ax = fig.add_subplot(gs[1, 0])
ax.set_facecolor(PALETTE["bg"])
lc = df["lifestyle_category"].value_counts()
wedges, texts, autotexts = ax.pie(
    lc.values, labels=lc.index, autopct="%1.1f%%",
    colors=[LIFESTYLE_COLORS[k] for k in lc.index],
    startangle=140, pctdistance=0.82,
    wedgeprops=dict(linewidth=2, edgecolor=PALETTE["bg"]))
for t in texts:      t.set_color(PALETTE["text"]); t.set_fontsize(10)
for t in autotexts:  t.set_color(PALETTE["bg"]); t.set_fontsize(9); t.set_fontweight("bold")
ax.set_title("Lifestyle Category", color=PALETTE["primary"], fontsize=13)

# Fitness level bar
ax = fig.add_subplot(gs[1, 1])
ax.set_facecolor(PALETTE["bg"])
fc = df["fitness_level"].value_counts()
bars = ax.bar(fc.index, fc.values,
              color=[FITNESS_COLORS[k] for k in fc.index],
              edgecolor=PALETTE["bg"], linewidth=1.5)
for b in bars:
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 5000,
            f"{b.get_height()/1e3:.0f}K",
            ha="center", va="bottom", color=PALETTE["text"], fontsize=10)
ax.set_facecolor(PALETTE["bg"])
ax.set_title("Fitness Level", color=PALETTE["primary"], fontsize=13)
ax.tick_params(colors=PALETTE["text"]); ax.spines[:].set_visible(False)
ax.set_ylim(0, fc.max() * 1.15)

# Age distribution
ax = fig.add_subplot(gs[1, 2:])
ax.set_facecolor(PALETTE["bg"])
ax.hist(df["age"], bins=47, color=PALETTE["primary"], edgecolor=PALETTE["bg"], alpha=0.85)
ax.axvline(df["age"].mean(), color=PALETTE["accent2"], linestyle="--", lw=2,
           label=f"Mean = {df['age'].mean():.1f}")
ax.legend(facecolor=PALETTE["card"], labelcolor=PALETTE["text"])
ax.set_title("Age Distribution", color=PALETTE["primary"], fontsize=13)
ax.set_xlabel("Age", color=PALETTE["text"])
ax.tick_params(colors=PALETTE["text"]); ax.spines[:].set_visible(False)

# Numeric histograms
plot_cols = [
    ("steps_per_day",      PALETTE["primary"]),
    ("active_minutes",     PALETTE["accent3"]),
    ("sleep_hours",        PALETTE["accent2"]),
    ("sleep_quality",      PALETTE["accent4"]),
    ("stress_level",       PALETTE["accent1"]),
    ("bmi",                PALETTE["accent3"]),
    ("heart_rate_resting", PALETTE["primary"]),
    ("workouts_per_week",  PALETTE["accent2"]),
]
positions = [(2,0),(2,1),(2,2),(2,3),(3,0),(3,1),(3,2),(3,3)]
for (col, color), (r, c_) in zip(plot_cols, positions):
    ax = fig.add_subplot(gs[r, c_])
    ax.set_facecolor(PALETTE["bg"])
    ax.hist(df[col], bins=40, color=color, alpha=0.85, edgecolor=PALETTE["bg"])
    ax.axvline(df[col].median(), color="white", linestyle="--", lw=1.3, alpha=0.6)
    ax.set_title(col.replace("_"," ").title(), color=PALETTE["primary"], fontsize=10)
    ax.tick_params(colors=PALETTE["text"], labelsize=8)
    ax.spines[:].set_visible(False)

# Correlation heatmap
ax = fig.add_subplot(gs[4, :])
ax.set_facecolor(PALETTE["bg"])
corr = df[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
            annot=True, fmt=".2f", linewidths=0.5, ax=ax,
            annot_kws={"size": 7}, cbar_kws={"shrink": 0.6})
ax.set_title("Correlation Heatmap — Numeric Features", color=PALETTE["primary"], fontsize=13, pad=10)
ax.tick_params(colors=PALETTE["text"], labelsize=8)

show_mpl("Overview Dashboard  (KPI cards + distributions + correlation heatmap)")


# ═══════════════════════════════════════════════════════════════
# SECTION B — LIFESTYLE & FITNESS ANALYSIS
# ═══════════════════════════════════════════════════════════════

# B1 — Grouped bar: avg metrics by lifestyle
grp_metrics = ["steps_per_day","active_minutes","workouts_per_week",
               "sleep_hours","stress_level","bmi"]
lif_grp = df.groupby("lifestyle_category")[grp_metrics].mean().reset_index()

fig = make_subplots(rows=2, cols=3,
    subplot_titles=[m.replace("_"," ").title() for m in grp_metrics],
    vertical_spacing=0.15, horizontal_spacing=0.08)
row_col = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3)]
for metric, (r, c) in zip(grp_metrics, row_col):
    for cat in lif_grp["lifestyle_category"]:
        val = lif_grp.loc[lif_grp["lifestyle_category"]==cat, metric].values[0]
        fig.add_trace(go.Bar(
            name=cat, x=[cat], y=[val],
            marker_color=LIFESTYLE_COLORS[cat],
            showlegend=(r==1 and c==1),
            text=f"{val:.1f}", textposition="outside",
        ), row=r, col=c)
fig.update_layout(
    title="Average Fitness Metrics by Lifestyle Category",
    title_font_size=20, height=700,
    paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
    font_color=PALETTE["text"], barmode="group",
)
show_plotly(fig, "B1  Avg Fitness Metrics by Lifestyle Category")

# B2 — Violin: BMI & Steps by fitness level
fig = make_subplots(rows=1, cols=2,
    subplot_titles=["BMI by Fitness Level", "Steps/Day by Fitness Level"])
for level in ["Fit","Moderate","Unfit"]:
    sub = SAMPLE[SAMPLE["fitness_level"]==level]
    fig.add_trace(go.Violin(y=sub["bmi"], name=level, box_visible=True, meanline_visible=True,
        fillcolor=FITNESS_COLORS[level], opacity=0.7, line_color=FITNESS_COLORS[level]),
        row=1, col=1)
    fig.add_trace(go.Violin(y=sub["steps_per_day"], name=level, box_visible=True,
        meanline_visible=True, fillcolor=FITNESS_COLORS[level], opacity=0.7,
        line_color=FITNESS_COLORS[level], showlegend=False), row=1, col=2)
fig.update_layout(
    title="BMI & Steps per Day Distribution by Fitness Level",
    title_font_size=20, height=500,
    paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
    font_color=PALETTE["text"],
)
show_plotly(fig, "B2  BMI & Steps Distribution by Fitness Level")

# B3 — Sunburst: Lifestyle → Fitness
ct = df.groupby(["lifestyle_category","fitness_level"]).size().reset_index(name="count")
fig = px.sunburst(ct, path=["lifestyle_category","fitness_level"],
                  values="count", color="lifestyle_category",
                  color_discrete_map=LIFESTYLE_COLORS,
                  title="Lifestyle → Fitness Level Breakdown")
fig.update_layout(paper_bgcolor=PALETTE["bg"], font_color=PALETTE["text"],
                  title_font_size=20, height=550)
show_plotly(fig, "B3  Sunburst — Lifestyle → Fitness Level")


# ═══════════════════════════════════════════════════════════════
# SECTION C — AGE GROUP ANALYSIS
# ═══════════════════════════════════════════════════════════════

# C1 — Multi-metric bar by age group
age_metrics = ["steps_per_day","active_minutes","bmi","sleep_hours",
               "stress_level","heart_rate_resting","workouts_per_week","consistency_score"]
age_grp = df.groupby("age_group", observed=True)[age_metrics].mean().reset_index()
colors_age = [PALETTE["primary"], PALETTE["accent3"], PALETTE["accent2"],
              PALETTE["accent1"], PALETTE["accent4"]]

fig = make_subplots(rows=2, cols=4,
    subplot_titles=[m.replace("_"," ").title() for m in age_metrics],
    vertical_spacing=0.18, horizontal_spacing=0.07)
rc = [(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3),(2,4)]
for metric, (r, c) in zip(age_metrics, rc):
    fig.add_trace(go.Bar(
        x=age_grp["age_group"].astype(str), y=age_grp[metric],
        marker_color=colors_age,
        text=[f"{v:.1f}" for v in age_grp[metric]],
        textposition="outside", showlegend=False,
    ), row=r, col=c)
fig.update_layout(
    title="Fitness Metrics Across Age Groups",
    title_font_size=20, height=700,
    paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
    font_color=PALETTE["text"],
)
show_plotly(fig, "C1  Fitness Metrics Across Age Groups")

# C2 — Stacked bar: age × fitness level
age_fit = (df.groupby(["age_group","fitness_level"], observed=True)
             .size().reset_index(name="count"))
fig = px.bar(age_fit, x="age_group", y="count", color="fitness_level",
             color_discrete_map=FITNESS_COLORS, barmode="stack",
             title="Fitness Level Distribution by Age Group")
fig.update_layout(paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
                  font_color=PALETTE["text"], title_font_size=20, height=480)
show_plotly(fig, "C2  Fitness Level Distribution by Age Group")


# ═══════════════════════════════════════════════════════════════
# SECTION D — SLEEP & STRESS DEEP DIVE
# ═══════════════════════════════════════════════════════════════

# D1 — Scatter: sleep hours vs sleep quality
fig = px.scatter(SAMPLE, x="sleep_hours", y="sleep_quality",
                 color="lifestyle_category", color_discrete_map=LIFESTYLE_COLORS,
                 opacity=0.45, trendline="ols",
                 title="Sleep Hours vs Sleep Quality (by Lifestyle)",
                 labels={"sleep_hours":"Sleep Hours","sleep_quality":"Sleep Quality"})
fig.update_layout(paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
                  font_color=PALETTE["text"], title_font_size=20, height=500)
show_plotly(fig, "D1  Sleep Hours vs Sleep Quality")

# D2 — Count heatmap: stress vs sleep
heat_data = (df.groupby(["stress_bin","sleep_bin"], observed=True)
               .size().reset_index(name="count"))
pivot = heat_data.pivot(index="stress_bin", columns="sleep_bin", values="count")
fig = go.Figure(go.Heatmap(
    z=pivot.values,
    x=pivot.columns.astype(str).tolist(),
    y=pivot.index.astype(str).tolist(),
    colorscale="RdYlGn_r",
    text=pivot.values, texttemplate="%{text:,}",
    hoverongaps=False,
))
fig.update_layout(
    title="Stress Level vs Sleep Quality — Count Heatmap",
    paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
    font_color=PALETTE["text"], title_font_size=20, height=450,
    xaxis_title="Sleep Quality", yaxis_title="Stress Level",
)
show_plotly(fig, "D2  Stress × Sleep Quality Count Heatmap")

# D3 — Box: stress by lifestyle & fitness
fig = px.box(SAMPLE, x="lifestyle_category", y="stress_level",
             color="fitness_level", color_discrete_map=FITNESS_COLORS,
             title="Stress Level by Lifestyle & Fitness Level")
fig.update_layout(paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
                  font_color=PALETTE["text"], title_font_size=20, height=480)
show_plotly(fig, "D3  Stress Level by Lifestyle & Fitness Level")


# ═══════════════════════════════════════════════════════════════
# SECTION E — ACTIVITY & BMI
# ═══════════════════════════════════════════════════════════════

# E1 — Scatter: steps vs BMI
fig = px.scatter(SAMPLE, x="steps_per_day", y="bmi",
                 color="fitness_level", color_discrete_map=FITNESS_COLORS,
                 opacity=0.4, trendline="ols",
                 title="Daily Steps vs BMI (by Fitness Level)")
fig.update_layout(paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
                  font_color=PALETTE["text"], title_font_size=20, height=500)
show_plotly(fig, "E1  Daily Steps vs BMI")

# E2 — 3D scatter
fig = px.scatter_3d(SAMPLE.sample(5000, random_state=1),
                    x="steps_per_day", y="active_minutes", z="bmi",
                    color="lifestyle_category", color_discrete_map=LIFESTYLE_COLORS,
                    opacity=0.6, size_max=4,
                    title="3D: Steps × Active Minutes × BMI")
fig.update_layout(paper_bgcolor=PALETTE["bg"],
                  font_color=PALETTE["text"], title_font_size=20, height=600)
show_plotly(fig, "E2  3D Scatter — Steps × Active Minutes × BMI")

# E3 — Radar chart
categories = ["steps_per_day","active_minutes","sleep_quality",
              "diet_quality","hydration_liters","consistency_score"]
radar_data = df.groupby("lifestyle_category")[categories].mean()
radar_norm = (radar_data - radar_data.min()) / (radar_data.max() - radar_data.min())

fig = go.Figure()
for cat in radar_norm.index:
    vals = radar_norm.loc[cat].tolist() + [radar_norm.loc[cat].iloc[0]]
    labs = categories + [categories[0]]
    fig.add_trace(go.Scatterpolar(
        r=vals, theta=labs, fill="toself",
        name=cat, line_color=LIFESTYLE_COLORS[cat],
        fillcolor=LIFESTYLE_COLORS[cat], opacity=0.3
    ))
fig.update_layout(
    polar=dict(bgcolor=PALETTE["card"],
               radialaxis=dict(visible=True, range=[0,1], color=PALETTE["text"])),
    title="Lifestyle Radar — Normalised Average Metrics",
    paper_bgcolor=PALETTE["bg"], font_color=PALETTE["text"],
    title_font_size=20, height=550,
)
show_plotly(fig, "E3  Radar Chart — Lifestyle Profiles")


# ═══════════════════════════════════════════════════════════════
# SECTION F — HEART RATE & HEALTH METRICS
# ═══════════════════════════════════════════════════════════════

# F1 — Scatter: BMI vs resting HR
fig = px.scatter(SAMPLE, x="bmi", y="heart_rate_resting",
                 color="lifestyle_category", color_discrete_map=LIFESTYLE_COLORS,
                 opacity=0.4, trendline="ols",
                 title="BMI vs Resting Heart Rate")
fig.update_layout(paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
                  font_color=PALETTE["text"], title_font_size=20, height=500)
show_plotly(fig, "F1  BMI vs Resting Heart Rate")

# F2 — Horizontal violin: avg HR by fitness level
fig = go.Figure()
for level in ["Fit","Moderate","Unfit"]:
    vals = SAMPLE[SAMPLE["fitness_level"]==level]["heart_rate_avg"]
    fig.add_trace(go.Violin(x=vals, name=level, orientation="h",
        side="positive", meanline_visible=True,
        fillcolor=FITNESS_COLORS[level], line_color=FITNESS_COLORS[level], opacity=0.65))
fig.update_layout(
    title="Average Heart Rate Distribution by Fitness Level",
    paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
    font_color=PALETTE["text"], title_font_size=20, height=450,
    xaxis_title="Heart Rate (avg bpm)", violingap=0.05, violinmode="overlay",
)
show_plotly(fig, "F2  Avg Heart Rate Distribution by Fitness Level")

# F3 — Parallel coordinates
pc_cols = ["age","steps_per_day","sleep_hours","stress_level",
           "bmi","heart_rate_resting","consistency_score"]
fig = px.parallel_coordinates(
    SAMPLE[pc_cols + ["fitness_level"]].dropna(),
    dimensions=pc_cols,
    color=SAMPLE["fitness_level"].map({"Fit":2,"Moderate":1,"Unfit":0}),
    color_continuous_scale=["#FF6B6B","#FFD93D","#6BCB77"],
    labels={c: c.replace("_"," ").title() for c in pc_cols},
    title="Parallel Coordinates — Multi-metric Profile (coloured by Fitness Level)",
)
fig.update_layout(paper_bgcolor=PALETTE["bg"], font_color=PALETTE["text"],
                  title_font_size=20, height=550)
show_plotly(fig, "F3  Parallel Coordinates — Multi-metric Profiles")


# ═══════════════════════════════════════════════════════════════
# SECTION G — CONSISTENCY, DIET & HYDRATION
# ═══════════════════════════════════════════════════════════════

# G1 — Bubble chart: diet × consistency (bubble = hydration)
fig = px.scatter(SAMPLE.sample(8000, random_state=7),
                 x="diet_quality", y="consistency_score",
                 size="hydration_liters", color="lifestyle_category",
                 color_discrete_map=LIFESTYLE_COLORS, opacity=0.55,
                 size_max=18, hover_data=["age","bmi"],
                 title="Diet Quality vs Consistency Score (bubble = Hydration)")
fig.update_layout(paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
                  font_color=PALETTE["text"], title_font_size=20, height=550)
show_plotly(fig, "G1  Diet Quality vs Consistency Score (Bubble Chart)")

# G2 — Bar: diet & hydration by fitness level
dh = df.groupby("fitness_level")[["diet_quality","hydration_liters"]].mean().reset_index()
fig = make_subplots(rows=1, cols=2,
    subplot_titles=["Diet Quality by Fitness Level","Hydration by Fitness Level"])
for i, col in enumerate(["diet_quality","hydration_liters"], 1):
    for _, row in dh.iterrows():
        fig.add_trace(go.Bar(
            x=[row["fitness_level"]], y=[row[col]],
            name=row["fitness_level"],
            marker_color=FITNESS_COLORS[row["fitness_level"]],
            showlegend=(i==1),
            text=f"{row[col]:.2f}", textposition="outside",
        ), row=1, col=i)
fig.update_layout(
    title="Diet Quality & Hydration by Fitness Level",
    paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
    font_color=PALETTE["text"], title_font_size=20, height=450, barmode="group",
)
show_plotly(fig, "G2  Diet Quality & Hydration by Fitness Level")

# G3 — Heatmap: workouts × diet → consistency score
heat2 = (df.groupby(["workout_bin","diet_bin"], observed=True)
           ["consistency_score"].mean().reset_index())
piv2 = heat2.pivot(index="workout_bin", columns="diet_bin", values="consistency_score")
fig = go.Figure(go.Heatmap(
    z=piv2.values,
    x=piv2.columns.astype(str).tolist(),
    y=piv2.index.astype(str).tolist(),
    colorscale="Plasma",
    text=np.round(piv2.values, 2),
    texttemplate="%{text}",
))
fig.update_layout(
    title="Avg Consistency Score: Workouts × Diet Quality",
    paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
    font_color=PALETTE["text"], title_font_size=20, height=450,
    xaxis_title="Diet Quality", yaxis_title="Workouts per Week",
)
show_plotly(fig, "G3  Avg Consistency Score — Workouts × Diet Quality")


# ═══════════════════════════════════════════════════════════════
# SECTION H — INTERACTIVE MASTER DASHBOARD
# ═══════════════════════════════════════════════════════════════
fig = make_subplots(
    rows=3, cols=3,
    subplot_titles=[
        "Lifestyle Share","Fitness Level","Steps Distribution",
        "BMI by Fitness","Steps vs BMI","HR Resting vs BMI",
        "Sleep Quality by Lifestyle","Stress by Lifestyle","Consistency by Fitness"
    ],
    specs=[
        [{"type":"pie"},    {"type":"bar"},     {"type":"histogram"}],
        [{"type":"violin"}, {"type":"scatter"}, {"type":"scatter"}],
        [{"type":"violin"}, {"type":"box"},     {"type":"violin"}],
    ],
    vertical_spacing=0.10, horizontal_spacing=0.07,
)

# Row 1
lc = df["lifestyle_category"].value_counts()
fig.add_trace(go.Pie(labels=lc.index, values=lc.values,
    marker_colors=[LIFESTYLE_COLORS[k] for k in lc.index], hole=0.45), row=1, col=1)

fc = df["fitness_level"].value_counts()
fig.add_trace(go.Bar(x=fc.index, y=fc.values,
    marker_color=[FITNESS_COLORS[k] for k in fc.index], showlegend=False), row=1, col=2)

fig.add_trace(go.Histogram(x=SAMPLE["steps_per_day"], nbinsx=50,
    marker_color=PALETTE["primary"], showlegend=False), row=1, col=3)

# Row 2
for level in ["Fit","Moderate","Unfit"]:
    sub = SAMPLE[SAMPLE["fitness_level"]==level]
    fig.add_trace(go.Violin(y=sub["bmi"], name=level, box_visible=True,
        fillcolor=FITNESS_COLORS[level], line_color=FITNESS_COLORS[level],
        meanline_visible=True, opacity=0.7, showlegend=False), row=2, col=1)

fig.add_trace(go.Scattergl(x=SAMPLE["steps_per_day"], y=SAMPLE["bmi"], mode="markers",
    marker=dict(color=SAMPLE["fitness_level"].map(FITNESS_COLORS), size=3, opacity=0.35),
    showlegend=False), row=2, col=2)

fig.add_trace(go.Scattergl(x=SAMPLE["bmi"], y=SAMPLE["heart_rate_resting"], mode="markers",
    marker=dict(color=SAMPLE["lifestyle_category"].map(LIFESTYLE_COLORS), size=3, opacity=0.35),
    showlegend=False), row=2, col=3)

# Row 3
for cat in ["Active","Sedentary","Athlete"]:
    sub = SAMPLE[SAMPLE["lifestyle_category"]==cat]
    fig.add_trace(go.Violin(y=sub["sleep_quality"], name=cat, box_visible=True,
        fillcolor=LIFESTYLE_COLORS[cat], line_color=LIFESTYLE_COLORS[cat],
        meanline_visible=True, opacity=0.7, showlegend=False), row=3, col=1)

for cat in ["Active","Sedentary","Athlete"]:
    sub = SAMPLE[SAMPLE["lifestyle_category"]==cat]
    fig.add_trace(go.Box(y=sub["stress_level"], name=cat,
        marker_color=LIFESTYLE_COLORS[cat], showlegend=False), row=3, col=2)

for level in ["Fit","Moderate","Unfit"]:
    sub = SAMPLE[SAMPLE["fitness_level"]==level]
    fig.add_trace(go.Violin(y=sub["consistency_score"], name=level, box_visible=True,
        fillcolor=FITNESS_COLORS[level], line_color=FITNESS_COLORS[level],
        meanline_visible=True, opacity=0.7, showlegend=False), row=3, col=3)

fig.update_layout(
    title="FITNESS DATASET — INTERACTIVE MASTER DASHBOARD",
    title_font_size=22, height=1100,
    paper_bgcolor=PALETTE["bg"], plot_bgcolor=PALETTE["card"],
    font_color=PALETTE["text"],
)
show_plotly(fig, "H  Interactive Master Dashboard (9-panel)")


print("\n" + "═"*60)
print("  ✅  All 20 charts displayed. EDA complete!")
print("═"*60 + "\n")
