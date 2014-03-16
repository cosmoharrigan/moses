"""
PLN representation of the "smokes" sample from Tuffy Markov Logic Networks

A test diary is located here:
https://github.com/opencog/test-datasets/tree/master/pln/tuffy/smokes/tests

More details on this sample are available here:
https://github.com/cosmoharrigan/tuffy/tree/master/samples/smoke
http://hazy.cs.wisc.edu/hazy/tuffy/doc/tuffy-manual.pdf

Instructions:
- Add the module path to your PYTHON_EXTENSION_DIRS in opencog.conf:
  ../opencog/python/pln/examples/tuffy/smokes
- Run the cogserver
- Clone the test-datasets repository:
  https://github.com/opencog/test-datasets
- From that repository, load this file into the cogserver:
  pln/tuffy/smokes/smokes.scm
- Run these commands in the cogserver:
  loadpy smokes_agent
  agents-start smokes_agent.InferenceAgent
- Use the Scheme shell to monitor the inference progress
"""

from opencog.cogserver import MindAgent
from opencog.atomspace import types
from pln.chainers import Chainer
from pln.rules import *

__author__ = 'Cosmo Harrigan'

__VERBOSE__ = False


class InferenceAgent(MindAgent):
    def __init__(self):
        self.chainer = None

    def create_chainer(self, atomspace):
        self.chainer = Chainer(atomspace, stimulateAtoms=False)

        # EvaluationToMember, MemberToInheritance
        self.chainer.add_rule(EvaluationToMemberRule(self.chainer))
        self.chainer.add_rule(MemberToEvaluationRule(self.chainer))
        self.chainer.add_rule(MemberToInheritanceRule(self.chainer))
        self.chainer.add_rule(InheritanceToMemberRule(self.chainer))

        # ModusPonens:
        # Implication smokes(x) cancer(X)
        # smokes(Anna)
        # |= cancer(Anna)
        self.chainer.add_rule(
            ModusPonensRule(self.chainer, types.ImplicationLink))

    def run(self, atomspace):
        if self.chainer is None:
            self.create_chainer(atomspace)
            return

        result = self.chainer.forward_step()

        if __VERBOSE__:
            print result

        return result