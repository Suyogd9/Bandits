import csv
import random
import sys

alg = sys.argv[1]
exp = float(sys.argv[2])
dist = float(sys.argv[3])
decay = float(sys.argv[4])
rwt = float(sys.argv[5])
w0 = float(sys.argv[6])
infile = sys.argv[7]

#Read the csv file
input_rewards = []
with open(infile, 'r') as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)
    for line in csv_reader:
        input_rewards.append(line)

#Bandits function
def bandit_basic(input_rewards, alg, exp, dist, decay, rwt, w0):

    # list of arm numbers
    Arms = [0, 1, 2, 3, 4, 5]
    Arms_count = [0, 0, 0, 0, 0, 0]
    cumulative_reward = 0
    Probability = []

    # Create a list of Initial weights of 6 Arms
    Initial_wt = [w0] * 6
    Weight_window = []

    for i in range(6):
        # In each iteration, add an empty list to the main list
        Weight_window.append([])
    reward_window = []

    for i in range(6):
        # In each iteration, add an empty list to the main list
        reward_window.append([])
    for i in range(6):
        Weight_window[i].append(Initial_wt[i])

    # Normalize weights for each arm and check if the elements in the list are equal if yes take the same weights
    equal_weights_start = all(ele == Initial_wt[0] for ele in Initial_wt)
    print(equal_weights_start)
    if equal_weights_start:
        norm_wt = [float(i) / 1 for i in Initial_wt]
    else:
        norm_wt = [(float(i) - min(Initial_wt)) / (max(Initial_wt) - min(Initial_wt)) for i in Initial_wt]

    # Calculate the initial probabilities
    for i in range(len(norm_wt)):
        Probability.append((norm_wt[i]) * (1 - exp) + (exp * dist))

    # Normalizing the probabilities
    Probability = [float(i) / sum(Probability) for i in Probability]

    print("-------------------------------------------------------------------")
    # To choose rewards form the rewards file and update the weight and probability of that arm using STAT, ROLL OR REC algo
    #depending on the input
    for i in range(len(input_rewards)):
        # Choose arms randomly based on the probabilities
        choice = random.choices(Arms, weights=Probability, k=1)
        Arms_count[choice[0]] += 1
        print("Current step:",i+1)
        print("Decision made i.e. Arm selected is:", choice[0] + 1)
        print("arms count",Arms_count)
        # Get the reward for that particular arm
        current_reward = int(input_rewards[i][choice[0]])
        print("current reward", current_reward)

        if alg == 'STAT':
            # update the weight for that particular arm
            Initial_wt[choice[0]] = (decay * Initial_wt[choice[0]]) + (rwt * current_reward)

        elif alg == 'ROLL':
            # update the weight for that particular arm
            Initial_wt[choice[0]] = Initial_wt[choice[0]] + (1 / Arms_count[choice[0]]) * (current_reward - Initial_wt[choice[0]])

        elif alg == 'REC':
            #index has number of times an arm is pulled
            index = Arms_count[choice[0]]

            #Take temporary variable for updation of weights in order to avoid drawbacks of list of lists
            temp_initial_weight = list(Initial_wt)

            #For the first 10 pull consider the rewards that are available before current iteration and update the weights accordingly
            if index < 11:
                temp_initial_weight[choice[0]] = ((1 - decay) ** (index - 1)) * Weight_window[choice[0]][0]
                for r in range((index - 10), index):
                    if (r-1) <= 0:
                        temp_initial_weight[choice[0]] += 0
                    else:
                        temp_initial_weight[choice[0]] += decay * (1 - decay) ** (index - 1 - r) * reward_window[choice[0]][r - 1]

                Weight_window[choice[0]].append(temp_initial_weight[choice[0]])

                reward_window[choice[0]].append(current_reward)

                Initial_wt = temp_initial_weight

            else:
                #If the arm count is greater than 10 then consider previous 10 rewards and update the weights accordingly
                temp_initial_weight[choice[0]] = ((1 - decay) ** (index - 1)) * Weight_window[choice[0]][0]

                for r in range(len(reward_window[choice[0]])):
                    temp_initial_weight[choice[0]] += decay*(1 - decay) ** (9-r) * reward_window[choice[0]][r]

                Weight_window[choice[0]].append(temp_initial_weight[choice[0]])
                Weight_window[choice[0]].pop(0)

                Initial_wt = temp_initial_weight

                reward_window[choice[0]].append(current_reward)
                reward_window[choice[0]].pop(0)

        #Normalize weights for each arm and check if the elements in the list are equal if yes take the same weights
        equal_weights = all(ele == Initial_wt[0] for ele in Initial_wt)
        if equal_weights:
            norm_wt = [float(i) / 1 for i in Initial_wt]
        else:
            norm_wt = [(float(i) - min(Initial_wt)) / (max(Initial_wt) - min(Initial_wt)) for i in Initial_wt]

        # Update the probability for that particular arm and normalize
        Probability[choice[0]] = (norm_wt[choice[0]]) * (1 - exp) + (exp * dist)
        #Check if probability is negative and handle
        if Probability[choice[0]] < 0:
            Probability[choice[0]] += abs(Probability[choice[0]])

        Probability = [float(i) / sum(Probability) for i in Probability]

        # Calculate cumulative reward
        cumulative_reward += current_reward;
        print("cumulative_reward", cumulative_reward)

        print("-----------------------------------------------------------------------")
    print("cumulative_reward", cumulative_reward)

#bandit function call
bandit_basic(input_rewards, alg, exp, dist, decay, rwt, w0)
