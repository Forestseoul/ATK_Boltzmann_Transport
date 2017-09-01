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
    na=33,
    nb=33,
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
nlsave('Graphene_mu-line-iso.hdf5', bulk_configuration)

# -------------------------------------------------------------
# Mobility
# -------------------------------------------------------------
mobility_full = nlread('Graphene_mu-line-full.hdf5', Mobility)[-1]

# Generate energy-dependent inverse relaxation times
inverse_relaxation_time=mobility_full.generateEnergyDependentInverseRelaxationTime(
    energies=numpy.linspace(-0.24, 0.24, 100)*eV
    )

kpoint_grid = MonkhorstPackGrid(
    na=99,
    nb=99,
    )

mobility = Mobility(
    configuration=bulk_configuration,
    method=Isotropic,
    energies=numpy.linspace(-0.24, 0.24, 100)*eV,
    inverse_relaxation_time=inverse_relaxation_time,
    electron_bands=[3,4],
    kpoints=kpoint_grid,
    temperature=300*Kelvin,
    fermi_shift=0.13*eV,
    energy_broadening=0.003*eV,
    calculate_hall_coefficients=False,
    )
nlsave('Graphene_mu-line-iso.hdf5', mobility)