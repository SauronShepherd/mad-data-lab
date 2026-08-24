import unittest

from server.state import InvestigationState, transition


class StateMachineTests(unittest.TestCase):
    def test_legal_player_journey(self):
        state = transition("BRIEFING", InvestigationState.INVESTIGATION)
        state = transition(state, InvestigationState.EXPERIMENT_RESULT)
        state = transition(state, InvestigationState.INVESTIGATION)
        state = transition(state, InvestigationState.VERDICT)
        self.assertEqual(transition(state, InvestigationState.DEBRIEF), "DEBRIEF")

    def test_illegal_transition_is_rejected(self):
        with self.assertRaises(ValueError):
            transition("BRIEFING", InvestigationState.DEBRIEF)
        with self.assertRaises(ValueError):
            transition("DEBRIEF", InvestigationState.INVESTIGATION)


if __name__ == "__main__": unittest.main()
