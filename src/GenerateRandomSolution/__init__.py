from ovito.data import DataCollection, ParticleType, DataTable, ElementType
from ovito.pipeline import ModifierInterface
import numpy as np
from traits.api import Bool, Int, ListFloat


class GenerateRandomSolution(ModifierInterface):
    only_selected = Bool(False, label="Only selected")
    concentrations = ListFloat([0.5, 0.5], label="Concentrations", minlen=1)
    seed = Int(1234, label="Seed")

    def modify(self, data: DataCollection, frame: int, **kwargs):
        if (self.only_selected) and "Selection" not in data.particles.keys():
            raise KeyError("No selection defined")
        if not np.isclose(np.sum(self.concentrations), 1):
            raise ValueError(f"Concentrations: {np.sum(self.concentrations)} != 1")

        rng = np.random.default_rng(self.seed)

        count = (
            data.particles.count
            if not self.only_selected
            else np.count_nonzero(data.particles["Selection"])
        )

        # Extend particle types if necessary
        while len(self.concentrations) > len(data.particles["Particle Type"].types):
            new_id = len(data.particles["Particle Type"].types) + 1
            data.particles_["Particle Type_"].types.append(
                ParticleType(
                    id=new_id,
                    name=f"Type {new_id}",
                    color=rng.random(size=3),
                )
            )

        # Populate new concentration array
        new_types = []
        for i, c in enumerate(self.concentrations):
            new_types += [i + 1] * int(count * c)
            x_p = np.cumsum(self.concentrations)

        while len(new_types) < count:
            new_types.append(np.sum(x_p < rng.random()) + 1)

        # Randomize new types
        new_types = np.array(new_types)
        rng.shuffle(new_types)

        # Assign new particle types
        if self.only_selected:
            data.particles_["Particle Type_"][
                np.where(data.particles["Selection"] == 1)[0]
            ] = new_types
        else:
            data.particles_["Particle Type_"][...] = new_types

        # Calculate new concentration
        ptype, count = np.unique(data.particles["Particle Type"], return_counts=True)
        conc = count / np.sum(count)

        # Create table to visualize the new concentrations
        table = DataTable(
            title="New concentrations",
            plot_mode=DataTable.PlotMode.BarChart,
        )
        table.x = table.create_property("Particle type", data=ptype)
        for i, p in enumerate(ptype):
            table.x.types.append(
                ElementType(
                    id=i, name=data.particles["Particle Type"].type_by_id(p).name
                )
            )
        table.y = table.create_property("Concentration", data=conc)
        data.objects.append(table)
