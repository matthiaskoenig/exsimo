from typing import Dict
from matplotlib.pyplot import Figure

from sbmlsim.experiment import SimulationExperiment
from sbmlsim.data import DataSet
from sbmlsim.timecourse import Timecourse, TimecourseSim
from sbmlsim.plotting_matplotlib import add_data, add_line, plt
from sbmlsim.pkpd import pkpd


class PathwayExperiment(SimulationExperiment):
    @property
    def datasets(self) -> Dict[str, DataSet]:
        dsets = {}
        dset_id = "Nuttal2008_TabA"
        df = self.load_data(dset_id)
        df = df[df.condition == "normal"]  # only healthy controls, no T2DM
        udict = {key: df[f"{key}_unit"].unique()[0] for key in
                    ["time", "hgp", "gng", "gly", "gng_hgp"]}

        dsets[dset_id] = DataSet.from_df(df, udict=udict, ureg=self.ureg)
        return dsets

    @property
    def simulations(self) -> Dict[str, TimecourseSim]:
        return {}

    @property
    def figures(self) -> Dict[str, Figure]:

        xunit = "hr"
        yunit_flux = "µmol/kg/min"
        yunit_ratio = "percent"

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
        fig.subplots_adjust(wspace=.3, hspace=.3)
        axes = (ax1, ax2, ax3, ax4)

        '''
        # simulation
        for s in results:
            time = s.time / 60 + 10  # +10
            ax1.plot(time, -s.HGP, color="black", linewidth=1.0)
            # ax1.set_ylim(0, 17)
            ax2.plot(time, -s.GNG, color="black", linewidth=1.0)
            # ax2.set_ylim(0, 12)
            ax3.plot(time, -s.GLY, color="black", linewidth=1.0)
            # ax3.set_ylim(0, 12)
            ax4.plot(time, s.GNG / s.HGP * 100, color="black", linewidth=1.0)
            # ax4.set_ylim(0, 100)
        '''

        # experimental data
        dset = self.datasets["Nuttal2008_TabA"]
        kwargs = {
            'color': "black",
            'linestyle': "None",
        }
        add_data(ax1, dset, xid="time", yid="hgp", xunit=xunit,
                 yunit=yunit_flux, label="HGP", **kwargs)
        add_data(ax2, dset, xid="time", yid="gng", xunit=xunit,
                 yunit=yunit_flux, label="GNG", **kwargs)
        add_data(ax3, dset, xid="time", yid="gly", xunit=xunit,
                 yunit=yunit_flux, label="GLY", **kwargs)
        add_data(ax4, dset, xid="time", yid="gng_hgp", xunit=xunit,
                 yunit=yunit_ratio, label="GNG/HGP", **kwargs)

        ax1.set_ylabel(f'HGP [{yunit_flux}]')
        ax2.set_ylabel(f'GNG [{yunit_flux}]')
        ax3.set_ylabel(f'GLY [{yunit_flux}]')
        ax4.set_ylabel(f'GNG/HGP [{yunit_ratio}]')
        for ax in axes:
            ax.set_xlabel(f'time [{xunit}]')
            ax.set_ylim(bottom=0)
            ax.legend()

        return {
            "fig1": fig
        }
