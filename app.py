import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Single Plane Balancing of Rotating Machinery")

# Input fields
o_amplitude = st.number_input("Original vibration amplitude (e.g. mils):", min_value=0.0, value=10.0)
o_phase = st.number_input("Original vibration phase (e.g. degrees):", min_value=0.0, max_value=360.0, value=0.0)
ot_amplitude = st.number_input("Original + trial weight vibration amplitude (e.g. mils):", min_value=0.0, value=15.0)
ot_phase = st.number_input("Original + trial weight vibration phase (e.g. degrees):", min_value=0.0, max_value=360.0, value=90.0)
tw_amplitude = st.number_input("Trial weight amplitude (e.g. oz):", min_value=0.0, value=1.0)
tw_phase = st.number_input("Trial weight phase (e.g. degrees):", min_value=0.0, max_value=360.0, value=180.0)

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

    # Helper function for wedge arrow head using annotate
    def polar_arrow(ax, angle_deg, length, color, label, text):
        angle_rad = np.radians(angle_deg)
        ax.annotate(
            '', 
            xy=(angle_rad, length), 
            xytext=(0, 0),
            arrowprops=dict(
                arrowstyle="wedge,tail_width=0.7",  # Wedge arrow head
                color=color,
                lw=2
            ),
            annotation_clip=False
        )
        ax.text(angle_rad, length * 1.05, text, color=color, ha='center', va='bottom', fontsize=10, fontweight='bold')
        # For legend
        ax.plot([], [], color=color, label=label)

    # Use the helper function for all vectors
    polar_arrow(ax, o_phase, o_amplitude, 'b', 'Original (o)', f'{o_amplitude:.2f}')
    polar_arrow(ax, ot_phase, ot_amplitude, 'g', 'Original+Trial (ot)', f'{ot_amplitude:.2f}')
    polar_arrow(ax, Phase_t, Amplitude_t, 'r', 'Effective (t)', f'{Amplitude_t:.2f}')
    polar_arrow(ax, cw_phase % 360, cw_amplitude, 'm', 'Correction (cw)', f'{cw_amplitude:.2f}')

    ax.set_theta_zero_location('E')
    ax.set_theta_direction(-1)
    ax.set_title('Vibration Vectors (Polar Plot)')
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    st.pyplot(fig)

    st.title("References")
    st.write("This application is based on the principles of single plane balancing in rotating machinery. The corrections are based on the following references(s):")
    st.write("[1] R. Kelm, D. Pavelek, and W. Kelm, “Rotor Balancing Tutorial,” in Proc. 45th Turbomachinery & 32nd Pump Symposia, Houston, TX, USA, Sept. 12–15, 2016.")