from typing import Dict
from matplotlib.pyplot import Figure
import numpy as np

from sbmlsim.experiment import SimulationExperiment
from sbmlsim.data import DataSet
from sbmlsim.timecourse import Timecourse, TimecourseSim
from sbmlsim.plotting_matplotlib import add_data, add_line, plt
from sbmlsim.pkpd import pkpd


class GlycogenExperiment(SimulationExperiment):
    @property
    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        for study_id in ['Magnusson1992', 'Rothman1991', 'Radziuk2001', 'Taylor1996']:
            dset_id = f"Glycogen_Tab{study_id}"
            df = self.load_data(dset_id)
            df = df[df.condition == "normal"]  # only healthy controls
            udict = {key: df[f"{key}_unit"].unique()[0] for key in
                     ["time", "gly"]}
            dsets[study_id] = DataSet.from_df(df, udict=udict, ureg=self.ureg)

        return dsets

    @property
    def simulations(self) -> Dict[str, TimecourseSim]:
        Q_ = self.ureg.Quantity

        # --- glycogenolysis ---
        glc_ext_GLY = np.linspace(3.6, 5.0, num=8)  # [mM]

        for glc_ext in glc_ext_GLY:
            # TODO: 1D parameter scan (time courses)
            tc_sim = TimecourseSim([
                Timecourse(start=0, end=65*60, steps=600,
                           changes={
                               '[glyglc]': Q_(500, "mM"),
                               '[glc_ext]': Q_(glc_ext, "mM"),
                           })
            ])

        # --- glycogen synthesis ---
        glc_ext_GS = np.linspace(5.5, 8.0, num=6)  # [mM]
        for glc_ext in glc_ext_GS:
            tc_sim = TimecourseSim([
                Timecourse(start=0, end=300, steps=600,
                           changes={
                               '[glyglc]': Q_(200, "mM"),
                               '[glc_ext]': Q_(glc_ext, "mM"),
                           })
            ])


        return {}

    @property
    def figures(self) -> Dict[str, Figure]:

        xunit_ax1 = "hr"
        xunit_ax2 = "min"
        yunit_gly = "mM"

        f, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(10, 5))
        f.subplots_adjust(wspace=.3, hspace=.3)
        axes = (ax1, ax2)

        # simulation
        '''
        for s in results_GLY:
            ax1.plot(s.time / 60, s['[glyglc]'], color="black", linewidth=1.0)
        for s in results_GS:
            ax2.plot(s.time / 60, s['[glyglc]'], color="black", linewidth=1.0)
        '''

        # experimental data
        kwargs = {
            'color': "black",
            'linestyle': "--",
        }
        dset = self.datasets["Magnusson1992"]
        add_data(ax1, dset, xid="time", yid="gly",
                 yid_sd="gly_sd",
                 xunit=xunit_ax1, yunit=yunit_gly, label="Glycogen", **kwargs)

        dset = self.datasets["Rothman1991"]
        for subject_id in dset.subject.unique():
            add_data(ax1, dset[dset.subject==subject_id], xid="time", yid="gly",
                 xunit=xunit_ax1, yunit=yunit_gly, label=f"Glycogen {subject_id}", **kwargs)

        dset = self.datasets["Radziuk2001"]
        for ref_id in dset.reference.unique():
            add_data(ax2, dset[dset.reference == ref_id], xid="time",
                     yid="gly",
                     xunit=xunit_ax2, yunit=yunit_gly,
                     label=f"Glycogen {ref_id}", **kwargs)

        dset = self.datasets["Taylor1996"]
        add_data(ax2, dset, xid="time", yid="gly",
                 yid_sd="gly_sd",
                 xunit=xunit_ax2, yunit=yunit_gly, label="Glycogen", **kwargs)

        ax1.set_xlabel(f'time [{xunit_ax1}]')
        ax2.set_xlabel(f'time [{xunit_ax2}]')
        for ax in axes:
            ax.set_ylabel('glycogen [mM]')

        ax1.set_ylim(0, 500)
        ax1.set_xlim(9, 65)
        ax2.set_ylim(180, 340)

        return {
            'fig1': f
        }


