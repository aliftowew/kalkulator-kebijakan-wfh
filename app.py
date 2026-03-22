import streamlit as st
import plotly.graph_objects as go

# Konfigurasi Halaman (Harus di baris paling atas)
st.set_page_config(page_title="Kalkulator WFH vs BBM", page_icon="⛽", layout="centered")

st.title("⛽ Dasbor Analitik Kebijakan WFH vs Konsumsi BBM")
st.markdown("Utak-atik parameter di bawah ini untuk melihat dampak riil WFH terhadap anggaran negara dan dompet rakyat.")

# --- AREA INPUT PARAMETER (Pindah ke Atas/Main View) ---
st.markdown("### ⚙️ Parameter Kebijakan")
with st.container():
    # Menggunakan 2 kolom agar rapi di PC, dan otomatis responsif (turun ke bawah) di HP
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        hari_wfh = st.slider("Jumlah Hari WFH per Minggu", min_value=1, max_value=5, value=1, step=1)
        subsidi = st.number_input("Besaran Subsidi per Liter (Rp)", value=1700)
        
    with col_input2:
        kepatuhan = st.slider("Tingkat Realisasi WFH (%)", min_value=10, max_value=100, value=100, step=5)
        harga_bbm = st.number_input("Harga Jual Pertalite (Rp)", value=10000)

    # Signature Semua Bisa Dihitung
    st.markdown("<p style='text-align: center; color: #757575; margin-top: 15px; margin-bottom: 0px; font-weight: bold;'>💡 Semua Bisa Dihitung</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9E9E9E; font-size: 0.85em; margin-top: 0px;'>by Alif Towew</p>", unsafe_allow_html=True)

st.markdown("---")

# --- LOGIKA KALKULASI ---
# Asumsi Dasar
total_konsumsi_tahunan = 28.1
konsumsi_bawah_tahunan = total_konsumsi_tahunan * (0.286 + 0.314) # Motor + Mobil <1400cc
konsumsi_atas_tahunan = total_konsumsi_tahunan * 0.963 # Semua Kendaraan

# Hitung Penghematan
pengali_hari = (hari_wfh * 52) / 365
faktor_kepatuhan = kepatuhan / 100

hemat_vol_bawah = konsumsi_bawah_tahunan * pengali_hari * faktor_kepatuhan
hemat_vol_atas = konsumsi_atas_tahunan * pengali_hari * faktor_kepatuhan

persen_bawah = (hemat_vol_bawah / total_konsumsi_tahunan) * 100
persen_atas = (hemat_vol_atas / total_konsumsi_tahunan) * 100

hemat_subsidi_triliun_atas = (hemat_vol_atas * 1_000_000 * 1000 * subsidi) / 1_000_000_000_000
hemat_rakyat_triliun_atas = (hemat_vol_atas * 1_000_000 * 1000 * harga_bbm) / 1_000_000_000_000

# --- TAMPILAN DASHBOARD UTAMA ---
st.subheader(f"⚡ Penghematan Konsumsi Nasional: {persen_bawah:.1f}% - {persen_atas:.1f}%")
st.caption("Dari total target Pertalite per tahun")

# Card Metrik
col1, col2, col3 = st.columns(3)
col1.metric("🛢️ Volume BBM Dihemat (Juta KL)", f"{hemat_vol_bawah:.2f} - {hemat_vol_atas:.2f}")
col2.metric("🏛️ Uang Negara Selamat (Subsidi)", f"Rp {hemat_subsidi_triliun_atas:.1f} T", f"{hari_wfh} hari WFH")
col3.metric("🛍️ Uang Rakyat Selamat", f"Rp {hemat_rakyat_triliun_atas:.1f} T", f"{hari_wfh} hari WFH")

st.markdown("---")

# --- VISUALISASI GRAFIK PLOTLY ---
# Karena layar HP sempit, grafik kita susun ke bawah alih-alih bersebelahan jika dibuka di mobile
st.markdown("### 📊 Visualisasi Data")
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    categories = ['Volume Tahunan']
    fig_volume = go.Figure(data=[
        go.Bar(name='Dihemat (Skenario Atas)', x=categories, y=[hemat_vol_atas], marker_color='#FF6B6B'),
        go.Bar(name='Tetap Dikonsumsi', x=categories, y=[total_konsumsi_tahunan - hemat_vol_atas], marker_color='#E0E0E0')
    ])
    fig_volume.update_layout(title="Perbandingan Volume di APBN", barmode='stack', margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_volume, use_container_width=True)

with col_chart2:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = persen_atas,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Klaim vs Riil ({hari_wfh} Hari)", 'font': {'size': 14}},
        gauge = {
            'axis': {'range': [None, 30]},
            'bar': {'color': "#FF6B6B"},
            'steps': [
                {'range': [0, persen_bawah], 'color': '#FFDADA'},
                {'range': [persen_bawah, persen_atas], 'color': '#FF8E8E'},
                {'range': [20, 20.5], 'color': 'black'}
            ],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 20}
        }
    ))
    fig_gauge.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_gauge, use_container_width=True)

hemat_subsidi_triliun_atas = (hemat_vol_atas * 1_000_000 * 1000 * subsidi) / 1_000_000_000_000
hemat_rakyat_triliun_atas = (hemat_vol_atas * 1_000_000 * 1000 * harga_bbm) / 1_000_000_000_000

# --- TAMPILAN DASHBOARD UTAMA ---
st.subheader(f"⚡ Penghematan Konsumsi Nasional: {persen_bawah:.1f}% - {persen_atas:.1f}%")
st.caption("Dari total target Pertalite per tahun")
st.markdown("---")

# Menggunakan fitur st.metric bawaan Streamlit untuk Card yang rapi
col1, col2, col3 = st.columns(3)
col1.metric("🛢️ Volume BBM Dihemat (Juta KL/Tahun)", f"{hemat_vol_bawah:.2f} - {hemat_vol_atas:.2f}")
col2.metric("🏛️ Uang Subsidi Negara yang dihemat", f"Rp {hemat_subsidi_triliun_atas:.1f} T", f"Skenario {hari_wfh} hari")
col3.metric("🛍️ Uang Masyarkat yang dihemat untuk bensin", f"Rp {hemat_rakyat_triliun_atas:.1f} T", f"Skenario {hari_wfh} hari")

st.markdown("---")

# --- VISUALISASI GRAFIK PLOTLY ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    categories = ['Volume Tahunan']
    fig_volume = go.Figure(data=[
        go.Bar(name='Dihemat', x=categories, y=[hemat_vol_atas], marker_color='#FF6B6B'),
        go.Bar(name='Tetap Dikonsumsi', x=categories, y=[total_konsumsi_tahunan - hemat_vol_atas], marker_color='#E0E0E0')
    ])
    fig_volume.update_layout(title="Perbandingan Volume di APBN", barmode='stack', margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_volume, use_container_width=True)

with col_chart2:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = persen_atas,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Klaim vs Riil ({hari_wfh} Hari)", 'font': {'size': 14}},
        gauge = {
            'axis': {'range': [None, 30]},
            'bar': {'color': "#FF6B6B"},
            'steps': [
                {'range': [0, persen_bawah], 'color': '#FFDADA'},
                {'range': [persen_bawah, persen_atas], 'color': '#FF8E8E'},
                {'range': [20, 20.5], 'color': 'black'}
            ],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 20}
        }
    ))
    fig_gauge.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_gauge, use_container_width=True)
