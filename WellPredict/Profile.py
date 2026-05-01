import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go

def user_profile():
    # Use session state email or default to Harsh Yadav
    user_email = st.session_state.get('email', 'Harsh Yadav')
    user_id = st.session_state.get('user_id', 'harsh_123')

    # Page Header
    st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h2>Patient Dashboard</h2>
            <p>Comprehensive overview of patient biometrics, risk assessments, and historical trend analysis.</p>
        </div>
    """, unsafe_allow_html=True)

    # Personal Information Banner
    st.markdown(f"""
        <div class="hero-section" style="padding: 1.5rem 2rem; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 2rem;">
                <div style="background-color: var(--primary-accent); width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem;">
                    🧑‍💻
                </div>
                <div>
                    <h3 style="margin: 0; color: #fff; font-size: 1.8rem;">{user_email}</h3>
                    <p style="margin: 0; color: var(--text-muted); font-size: 1.1rem;">Auth ID: <strong>{user_id}</strong></p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Generate Dummy Data for the Dashboard
    np.random.seed(42)
    dates = pd.date_range(end=datetime.date.today(), periods=30)
    
    # Dummy Vitals
    df_vitals = pd.DataFrame({
        'Date': dates,
        'BMI': np.linspace(28.5, 25.2, 30) + np.random.normal(0, 0.2, 30), # Improving BMI
        'Blood_Pressure_SYS': np.random.randint(118, 135, size=30),
        'Blood_Pressure_DIA': np.random.randint(75, 88, size=30),
        'Fasting_Glucose': np.linspace(110, 95, 30) + np.random.normal(0, 3, 30), # Improving Glucose
        'Heart_Rate': np.random.randint(65, 85, size=30)
    })

    # Latest Metrics
    latest = df_vitals.iloc[-1]
    prev = df_vitals.iloc[-2]

    # Key Metrics Section
    st.markdown("#### Current Vitals Summary")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="clinical-card" style="text-align: center;">', unsafe_allow_html=True)
        st.metric(label="BMI", value=f"{latest['BMI']:.1f}", delta=f"{latest['BMI'] - prev['BMI']:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="clinical-card" style="text-align: center;">', unsafe_allow_html=True)
        st.metric(label="Blood Pressure", value=f"{int(latest['Blood_Pressure_SYS'])}/{int(latest['Blood_Pressure_DIA'])}", delta=f"{int(latest['Blood_Pressure_SYS'] - prev['Blood_Pressure_SYS'])} sys")
        st.markdown('</div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="clinical-card" style="text-align: center;">', unsafe_allow_html=True)
        st.metric(label="Fasting Glucose (mg/dL)", value=f"{int(latest['Fasting_Glucose'])}", delta=f"{int(latest['Fasting_Glucose'] - prev['Fasting_Glucose'])}")
        st.markdown('</div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="clinical-card" style="text-align: center;">', unsafe_allow_html=True)
        st.metric(label="Resting Heart Rate", value=f"{int(latest['Heart_Rate'])} bpm", delta=f"{int(latest['Heart_Rate'] - prev['Heart_Rate'])} bpm")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Section
    st.markdown("#### Longitudinal Health Trends")
    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["BMI & Glucose Trend", "Blood Pressure Analysis", "Risk Factors Radar"])
    
    with tab1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df_vitals['Date'], y=df_vitals['BMI'], mode='lines+markers', name='BMI', line=dict(color='#00e5ff', width=3)))
        fig1.add_trace(go.Scatter(x=df_vitals['Date'], y=df_vitals['Fasting_Glucose'], mode='lines', name='Glucose (mg/dL)', yaxis='y2', line=dict(color='#00c49a', width=3, dash='dot')))
        
        fig1.update_layout(
            title="30-Day BMI and Fasting Glucose Reduction",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cad2c5'),
            yaxis=dict(title="BMI", gridcolor='rgba(255,255,255,0.1)'),
            yaxis2=dict(title="Glucose (mg/dL)", overlaying='y', side='right'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=0, r=0, t=40, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = px.line(df_vitals, x='Date', y=['Blood_Pressure_SYS', 'Blood_Pressure_DIA'], 
                       labels={'value': 'Blood Pressure (mmHg)', 'variable': 'Measurement'},
                       title="Systolic vs Diastolic Trend",
                       color_discrete_map={'Blood_Pressure_SYS': '#ff4d4d', 'Blood_Pressure_DIA': '#00e5ff'})
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cad2c5'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    with tab3:
        # Dummy risk factors data
        categories = ['Heart Disease', 'Diabetes', 'Kidney Disease', 'Hypertension', 'Obesity', 'Cholesterol']
        # Normalize to 0-100 scale for radar chart
        risk_scores_initial = [85, 70, 40, 75, 90, 65]
        risk_scores_current = [60, 45, 30, 50, 65, 55]

        fig3 = go.Figure()

        fig3.add_trace(go.Scatterpolar(
            r=risk_scores_initial,
            theta=categories,
            fill='toself',
            name='Initial Assessment (3 months ago)',
            line_color='rgba(255, 77, 77, 0.7)',
            fillcolor='rgba(255, 77, 77, 0.3)'
        ))
        
        fig3.add_trace(go.Scatterpolar(
            r=risk_scores_current,
            theta=categories,
            fill='toself',
            name='Current Assessment',
            line_color='rgba(0, 229, 255, 0.9)',
            fillcolor='rgba(0, 229, 255, 0.4)'
        ))

        fig3.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    color='#cad2c5',
                    gridcolor='rgba(255,255,255,0.2)'
                ),
                angularaxis=dict(color='#fff')
            ),
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cad2c5'),
            margin=dict(l=40, r=40, t=40, b=40),
            title="Multimodal Risk Factor Analysis (Improvement Shown)"
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Activity and Logs
    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        st.markdown("#### Recent Clinical Analytics")
        
        # Dummy historical predictions
        dummy_logs = [
            {"date": "2026-04-28", "type": "Heart Disease", "result": "Normal - No indications", "risk": "low"},
            {"date": "2026-04-20", "type": "Diabetes", "result": "Low Risk - Maintain lifestyle", "risk": "low"},
            {"date": "2026-04-15", "type": "Kidney Disease", "result": "Normal - No indications", "risk": "low"},
            {"date": "2026-03-10", "type": "Heart Disease", "result": "Low Risk - Maintain lifestyle", "risk": "low"},
        ]
        
        for log in dummy_logs:
            if log['risk'] == 'high':
                color = "#ef4444"
            elif log['risk'] == 'medium':
                color = "#f59e0b"
            else:
                color = "#10b981"
                
            st.markdown(f"""
            <div style="background-color: var(--card-bg); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid var(--glass-border); display: flex; justify-content: space-between; align-items: center; background: rgba(28, 37, 65, 0.6); backdrop-filter: blur(10px);">
                <div>
                    <span style="font-size: 0.9rem; color: var(--text-muted);">{log['date']}</span>
                    <h4 style="margin: 0.2rem 0; color: #fff;">{log['type']} Analysis</h4>
                </div>
                <div style="background-color: {color}20; border: 1px solid {color}; color: {color}; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold; font-size: 0.9rem; text-align: center; max-width: 250px;">
                    {log['result']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with right_col:
        st.markdown("#### Patient Attributes")
        st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
        st.markdown(f"**Name:** Harsh Yadav")
        st.markdown(f"**Age:** 21")
        st.markdown(f"**Gender:** Male")
        st.markdown(f"**Blood Group:** O+")
        st.markdown(f"**Height:** 182 cm")
        st.markdown(f"**Allergies:** None known")
        st.markdown(f"**Status:** Active Monitoring")
        
        # Additional mini chart for activity
        st.markdown("<br>**Weekly Activity Level (Minutes)**", unsafe_allow_html=True)
        activity_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Minutes': [45, 60, 30, 0, 45, 90, 120]
        })
        st.bar_chart(activity_data.set_index('Day'), use_container_width=True, color='#00e5ff')
        
        st.markdown("<br>💡 *Tip: Regular activity combined with dietary management has reduced your cardiovascular risk profile by 25% over the last quarter.*", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
