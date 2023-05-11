# Generate Random Solution
OVITO Python script modifier to chang the particle type values to create a random solid solution of a given composition.

## Description
Python script modifier for OVITO that changes the particle types in the whole data collection or a selected subset of particles to match a user provided target concentration. The new particle types are distributed randomly to approximate a perfect random solid solution. 

## Parameters 
- `only_selected` / "only selected": Apply the modifier only to the selected particles.
- `conc` / "concentration": List / tuple defining the target concentrations. Their sum has to be equal to 1. 
- `seed` / "Seed": Starting value for the random number generation. 

## Example

## Technical information / dependencies
- Tested on OVITO 3.x.x

## Contact
Daniel Utt (utt@ovito.org)