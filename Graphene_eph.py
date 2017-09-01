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
nlsave('Graphene_eph.hdf5', bulk_configuration)

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
k_a = numpy.linspace(1.66334, 1.71744, 20)
k_b = numpy.linspace(-0.027, 0.027, 20)
k_c = numpy.linspace(0, 0, 1)
kpoints = [[a, b, c] for a in k_a for b in k_b for c in k_c]*Angstrom**-1

q_a = numpy.linspace(-0.06, 0.06, 20)
q_b = numpy.linspace(-0.06, 0.06, 20)
q_c = numpy.linspace(0, 0, 1)
qpoints = [[a, b, c] for a in q_a for b in q_b for c in q_c]*Angstrom**-1

electron_phonon_coupling = ElectronPhononCoupling(
    configuration=bulk_configuration,
    dynamical_matrix=dynamical_matrix,
    hamiltonian_derivatives=hamiltonian_derivatives,
    kpoints_cartesian=kpoints,
    qpoints_cartesian=qpoints,
    electron_bands=[3, 4],
    phonon_modes=All,
    energy_tolerance=0.01*eV,
    initial_state_energy_range=[-0.5,0.5]*eV,
    store_dense_coupling_matrices=False,
    )
nlsave('Graphene_eph.hdf5', electron_phonon_coupling)
