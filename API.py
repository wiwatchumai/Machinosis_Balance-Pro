from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/balance', methods=['POST'])
def balance():
    data = request.get_json()

    o_amplitude = data.get("o_amplitude")
    o_phase = data.get("o_phase")
    ot_amplitude = data.get("ot_amplitude")
    ot_phase = data.get("ot_phase")
    tw_amplitude = data.get("tw_amplitude")
    rotor_speed = data.get("rotor_speed")
    balancing_radius = data.get("balancing_radius")
    rotor_weight = data.get("rotor_weight")
    tw_percentage = data.get("tw_percentage")
    tw_phase = data.get("tw_phase")

    # Predicted trial weight
    tw_predicted = 35.27396195 * ((tw_percentage / 100) * rotor_weight * 0.45359237 * 9.81) / (
        balancing_radius * 0.0245 * ((rotor_speed * (2 * np.pi / 60)) ** 2)
    )

    # Real and Imaginary components
    Re_O = o_amplitude * np.cos(np.radians(o_phase))
    Im_O = o_amplitude * np.sin(np.radians(o_phase))
    Re_O_t = ot_amplitude * np.cos(np.radians(ot_phase))
    Im_O_t = ot_amplitude * np.sin(np.radians(ot_phase))

    # Effective vector
    Re_t = Re_O_t - Re_O
    Im_t = Im_O_t - Im_O
    Amplitude_t = np.sqrt(Re_t ** 2 + Im_t ** 2)
    Phase_t = (np.degrees(np.arctan2(Im_t, Re_t)) + 360) % 360

    # Influence coefficient
    influence_coefficient = tw_amplitude / Amplitude_t if Amplitude_t != 0 else 0
    phase_influence_coefficient = tw_phase - Phase_t

    # Heavy spot
    hs_amplitude = influence_coefficient * o_amplitude
    hs_phase = o_phase + phase_influence_coefficient

    # Predicted influence coefficient and heavy spot
    influence_coefficient_predicted = tw_predicted / Amplitude_t if Amplitude_t != 0 else 0
    hs_amplitude_predicted = influence_coefficient_predicted * o_amplitude
    hs_phase_predicted = o_phase + phase_influence_coefficient

    # Correction weight
    cw_amplitude = hs_amplitude
    cw_amplitude_predicted = hs_amplitude_predicted
    cw_phase = hs_phase + 180

    return jsonify({
        "tw_predicted": tw_predicted,
        "effective_vector": {
            "amplitude": Amplitude_t,
            "phase": Phase_t
        },
        "influence_coefficient": {
            "magnitude": influence_coefficient,
            "phase": phase_influence_coefficient
        },
        "heavy_spot": {
            "amplitude": hs_amplitude,
            "phase": hs_phase
        },
        "influence_coefficient_predicted": {
            "magnitude": influence_coefficient_predicted,
            "phase": phase_influence_coefficient
        },
        "heavy_spot_predicted": {
            "amplitude": hs_amplitude_predicted,
            "phase": hs_phase_predicted
        },
        "correction_weight": {
            "amplitude": cw_amplitude,
            "phase": cw_phase
        },
        "correction_weight_predicted": {
            "amplitude": cw_amplitude_predicted,
            "phase": cw_phase
        }
    })

if __name__ == "__main__":
    app.run(debug=True)