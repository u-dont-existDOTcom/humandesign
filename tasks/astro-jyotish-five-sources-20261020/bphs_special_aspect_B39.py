"""BPHS Ch26.10–12 planet-specific sphuta drishti, research-only.

Use an explicitly oriented angular difference target minus aspector, modulo 360.
Not a production chart engine; no actual human outcomes or Mars/Jupiter/Saturn
causality is claimed. The source has competing English renderings; these
piecewise expressions follow the Sanskrit degrees-within-sign convention.
"""
from comparative_aspect_methods_B38 import bphs_general_exact_virupas

def bphs_sphuta_special(degrees:float, *, planet:str)->float:
    # fail closed for invalid angles and unsupported planets
    ordinary=bphs_general_exact_virupas(degrees)
    if planet not in ('Mars','Jupiter','Saturn'):
        raise ValueError('Select Mars, Jupiter or Saturn, not a default planet')
    d=float(degrees)
    if planet=='Saturn':
        if 30<=d<=60: return 2*(d-30)
        if 60<=d<=90: return 60-(d-60)/2
        if 240<=d<=270: return 30+(d-240)
        if 270<=d<=300: return 2*(300-d)
    if planet=='Mars':
        if 60<=d<=90: return 15+1.5*(d-60)
        if 90<=d<=120: return 60-(d-90)
        if 180<=d<=210: return 60.0
        if 210<=d<=240: return 60-(d-210)
    if planet=='Jupiter':
        if 90<=d<=120: return 45+(d-90)/2
        if 120<=d<=150: return 60-2*(d-120)
        if 210<=d<=240: return 45+(d-210)/2
        if 240<=d<270: return 60-2*(d-240)
    return ordinary
