#!/usr/bin/env python
import os

from wpg import srwlib
from wpg import srwlpy


def set_optics(mirror_profile=False):

    el = []

    el.append(srwlib.SRWLOptD(0.71))
    # M2: ellipsoidMirror 170.0m
    el.append(srwlib.SRWLOptMirEl(_p=170.0, _q=1.6, _ang_graz=0.01385, _size_tang=0.184, _size_sag=0.01, _nvx=-0.999904090283, _nvy=0.0, _nvz=-0.013849557214, _tvx=-0.013849557214, _tvy=0.0, _x=0.0, _y=0.0))
    
    ifnElMirror1 = mirror_profile
    if ifnElMirror1:
        assert os.path.isfile(ifnElMirror1), "Missing input file mirror_2d.dat, required by M2 beamline element"
        hProfDataElMirror1 = srwlib.srwl_uti_read_data_cols(ifnElMirror1, "\t")
        el.append(srwlib.srwl_opt_setup_surf_height_2d(hProfDataElMirror1, _dim="x", _ang=0.01385, _amp_coef=1.0))
    el.append(srwlib.SRWLOptD(0.5))
    # M3: ellipsoidMirror 170.5m
    el.append(srwlib.SRWLOptMirEl(_p=170.5, _q=1.1, _ang_graz=0.01385, _size_tang=0.184, _size_sag=0.01, _nvx=0.0, _nvy=0.999904090283, _nvz=-0.013849557214, _tvx=0.0, _tvy=0.013849557214, _x=0.0, _y=0.0))

    ifnElMirror2 = mirror_profile
    if ifnElMirror2:
        assert os.path.isfile(ifnElMirror2), "Missing input file mirror_2d.dat, required by M3 beamline element"
        hProfDataElMirror2 = srwlib.srwl_uti_read_data_cols(ifnElMirror2, "\t")
        el.append(srwlib.srwl_opt_setup_surf_height_2d(hProfDataElMirror2, _dim="y", _ang=0.01385, _amp_coef=1.0))
    el.append(srwlib.SRWLOptD(1.1))
    # Sample: watch 171.6m

    pp = []
    pp.append([0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    # M2
    pp.append([0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    if ifnElMirror1:
        pp.append([0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0])
    pp.append([0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    # M3
    pp.append([0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    if ifnElMirror2:
        pp.append([0, 0, 1.0, 0, 0, 1.0, 1.0, 1.0, 1.0])
    pp.append([0, 0, 1.0, 1, 0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    # Sample
    # final post-propagation
    pp.append([0, 0, 1.0, 0, 0, 0.05, 20.0, 0.05, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    return srwlib.SRWLOptC(el, pp)

