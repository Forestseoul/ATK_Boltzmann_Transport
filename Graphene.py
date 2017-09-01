# Set up lattice
lattice = Hexagonal(2.4612*Angstrom, 20.0*Angstrom)

# Define elements
elements = [Carbon, Carbon]

# Define coordinates
fractional_coordinates = [[ 0.            ,  0.            ,  0.            ],
                          [ 0.333333333333,  0.666666666667,  0.            ]]

# Set up configuration
bulk_configuration = BulkConfiguration(
    bravais_lattice=lattice,
    elements=elements,
    fractional_coordinates=fractional_coordinates
    )
