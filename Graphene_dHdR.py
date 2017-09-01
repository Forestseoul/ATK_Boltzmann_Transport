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
nlsave('Graphene_dHdR.hdf5', bulk_configuration)

# -------------------------------------------------------------
# Hamiltonian Derivatives
# -------------------------------------------------------------
hamiltonian_derivatives = HamiltonianDerivatives(
    configuration=bulk_configuration,
    repetitions=(11, 11, 1),
    atomic_displacement=0.01*Angstrom,
    )
nlsave('Graphene_dHdR.hdf5', hamiltonian_derivatives)
