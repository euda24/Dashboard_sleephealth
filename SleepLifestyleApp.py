
# Importing libraries - ensure streamlit installed
import pandas as pd
import plotly.express as px
import streamlit as st

##### SET-UP and STYLING #####

# Page Configuration (e.g. title, layout etc.)
st.set_page_config(
    page_title = "Sleep and Lifestyle Insights",
    page_icon = ":bed:",
    layout ="wide"
)

# Design / UI (colours, font etc.)

# colours for key streamlit elements (headers,containers, font etc.)
PRIMARY = "#d4826b"         # colour for accent / headings - teracotta
PAGE_BG = "#f8f6f4"        # page background - off white
CARD_BG = "#ffffff"         # card background - white
KPI_BG  = "#f5ede4"     # kpi card background - cream
TEXT =    "#2b2b2b"            # primary text - dark grey
SUBTEXT = "#8a7f7a"         # secondary text - warm grey
BORDER =  "#e5dfd8"        # border - v light grey

#Plotly styling for charts (e.g. axis, grid etc.)
chart_main = dict(
    template = "seaborn",
    margin = dict(l=10, r=10, t=42, b=10),
    paper_bgcolor = CARD_BG,        
    plot_bgcolor = "#faf8f6",       
    font = dict(
        color = TEXT,
        family = "'Segoe UI', 'Helvetica', sans-serif" 
    ),
    xaxis = dict(
        gridcolor = "#f0ebe6",      
        linecolor = BORDER,         
        zerolinecolor = BORDER,
    ),
    yaxis = dict(
        gridcolor = "#f0ebe6",      
        linecolor = BORDER,         
        zerolinecolor = BORDER,
    ),
)

# colours for charts data (e.g. bars, lines, scatter pointe etc.)

chart_dt = [
    "#d4826b",  # teracotta
    "#6c9A8b",  # green sage
    "#e6B89c",  # peachy
    "#aa8976",  # beige
    "#4a6C6f"   # deep grey
]

# colours for sleep disorders
dmap = {"None": chart_dt[1], "Sleep Apnea": chart_dt[3], "Insomnia": chart_dt[0]}



DASH_CSS = f"""
    <style>
      .stApp {{
        background: {PAGE_BG};
      }}
      .app-title {{
        font-size: 2.0rem; 
        font-weight: 700; 
        color: {PRIMARY}; 
        letter-spacing: .2px;
        margin-top: 4rem;
        margin-bottom: 0.2rem;
      }}
      .app-subtitle {{
        font-size: 1rem; 
        color: {SUBTEXT};
        margin-bottom: 1.0rem;
      }}
      .section-title {{
        font-size: 1.25rem; 
        font-weight: 700; 
        color: {TEXT};
        margin: 0.4rem 0 0.8rem 0;
      }}
      .chart-card {{
        background: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 14px 14px 6px 14px;
        box-shadow: 
        0 1px 2px rgba(0,0,0,0.04),
        0 6px 20px rgba(0,0,0,0.04);
      }}
      .kpi-card {{
        background: {KPI_BG};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 
            0 1px 3px rgba(0, 0, 0, 0.08),
            0 6px 12px rgba(0, 0, 0, 0.10),
            0 12px 24px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, 
        box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
        font-weight:700;
      }}
      .kpi-label {{
        color: {SUBTEXT};
        font-size: 0.9rem;
        margin-bottom: 6px;
      }}
      .kpi-value {{
        color: {TEXT};
        font-weight: 700;
        font-size: 1.6rem;
        line-height: 1.1;
      }}
      .block-container {{
        padding-top: 1.2rem;
        padding-bottom: 1.2rem;
      }}
      .stMultiSelect span[data-baseweb="tag"] {{
        background-color: {PRIMARY};
      }}
      .stSlider > div > div > div > div {{
        background-color: {BORDER} ; 
      }}
    </style>
    """


st.markdown(DASH_CSS,unsafe_allow_html=True)


##### LOAD DATASET #####

dt = pd.read_csv('dummy_data.csv')
dt["Sleep Disorder"] = dt["Sleep Disorder"].fillna("None")
dt["Age"] = pd.to_numeric(dt["Age"], errors="coerce")

#### MAIN DASHBOARD ####

### SIDEBAR - FILTERS ###

st.sidebar.header("Filter Here:")

#Gender Filter
Gender = st.sidebar.multiselect(
    "Select the Gender:",
    options = dt["Gender"].unique(),
    default=dt["Gender"].unique()
)

#Sleep Disorder Filter
Sleep_disorder = st.sidebar.multiselect(
    "Select the Disorder:",
    options = dt["Sleep Disorder"].unique(),
    default=dt["Sleep Disorder"].unique()
)

# Age Slider

age_min = int(dt["Age"].min())
age_max = int(dt["Age"].max())
age_range = st.sidebar.slider(
    "Age range",
    min_value=age_min,
    max_value=age_max,
    value=(age_min, age_max),
    step=1,
)

#selecting data for filtering
dfl = dt.query(
    "Gender == @Gender & `Sleep Disorder` == @Sleep_disorder &" \
    "Age >= @age_range[0] and Age <= @age_range[1]"
)


### BODY OF DASH ###

## Headers ##
st.markdown('<div class="app-title">Sleep & Lifestyle Insights</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Overview of key sleep metrics and distributions</div>', unsafe_allow_html=True)


## KPI cards - 3 columns ##

avg_sleepdur = round(float(dfl["Sleep Duration"].median()), 1)
avg_sleepqual = round(float(dfl["Quality of Sleep"].median()), 1)
sleep_disorder_rate = round(100 * (dfl["Sleep Disorder"]!= "None").mean())

k1, k2, k3 = st.columns(3)
with k1:
    st.markdown('<div class="kpi-card"style="background:{KPI_BG};"><div class="kpi-label"style="color:{TEXT};">Avg Sleep Duration</div>'
                f'<div class="kpi-value">{avg_sleepdur} hrs</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="kpi-card"style="background:{KPI_BG};"><div class="kpi-label"style="color:{TEXT};">Avg Quality of Sleep</div>'
                f'<div class="kpi-value">{avg_sleepqual} / 10</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="kpi-card"style="background:{KPI_BG};"><div class="kpi-label" style="color:{TEXT};">Has Sleep Disorder</div>'
                f'<div class="kpi-value">{sleep_disorder_rate}%</div></div>', unsafe_allow_html=True)

st.markdown("***")

## Dash Charts ##

# ROW 1 #

r1c1, r1c2 = st.columns((7, 5))

# Scatter
with r1c1:
    with st.container():
        st.markdown('<div class="section-title">Sleep Quality by Duration</div>', unsafe_allow_html=True)
        try:
            scatter1 = px.scatter(
                dfl,
                x="Sleep Duration",
                y="Quality of Sleep",
                trendline="ols",
                color_discrete_sequence=[chart_dt[0]],
                labels={"Sleep Duration": "Sleep Duration (hrs)", "Quality of Sleep": "Quality Score"},
            )
        except Exception:
            scatter1 = px.scatter(
                dfl,
                x="Sleep Duration",
                y="Quality of Sleep",
                color_discrete_sequence=[chart_dt[0]],
                labels={"Sleep Duration": "Sleep Duration (hrs)", "Quality of Sleep": "Quality Score"},
            )
        scatter1.update_layout(**chart_main, height=380)
        st.plotly_chart(scatter1, use_container_width=True)
        

# Pie
with r1c2:
    with st.container():
        st.markdown('<div class="section-title">Distribution of Sleep Disorders</div>', unsafe_allow_html=True)
        disorder_counts = (
            dfl["Sleep Disorder"]
            .value_counts(dropna=False)
            .rename_axis("Sleep Disorder")
            .reset_index(name="Count")
        )
        pie1 = px.pie(
            disorder_counts,
            names="Sleep Disorder",
            values="Count",
            hole=0.45,
            color="Sleep Disorder",
            color_discrete_map=dmap,
        )
        pie1.update_traces(textposition="inside", textinfo="percent+label",texttemplate="%{label}<br>%{percent:.0%}")
        pie1.update_layout(**chart_main, height=380, legend_title="Type",legend=dict(
        orientation="h", 
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.5
    ))
        st.plotly_chart(pie1, use_container_width=True)


# ROW 2 #

# Bar chart
with st.container():
    st.markdown('<div class="section-title">Sleep Disorder Prevalence by Gender</div>', unsafe_allow_html=True)

    disorder_order = ["None", "Sleep Apnea", "Insomnia"]
    gender_order = sorted(dfl["Gender"].dropna().unique())

    
    idx = pd.MultiIndex.from_product([disorder_order, gender_order], names=["Sleep Disorder", "Gender"])
    r2 = (
        dfl
        .groupby(["Sleep Disorder", "Gender"])
        .size()
        .reindex(idx, fill_value=0)
        .reset_index(name="Count")
    )

    bar1 = px.bar(
        r2,
        x="Sleep Disorder",
        y="Count",
        color="Gender",
        barmode="group",
        category_orders={"Sleep Disorder": disorder_order, "Gender": gender_order},
        color_discrete_sequence=chart_dt[:2],
        labels={"Sleep Disorder": "", "Count": "Count"},
    )
    bar1.update_layout(**chart_main, height=400, legend_title=None)
    st.plotly_chart(bar1, use_container_width=True)
    


# ROW 3 #
r3c1, r3c2 = st.columns((5, 7))

with r3c1:
    with st.container():
        st.markdown('<div class="section-title">Sleep Duration by Stress </div>', unsafe_allow_html=True)
        try:
            scatter2 = px.scatter(
                dfl,
                x="Sleep Duration",
                y="Stress Level",
                trendline="ols",
                color_discrete_sequence=[chart_dt[0]],
                labels={"Sleep Duration": "Sleep Duration (hrs)", "Stress Level": "Stress Score"},
            )
        except Exception:
            scatter2 = px.scatter(
                dfl,
                x="Sleep Duration",
                y="Stress Level",
                color_discrete_sequence=[chart_dt[0]],
                labels={"Sleep Duration": "Sleep Duration (hrs)", "Stress Level": "Stress Score"},
            )
        scatter2.update_layout(**chart_main, height=380)
        st.plotly_chart(scatter2, use_container_width=True)
    

with r3c2:     
    with st.container():
        st.markdown('<div class="section-title">Stress by Sleep Disorder</div>', unsafe_allow_html=True)

        sdt = dfl[["Sleep Disorder", "Stress Level"]].dropna().copy()

        disorder_order = ["None", "Sleep Apnea", "Insomnia"]
        disorder_order = [d for d in disorder_order if d in set(sdt["Sleep Disorder"])]

      
        scores = sorted(sdt["Stress Level"].unique())

    
        grid = pd.MultiIndex.from_product([scores, disorder_order], names=["Stress Level", "Sleep Disorder"])
        counts = (
            sdt.groupby(["Stress Level", "Sleep Disorder"]).size()
            .reindex(grid, fill_value=0)
            .reset_index(name="count")
        )

        bar2 = px.bar(
            counts,
            x="count",
            y="Stress Level",
            color="Sleep Disorder",
            orientation="h",
            barmode="group",
            category_orders={"Stress Level": scores, "Sleep Disorder": disorder_order},
            color_discrete_map = dmap,
        )

        bar2.update_layout(
            **chart_main,
            height=max(380, 46 * len(scores)),
            legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="left", x=0),
            bargap=0.25,
        )
        bar2.update_yaxes(title= "Stress Score") 
        bar2.update_xaxes(
            title= "Counts",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.08)",
            zeroline=False
        )
        st.plotly_chart(bar2, use_container_width=True)
