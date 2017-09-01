# -*- coding: utf-8 -*-
# -------------------------------------------------------------
# Bulk Configuration
# -------------------------------------------------------------

# Set up lattice
lattice = Hexagonal(2.45576592572*Angstrom, 20.0*Angstrom)

# Define elements
elements = [Carbon, Carbon]

# Define coordinates
fractional_coordinates = [[ 0.000000000011, -0.000000000011,  0.            ],
                          [ 0.333333333353,  0.666666666647,  0.            ]]

# Set up configuration
bulk_configuration = BulkConfiguration(
    bravais_lattice=lattice,
    elements=elements,
    fractional_coordinates=fractional_coordinates
    )

# -------------------------------------------------------------
# Calculator
# -------------------------------------------------------------
#----------------------------------------
# Exchange-Correlation
#----------------------------------------
exchange_correlation = LDA.PZ

k_point_sampling = MonkhorstPackGrid(
    na=3,
    nb=3,
    )
numerical_accuracy_parameters = NumericalAccuracyParameters(
    occupation_method=MethfesselPaxton(1000.0*Kelvin*boltzmann_constant, 1),
    k_point_sampling=k_point_sampling,
    density_mesh_cutoff=90.0*Hartree,
    )

calculator = LCAOCalculator(
    exchange_correlation=exchange_correlation,
    numerical_accuracy_parameters=numerical_accuracy_parameters,
    )

bulk_configuration.setCalculator(calculator)
nlprint(bulk_configuration)
bulk_configuration.update()
nlsave('Graphene_dynmat.hdf5', bulk_configuration)

# -------------------------------------------------------------
# Dynamical Matrix
# -------------------------------------------------------------
dynamical_matrix = DynamicalMatrix(
    configuration=bulk_configuration,
    repetitions=(11, 11, 1),
    atomic_displacement=0.01*Angstrom,
    acoustic_sum_rule=True,
    symmetrize=True,
    finite_difference_method=Central,
    force_tolerance=1e-08*Hartree/Bohr**2,
    processes_per_displacement=1,
    log_filename_prefix='displacement_',
    use_wigner_seitz_scheme=False,
    )
nlsave('Graphene_dynmat.hdf5', dynamical_matrix)

# -------------------------------------------------------------
# Phonon Bandstructure
# -------------------------------------------------------------
phonon_bandstructure = PhononBandstructure(
    configuration=bulk_configuration,
    dynamical_matrix=dynamical_matrix,
    route=['G', 'M', 'K', 'G'],
    points_per_segment=100,
    number_of_bands=All
    )
nlsave('Graphene_dynmat.hdf5', phonon_bandstructure)
