from pathlib import Path
import json

from qiskit import QuantumCircuit

from tools.qucat.qucat import *

import subprocess, sys

"""
the following commands set the R that rpy2 uses, for each session
for instance, after restarting the command line, we would need to repeat the execution of these commands

export R_HOME="$(R RHOME)"
export RPY2_CFFI_MODE=ABI
"""

QUCAT_PATH = Path("tools/qucat")
CONFIG_QUCAT = Path(QUCAT_PATH, "config_qucat.json")

def translate_ps(ps_path, num_qubits, meas_qubits):
    with open(ps_path, "r") as f:
        ps_file = json.load(f)  

    ps_str = "[program_specification]\n"
    for in_st, prob_dist in ps_file.items():
        meas_prob = {}
        for val, prob in prob_dist.items():
            val_str=""
            for i in meas_qubits:
                val_str+=str(val[i-(num_qubits-1)])
                meas_prob[val_str] = meas_prob.get(val_str,0) + prob

        for val, prob in meas_prob.items():
            if (len(str(val)))==len(meas_qubits):
                ps_str += f"{in_st},{val}={prob}\n"

    return ps_str

def program_part(input_circuit_path, num_qubits, meas_qubits):
    qubits = ",".join(str(i) for i in range(num_qubits))
    meas_qubits=",".join(str(i) for i in meas_qubits)

    res = f"[program]\nroot={input_circuit_path}\nnum_qubit={num_qubits}\ninputID={qubits}\noutputID={meas_qubits}"

    return res

def qucat_config_part():
    with open(CONFIG_QUCAT, "r") as f:
        qucat_config = json.load(f)

    pict_root = qucat_config["qucat_configuration"]["pict_root"]
    k = qucat_config["qucat_configuration"]["k"]
    sign_lvl = qucat_config["qucat_configuration"]["significance_level"]
    func = qucat_config["qucat_configuration"]["functionality"]
    seed_file = qucat_config["qucat_configuration"]["seeding_file"]

    return f"[qucat_configuration]\npict_root={pict_root}\nk={k}\nsignificance_level={sign_lvl}", func, seed_file


def build_qucat_config(input_circuit_path,
                       ps_path):
    """
    we assume ./ to be folder tool_model
    this function translates the information from config.json (in the folder tool_model) to a .ini file used by QuCat
    most of the information in config.json is used to automatically create the .ini
    however, there are some QuCat settings, specifically the ones regarding the *qucat_configuration* field, that are not in config.json
    for those settings, the user can modify the file config_qucat.json (./tools/qucat)
    the user can also specify in config_qucat.json some settings that in the original QuCat were asked iteractively (functionality and seeding rows)
    """
    #build a folder for quito data made from our resources
    data_folder = Path(QUCAT_PATH,"data")
    qc_name = ps_path.split("/")[-1].replace(".json","")
    ini_file = Path(data_folder, qc_name + ".ini")
    result_folder = Path("./data/results/qucat")
    if not data_folder.exists():
        data_folder.mkdir()
    if not result_folder.exists():
        result_folder.mkdir()
    

    qc = QuantumCircuit.from_qasm_file(input_circuit_path)
    # print(qc)
    num_qubits = qc.num_qubits
    meas_qubits = []
    for instruction in qc.data:
        if instruction.operation.name == 'measure':
            for q in instruction.qubits:
                meas_qubits.append(qc.find_bit(q).index)
    #program
    p1 = program_part(input_circuit_path, num_qubits, meas_qubits)

    #program_specification
    ps_str = translate_ps(ps_path, num_qubits, meas_qubits)

    #quito_configuration
    p3, funct, seed_file = qucat_config_part() 

    res = p1+"\n\n"+ps_str+"\n\n"+p3
    #print(res)
    with open(ini_file, "w") as f:
        f.write(res)

    return ini_file, funct, seed_file


def exec_qucat(input_circuit_path, ps_path):
    ini_file, funct, seed_file = build_qucat_config(input_circuit_path, ps_path)
    qucat_run(ini_file=ini_file,
              functionality=funct,
              seedrow_file=seed_file)

    # if seed_file is None:
    #     inputs=f"3\n{funct}\n{ini_file}\n2\n4\n"
    # else:
    #     inputs=f"3\n{funct}\n{ini_file}\n1\n{seed_file}\n4\n"

    # result = subprocess.run(
    #     ["uv", "run", "./tools/qucat/qucat.py"],
    #     input=inputs,
    #     check=False,
    #     text=True
    # )

    #print(result.stdout)

#exec_qucat()

