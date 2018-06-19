from SimEx.Analysis.DiffractionAnalysis import DiffractionAnalysis

import numpy, pyFAI
from matplotlib import pyplot as plt
import os, h5py

pattern_indices = 'all'
input_path="diffr.h5"

def main():

    analyzer = DiffractionAnalysis(input_path=input_path,
                                   pattern_indices=pattern_indices,
                                   poissonize=True
                                   )

    parameters = diffractionParameters(input_path)
    nx, ny = parameters["geom"]["mask"].shape
    mask = parameters["geom"]["mask"]
    nx,ny = mask.shape
    beamstop = 20
    mask[nx//2-beamstop//2:nx//2+beamstop//2+1, ny//2-beamstop//2:ny//2+beamstop//2+1]
    analyzer.mask = mask

    pattern = numpy.mean([p for p in analyzer.patterns_iterator],axis=0)
    qs, intensities = azimuthalIntegration(pattern, diffractionParameters(input_path))

    plt.plot(qs, intensities)

    plt.xlabel(r"$2\theta$ (deg)")
    plt.ylabel("Intensity (arb. units)")
    plt.tight_layout()

    plt.show()

def azimuthalIntegration(pattern, parameters):

    # Extract parameters.
    beam = parameters['beam']
    geom = parameters['geom']

    # Photon energy and wavelength
    E0 = beam['photonEnergy']
    lmd = 1239.8 / E0

    # Pixel dimension
    apix = geom['pixelWidth']
    # Sample-detector distance
    Ddet = geom['detectorDist']
    # Number of pixels in each dimension
    Npix = geom['mask'].shape[0]

    # Find center.
    center = 0.5*(Npix-1)

    azimuthal_integrator = pyFAI.AzimuthalIntegrator(
            dist=Ddet,
            pixel1=apix,
            pixel2=apix,
            wavelength=lmd*1e-9)


    azimuthal_integrator.setFit2D(
            directDist=Ddet*1e3,
            centerX=center,
            centerY=center,
            tilt=0.0,
            tiltPlanRotation=0.0,
            pixelX=apix*1e6,
            pixelY=apix*1e6,
            )
    qs, intensities = azimuthal_integrator.integrate1d(
            pattern,
            min(Npix,1024),
            #unit="q_nm^-1",
            unit="2th_deg",
            )

    return qs, intensities

def diffractionParameters(path):
    """ Extract beam parameters and geometry from given file or directory.

    :param path: Path to file that holds the parameters to extract.
    :type path: str

    """

    # Check if old style.
    if os.path.isdir(path):
        h5_file = os.path.join(path, "diffr_out_0000001.h5")
    elif os.path.isfile(path):
        h5_file = path
    else:
        raise IOError("%s: no such file or directory." % (path))

    # Setup return dictionary.
    parameters_dict = {'beam':{}, 'geom':{}}

    # Open file.
    try:
        with h5py.File(h5_file, 'r') as h5:
            # Loop over entries in /params.
            for top_key in ['beam', 'geom']:
                # Loop over groups.
                for key, val in h5['params/%s' % (top_key)].items():
                    # Insert into return dictionary.
                    parameters_dict[top_key][key] = val.value
    except:
        pass
    # Return.
    return parameters_dict

if __name__ == "__main__":
    main()



