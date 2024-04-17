from typing import Union
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from math import pi


def A() -> QuantumCircuit:
    qc = QuantumCircuit(1, name="A")
    qc.h(0)
    return qc

def C() -> QuantumCircuit:
    qc = QuantumCircuit(1, name="C")
    qc.x(0)
    return qc

def G() -> QuantumCircuit:
    qc = QuantumCircuit(1, name="G")
    return qc

def U() -> QuantumCircuit:
    qc = QuantumCircuit(1, name="U")
    qc.x(0)
    qc.h(0)
    return qc
    

def create_circuit(RNA: str) -> Union[QuantumCircuit, QuantumRegister, ClassicalRegister]:
    rna_len = len(RNA)

    q = QuantumRegister(rna_len, name="RNA")
    meas = ClassicalRegister(rna_len, name="meas")

    qc = QuantumCircuit(q, meas)

    op = {
        "A": A,
        "C": C,
        "G": G,
        "U": U
    }

    for i,base in enumerate(RNA[::-1]):
        op_qc = op[base]()
        qc.append(op_qc, [i])

    qc.barrier()
    qc.ry(pi, q)
    
    return qc, q, meas

def measure_cg(qc: QuantumCircuit, qreg:QuantumRegister, creg: ClassicalRegister) -> QuantumCircuit:
    qc_c = qc.copy()
    qc_c.barrier()
    qc_c.measure(qreg, creg)
    return qc_c

def measure_au(qc: QuantumCircuit, qreg:QuantumRegister, creg: ClassicalRegister) -> QuantumCircuit:
    qc_c = qc.copy()
    qc_c.barrier()
    qc_c.h(qreg)
    qc_c.measure(qreg, creg)
    return qc_c

def decode(counts:dict, bases:list, DNA:str='') -> str:
    dna_len = len(list(counts.keys())[0])

    if(not DNA):
        DNA_ = ['x']*dna_len
    else:
        DNA_ = list(DNA)

    check = [0]*dna_len

    for i, k in enumerate(list(counts.keys())):
        for j, v in enumerate(k):
            if(i == 0):
                check[j] = int(v) 
                continue

            actual_check_val = check[j]
            check[j] = 2 if actual_check_val != int(v) else int(v) 
    
    for i,v in enumerate(check):

        if(v > len(bases)-1):
            continue
        DNA_[i] = bases[v]
    
    return ''.join(DNA_)

def decode_cg(counts: dict, DNA: str='') -> str:
    return decode(counts, ['G', 'C'], DNA)

def decode_au(counts: dict, DNA: str='') -> str:
    return decode(counts, ['A', 'T'], DNA)
