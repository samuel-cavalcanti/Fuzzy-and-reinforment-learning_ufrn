from PioneerRobot.VrepPioneer import VrepPioneer
from Model.DeepQLearning import DeepQLearning
import keras
from Agent import Agent
from reward_function import RewardFunction


def build_model(input_shape: tuple, output_size: int) -> keras.Model:
    n_nodes = 45
    input_layer = keras.layers.Input(shape=input_shape)

    first_hidden_layer = keras.layers.Dense(n_nodes, activation="relu")(input_layer)

    second_hidden_layer = keras.layers.Dense(n_nodes, activation="relu")(first_hidden_layer)

    third_hidden_layer = keras.layers.Dense(n_nodes, activation="relu")(second_hidden_layer)

    output_layer = keras.layers.Dense(output_size, activation=keras.activations.softmax)(third_hidden_layer)

    model = keras.models.Model(inputs=input_layer, outputs=output_layer)

    model.compile(optimizer=keras.optimizers.Adam(), loss="mse")
    return model


def build_reward_function():
    close_points = [-1.2, 0, 0.2, 0.3]

    good_points = [0.2, 0.4, 0.7]

    far_points = [0.6, 0.8, 1, 1.2]

    bad_points = [-1, -1, 0]

    neutral_points = [-0.5, 0, 0.5]

    good_reward_points = [0, 1, 1.2]

    reward_function = RewardFunction(close_points, good_points, far_points,
                                     bad_points, good_reward_points, neutral_points)

    return reward_function


if __name__ == '__main__':
    robot = VrepPioneer("127.0.0.1", 19996)
    neural_network = build_model((2,), 2)

    model = DeepQLearning(model=neural_network, random_func=robot.random_move, size_memory=1000)

    reward_function = build_reward_function()

    agent = Agent(robot, model, reward_function)

    # agent.control_agent()

    model_file = "Weights/robot"

    # agent.learn_by_demonstration("Dataset/dataset.csv", model_file)

    agent.learn(model_file)
