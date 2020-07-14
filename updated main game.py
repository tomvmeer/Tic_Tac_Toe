import QLearning
import operator

computer1 = QLearning.Agent("AI", exp_rate=0)
computer1.loadPolicy("policy_Player1")
rules1 = computer1.state_values
computer2 = QLearning.Agent("AI2", exp_rate=0)
computer2.loadPolicy("policy_Player2")
rules2 = computer2.state_values
print(max(rules1.items(), key=operator.itemgetter(1)))
print(max(rules2.items(), key=operator.itemgetter(1)))
