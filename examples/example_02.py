from ovito.io import import_file
from ovito.modifiers import ExpressionSelectionModifier
import GenerateRandomSolution as grs
from numpy import unique


def printParticleTypeDistribution(data):
    uni, cts = unique(data.particles["Particle Type"], return_counts=True)
    for u, c in zip(uni, cts):
        print(f"Type = {u}: concentration = {c/data.particles.count}")


def main():
    print(grs.__file__)
    pipeline = import_file("fcc.lmp")
    print("\nInitial particle types:")
    printParticleTypeDistribution(pipeline.compute())

    print("\nSelecting atoms with a reduced position < 0.5")
    pipeline.modifiers.append(
        ExpressionSelectionModifier(expression="ReducedPosition.X < 0.5")
    )

    targetConcentrations = [0.25, 0.5, 0.25]
    seed = 1323
    print("\nModifier settings:")
    print(f"Target concentrations = {targetConcentrations}")
    print(f"Seed = {seed}")
    print(f"Only selected = {True}")

    mod = grs.GenerateRandomSolidSolution()
    mod.concentrations = targetConcentrations
    mod.seed = seed
    mod.only_selected = True
    pipeline.modifiers.append(mod)

    print("\nFinal particle types:")
    printParticleTypeDistribution(pipeline.compute())


if __name__ == "__main__":
    main()
