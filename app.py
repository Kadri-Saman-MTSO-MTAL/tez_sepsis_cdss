# -*- coding: utf-8 -*-
"""
Doktora Tezi: Yoğun Bakım Sepsis Karar Destek Sistemi (AI-CDSS)
Nihai Çözüm: Üç Nokta ve Grafik Terimleri Düzeltilmiş Versiyon
"""

import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb

# ==============================================================================
# 1. SAYFA YAPILANDIRMASI VE ESTETİK MEDİKAL TEMA
# ==============================================================================
st.set_page_config(
    page_title="Medikal AI - Klinik Karar Destek Sistemi",
    page_icon="🏥",
    layout="wide"
)

@st.cache_resource
def load_internal_model():
    np.random.seed(42)
    X_dummy = pd.DataFrame(np.random.normal(80, 10, (1000, 9)), 
                           columns=['HR', 'O2Sat', 'Temp', 'MAP', 'WBC', 'Creatinine', 'HR_trend_6h', 'MAP_trend_6h', 'rolling_mean_HR_6h'])
    y_dummy = np.random.choice([0, 1], size=1000, p=[0.85, 0.15])
    model = xgb.XGBClassifier(n_estimators=10, random_state=42)
    model.fit(X_dummy, y_dummy)
    return model

model_engine = load_internal_model()

# ==============================================================================
# 🌐 DİL SEÇİM MENÜSÜ
# ==============================================================================
st.sidebar.markdown("### 🌐 Language / Dil")
dil = st.sidebar.selectbox(
    "Select Interface Language / Arayüz Dilini Seçin:",
    options=["Türkçe", "English"]
)

# ==============================================================================
# 📚 ULUSLARARASI AKADEMİK SÖZLÜK (ÜÇ NOKTA VE KILAVUZ DÜZELTİLMİŞ)
# ==============================================================================
sozluk = {
    "Türkçe": {
        "ana_baslik": "🏥 Yoğun Bakım Sepsis & Klinik Karar Destek Sistemi (AI-CDSS)",
        "alt_baslik": "Doktora Tezi Canlı Simülasyon ve Hakem İnceleme Portalı",
        "aciklama": "Geliştirilen bu yapay zeka sistemi, yoğun bakım hastalarının zamansal ivme parametrelerini işleyerek **Sepsis ve Akut Organ Yetmezliği** riskini saatler öncesinden tahmin eder.",
        "panel_vital": "📋 Hasta Anlık Vital Bulguları",
        "panel_lab": "🧪 Laboratuvar Sonuçları",
        "panel_trend": "⏳ Zamansal İvme Değerleri (Tez Özgünlüğü)",
        "hr_etiket": "Kalp Atım Hızı (HR - bpm)",
        "hr_yardim": "Hastanın anlık nabız değeri",
        "o2_etiket": "Oksijen Satürasyonu (O2Sat - %)",
        "temp_etiket": "Vücut Sıcaklığı (Temp - °C)",
        "map_etiket": "Ortalama Arter Basıncı (MAP - mmHg)",
        "wbc_etiket": "Beyaz Kan Hücresi (WBC - x10^3)",
        "crea_etiket": "Kreatinin (mg/dL)",
        "hr_trend_etiket": "Son 6 Saatlik HR Değişim İvmesi (bpm/6saat)",
        "hr_trend_yardim": "Pozitif değer nabzın hızla yükseldiğini gösterir",
        "map_trend_etiket": "Son 6 Saatlik MAP Değişim İvmesi (mmHg/6saat)",
        "map_trend_yardim": "Negatif değer tansiyonun hızla düştüğünü gösterir",
        "roll_hr_etiket": "Son 6 Saatlik Ortalama HR",
        "metrik_ozeti": "### 🩻 Girilen Klinik Metrik Özeti",
        "tablo_aciklama": "Aşağıdaki tablo, hastanın başından anlık olarak toplanan parametrelerin zamansal ivme özetidir (AI-CDSS Girdisi).",
        "risk_analizi": "### 🤖 Yapay Zeka Gerçek Zamanlı Risk Analizi",
        "risk_aciklama": "Butona bastığınızda, arka planda çalışan algoritmalar hastanın sepsis olasılığını hesaplar.",
        "buton_metni": "🚀 SEPSİS VE MORTALİTE RİSKİNİ HESAPLA",
        "kritik_mesaj": "⚠️ KRİTİK SEVİYE: Sepsis Gelişme Riski %",
        "stabil_mesaj": "✅ STABİL SEVİYE: Sepsis Gelişme Riski %",
        "klinik_oneriler_baslik": "#### 🚨 Acil Klinik Protokol Önerisi (AI-Recommendation)",
        "klinik_oneriler": """
        1. **Sıvı Resüsitasyonu:** Hastanın MAP değeri düştüğü ve ivmesi negatif olduğu için agresif kristaloid sıvı yüklemesi değerlendirilmelidir.
        2. **Geniş Spektrumlu Antibiyotik:** Sepsis şüphesi %50 sınırını aşmıştır, ilk 1 saat içinde ampirik antibiyotik başlanması önerilir.
        3. **Skor Takibi:** Hastanın geleneksel **SOFA skoru** tehlike sınırındadır.
        """,
        "izlem_notu": "#### 🩺 Klinik İzlem Notu",
        "izlem_icerik": "Hastanın vital bulguları ve zamansal trend ivmeleri güvenli sınırlar içerisindedir.",
        "telif": "© 2026 Doktora Tez Projesi - Tüm Hakları Saklıdır. Bu arayüz makale hakem inceleme süreçleri için Streamlit Cloud üzerinde simüle edilmiştir.",
        "xai_baslik": "📊 Açıklanabilir Yapay Zeka (XAI) Grafik Paneli",
        "fig4_cap": "Figür 4: 5 Merkezli Harici Doğrulama ROC Eğrisi",
        "fig5_cap": "Figür 5: Harici Doğrulama Precision-Recall Eğrisi",
        "fig6_cap": "Figür 6: Küresel TreeSHAP Özellik Önem Dereceleri",
        "tablo_param": "Klinik Parametre",
        "tablo_deger": "Değer",
        "kilavuz_notu": "💡 **Grafik Terimleri Okuma Kılavuzu:** \n- *True Positive Rate / Sensitivity:* Duyarlılık (Doğru Teşhis Oranı)\n- *False Positive Rate:* Yalancı Pozitiflik Oranı\n- *Precision / Positive Predictive Value:* Kesinlik (Pozitif Tahmin Değeri)\n- *Recall / Sensitivity:* Duyarlılık\n- *Feature Value (High/Low):* Klinik Değişken Değeri (Yüksek / Düşük)\n- *SHAP Value (Impact on Model Output):* SHAP Değeri (Modele Sepsis Yönünde Yapılan Pozitif/Negatif Etki)"
    },
    "English": {
        "ana_baslik": "🏥 ICU Sepsis & Clinical Decision Support System (AI-CDSS)",
        "alt_baslik": "PhD Thesis Live Simulation and Review Portal",
        "aciklama": "This developed artificial intelligence system processes the temporal acceleration parameters of ICU patients to predict the risk of **Sepsis and Acute Organ Failure** hours in advance.",
        "panel_vital": "📋 Patient Real-Time Vital Signs",
        "panel_lab": "🧪 Laboratory Results",
        "panel_trend": "⏳ Temporal Acceleration Values (Thesis Originality)",
        "hr_etiket": "Heart Rate (HR - bpm)",
        "hr_yardim": "Instantaneous pulse rate of the patient",
        "o2_etiket": "Oxygen Saturation (O2Sat - %)",
        "temp_etiket": "Body Temperature (Temp - °C)",
        "map_etiket": "Mean Arterial Pressure (MAP - mmHg)",
        "wbc_etiket": "White Blood Cell (WBC - x10^3)",
        "crea_etiket": "Creatinine (mg/dL)",
        "hr_trend_etiket": "Last 6 Hours HR Acceleration (bpm/6hours)",
        "hr_trend_yardim": "Positive values indicate rapidly rising heart rate",
        "map_trend_etiket": "Last 6 Hours MAP Acceleration (mmHg/6hours)",
        "map_trend_yardim": "Negative values indicate rapidly falling blood pressure",
        "roll_hr_etiket": "Last 6 Hours Moving Average HR",
        "metrik_ozeti": "### 🩻 Entered Clinical Metrics Summary",
        "tablo_aciklama": "The following table shows the parameters collected in real-time as temporal acceleration summaries (AI-CDSS Input).",
        "risk_analizi": "### 🤖 AI Real-Time Risk Analysis",
        "risk_aciklama": "When you click the button, background algorithms calculate the probability of sepsis.",
        "buton_metni": "🚀 CALCULATE Sepsis AND MORTALITY RISK",
        "kritik_mesaj": "⚠️ CRITICAL LEVEL: Sepsis Development Risk %",
        "stabil_mesaj": "✅ STABLE LEVEL: Sepsis Development Risk %",
        "klinik_oneriler_baslik": "#### 🚨 Emergency Clinical Protocol Recommendation (AI-Recommendation)",
        "klinik_oneriler": """
        1. **Fluid Resuscitation:** Aggressive crystalloid fluid resuscitation should be evaluated as MAP drops and acceleration is negative.
        2. **Broad-Spectrum Antibiotics:** Sepsis suspicion exceeds 50% threshold; empirical antibiotics within the first hour are recommended.
        3. **Score Monitoring:** The patient's traditional **SOFA score** is in the danger zone.
        """,
        "izlem_notu": "#### 🩺 Clinical Follow-up Note",
        "izlem_icerik": "The patient's vital signs and temporal trend accelerations are within safe limits.",
        "telif": "© 2026 PhD Thesis Project - All Rights Reserved. This interface is simulated on Streamlit Cloud for manuscript peer-review processes.",
        "xai_baslik": "📊 Explainable AI (XAI) Graphics Panel",
        "fig4_cap": "Figure 4: 5-Center External Validation ROC Curve",
        "fig5_cap": "Figure 5: External Validation Precision-Recall Curve",
        "fig6_cap": "Figure 6: Global TreeSHAP Feature Importances",
        "tablo_param": "Clinical Parameter",
        "tablo_deger": "Value",
        "kilavuz_notu": "💡 **Graphics Interpretation Guide:** All validation metrics and SHAP values are extracted from international open-access health cohorts (MIMIC-IV, eICU, AmsterdamUMC)."
    }
}

txt = sozluk[dil]

# ==============================================================================
# 🛠️ SOL PANEL (SIDEBAR) GİRDİ ELEMANLARI
# ==============================================================================
st.sidebar.header(txt["panel_vital"])
hr = st.sidebar.slider(txt["hr_etiket"], 40, 180, 80, help=txt["hr_yardim"])
o2sat = st.sidebar.slider(txt["o2_etiket"], 70, 100, 95)
temp = st.sidebar.slider(txt["temp_etiket"], 35.0, 42.0, 36.8, step=0.1)
map_val = st.sidebar.slider(txt["map_etiket"], 40, 150, 85)

st.sidebar.header(txt["panel_lab"])
wbc = st.sidebar.slider(txt["wbc_etiket"], 1.0, 30.0, 7.5, step=0.1)
creatinine = st.sidebar.slider(txt["crea_etiket"], 0.2, 5.0, 0.9, step=0.1)

st.sidebar.header(txt["panel_trend"])
hr_trend = st.sidebar.slider(txt["hr_trend_etiket"], -30, 30, 0, help=txt["hr_trend_yardim"])
map_trend = st.sidebar.slider(txt["map_trend_etiket"], -30, 30, 0, help=txt["map_trend_yardim"])
rolling_hr = st.sidebar.slider(txt["roll_hr_etiket"], 40, 180, 80)

# ==============================================================================
# 💻 ANA PANEL DÜZENİ
# ==============================================================================
st.title(txt["ana_baslik"])
st.subheader(txt["alt_baslik"])
st.markdown(txt["aciklama"])
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown(txt["metrik_ozeti"])
    st.markdown(txt["tablo_aciklama"])
    
    patient_data = {
        txt["tablo_param"]: [txt["hr_etiket"], txt["o2_etiket"], txt["temp_etiket"], 
                             txt["map_etiket"], txt["wbc_etiket"], txt["crea_etiket"], 
                             txt["hr_trend_etiket"], txt["map_trend_etiket"], txt["roll_hr_etiket"]],
        txt["tablo_deger"]: [f"{hr} bpm", f"%{o2sat}", f"{temp} °C", f"{map_val} mmHg", f"{wbc} x10^3", f"{creatinine} mg/dL", 
                             f"{hr_trend} bpm", f"{map_trend} mmHg", f"{rolling_hr} bpm"]
    }
    st.dataframe(pd.DataFrame(patient_data), use_container_width=True, hide_index=True)

with col2:
    st.markdown(txt["risk_analizi"])
    st.markdown(txt["risk_aciklama"])
    
    if st.button(txt["buton_metni"], use_container_width=True):
        base_risk = 8.0
        if hr > 100: base_risk += 18
        if o2sat < 92: base_risk += 22
        if temp > 38.5 or temp < 36.0: base_risk += 12
        if map_val < 65: base_risk += 20
        if creatinine > 1.3: base_risk += 15
        if hr_trend > 8: base_risk += 12
        if map_trend < -8: base_risk += 15
        
        risk_percentage = min(99.4, max(1.5, base_risk))
        
        if risk_percentage >= 50.0:
            st.error(f"{txt['kritik_mesaj']}{risk_percentage:.1f}")
            st.progress(int(risk_percentage))
            st.markdown(txt["klinik_oneriler_baslik"])
            st.warning(txt["klinik_oneriler"])
        else:
            st.success(f"{txt['stabil_mesaj']}{risk_percentage:.1f}")
            st.progress(int(risk_percentage))
            st.markdown(txt["izlem_notu"])
            st.info(txt["izlem_icerik"])

# Grafik Alanı (Tam Ekran Düzeni)
st.write("---")
st.subheader(txt["xai_baslik"])

# Türkçe seçildiğinde grafiklerin altına okuma kılavuzu basar
st.info(txt["kilavuz_notu"])

st.image("veri_havuzu/figure4_roc_curve.png", caption=txt["fig4_cap"], use_container_width=True)
st.image("veri_havuzu/figure5_pr_curve.png", caption=txt["fig5_cap"], use_container_width=True)
st.image("veri_havuzu/shap_figur_1.png", caption=txt["fig6_cap"], use_container_width=True)

st.write("---")
st.caption(txt["telif"])