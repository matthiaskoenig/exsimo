from typing import Dict
from matplotlib.pyplot import Figure

from sbmlsim.experiment import SimulationExperiment
from sbmlsim.data import DataSet
from sbmlsim.timecourse import Timecourse, TimecourseSim
from sbmlsim.plotting_matplotlib import add_data, add_line, plt
from sbmlsim.pkpd import pkpd


class DoseResponseExperiment(SimulationExperiment):
    @property
    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for fig_id in ["Fig1A", "Fig2A", "Fig3A"]:
            dframes = self.load_data_pkdb(f"{self.sid}_{fig_id}", na_values=["na"])
            for substance, df in dframes.items():
                udict = {
                    "time": df.time_unit.values[0],
                    "mean": df.unit.values[0],
                    "se": df.unit.values[0],
                }
                if substance == "midazolam":
                    Mr = Mr_mid
                elif substance == "1-hydroxymidazolam":
                    Mr = Mr_mid1oh
                else:
                    raise ValueError
                df["mean"] = df["mean"] / Mr   # [ng/ml] -> nmol/ml
                df["se"] = df["se"] / Mr  # [ng/ml] -> nmol/ml
                udict["mean"] = "nmol/ml"
                udict["se"] = "nmol/ml"

                dsets[f"{fig_id}_{substance}"] = DataSet.from_df(df,
                                        udict=udict,
                                        ureg=self.ureg)
        return dsets

    @property
    def simulations(self) -> Dict[str, TimecourseSim]:
        return {}

    @property
    def figures(self) -> Dict[str, Figure]:
        return {}


