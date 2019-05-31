"""Arm policy, computes action based on cumulative clipped advantage values
"""
import torch


class Policy():
    """Arm policy - initialized with arbitrary network
    that maps observations to vector of size one greater than
    the size of the action space.

    If started in debug mode, debug logs of action values
    and percentages are printed.

    Arguments:
        network {torch.nn.Module} -- arbitrary pytorch network

    Keyword Arguments:
        debug {bool} -- toggle to enable debug logs (default: {False})
    """

    def __init__(self, network, future=False, debug=False):
        self.network = network
        self.future = future
        self.debug = debug

        self.device = network.device

    def __call__(self, obs, action_dim):
        return self.forward(obs, action_dim)

    def forward(self, obs, action_dim):
        """Computes action from observations and action space
        dimensionality

        Arguments:
            obs {torch.Tensor} -- tensor of observations
            action_dim {int} -- dimensionality of actions space

        Returns:
            int -- action
        """
        values = self.network(obs)
        expected_values = values[:, 0]
        cf_values = values[:, 1:]
        action_values = torch.clamp(cf_values - expected_values, min=0.0)
        if torch.sum(action_values):
            action_probs = action_values / torch.sum(action_values)
        else:
            action_probs = torch.full([action_dim], 1/action_dim)
        action = int(torch.multinomial(action_probs, 1))
        if self.debug:
            print('q_plus: ', cf_values)
            print('v: ', expected_values)
            print('action values: ', action_values)
            print('action probs: ', action_probs)
            print('action: ', action)
        return action
