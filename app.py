import streamlit as st
import plotly.graph_objects as go

# Konfigurasi Halaman 
st.set_page_config(page_title="Kalkulator WFH vs BBM", page_icon="⛽", layout="centered")

st.title("⛽ Dasbor Analitik Kebijakan WFH vs Konsumsi BBM")
st.markdown("Pemerintah merencanakan WFH 1 hari/minggu mulai 1 April. Utak-atik parameter di bawah ini untuk melihat dampak riilnya menggunakan **dua pendekatan perhitungan**.")

# --- AREA INPUT PARAMETER UMUM ---
st.markdown("### ⚙️ Parameter Kebijakan Umum")
with st.container():
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        hari_wfh = st.slider("Jumlah Hari WFH per Minggu", min_value=1, max_value=5, value=1, step=1)
        kepatuhan = st.slider("Tingkat Realisasi WFH (%)", min_value=10, max_value=100, value=100, step=5)
    with col_input2:
        minggu_wfh = st.number_input("Durasi WFH (Minggu/Tahun)", value=39, help="39 minggu karena dimulai 1 April")
        subsidi = st.number_input("Besaran Subsidi per Liter (Rp)", value=1700)
        harga_bbm = st.number_input("Harga Jual Pertalite (Rp)", value=10000)

    # Signature Semua Bisa Dihitung
    st.markdown("<p style='text-align: center; color: #757575; margin-top: 15px; margin-bottom: 0px; font-weight: bold;'>💡 Semua Bisa Dihitung</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9E9E9E; font-size: 0.85em; margin-top: 0px;'>by Alif Towew</p>", unsafe_allow_html=True)

st.markdown("---")

# Total Konsumsi Target
total_konsumsi_tahunan = 28.1 # Juta KL

# --- TABS UNTUK 2 PENDEKATAN ---
tab1, tab2 = st.tabs(["📉 Top-Down (Volume BBM)", "🧑‍💻 Bottom-Up (Data Pekerja)"])

# ==========================================
# TAB 1: PENDEKATAN TOP-DOWN (Volume Harian)
# ==========================================
with tab1:
    st.markdown("**Pendekatan Top-Down:** Menghitung penghematan dengan memotong porsi volume konsumsi harian kendaraan dari total alokasi Pertamina.")
    
    # Logika Top-Down (Asumsi harian dari catatan)
    # Konsumsi harian bawah = 46.302 KL/hari | Atas = 74.138 KL/hari
    hemat_vol_bawah = (46302 * hari_wfh * minggu_wfh * (kepatuhan / 100)) / 1_000_000
    hemat_vol_atas = (74138 * hari_wfh * minggu_wfh * (kepatuhan / 100)) / 1_000_000
    
    persen_bawah = (hemat_vol_bawah / total_konsumsi_tahunan) * 100
    persen_atas = (hemat_vol_atas / total_konsumsi_tahunan) * 100
    
    hemat_subsidi_triliun_atas = (hemat_vol_atas * subsidi * 1000) / 1000 # Simplifikasi konversi ke Triliun
    hemat_rakyat_triliun_atas = (hemat_vol_atas * harga_bbm * 1000) / 1000

    st.subheader(f"⚡ Penghematan: {persen_bawah:.1f}% - {persen_atas:.1f}%")
    
    # Card Metrik
    col1_1, col1_2, col1_3 = st.columns(3)
    col1_1.metric("🛢️ Volume BBM Dihemat", f"{hemat_vol_bawah:.2f} - {hemat_vol_atas:.2f} Jt KL")
    col1_2.metric("🏛️ Uang subsidi negara yg bisa dihemat", f"Rp {hemat_subsidi_triliun_atas:.1f} T", "Skenario Atas")
    col1_3.metric("🛍️ Uang masyarakat yg dihemat untuk bensin", f"Rp {hemat_rakyat_triliun_atas:.1f} T", "Skenario Atas")
    
    st.markdown("---")
    col_chart1_1, col_chart1_2 = st.columns(2)
    with col_chart1_1:
        fig_vol1 = go.Figure(data=[
            go.Bar(name='Dihemat (Max)', x=['Volume Tahunan'], y=[hemat_vol_atas], marker_color='#FF6B6B'),
            go.Bar(name='Tetap Dikonsumsi', x=['Volume Tahunan'], y=[total_konsumsi_tahunan - hemat_vol_atas], marker_color='#E0E0E0')
        ])
        fig_vol1.update_layout(title="Perbandingan Volume di APBN", barmode='stack', margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_vol1, use_container_width=True, key="vol_topdown")

    with col_chart1_2:
        fig_gauge1 = go.Figure(go.Indicator(
            mode="gauge+number", value=persen_atas, domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Klaim vs Riil (Top-Down)", 'font': {'size': 14}},
            gauge={
                'axis': {'range': [None, 30]}, 'bar': {'color': "#FF6B6B"},
                'steps': [{'range': [0, persen_bawah], 'color': '#FFDADA'}, {'range': [persen_bawah, persen_atas], 'color': '#FF8E8E'}],
                'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 20}
            }
        ))
        fig_gauge1.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_gauge1, use_container_width=True, key="gauge_topdown")

# ==========================================
# TAB 2: PENDEKATAN BOTTOM-UP (Data Pekerja)
# ==========================================
with tab2:
    st.markdown("**Pendekatan Bottom-Up:** Menghitung penghematan dengan mengalikan jumlah pekerja penuh dengan konsumsi bensin harian motor mereka.")
    
    col_t2_1, col_t2_2, col_t2_3 = st.columns(3)
    pekerja_total = col_t2_1.number_input("Total Pekerja Penuh (Juta Org)", value=100.5, step=1.0)
    proporsi_motor = col_t2_2.slider("Pekerja Bermotor (%)", min_value=10, max_value=100, value=50, step=5)
    konsumsi_liter = col_t2_3.number_input("Bensin/Pekerja (L/hari)", value=1.5, step=0.1)

    # Logika Bottom-Up
    pekerja_wfh_juta = pekerja_total * (proporsi_motor / 100)
    # Volume Juta Liter = Ribu KL. Dibagi 1000 jadi Juta KL.
    vol_harian_juta_kl = (pekerja_wfh_juta * konsumsi_liter) / 1000 
    
    hemat_vol_pekerja = vol_harian_juta_kl * hari_wfh * minggu_wfh * (kepatuhan / 100)
    persen_pekerja = (hemat_vol_pekerja / total_konsumsi_tahunan) * 100
    
    hemat_subsidi_pekerja = (hemat_vol_pekerja * subsidi * 1000) / 1000
    hemat_rakyat_pekerja = (hemat_vol_pekerja * harga_bbm * 1000) / 1000

    st.subheader(f"⚡ Penghematan Nasional: {persen_pekerja:.2f}%")
    
    # Card Metrik
    col2_1, col2_2, col2_3 = st.columns(3)
    col2_1.metric("🛢️ Volume BBM Dihemat", f"{hemat_vol_pekerja:.2f} Jt KL")
    col2_2.metric("🏛️ Uang subsidi negara yg bisa dihemat", f"Rp {hemat_subsidi_pekerja:.1f} T")
    col2_3.metric("🛍️ Uang masyarakat yg dihemat untuk bensin", f"Rp {hemat_rakyat_pekerja:.1f} T")

    st.markdown("---")
    col_chart2_1, col_chart2_2 = st.columns(2)
    with col_chart2_1:
        fig_vol2 = go.Figure(data=[
            go.Bar(name='Dihemat (Pekerja)', x=['Volume Tahunan'], y=[hemat_vol_pekerja], marker_color='#1565C0'),
            go.Bar(name='Tetap Dikonsumsi', x=['Volume Tahunan'], y=[total_konsumsi_tahunan - hemat_vol_pekerja], marker_color='#E0E0E0')
        ])
        fig_vol2.update_layout(title="Perbandingan Volume di APBN", barmode='stack', margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_vol2, use_container_width=True, key="vol_bottomup")

    with col_chart2_2:
        fig_gauge2 = go.Figure(go.Indicator(
            mode="gauge+number", value=persen_pekerja, domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Klaim vs Riil (Bottom-Up)", 'font': {'size': 14}},
            gauge={
                'axis': {'range': [None, 30]}, 'bar': {'color': "#1565C0"},
                'steps': [{'range': [0, persen_pekerja], 'color': '#BBDEFB'}],
                'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 20}
            }
        ))
        fig_gauge2.update_layout(margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_gauge2, use_container_width=True, key="gauge_bottomup")
