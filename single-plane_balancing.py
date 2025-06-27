import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# This program aims to find the solution to the single plane balancing problme in rotor dynamics
# This algorithm mainly focuses on "Field Balancing"
# Least machinery pause is required

# Input rotor original vibration vector
o_amplitude = float(input("Enter the original vibration amplitude (in mils): "))
o_phase = float(input("Enter the original vibration phase (in degrees): "))
# Input rotor original + trial weight vector
ot_amplitude = float(input("Enter the original + trial weight vibration amplitude (in mils): "))
ot_phase = float(input("Enter the original + trial weight vibration phase (in degrees): "))

# Input trial weight vector
tw_amplitude = float(input("Enter the trial weight amplitude (in oz): "))
tw_phase = float(input("Enter the trial weight phase (in degrees): "))

# calculate the Real and Imaginary components of the original and trial weight vibration vectors
Re_O = o_amplitude * np.cos(np.radians(o_phase))
Im_O = o_amplitude * np.sin(np.radians(o_phase))
Re_O_t = ot_amplitude * np.cos(np.radians(ot_phase))
Im_O_t = ot_amplitude * np.sin(np.radians(ot_phase))

# calculate the effective vector
Re_t = Re_O_t - Re_O
Im_t = Im_O_t - Im_O
Amplitude_t= np.sqrt(Re_t**2 + Im_t**2)
Phase_t= np.degrees(np.arctan2(Im_t, Re_t)) + 360

print(f"Effective vibration vector: {Amplitude_t:.2f} mils at {Phase_t:.2f} degrees") # .2f mean 2 digit float 

#___________________________________________________________________#

magnitude_o = np.sqrt(Re_O**2 + Im_O**2)
# calculate the influence coefficient 
#calculate the influence coefficient
influence_coefficient = (tw_amplitude)/Amplitude_t
phase_influence_coefficient = tw_phase - Phase_t

print(f"Influence Coefficient: {influence_coefficient:.2f} at {phase_influence_coefficient:.2f} degrees")

#calculate the heavy spot
hs_amplitude = influence_coefficient * o_amplitude
hs_phase = o_phase + phase_influence_coefficient

print(f"Heavy Spot: {hs_amplitude:.2f} mils at {hs_phase:.2f} degrees")

#___________________________________________________________________#

# calculate correction weight
cw_amplitude = hs_amplitude
cw_phase = hs_phase + 180  # 180 degrees phase shift for correction weight

print(f"Correction Weight: {cw_amplitude:.2f} mils at {cw_phase:.2f} degrees")

# Polar plot of vectors: original (o), original+trial (ot), and effective (t)
plt.figure(figsize=(7, 7))
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
ax.arrow(np.radians(Phase_t % 360), 0, 0, Amplitude_t, 
         length_includes_head=True, head_width=0.1, head_length=0.1, color='r', label='Effective (t)')
ax.text(np.radians(Phase_t % 360), Amplitude_t * 1.05, f'{Amplitude_t:.2f}', color='r', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_theta_zero_location('E')
ax.set_theta_direction(-1)
ax.set_title('Vibration Vectors (Polar Plot)')
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
plt.show()