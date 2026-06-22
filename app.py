import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="SkyReward Retention Tower",
                   page_icon="✈️", layout="wide")

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
# Makes the app look polished — dark navy header, card styling, colored tags
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.block-container { padding: 0 2rem 2rem 2rem !important; max-width: 100% !important; }
footer, #MainMenu, header { display: none !important; }

/* Top header bar */
.top-header {
    background: linear-gradient(135deg, #0f1f3d 0%, #1a3a5c 100%);
    color: white;
    padding: 18px 32px;
    margin: -1rem -2rem 1.5rem -2rem;
    display: flex;
    align-items: center;
    gap: 14px;
    border-bottom: 3px solid #2e7d6e;
}
.top-header h1 { font-size: 22px; font-weight: 700; margin: 0; }
.top-header p  { font-size: 13px; margin: 0; opacity: 0.7; }

/* KPI cards */
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 18px 22px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    border-top: 4px solid #1a3a5c;
    text-align: center;
}
.kpi-card.green  { border-top-color: #2e7d6e; }
.kpi-card.orange { border-top-color: #e8a020; }
.kpi-card.red    { border-top-color: #c0392b; }
.kpi-val { font-size: 2rem; font-weight: 700; color: #1a3a5c; line-height: 1.1; }
.kpi-lbl { font-size: 0.78rem; color: #888; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }

/* Risk tags */
.tag-high   { background:#fdecea; color:#c0392b; padding:3px 12px; border-radius:20px; font-weight:600; font-size:0.78rem; }
.tag-medium { background:#fef3e2; color:#e8a020; padding:3px 12px; border-radius:20px; font-weight:600; font-size:0.78rem; }
.tag-low    { background:#e8f5e9; color:#2e7d6e; padding:3px 12px; border-radius:20px; font-weight:600; font-size:0.78rem; }

/* Recommendation cards */
.rec-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 10px 0;
    border-left: 5px solid #2e7d6e;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.rec-card.orange { border-left-color: #e8a020; }
.rec-card.red    { border-left-color: #c0392b; }
.rec-title { font-size: 1.05rem; font-weight: 700; color: #1a3a5c; margin-bottom: 10px; }
.rec-row   { font-size: 0.88rem; color: #444; margin: 4px 0; }
.rec-label { font-weight: 600; color: #1a3a5c; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    return pd.read_csv('final_results.csv')

df = load()

COLORS = {
    'Champions': '#1a3a5c',
    'Loyalists': '#2e7d6e',
    'Dormant':   '#e8a020',
    'At-Risk':   '#c0392b',
}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈️ SkyReward Analytics")
    st.caption("Retention Intelligence Platform")
    st.divider()
    page = st.radio("Navigate", [
        "📊 Overview",
        "🔍 Member Lookup",
        "🎯 Segment Analysis",
        "💡 Retention Playbook"
    ])
    st.divider()
    st.markdown("**Filters**")
    provinces = sorted(df['Province'].unique())
    province_filter = st.multiselect("Province", provinces, default=provinces)
    card_filter = st.multiselect("Loyalty Card",
                                  ['Star','Nova','Aurora'],
                                  default=['Star','Nova','Aurora'])

filtered = df[
    df['Province'].isin(province_filter) &
    df['Loyalty Card'].isin(card_filter)
]

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-header">
    <div>✈️</div>
    <div>
        <h1>SkyReward Retention Control Tower</h1>
        <p>Loyalty Intelligence Dashboard &nbsp;·&nbsp; {len(filtered):,} members &nbsp;·&nbsp; Churn Model AUC: 0.85 </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Overview":

    # KPI Row — custom styled cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card">
            <div class="kpi-val">{len(filtered):,}</div>
            <div class="kpi-lbl">Total Members</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card red">
            <div class="kpi-val">{filtered['churn'].mean()*100:.1f}%</div>
            <div class="kpi-lbl">Churn Rate</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card orange">
            <div class="kpi-val">{(filtered['risk_tier']=='High Risk').sum():,}</div>
            <div class="kpi-lbl">High Risk Members</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card green">
            <div class="kpi-val">${filtered['CLV'].mean():,.0f}</div>
            <div class="kpi-lbl">Avg Customer LTV</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Risk distribution bar chart
    with col1:
        st.markdown("#### Churn Risk Distribution")
        risk_counts = filtered['risk_tier'].value_counts().reindex(
            ['Low Risk','Medium Risk','High Risk']).reset_index()
        risk_counts.columns = ['Risk Tier','Count']
        fig = px.bar(risk_counts, x='Risk Tier', y='Count',
                     color='Risk Tier',
                     color_discrete_map={'Low Risk':'#2e7d6e',
                                         'Medium Risk':'#e8a020',
                                         'High Risk':'#c0392b'},
                     text='Count')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, plot_bgcolor='white',
                          paper_bgcolor='white', font_family='Inter', font_color='#333333',
                          margin=dict(t=20,b=20))
        fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        fig.update_xaxes(title_font_color='#333333', tickfont_color='#333333')
        fig.update_yaxes(title_font_color='#333333', tickfont_color='#333333')
        st.plotly_chart(fig, use_container_width=True)

    # Segment donut chart
    with col2:
        st.markdown("#### Customer Value Segments")
        seg_counts = filtered['segment_label'].value_counts().reset_index()
        seg_counts.columns = ['Segment','Count']
        fig2 = px.pie(seg_counts, names='Segment', values='Count',
                      color='Segment',
                      color_discrete_map=COLORS, hole=0.5)
        fig2.update_traces(textinfo='percent+label',
                           textfont_size=12)
        fig2.update_layout(showlegend=True, font_family='Inter', font_color='#333333',
                           margin=dict(t=20,b=20),
                           paper_bgcolor='white')
        st.plotly_chart(fig2, use_container_width=True)

    # Churn rate by segment — horizontal bar
    st.markdown("#### Churn Rate by Segment")
    seg_churn = filtered.groupby('segment_label')['churn'].mean()*100
    seg_churn = seg_churn.reset_index()
    seg_churn.columns = ['Segment','Churn Rate (%)']
    seg_churn['color'] = seg_churn['Segment'].map(COLORS)
    fig3 = px.bar(seg_churn, x='Churn Rate (%)', y='Segment',
                  orientation='h', color='Segment',
                  color_discrete_map=COLORS, text='Churn Rate (%)')
    fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig3.update_layout(showlegend=False, plot_bgcolor='white',
                       paper_bgcolor='white', font_family='Inter', font_color='#333333',
                       margin=dict(t=10,b=10))
    fig3.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig3, use_container_width=True)

    # Feature importance bar
    st.markdown("#### What Drives Churn — Model Feature Importance")
    fi_df = pd.DataFrame({
        'Feature':    ['Tenure Years','Flight Consistency','Total Flights',
                       'Avg Flights/Month','CLV','Points Accumulated',
                       'Distance','Salary'],
        'Importance': [49.82, 40.49, 3.11, 2.39, 1.07, 0.74, 0.72, 0.62]
    })
    fig4 = px.bar(fi_df, x='Importance', y='Feature', orientation='h',
                  color='Importance',
                  color_continuous_scale=['#aec6cf','#1a3a5c'],
                  text='Importance')
    fig4.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig4.update_layout(showlegend=False, plot_bgcolor='white',
                       paper_bgcolor='white', font_family='Inter', font_color='#333333',
                       coloraxis_showscale=False,
                       margin=dict(t=10,b=10))
    fig4.update_xaxes(showgrid=True, gridcolor='#f0f0f0')
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: MEMBER LOOKUP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔍 Member Lookup":
    st.markdown("#### Find Members by Risk & Segment")

    c1, c2, c3 = st.columns(3)
    with c1:
        risk_sel = st.selectbox("Risk Tier",
                                ['All','High Risk','Medium Risk','Low Risk'])
    with c2:
        seg_sel = st.selectbox("Segment",
                               ['All','Champions','Loyalists','Dormant','At-Risk'])
    with c3:
        sort_sel = st.selectbox("Sort By",
                                ['Churn Probability ↓','CLV ↓','Tenure ↑'])

    view = filtered.copy()
    if risk_sel != 'All':
        view = view[view['risk_tier'] == risk_sel]
    if seg_sel != 'All':
        view = view[view['segment_label'] == seg_sel]

    sort_map = {'Churn Probability ↓':('churn_prob',False),
                'CLV ↓':('CLV',False),
                'Tenure ↑':('tenure_years',True)}
    scol, sasc = sort_map[sort_sel]
    view = view.sort_values(scol, ascending=sasc)

    # Summary metrics for filtered view
    c1, c2, c3 = st.columns(3)
    c1.metric("Members shown", f"{len(view):,}")
    c2.metric("Avg churn prob", f"{view['churn_prob'].mean()*100:.1f}%")
    c3.metric("Avg CLV", f"${view['CLV'].mean():,.0f}")

    # Table
    display = view[['Loyalty Number','Province','Loyalty Card','CLV',
                    'tenure_years','avg_flights_month',
                    'churn_prob','risk_tier','segment_label']].head(300).copy()
    display.columns = ['Member ID','Province','Card','CLV ($)',
                       'Tenure (yrs)','Avg Flights/Mo',
                       'Churn Prob','Risk','Segment']
    display['CLV ($)']       = display['CLV ($)'].apply(lambda x: f'${x:,.0f}')
    display['Churn Prob']    = display['Churn Prob'].apply(lambda x: f'{x*100:.1f}%')
    display['Tenure (yrs)']  = display['Tenure (yrs)'].apply(lambda x: f'{x:.1f}')
    display['Avg Flights/Mo']= display['Avg Flights/Mo'].apply(lambda x: f'{x:.1f}')

    st.dataframe(display, use_container_width=True,
                 hide_index=True, height=420)

    # Individual member lookup
    st.divider()
    st.markdown("#### Individual Member Profile")
    member_id = st.number_input("Enter Member ID",
                                 min_value=int(df['Loyalty Number'].min()),
                                 max_value=int(df['Loyalty Number'].max()),
                                 value=int(df['Loyalty Number'].iloc[0]))
    member = df[df['Loyalty Number'] == member_id]
    if not member.empty:
        m = member.iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Churn Probability", f"{m['churn_prob']*100:.1f}%")
        c2.metric("Risk Tier", m['risk_tier'])
        c3.metric("Segment", m['segment_label'])
        c4.metric("CLV", f"${m['CLV']:,.0f}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Province", m['Province'])
        c2.metric("Card Tier", m['Loyalty Card'])
        c3.metric("Tenure", f"{m['tenure_years']:.1f} yrs")
        c4.metric("Avg Flights/Month", f"{m['avg_flights_month']:.1f}")

        # Recommended action based on segment + risk
        actions = {
            ('Champions','High Risk'):
                "🚨 Send Status Accelerator — 2x points on next 3 flights via email. Target: book within 30 days.",
            ('Champions','Medium Risk'):
                "⚠️ Personalized email with route suggestions. Monitor for 45 days.",
            ('Champions','Low Risk'):
                "✅ Quarterly newsletter + 1-year anniversary recognition.",
            ('Loyalists','High Risk'):
                "🚨 App push notification — companion ticket offer, valid 60 days.",
            ('Loyalists','Medium Risk'):
                "⚠️ Check for 45-day flight gap. If triggered, send reactivation nudge.",
            ('Loyalists','Low Risk'):
                "✅ Standard engagement. No intervention needed.",
            ('Dormant','High Risk'):
                "🚨 Direct mail — complimentary business class upgrade on next booking.",
            ('Dormant','Medium Risk'):
                "⚠️ Email win-back with premium offer. 90-day window.",
            ('Dormant','Low Risk'):
                "⚠️ Monitor for 1 more month before escalating.",
            ('At-Risk','High Risk'):
                "🚨 Personal phone outreach by loyalty team + custom retention package.",
            ('At-Risk','Medium Risk'):
                "🚨 3-email sequence over 2 weeks with escalating offers.",
            ('At-Risk','Low Risk'):
                "⚠️ Flag for next quarterly review.",
        }
        action = actions.get((m['segment_label'], m['risk_tier']),
                             "✅ No immediate action required.")
        st.info(f"**Recommended Action:** {action}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: SEGMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🎯 Segment Analysis":
    st.markdown("#### Customer Segment Deep Dive")

    seg = st.selectbox("Select Segment",
                       ['Champions','Loyalists','Dormant','At-Risk'])
    data = filtered[filtered['segment_label'] == seg]
    color = COLORS[seg]

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Members",    f"{len(data):,}")
    c2.metric("Avg CLV",    f"${data['CLV'].mean():,.0f}")
    c3.metric("Churn Rate", f"{data['churn'].mean()*100:.1f}%")
    c4.metric("Avg Tenure", f"{data['tenure_years'].mean():.1f} yrs")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Province Breakdown")
        prov = data['Province'].value_counts().head(8).reset_index()
        prov.columns = ['Province','Count']
        fig = px.bar(prov, x='Count', y='Province', orientation='h',
                     color_discrete_sequence=[color], text='Count')
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False, plot_bgcolor='white',
                          paper_bgcolor='white', font_family='Inter', font_color='#333333',
                          margin=dict(t=10,b=10))
        fig.update_xaxes(title_font_color='#333333', tickfont_color='#333333')
        fig.update_yaxes(title_font_color='#333333', tickfont_color='#333333')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### CLV Distribution")
        fig2 = px.histogram(data, x='CLV', nbins=40,
                            color_discrete_sequence=[color])
        fig2.add_vline(x=data['CLV'].mean(), line_dash='dash',
                       line_color='red',
                       annotation_text=f"Mean: ${data['CLV'].mean():,.0f}")
        fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                           font_family='Inter', font_color='#333333',margin=dict(t=10,b=10))
        fig2.update_xaxes(title_font_color='#333333', tickfont_color='#333333')
        fig2.update_yaxes(title_font_color='#333333', tickfont_color='#333333')
        st.plotly_chart(fig2, use_container_width=True)

    # Churn prob distribution
    st.markdown("##### Churn Probability Distribution")
    fig3 = px.histogram(data, x='churn_prob', nbins=30,
                        color_discrete_sequence=[color],
                        labels={'churn_prob':'Churn Probability'})
    fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                       font_family='Inter', font_color='#333333', margin=dict(t=10,b=10))
    fig3.update_xaxes(title_font_color='#333333', tickfont_color='#333333')
    fig3.update_yaxes(title_font_color='#333333', tickfont_color='#333333')
    st.plotly_chart(fig3, use_container_width=True)

    # Strategic note
    narratives = {
        'Champions':
            "High CLV ($8,135 avg) but 35% churn rate — the highest of any segment. These are new members (avg 0.96 yr tenure) who haven't formed a flying habit yet. The 6-month window after enrollment is the critical intervention point. If they fly 3+ times in their first 6 months, churn drops dramatically.",
        'Loyalists':
            "The backbone of the program. 9,969 members, 5% churn rate, 20+ avg flights, 3+ year tenure. Protecting this segment is the single highest-ROI action available. Even a 1% improvement in Loyalist retention has greater revenue impact than any other initiative.",
        'Dormant':
            "Previously active flyers (14.2 avg flights) who went completely silent. Average salary of $223,795 — these are premium travelers who likely shifted to a competitor. A business class upgrade offer is the most compelling reactivation lever for this group.",
        'At-Risk':
            "Tiny group (8 members) but showing complete disengagement — zero flights, short tenure. Needs personal outreach from the loyalty team, not automated email."
    }
    st.info(f"**Strategic Note:** {narratives[seg]}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: RETENTION PLAYBOOK
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💡 Retention Playbook":
    st.markdown("#### Retention Playbook — 3 Executable Recommendations")
    st.caption("Each recommendation names the segment, trigger, channel, cost, and success metric.")

    st.markdown("""
    <div class="rec-card">
        <div class="rec-title">🏆 Recommendation 1 — Champions Status Accelerator</div>
        <div class="rec-row"><span class="rec-label">Who:</span> 6,303 Champions with &lt;18 months tenure and ≥2 flights in 2017</div>
        <div class="rec-row"><span class="rec-label">When:</span> Within 60 days of 6-month membership anniversary</div>
        <div class="rec-row"><span class="rec-label">What:</span> 2x points multiplier on next 3 flights — email sequence, 3 touchpoints over 6 weeks</div>
        <div class="rec-row"><span class="rec-label">Why:</span> 35% churn driven by habit absence. Members who fly 3+ times in first 6 months show dramatically lower future churn</div>
        <div class="rec-row"><span class="rec-label">Cost:</span> ~$188,550 if 20% redeem &nbsp;|&nbsp; <span class="rec-label">Revenue recovered:</span> $2.6M if 5% churn prevented</div>
        <div class="rec-row"><span class="rec-label">Success metric:</span> 15% improvement in second-flight booking within 90 days (A/B test)</div>
    </div>

    <div class="rec-card orange">
        <div class="rec-title">🛡️ Recommendation 2 — Loyalist Protection Protocol</div>
        <div class="rec-row"><span class="rec-label">Who:</span> Top 800 Loyalists by churn probability</div>
        <div class="rec-row"><span class="rec-label">When:</span> Triggered by 45-day gap in flight activity</div>
        <div class="rec-row"><span class="rec-label">What:</span> App push notification (4x higher open rate than email) + companion ticket offer</div>
        <div class="rec-row"><span class="rec-label">Why:</span> Loyalists disengage quietly. 45-day trigger catches it before cancellation</div>
        <div class="rec-row"><span class="rec-label">Cost:</span> Low (app push only) &nbsp;|&nbsp; <span class="rec-label">Trade-off:</span> Free rider risk — mitigated by gap trigger targeting</div>
        <div class="rec-row"><span class="rec-label">Success metric:</span> 40% re-engagement within 60 days of notification</div>
    </div>

    <div class="rec-card red">
        <div class="rec-title">✈️ Recommendation 3 — Dormant Premium Win-Back</div>
        <div class="rec-row"><span class="rec-label">Who:</span> 457 Dormant members, top 150 by CLV prioritized first</div>
        <div class="rec-row"><span class="rec-label">When:</span> Immediate launch, 90-day campaign window</div>
        <div class="rec-row"><span class="rec-label">What:</span> Complimentary business class upgrade (direct mail for top 50, email for rest)</div>
        <div class="rec-row"><span class="rec-label">Why:</span> Avg salary $223K — premium offer resonates more than a discount for this demographic</div>
        <div class="rec-row"><span class="rec-label">Cost:</span> ~$45,000 &nbsp;|&nbsp; <span class="rec-label">Revenue recovered:</span> $869K at 25% reactivation rate</div>
        <div class="rec-row"><span class="rec-label">Success metric:</span> 25% reactivation (≥1 flight booked within 90 days)</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### Revenue Impact Summary")

    impact = pd.DataFrame({
        'Initiative':        ['Champions Accelerator','Loyalist Protocol','Dormant Win-Back'],
        'Target Members':    [6303, 800, 457],
        'Estimated Cost':    ['$188,550','Low (app push)','$45,000'],
        'Revenue Recovered': ['$2.6M','High','$869,592'],
        'Launch Timeline':   ['60 days','30 days','Immediate'],
        'Success Metric':    ['15% lift in 2nd booking','40% re-engagement','25% reactivation']
    })
    st.dataframe(impact, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("#### Model Performance Summary")
    col1, col2 = st.columns(2)

    with col1:
        models_df = pd.DataFrame({
            'Model':     ['Logistic Regression','Random Forest','Gradient Boosting'],
            'AUC Score': [0.8136, 0.8221, 0.8515]
        })
        fig = px.bar(models_df, x='Model', y='AUC Score',
                     color='AUC Score',
                     color_continuous_scale=['#aec6cf','#1a3a5c'],
                     text='AUC Score')
        fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        fig.update_layout(showlegend=False, plot_bgcolor='white',
                          paper_bgcolor='white', font_family='Inter', font_color='#333333',
                          coloraxis_showscale=False,
                          yaxis_range=[0.78, 0.88],
                          margin=dict(t=20,b=10))
        fig.update_xaxes(title_font_color='#333333', tickfont_color='#333333')
        fig.update_yaxes(title_font_color='#333333', tickfont_color='#333333')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### Key Findings")
        st.markdown("""
        - **Tenure** is the #1 churn predictor (49.8%) — it's an onboarding problem more than a retention problem
        - **Flight consistency** ranks #2 (40.5%) — irregular flyers disengage more than infrequent but consistent ones  
        - **Salary and demographics** contribute <1% — retention is behavioral, not demographic
        - **661 behavioral churners** would have been missed by a formal-cancellation-only model
        - **16.3% overall churn rate** — 1 in 6 members disengaged in 2018
        """)

    st.caption("Built by Abhit · C&A Club IIT Guwahati · Summer Projects 2026 · Gradient Boosting AUC: 0.85")
