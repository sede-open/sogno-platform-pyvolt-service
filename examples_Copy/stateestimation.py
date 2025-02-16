import logging
import numpy as np
from pyvolt import nv_state_estimator
from pyvolt import measurement
from powerflow import get_powerflow_results  # Import the function from powerflow.py

logging.basicConfig(filename='run_nv_state_estimator.log', level=logging.INFO, filemode='w')

def run_state_estimation(results_pf, system):
    """ Write here the percent uncertainties of the measurements"""
    V_unc = 0
    I_unc = 0
    Sinj_unc = 0
    S_unc = 0
    Pmu_mag_unc = 0
    Pmu_phase_unc = 0

    # Create measurements data structures
    measurements_set = measurement.MeasurementSet()
    for node in results_pf.nodes:
        measurements_set.create_measurement(node.topology_node, measurement.ElemType.Node, measurement.MeasType.Vpmu_mag,
                                            np.absolute(node.voltage_pu), Pmu_mag_unc)
    for node in results_pf.nodes:
        measurements_set.create_measurement(node.topology_node, measurement.ElemType.Node, measurement.MeasType.Vpmu_phase,
                                            np.angle(node.voltage_pu), Pmu_phase_unc)
    measurements_set.meas_creation()

    # Perform state estimation
    state_estimation_results = nv_state_estimator.DsseCall(system, measurements_set)
    return state_estimation_results

def get_state_estimation_results():
    _, results_pf, system = get_powerflow_results()
    state_estimation_results = run_state_estimation(results_pf, system)
    output = "State Estimation Results:<br>"
    for node in state_estimation_results.nodes:
        output += f'{node.topology_node.uuid}={node.voltage}<br>'
    return output

if __name__ == "__main__":
    output = get_state_estimation_results()
    print(output)
