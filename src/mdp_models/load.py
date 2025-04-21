import pkg_resources
from collections import defaultdict
import toml

def load(model_name,file_name="models.toml") :
    full_file_name = pkg_resources.resource_filename('mdp_models', "models/" + file_name)
    with open(full_file_name, 'r') as f:
    	models = toml.load(f)
    nodes = models[model_name]
    states = list()
    actions = defaultdict(list)
    transitions = defaultdict(list)
    probabilities = defaultdict(list)
    rewards = defaultdict(list)
    for node in nodes :
        states.append(node["state"])
        actions[node["state"]].append(node["action"])
        transitions[(node["state"],node["action"])].append(node["new-state"])
        probabilities[(node["state"],node["action"],node["new-state"])] = node["probability"]
        rewards[(node["state"],node["action"],node["new-state"])] = node["reward"]
    states = set(states)
    for state in actions :
        actions[state] = set(actions[state])
    def state_iterator() :
        nonlocal states
        return iter(states)
    def action_function(state) :  
        nonlocal actions
        return lambda : iter(actions[state])
    def transition_function(state,action) :
        nonlocal transitions
        return lambda : iter(transitions[(state,action)])
    def probability_function(state,action,new_state) :
        nonlocal probabilities
        return probabilities[(state,action,new_state)]
    def reward_function(state,action,new_state) :
        nonlocal rewards
        return rewards[(state,action,new_state)]
    return state_iterator,action_function,transition_function,probability_function,reward_function




