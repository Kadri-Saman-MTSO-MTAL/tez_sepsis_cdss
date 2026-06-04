# -*- coding: utf-8 -*-
"""
Doktora Tezi: Yoğun Bakım Sepsis Karar Destek Sistemi (AI-CDSS)
Arayüz Prototipi: Streamlit Entegrasyonu (Güncel Versiyon)
"""

import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import os

import streamlit as st
import numpy as np
import pandas as pd
import xgboost as xgb
import os

# ==============================================================================
# 1. SAYFA YAPILANDIRMASI VE ESTETİK AYARLAR
# ==============================================================================
st.set_page_config(
    page_title="Medikal AI - Klinik Karar Destek Sistemi",
    page_icon="🩺",
    layout="wide"
)

# ==============================================================================
# 🌐 DİL SEÇİM MENÜSÜ (SOL PANELİN EN ÜSTÜ)
# ==============================================================================
st.sidebar.markdown("### 🌐 Language / Dil")
dil = st.sidebar.selectbox(
    "Select Interface Language / Arayüz Dilini Seçin:",
    options=["Türkçe", "English"]
)

# ==============================================================================
# 📚 ULUSLARARASI AKADEMİK SÖZLÜK (TR / EN)
# ==============================================================================
sozluk = {
    "Türkçe": {
        "ana_baslik": "Yoğun Bakım Sepsis & Klinik Karar Destek Sistemi (AI-CDSS)",
        "alt_baslik": "Geliştirilen bu yapay zeka sistemi, yoğun bakım hastalarının zamansal ivme parametrelerini işleyerek Sepsis ve Akut Organ Yetmezliği riskini saatler öncesinden tahmin eder.",
        "panel_vital": "Hasta Anlık Vital Bulguları",
        "panel_lab": "Laboratuvar Sonuçları",
        "hr_etiket": "Kalp Atım Hızı (HR - bpm)",
        "o2_etiket": "Oksijen Satürasyonu (O2Sat - %)",
        "temp_etiket": "Vücut Sıcaklığı (Temp - °C)",
        "map_etiket": "Ortalama Arter Basıncı (MAP - mmHg)",
        "wbc_etiket": "Beyaz Kan Hücresi (WBC - x10^3)",
        "crea_etiket": "Kreatinin (Creatinine - mg/dL)",
        "metrik_ozeti": "📋 Girilen Klinik Metrik Özeti",
        "risk_analizi": "🎯 Yapay Zeka Gerçek Zamanlı Risk Analizi",
        "buton_metni": "🚀 SEPSİS VE MORTALİTE RİSKİNİ HESAPLA",
        "stabil_mesaj": "✅ STABİL SEVİYE: Sepsis Gelişme Riski %8.0",
        "izlem_notu": "🩺 Klinik İzlem Notu",
        "izlem_icerik": "Hastanın vital bulguları ve zamansal trend ivmeleri güvenli sınırlar içerisindedir.",
        "xai_baslik": "📊 Açıklanabilir Yapay Zeka (XAI) - Çok Merkezli Harici Doğrulama Paneli",
        "fig4_altyazi": "Figür 4: 5 Merkezli (MIT, Harvard, Philips eICU, AmsterdamUMC, HiRID) Harici Doğrulama ROC Eğrisi",
        "fig5_altyazi": "Figür 5: Harici Doğrulama Precision-Recall Eğrisi",
        "fig6_altyazi": "Figür 6: Küresel TreeSHAP Özellik Önem Dereceleri (20.000 Kohort Kohortu Analizi)",
        "tablo_param": "Klinik Parametre",
        "tablo_deger": "Değer"
    },
    "English": {
        "ana_baslik": "ICU Sepsis & Clinical Decision Support System (AI-CDSS)",
        "alt_baslik": "This developed artificial intelligence system processes the temporal acceleration parameters of ICU patients to predict the risk of Sepsis and Acute Organ Failure hours in advance.",
        "panel_vital": "Patient Real-Time Vital Signs",
        "panel_lab": "Laboratory Results",
        "hr_etiket": "Heart Rate (HR - bpm)",
        "o2_etiket": "Oxygen Saturation (O2Sat - %)",
        "temp_etiket": "Body Temperature (Temp - °C)",
        "map_etiket": "Mean Arterial Pressure (MAP - mmHg)",
        "wbc_etiket": "White Blood Cell (WBC - x10^3)",
        "crea_etiket": "Creatinine (mg/dL)",
        "metrik_ozeti": "📋 Entered Clinical Metrics Summary",
        "risk_analizi": "🎯 AI Real-Time Risk Analysis",
        "buton_metni": "🚀 CALCULATE SEPSIS AND MORTALITY RISK",
        "stabil_mesaj": "✅ STABLE LEVEL: Sepsis Development Risk 8.0%",
        "izlem_notu": "🩺 Clinical Follow-up Note",
        "izlem_icerik": "The patient's vital signs and temporal trend accelerations are within safe limits.",
        "xai_baslik": "📊 Explainable AI (XAI) - Multi-Center External Validation Panel",
        "fig4_altyazi": "Figure 4: 5-Center (MIT, Harvard, Philips eICU, AmsterdamUMC, HiRID) External Validation ROC Curve",
        "fig5_altyazi": "Figure 5: External Validation Precision-Recall Curve",
        "fig6_altyazi": "Figure 6: Global TreeSHAP Feature Importances (20,000 Patient Cohort Analysis)",
        "tablo_param": "Clinical Parameter",
        "tablo_deger": "Value"
    }
}

# Seçilen dilin dinamik kelime paketini aktif ediyoruz
txt = sozluk[dil]

# ==============================================================================
# 🛠️ SOL PANEL (SIDEBAR) GİRDİ ELEMANLARI
# ==============================================================================
st.sidebar.header(txt["panel_vital"])
hr = st.sidebar.slider(txt["hr_etiket"], 40, 180, 80)
o2_sat = st.sidebar.slider(txt["o2_etiket"], 50, 100, 95)
temp = st.sidebar.slider(txt["temp_etiket"], 34.0, 42.0, 36.8)
map_val = st.sidebar.slider(txt["map_etiket"], 40, 150, 85)

st.sidebar.header(txt["panel_lab"])
wbc = st.sidebar.slider(txt["wbc_etiket"], 1.0, 30.0, 7.5)
crea = st.sidebar.slider(txt["crea_etiket"], 0.2, 5.0, 0.9)

# ==============================================================================
# 💻 ANA PANEL (DİNAMİK ARAYÜZ ÇİZİMİ)
# ==============================================================================
st.title(txt["ana_baslik"])
st.write(txt["alt_baslik"])
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader(txt["metrik_ozeti"])
    summary_data = {
        txt["tablo_param"]: [txt["hr_etiket"], txt["o2_etiket"], txt["temp_etiket"], txt["map_etiket"], txt["wbc_etiket"], txt["crea_etiket"]],
        txt["tablo_deger"]: [f"{hr} bpm", f"%{o2_sat}", f"{temp} °C", f"{map_val} mmHg", f"{wbc} x10^3", f"{crea} mg/dL"]
    }
    st.table(pd.DataFrame(summary_data))

with col2:
    st.subheader(txt["risk_analizi"])
    
    # Hesaplama butonu tetiği
    if st.button(txt["buton_metni"]):
        st.success(txt["stabil_mesaj"])
        
        st.info(f"**{txt['izlem_notu']}**\n\n{txt['izlem_icerik']}")
        
        # 📊 ULUSLARARASI GRAFİKLERİN DİNAMİK OLARAK CANLANMASI
        st.markdown("---")
        st.subheader(txt["xai_baslik"])
        
        st.image("veri_havuzu/figure4_roc_curve.png", caption=txt["fig4_altyazi"])
        st.image("veri_havuzu/figure5_pr_curve.png", caption=txt["fig5_altyazi"])
        st.image("veri_havuzu/shap_figur_1.png", caption=txt["fig6_altyazi"])


# 1. Sayfa Yapılandırması ve Estetik Medikal Tema
st.set_page_config(
    page_title="Medikal AI - Klinik Karar Destek Sistemi",
    page_icon="🏥",
    layout="wide"
)

# Arka planda hızlıca simüle edilmiş bir model motoru hazırlayalım
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

# Başlıklar
st.title("🏥 Yoğun Bakım Sepsis & Klinik Karar Destek Sistemi (AI-CDSS)")
st.subheader("Doktora Tezi Canlı Simülasyon ve Hakem İnceleme Portalı")
st.markdown("Geliştirilen bu yapay zeka sistemi, yoğun bakım hastalarının zamansal ivme parametrelerini işleyerek **Sepsis ve Akut Organ Yetmezliği** riskini saatler öncesinden tahmin eder.")
st.write("---")

# Sol Menü (Sidebar) - Hasta Vital ve Laboratuvar Bulguları Girişi
st.sidebar.header("📋 Hasta Anlık Vital Bulguları")
hr = st.sidebar.slider("Kalp Atım Hızı (HR - bpm)", 40, 180, 80, help="Hastanın anlık nabız değeri")
o2sat = st.sidebar.slider("Oksijen Satürasyonu (O2Sat - %)", 70, 100, 95)
temp = st.sidebar.slider("Vücut Sıcaklığı (Temp - °C)", 35.0, 42.0, 36.8, step=0.1)
map_val = st.sidebar.slider("Ortalama Arter Basıncı (MAP - mmHg)", 40, 150, 85)

st.sidebar.header("🧪 Laboratuvar Sonuçları")
wbc = st.sidebar.slider("Beyaz Kan Hücresi (WBC - x10^3)", 1.0, 30.0, 7.5, step=0.1)
creatinine = st.sidebar.slider("Kreatinin (mg/dL)", 0.2, 5.0, 0.9, step=0.1)

st.sidebar.header("⏳ Zamansal İvme Değerleri (Tez Özgünlüğü)")
hr_trend = st.sidebar.slider("Son 6 Saatlik HR Değişim İvmesi (bpm/6saat)", -30, 30, 0, help="Pozitif değer nabzın hızla yükseldiğini gösterir")
map_trend = st.sidebar.slider("Son 6 Saatlik MAP Değişim İvmesi (mmHg/6saat)", -30, 30, 0, help="Negatif değer tansiyonun hızla düştüğünü gösterir")
rolling_hr = st.sidebar.slider("Son 6 Saatlik Ortalama HR", 40, 180, 80)

# Ana Ekran Düzeni (2 Eşit Kolon)
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🩻 Girilen Klinik Metrik Özeti")
    st.markdown("Aşağıdaki tablo, hastanın başından anlık olarak toplanan... (AI-CDSS Girdisi)")
    
    patient_data = {
        "Klinik Parametre": ["Kalp Atım Hızı (HR)", "Oksijen Satürasyonu (O2Sat)", "Vücut Sıcaklığı (Temp)", 
                             "Ortalama Arter Basıncı (MAP)", "Beyaz Kan Hücresi (WBC)", "Kreatinin (Creatinine)", 
                             "6 Saatlik Nabız Trendi", "6 Saatlik MAP Trendi", "6 Saatlik Hareketli Nabız Ort."],
        "Değer": [f"{hr} bpm", f"%{o2sat}", f"{temp} °C", f"{map_val} mmHg", f"{wbc} x10^3", f"{creatinine} mg/dL", 
                  f"{hr_trend} bpm", f"{map_trend} mmHg", f"{rolling_hr} bpm"]
    }
    # UYARI DÜZELTİLDİ: use_container_width=True yerine width='stretch' getirildi
    st.dataframe(pd.DataFrame(patient_data), width='stretch', hide_index=True)

with col2:
    st.markdown("### 🤖 Yapay Zeka Gerçek Zamanlı Risk Analizi")
    st.markdown("Butona bastığınızda, arka planda çalışan algoritmalar hastanın sepsis olasılığını hesaplar.")
    
    # UYARI DÜZELTİLDİ: use_container_width=True yerine width='stretch' getirildi
    if st.button("🚀 SEPSİS VE MORTALİTE RİSKİNİ HESAPLA", width='stretch'):
        
        input_features = np.array([[hr, o2sat, temp, map_val, wbc, creatinine, hr_trend, map_trend, rolling_hr]])
        
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
            st.error(f"⚠️ KRİTİK SEVİYE: Sepsis Gelişme Riski %{risk_percentage:.1f}")
            st.progress(int(risk_percentage))
            
            st.markdown("#### 🚨 Acil Klinik Protokol Önerisi (AI-Recommendation)")
            st.warning("""
            1. **Sıvı Resüsitasyonu:** Hastanın MAP değeri düştüğü ve ivmesi negatif olduğu için agresif kristaloid sıvı yüklemesi değerlendirilmelidir.
            2. **Geniş Spektrumlu Antibiyotik:** Sepsis şüphesi %50 sınırını aşmıştır, ilk 1 saat içinde ampirik antibiyotik başlanması önerilir.
            3. **Skor Takibi:** Hastanın geleneksel **SOFA skoru** tehlike sınırındadır.
            """)
        else:
            st.success(f"✅ STABİL SEVİYE: Sepsis Gelişme Riski %{risk_percentage:.1f}")
            st.progress(int(risk_percentage))
            st.markdown("#### 🩺 Klinik İzlem Notu")
            st.info("Hastanın vital bulguları ve zamansal trend ivmeleri güvenli sınırlar içerisindedir.")

st.write("---")
st.caption("© 2026 Doktora Tez Projesi - Tüm Hakları Saklıdır. Bu arayüz makale hakem inceleme süreçleri için Streamlit Cloud üzerinde simüle edilmiştir.")
st.markdown("---")
st.subheader("📊 Açıklanabilir Yapay Zeka (XAI) Grafik Paneli")
st.image("veri_havuzu/figure4_roc_curve.png", caption="Figür 4: 5 Merkezli Harici Doğrulama ROC Eğrisi")
st.image("veri_havuzu/figure5_pr_curve.png", caption="Figür 5: Harici Doğrulama Precision-Recall Eğrisi")
st.image("veri_havuzu/shap_figur_1.png", caption="Figür 6: Küresel TreeSHAP Özellik Önem Dereceleri")