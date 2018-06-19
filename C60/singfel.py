from SimEx import *

sample = 'c60_super10.pdb'
#sample = 'c60.pdb'




# Detector panel: 3x oversampled
oversampling_factor=3
detector_panel = DetectorPanel(ranges={'fast_scan_min': 0,
                                       'fast_scan_max': 1536//oversampling_factor-1,
                                       'slow_scan_min': 0,
                                       'slow_scan_max': 1536//oversampling_factor-1},
                                       pixel_size=1.1e-4*meter*oversampling_factor,
                                       photon_response=1.0,
                                       distance_from_interaction_plane=0.0794*meter,
                                       corners={'x': -256, 'y': -256},
                                       )

detector_geometry = DetectorGeometry(panels=[detector_panel])

beam = PhotonBeamParameters(
                        photon_energy=10.0e3*electronvolt,
                        beam_diameter_fwhm=2.0e-7*meter,
                        pulse_energy=2.0e-3*joule,
                        photon_energy_relative_bandwidth=0.001,
                        divergence=None,
                        photon_energy_spectrum_type="tophat",
                    )

parameters = SingFELPhotonDiffractorParameters(
        uniform_rotation=False,
        sample=sample,
        number_of_diffraction_patterns=9923,
        detector_geometry=detector_geometry,
        beam_parameters=beam
)

diffractor = SingFELPhotonDiffractor(
        parameters=parameters,
        input_path=None,
        output_path="diffr",
        )

#diffractor.backengine()
diffractor.saveH5()


