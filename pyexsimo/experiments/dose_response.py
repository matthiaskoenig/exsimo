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

        # dose-response data for hormones
        for hormone_key in ['Epinephrine', 'Glucagon', 'Insulin']:
            df = self.load_data(f"DoseResponse_Tab{hormone_key}")
            df = df[df.condition == "normal"]  # only healthy controls
            epi_normal_studies = [
                "Degn2004", "Lerche2009", "Mitrakou1991",
                "Levy1998", "Israelian2006", "Jones1998",
                "Segel2002"
            ]
            glu_normal_studies = [
                "Butler1991", "Cobelli2010", "Fery1993"
                "Gerich1993", "Henkel2005", "Mitrakou1991"
                "Basu2009", "Mitrakou1992",
                "Degn2004", "Lerche2009",
                "Levy1998", "Israelian2006",
                "Segel2002"
            ]
            ins_normal_studies = [
                'Ferrannini1988', 'Fery1993', 'Gerich1993', 'Basu2009',
                'Lerche2009', 'Henkel2005', 'Butler1991', 'Knop2007',
                'Cobelli2010', 'Mitrakou1992',
            ]
            # filter studies
            if hormone_key == "Epinephrine":
                df = df[df.reference.isin(epi_normal_studies)]
            elif hormone_key == "Glucagon":
                df = df[df.reference.isin(glu_normal_studies)]
                # correct glucagon data for insulin suppression (hyperinsulinemic clamps)
                insulin_supression = 3.4
                glu_clamp_studies = [
                    "Degn2004", "Lerche2009", "Levy1998", "Israelian2006","Segel2002"
                ]
                df.loc[df.reference.isin(glu_clamp_studies), 'mean'] = insulin_supression * df[df.reference.isin(glu_clamp_studies)]['mean']
                df.loc[df.reference.isin(glu_clamp_studies), 'se'] = insulin_supression * df[df.reference.isin(glu_clamp_studies)]['se']


            elif hormone_key == "Insulin":
                df = df[df.reference.isin(ins_normal_studies)]

            # correct glucagon data for insulin_suppression
            # insulin_supression = 3.4
            # glu_corrected = [
            #
            # ]

            udict = {
                'glc': df["glc_unit"].unique()[0],
                'mean': df["unit"].unique()[0],
            }
            dsets[hormone_key.lower()] = DataSet.from_df(df, udict=udict, ureg=self.ureg)

        return dsets

    @property
    def simulations(self) -> Dict[str, TimecourseSim]:
        return {}

    @property
    def figures(self) -> Dict[str, Figure]:

        xunit = "mM"
        yunit_hormone = "pmol/l"
        yunit_gamma = "dimensionless"

        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 10))
        f.subplots_adjust(wspace=.3, hspace=.3)
        axes = (ax1, ax2, ax3, ax4)

        # simulation
        '''
        ax1.plot(glc_ext_vec, dose_response['glu'], color="black")
        ax2.plot(glc_ext_vec, dose_response['epi'], color="black",
                 linewidth=2.0)
        ax3.plot(glc_ext_vec, dose_response['ins'], color="black",
                 linewidth=2.0)
        ax4.plot(glc_ext_vec, dose_response['gamma'], color="black",
                 linewidth=2.0)
        '''

        # experimental data
        kwargs = {
            'color': "black",
            'linestyle': "None",
        }
        add_data(ax1, self.datasets["glucagon"], xid="glc", yid="mean", yid_se="se",
                 xunit=xunit, yunit=yunit_hormone, label="Glucagon", **kwargs)
        add_data(ax2, self.datasets["epinephrine"], xid="glc", yid="mean",
                 yid_se="se",
                 xunit=xunit, yunit=yunit_hormone, label="Epinephrine", **kwargs)
        add_data(ax3, self.datasets["insulin"], xid="glc", yid="mean",
                 yid_se="se",
                 xunit=xunit, yunit=yunit_hormone, label="Insulin", **kwargs)

        ax1.set_ylabel(f'glucagon [{yunit_hormone}]')
        ax1.set_ylim(0, 200)
        ax2.set_ylabel(f'epinephrine [{yunit_hormone}]')
        ax2.set_ylim(0, 7000)
        ax3.set_ylabel(f'insulin [{yunit_hormone}]')
        ax3.set_ylim(0, 800)
        ax4.set_ylabel(f'gamma [{yunit_gamma}]')
        ax4.set_ylim(0, 1)

        for ax in axes:
            ax.set_xlabel(f'glucose [{xunit}]')
            ax.set_xlim(2, 20)

        ax2.set_xlim(2, 8)

        return {
            'fig1': f
        }


