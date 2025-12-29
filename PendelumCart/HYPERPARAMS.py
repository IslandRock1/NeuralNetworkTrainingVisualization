

# NeuralNetwork size
NUM_INPUT_NODES = 5
NUM_OUTPUT_NODES = 1
NUM_NODES_IN_HIDDEN_LAYERS = [20, 50, 20] # Example [10, 20, 5]
LAYER_STRUCTURE = [NUM_INPUT_NODES] + NUM_NODES_IN_HIDDEN_LAYERS + [NUM_OUTPUT_NODES]
# [] for hidden layers means the input and output is directly connected.

# Training size
NUM_NETWORKS_PER_ITERATION = 100 # Warning, will take long time, even with less than 100

# Genetic modifications
STOPPING_CRITERICA = 0 # 0 means the model will not stop without the user stopping it
MAX_TIME = 0

PERCENTAGE_OF_BEST_NETWORKS_TO_KEEP = 5
PERCENTAGE_OF_NEW_RANDOM_NETWORKS = 20

PERCENTAGE_OF_NETWORKS_TO_BE_ALTERNATIVES_FOR_MODIFIED = 30

SCALE_VALUE_FOR_CHANGES_TO_BIAS_AND_WEIGHT = 0.1

# The next three must sum to 100
PERCENTAGE_CHANCE_TO_CHANGE_ACTIVATION_FUNCTION = 3 # 3
PERCENTAGE_CHANCE_TO_CHANGE_BIAS = 7 # 7
PERCENTAGE_CHANCE_TO_CHANGE_ONE_WEIGHT = 90 # 90

MAX_NUMBER_OF_CHANGES_PER_MUTATION = 5


# Computer specs
NUM_CPU_CORES = 7 # 0 will default to the number of physical cores the processor has.

# Debug info
DEBUG_INFO = True


# Simulation Params
