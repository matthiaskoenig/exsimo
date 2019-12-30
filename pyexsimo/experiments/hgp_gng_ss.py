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
        return {}

    @property
    def simulations(self) -> Dict[str, TimecourseSim]:

        # TODO: model change, constant boundary
        # TODO: 2D parameter scan

        glc_ext_vec = np.linspace(2, 14, num=40)
        glyglc_vec = np.linspace(0, 500, num=40)

        HGP = np.zeros(shape=(glc_ext_vec.size, glyglc_vec.size))
        GNG = np.zeros(shape=(glc_ext_vec.size, glyglc_vec.size))
        GLY = np.zeros(shape=(glc_ext_vec.size, glyglc_vec.size))

        print(r2.timeCourseSelections)
        Nt = 10

        results = []

        for p, glc_ext in enumerate(glc_ext_vec):
            for q, glyglc in enumerate(glyglc_vec):
                r2.resetAll()
                r2.resetToOrigin()
                r2.setValue('[glyglc]', glyglc)  # [mM]
                r2.setValue('[glc_ext]', glc_ext)  # [mM]

                s = r2.simulate(0, 1000, Nt)
                s = pd.DataFrame(s, columns=s.colnames)
                HGP[p, q] = s.HGP[Nt - 1]
                GNG[p, q] = s.GNG[Nt - 1]
                GLY[p, q] = s.GLY[Nt - 1]
                results.append(s)

        return {}

    @property
    def figures(self) -> Dict[str, Figure]:


        return {
        }
