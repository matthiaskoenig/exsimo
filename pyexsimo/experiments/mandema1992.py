from typing import Dict
from matplotlib.pyplot import Figure

from sbmlsim.experiment import SimulationExperiment
from sbmlsim.data import DataSet
from sbmlsim.timecourse import Timecourse, TimecourseSim
from sbmlsim.plotting_matplotlib import add_data, add_line, plt
from sbmlsim.pkpd import pkpd

from pkdb_models.models.midazolam.molecular_weights import Mr_mid, Mr_mid1oh

class Mandema1992(SimulationExperiment):
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
        return {
            **self.simulation_mid()
        }

    @property
    def figures(self) -> Dict[str, Figure]:
        return {
            **self.figure_mid()
        }

    def figure_mid(self):
        title = f"{self.sid}"
        xunit = "min"
        yunit_mid = "nmol/ml"
        yunit_mid1oh = "nmol/ml"

        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))

        # simulation
        ax1.set_title(f"{title} (midazolam iv)")
        ax2.set_title(f"{title} (1-hydroxymidazolam iv)")
        ax3.set_title(f"{title} (midazolam po)")
        for ax in (ax1, ax2, ax3):
            ax.set_ylabel(f"midazolam [{yunit_mid}]")
        for ax in (ax4, ax5, ax6):
            ax.set_ylabel(f"1-hydroxy midazolam [{yunit_mid1oh}]")

        kwargs = {"color": "black", "linewidth": 2.0}
        add_line(ax=ax1, data=self.results['mid_iv'], xid='time', yid="Cve_mid",
                 xunit=xunit, yunit=yunit_mid,
                 label="midazolam venous blood", **kwargs)
        add_line(ax=ax4, data=self.results['mid_iv'], xid='time', yid="Cve_mid1oh",
                 xunit=xunit, yunit=yunit_mid1oh,
                 label="1-hydroxy midazolam venous blood", **kwargs)

        add_line(ax=ax2, data=self.results['mid1oh_iv'], xid='time', yid="Cve_mid",
                 xunit=xunit, yunit=yunit_mid,
                 label="midazolam venous blood", **kwargs)
        add_line(ax=ax5, data=self.results['mid1oh_iv'], xid='time', yid="Cve_mid1oh",
                 xunit=xunit, yunit=yunit_mid1oh,
                 label="1-hydroxy midazolam venous blood", **kwargs)

        add_line(ax=ax3, data=self.results['mid_po'], xid='time', yid="Cve_mid",
                 xunit=xunit, yunit=yunit_mid,
                 label="midazolam venous blood", **kwargs)
        add_line(ax=ax6, data=self.results['mid_po'], xid='time', yid="Cve_mid1oh",
                 xunit=xunit, yunit=yunit_mid1oh,
                 label="1-hydroxy midazolam venous blood", **kwargs)

        # plot data
        data_def = {
            "Fig1A_midazolam": {'ax': ax1, 'key': 'mid', 'unit': yunit_mid},
            "Fig1A_1-hydroxymidazolam": {'ax': ax4, 'key': 'mid1oh', 'unit': yunit_mid1oh},
            "Fig2A_1-hydroxymidazolam": {'ax': ax5, 'key': 'mid1oh', 'unit': yunit_mid1oh},
            "Fig3A_midazolam": {'ax': ax3, 'key': 'mid', 'unit': yunit_mid},
            "Fig3A_1-hydroxymidazolam": {'ax': ax6, 'key': 'mid1oh', 'unit': yunit_mid1oh},
        }
        for dset_key, dset_info in data_def.items():
            add_data(dset_info['ax'], self.datasets[dset_key],
                     xid="time", yid="mean", yid_se="se",
                    xunit=xunit, yunit=dset_info['unit'], count=None, color="black",
                 label=dset_info['key'])

        for ax in (ax1, ax2, ax3, ax4, ax5, ax6):
            # ax.set_yscale("log")
            ax.set_xlabel(f"time [{xunit}]")
            ax.legend()
        return {"fig1": fig}

    def simulation_mid(self) -> Dict[str, TimecourseSim]:
        """ Mandema1992

        - midazolam, iv, 0.1 [mg/kg]
        - 1-hydroxy midazolam, iv, 0.15 [mg/kg]
        - midazolam, po, 7.5 [mg]
        """
        Q_ = self.ureg.Quantity

        # FIXME: use real body weight of study
        bodyweight = Q_(69, 'kg')
        mid_iv = Q_(0.1, 'mg/kg') * bodyweight
        mid1oh_iv = Q_(0.15, 'mg/kg') * bodyweight
        mid_po = Q_(7.5, 'mg')

        tcsims = {}
        tcsims["mid_iv"] = TimecourseSim([
            Timecourse(start=0, end=300, steps=600, changes={
                'IVDOSE_mid': mid_iv}),
        ])
        tcsims["mid1oh_iv"] = TimecourseSim([
            Timecourse(start=0, end=300, steps=600, changes={
                'IVDOSE_mid1oh': mid1oh_iv}),
        ])
        tcsims["mid_po"] = TimecourseSim([
            Timecourse(start=0, end=300, steps=600, changes={
                'PODOSE_mid': mid_po}),
        ])

        return tcsims
