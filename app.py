import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Single Plane Balancing of Rotating Machinery")

# Input fields
o_amplitude = st.number_input("Original vibration amplitude (in mils):", min_value=0.0, value=10.0)
o_phase = st.number_input("Original vibration phase (in degrees):", min_value=0.0, max_value=360.0, value=0.0)
ot_amplitude = st.number_input("Original + trial weight vibration amplitude (in mils):", min_value=0.0, value=15.0)
ot_phase = st.number_input("Original + trial weight vibration phase (in degrees):", min_value=0.0, max_value=360.0, value=90.0)
tw_amplitude = st.number_input("Trial weight amplitude (in oz):", min_value=0.0, value=1.0)
tw_phase = st.number_input("Trial weight phase (in degrees):", min_value=0.0, max_value=360.0, value=180.0)

if st.button("Calculate and Plot"):
    # Calculate real and imaginary components
    Re_O = o_amplitude * np.cos(np.radians(o_phase))
    Im_O = o_amplitude * np.sin(np.radians(o_phase))
    Re_O_t = ot_amplitude * np.cos(np.radians(ot_phase))
    Im_O_t = ot_amplitude * np.sin(np.radians(ot_phase))

    # Effective vector
    Re_t = Re_O_t - Re_O
    Im_t = Im_O_t - Im_O
    Amplitude_t = np.sqrt(Re_t**2 + Im_t**2)
    Phase_t = np.degrees(np.arctan2(Im_t, Re_t)) % 360

    st.write(f"**Effective vibration vector:** {Amplitude_t:.2f} mils at {Phase_t:.2f} degrees")

    # Influence coefficient
    influence_coefficient = (tw_amplitude) / Amplitude_t if Amplitude_t != 0 else 0
    phase_influence_coefficient = tw_phase - Phase_t
    st.write(f"**Influence Coefficient:** {influence_coefficient:.2f} at {phase_influence_coefficient:.2f} degrees")

    # Heavy spot
    hs_amplitude = influence_coefficient * o_amplitude
    hs_phase = o_phase + phase_influence_coefficient
    st.write(f"**Heavy Spot:** {hs_amplitude:.2f} mils at {hs_phase:.2f} degrees")

    # Correction weight
    cw_amplitude = hs_amplitude
    cw_phase = hs_phase + 180
    st.write(f"**Correction Weight:** {cw_amplitude:.2f} mils at {cw_phase:.2f} degrees")

    # Polar plot
    fig = plt.figure(figsize=(7, 7))
    ax = plt.subplot(111, polar=True)

    # Original vector
    ax.arrow(np.radians(o_phase), 0, 0, o_amplitude, 
             length_includes_head=True, head_width=0.1, head_length=0.1, color='b', label='Original (o)')
    ax.text(np.radians(o_phase), o_amplitude * 1.05, f'{o_amplitude:.2f}', color='b', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Original + trial vector
    ax.arrow(np.radians(ot_phase), 0, 0, ot_amplitude, 
             length_includes_head=True, head_width=0.1, head_length=0.1, color='g', label='Original+Trial (ot)')
    ax.text(np.radians(ot_phase), ot_amplitude * 1.05, f'{ot_amplitude:.2f}', color='g', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Effective vector (t)
    ax.arrow(np.radians(Phase_t), 0, 0, Amplitude_t, 
             length_includes_head=True, head_width=0.1, head_length=0.1, color='r', label='Effective (t)')
    ax.text(np.radians(Phase_t), Amplitude_t * 1.05, f'{Amplitude_t:.2f}', color='r', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_theta_zero_location('E')
    ax.set_theta_direction(-1)
    ax.set_title('Vibration Vectors (Polar Plot)')
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    st.pyplot(fig)

    st.title("References")
    st.write("This application is based on the principles of single plane balancing in rotating machinery. The corrections are based on the following references(s):")
    st.write("[1] R. Kelm, D. Pavelek, and W. Kelm, “Rotor Balancing Tutorial,” in Proc. 45th Turbomachinery & 32nd Pump Symposia, Houston, TX, USA, Sept. 12–15, 2016.")