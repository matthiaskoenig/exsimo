from typing import Dict
from matplotlib.pyplot import Figure
import numpy as np
import pandas as pd

from sbmlsim.experiment import SimulationExperiment
from sbmlsim.data import DataSet
from sbmlsim.timecourse import Timecourse, TimecourseSim, TimecourseScan
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
    def scans(self) -> Dict[str, TimecourseScan]:
        Q_ = self.ureg.Quantity
        glc_scan = TimecourseScan(
            tcsim=TimecourseSim([
                Timecourse(start=0, end=70*60, steps=2000, changes={
                    '[glyglc]': Q_(350, 'mM')
                })
            ], time_offset=600),
            scan={'[glc_ext]': Q_(np.linspace(3.6, 4.6, num=6), 'mM')},
        )
        return {
            "glc_scan": glc_scan
        }

    @property
    def figures(self) -> Dict[str, Figure]:

        xunit = "hr"
        yunit_flux = "µmol/kg/min"
        yunit_ratio = "percent"

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
        fig.subplots_adjust(wspace=.3, hspace=.3)
        axes = (ax1, ax2, ax3, ax4)

        result = self.scan_results['glc_scan']
        kwargs = {
            'color': "black",
            'linestyle': "-",
            'linewidth': "2",
        }
        add_line(ax1, result, xid="time", yid="HGP", xunit=xunit, yunit=yunit_flux,
                 all_lines=True, **kwargs)
        add_line(ax2, result, xid="time", yid="GNG", xunit=xunit, yunit=yunit_flux,
                 all_lines=True, **kwargs)
        add_line(ax3, result, xid="time", yid="GLY", xunit=xunit, yunit=yunit_flux,
                 all_lines=True, **kwargs)

        # manual plot of s.GNG/s.HGP * 100
        for df in result.frames:
            xk = df['time'].values * result.ureg(result.udict['time'])
            xk = xk.to(xunit)
            yk = df['GNG'].values/df['HGP'].values * 100
            ax4.plot(xk, yk, '-', **kwargs)

        # experimental data
        dset = self.datasets["Nuttal2008_TabA"]
        kwargs = {
            'color': "black",
            'linestyle': "None",
            'alpha': 0.6,
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
        ax1.set_ylim(top=30)
        ax2.set_ylabel(f'GNG [{yunit_flux}]')
        ax2.set_ylim(top=14)
        ax3.set_ylabel(f'GLY [{yunit_flux}]')
        ax3.set_ylim(top=20)
        ax4.set_ylabel(f'GNG/HGP [{yunit_ratio}]')
        ax4.set_ylim(top=100)
        for ax in axes:
            ax.set_xlabel(f'time [{xunit}]')
            ax.set_ylim(bottom=0)
            ax.set_xlim(left=10)
            ax.legend()

        return {
            "fig1": fig
        }
