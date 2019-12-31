from typing import Dict
from matplotlib.pyplot import Figure
import numpy as np
import pandas as pd

from sbmlsim.experiment import SimulationExperiment
from sbmlsim.data import DataSet
from sbmlsim.timecourse import Timecourse, TimecourseSim, TimecourseScan
from sbmlsim.plotting_matplotlib import add_data, add_line, plt


class PathwaySSExperiment(SimulationExperiment):
    @property
    def datasets(self) -> Dict[str, DataSet]:
        return {}

    @property
    def scans(self) -> Dict[str, TimecourseScan]:
        Q_ = self.ureg.Quantity
        ss_scan = TimecourseScan(
            tcsim=TimecourseSim([
                Timecourse(start=0, end=1000, steps=10)
            ]),
            scan={
                # '[glc_ext]': Q_(np.linspace(2, 14, num=10), 'mM'),
                # '[glyglc]': Q_(np.linspace(0, 500, num=10), 'mM')
                '[glc_ext]': Q_(np.linspace(2, 14, num=40), 'mM'),
                '[glyglc]': Q_(np.linspace(0, 500, num=40), 'mM')
            },
        )
        return {
            "ss_scan": ss_scan
        }

    @property
    def simulations(self) -> Dict[str, TimecourseSim]:
        return {}

    @property
    def figures(self) -> Dict[str, Figure]:
        import matplotlib
        import matplotlib.cm as cm
        matplotlib.rcParams['contour.negative_linestyle'] = 'solid'

        f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        f.subplots_adjust(hspace=0.3, wspace=0.3)
        axes = (ax1, ax2, ax3)
        for ax in (ax1, ax2, ax3):
            ax.set_xlabel('glucose [mM]')
            ax.set_ylabel('glycogen [mM]')

        # data processing
        result = self.scan_results['ss_scan']
        tcscan = self.scans['ss_scan']
        glc_ext = tcscan.scan['[glc_ext]']
        glyglc = tcscan.scan['[glyglc]']

        n0 = len(result.vecs[0])
        n1 = len(result.vecs[1])
        HGP = np.zeros(shape=(n0, n1))
        GNG = np.zeros(shape=(n0, n1))
        GLY = np.zeros(shape=(n0, n1))

        for k, df in enumerate(result.frames):
            index_list = result.indices[k]
            HGP[index_list] = df.HGP.values[-1]
            GNG[index_list] = df.GNG.values[-1]
            GLY[index_list] = df.GLY.values[-1]

        if result.keys[0] == '[glc_ext]':
            pass
        else:
            HGP = HGP.transpose()
            GNG = GNG.transpose()
            GLY = GLY.transpose()

        # HGP
        ax1.set_title("HGU/HGP")
        ax2.set_title("glycolysis/gluconeogenesis")
        ax3.set_title("glycogen synthesis/glycogenolysis")

        for ax, data in {ax1: HGP, ax2: GNG, ax3: GLY}.items():

            im = ax.imshow(data.transpose(), interpolation='bilinear',
                            cmap=cm.seismic, origin="lower",
                            extent=[2, 14, 0, 500],
                            # extent=[np.min(glc_ext), np.max(glc_ext), np.min(glyglc), np.max(glyglc)],
                            aspect="auto")

            CS = ax.contour(glc_ext, glyglc, (data.transpose()),
                             np.linspace(-28, 28, num=15),
                             colors='k')
            ax.clabel(CS, inline=1, fontsize=10)

        return {
            'fig1': f
        }
