import logging
from pathlib import Path
from pyvolt import network
from pyvolt import nv_powerflow
import numpy
import cimpy
import os

logging.basicConfig(filename='run_nv_powerflow.log', level=logging.INFO, filemode='w')

def run_powerflow():
    # Set the path for the XML files
    this_file_folder = Path(__file__).parents
    p = str(this_file_folder) + "/examples/sample_data/CIGRE-MV-NoTap"
    xml_path = Path(p)

    xml_files = [r"sample_data/CIGRE-MV-NoTap/Rootnet_FULL_NE_06J16h_DI.xml",
                 r"sample_data/CIGRE-MV-NoTap/Rootnet_FULL_NE_06J16h_EQ.xml",
                 r"sample_data/CIGRE-MV-NoTap/Rootnet_FULL_NE_06J16h_SV.xml",
                 r"sample_data/CIGRE-MV-NoTap/Rootnet_FULL_NE_06J16h_TP.xml"]

    # Read CIM files and create new network.System object
    res = cimpy.cim_import(xml_files, "cgmes_v2_4_15")
    system = network.System()
    base_apparent_power = 25  # MW
    system.load_cim_data(res['topology'], base_apparent_power)

    # Execute power flow analysis
    results_pf, num_iter = nv_powerflow.solve(system)
    return results_pf, num_iter, system

def get_powerflow_results():
    results_pf, num_iter, system = run_powerflow()
    output = f"Powerflow converged in {num_iter} iterations.<br>Results:<br>"
    for node in results_pf.nodes:
        output += f'{node.topology_node.uuid}={node.voltage_pu}<br>'
    return output, results_pf, system

if __name__ == "__main__":
    results_pf, num_iter, system = run_powerflow()
    output = f"Powerflow converged in {num_iter} iterations.<br>Results:<br>"
    for node in results_pf.nodes:
        output += f'{node.topology_node.uuid}={node.voltage_pu}<br>'
    print(output)
