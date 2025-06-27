import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Single-Plane Balancing", page_icon="favicon.png")

col1, col2 = st.columns([8, 2])
with col1:
    st.title("Single Plane Balancing of Rotating Machinery")
with col2:
    st.write("")  # Add vertical space above the image
    st.write("")  # Add more space if needed
    st.image("favicon.png", width=100)

st.write("Made by Wiwat Chumai (Mechanical and Aerospace Engineering, Kyushu University)")
# Input fields
o_amplitude = st.number_input("Original vibration amplitude (e.g. mils):", min_value=0.0)
o_phase = st.number_input("Original vibration phase (e.g. degrees):", min_value=0.0, max_value=360.0)
ot_amplitude = st.number_input("Original + Trial weight vibration amplitude (e.g. mils):", min_value=0.0)
ot_phase = st.number_input("Original + Trial weight vibration phase (e.g. degrees):", min_value=0.0, max_value=360.0)

with st.container():
    st.markdown("----------------------------------------------------")  # horizontal line for separation
    st.markdown("**Trial weight estimation**")
    rotor_speed = st.number_input("Rotor speed (RPM):", min_value=1000.0)
    balancing_radius = st.number_input("Balancing radius (inches):", min_value=0.0)
    rotor_weight = st.number_input("Rotor weight (pounds):", min_value=1000.0)
    tw_percentage = st.number_input("Trial weight percentage to rotor weight (e.g., 5 for 5%):", min_value=10.0)
    st.markdown("---------------------------------------------------")  # horizontal line for separation

tw_amplitude = st.number_input("YOUR Trial weight (e.g. oz):", min_value=0.0)
tw_phase = st.number_input("Trial weight phase (e.g. degrees):", min_value=0.0, max_value=360.0)

if st.button("Run Balancing Analysis"):
    tw_predicted = 35.27396195 * ((tw_percentage / 100) * rotor_weight * 0.45359237 * 9.81) / (balancing_radius * 0.0245 * ((rotor_speed * (2 * np.pi / 60)) ** 2))
    tw_predicted_grams = 1000.00 * ((tw_percentage / 100) * rotor_weight * 0.45359237 * 9.81) / (balancing_radius * 0.0245 * ((rotor_speed * (2 * np.pi / 60)) ** 2))
    st.write(f"**Estimated Trial Weight:** {tw_predicted:.2f} oz / {tw_predicted_grams:.2f} grams")

    Re_O = o_amplitude * np.cos(np.radians(o_phase))
    Im_O = o_amplitude * np.sin(np.radians(o_phase))
    Re_O_t = ot_amplitude * np.cos(np.radians(ot_phase))
    Im_O_t = ot_amplitude * np.sin(np.radians(ot_phase))

    Re_t = Re_O_t - Re_O
    Im_t = Im_O_t - Im_O
    Amplitude_t = np.sqrt(Re_t**2 + Im_t**2)
    Phase_t = np.degrees(np.arctan2(Im_t, Re_t)) + 360

    st.write(f"**Effective Vibration Vector:** {Amplitude_t:.2f} mils @ {Phase_t:.2f} degrees")

    magnitude_o = np.sqrt(Re_O**2 + Im_O**2)
    influence_coefficient = tw_amplitude / Amplitude_t
    phase_influence_coefficient = tw_phase - Phase_t

    st.write(f"**Influence Coefficient:** {influence_coefficient:.2f} @ {phase_influence_coefficient:.2f} degrees")

    hs_amplitude = influence_coefficient * o_amplitude
    hs_phase = o_phase + phase_influence_coefficient

    st.write(f"**Heavy Spot:** {hs_amplitude:.2f} mils @ {hs_phase:.2f} degrees")

    influence_coefficient_predicted = tw_predicted / Amplitude_t
    hs_amplitude_predicted = influence_coefficient_predicted * o_amplitude

    cw_amplitude = hs_amplitude
    cw_amplitude_predicted = hs_amplitude_predicted
    cw_phase = hs_phase + 180

    st.write(f"**Correction Weight:** {cw_amplitude:.2f} mils @ {cw_phase:.2f} degrees")

    # Plotting polar plot
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)

    ax.arrow(np.radians(o_phase), 0, 0, o_amplitude, 
             length_includes_head=True, head_width=0.1, head_length=0.1, color='b', label='Original (o)')
    ax.text(np.radians(o_phase), o_amplitude * 1.05, f'{o_amplitude:.2f}', color='b', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.arrow(np.radians(ot_phase), 0, 0, ot_amplitude, 
             length_includes_head=True, head_width=0.1, head_length=0.1, color='g', label='Original+Trial (ot)')
    ax.text(np.radians(ot_phase), ot_amplitude * 1.05, f'{ot_amplitude:.2f}', color='g', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.arrow(np.radians(Phase_t % 360), 0, 0, Amplitude_t, 
             length_includes_head=True, head_width=0.1, head_length=0.1, color='r', label='Effective (t)')
    ax.text(np.radians(Phase_t % 360), Amplitude_t * 1.05, f'{Amplitude_t:.2f}', color='r', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_theta_zero_location('E')
    ax.set_theta_direction(-1)
    ax.set_title('Vibration Vectors (Polar Plot)')
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))

    st.pyplot(fig)

    st.markdown("---------------------------------------------------")  # horizontal line for separation

    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("References")
    with col2:
        st.write("")  # Add vertical space above the image
        st.write("")
        st.image("mcl.png", width=120)

    st.write("This application is developed based on the principles of single-plane balancing for rotating machinery. The correction methods implemented are guided by the following reference(s):")
    st.write("[1] R. Kelm, D. Pavelek, and W. Kelm, “Rotor Balancing Tutorial,” in Proc. 45th Turbomachinery & 32nd Pump Symposia, Houston, TX, USA, Sept. 12–15, 2016.")
    st.write("[2] R. C. Eisenmann Sr. and R. C. Eisenmann Jr., Machinery Malfunction Diagnosis and Correction: Vibration Analysis and Troubleshooting for the Process Industries. Upper Saddle River, NJ, USA: Hewlett-Packard Professional Books, 1997.")

    st.markdown("---------------------------------------------------")  # horizontal line for separation

    st.title("Author")
    col1, col2 = st.columns([2, 8])
    with col1:
        st.write("")  # Add vertical space above the image
        st.image("author.png", width=115)  #
    with col2:
        st.write("Wiwat Chumai")  # Add vertical space above the image
        st.write("Mechanical and Aerospace Engineering, Kyushu University")
        st.write("This application was developed by a mechanical engineering student at **Kyushu University**, Japan 🇯🇵.")  # Add vertical space above the image
    
    st.markdown("---")
    st.write("📬 **Questions or Suggestions?** Please do not hesitate to contact. Feel free to reach out through the channels below:")
    st.markdown(
        "🔗 [GitHub Repository](https://github.com/wiwatchumai/Machinosis_Balance-Pro.git) &nbsp;&nbsp;🚀  \n"
        "📧 [Email Me](mailto:wiwatchumai@gmail.com) &nbsp;&nbsp;✉️  \n"
        "🔍 [More About the Author](https://v0-new-project-znvvxbesxef.vercel.app/) &nbsp;&nbsp;📖"
    )
