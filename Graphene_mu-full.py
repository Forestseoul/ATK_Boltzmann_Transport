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
# Dynamical matrix
# -------------------------------------------------------------
dynamical_matrix = nlread('Graphene_dynmat.hdf5', DynamicalMatrix)[-1]

# -------------------------------------------------------------
# Hamiltonian derivatives
# -------------------------------------------------------------
hamiltonian_derivatives = nlread('Graphene_dHdR.hdf5', HamiltonianDerivatives)[-1]

# -------------------------------------------------------------
# Electron Phonon Coupling
# -------------------------------------------------------------
electron_phonon_coupling = nlread('Graphene_eph.hdf5', ElectronPhononCoupling)[-1]

# -------------------------------------------------------------
# Mobility
# -------------------------------------------------------------
mobility = Mobility(
    configuration=bulk_configuration,
    method=Full,
    electron_phonon_coupling=electron_phonon_coupling,
    temperature=300*Kelvin,
    phonon_modes=All,
    electron_bands=All,
    fermi_shift=0.13*eV,
    energy_broadening=0.003*eV,
    refinement=1,
    calculate_hall_coefficients=False,
    )
nlsave('Graphene_mu-full.hdf5', mobility)
