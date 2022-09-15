import random
from get_all_routes import get_best_nodes, get_route
#from get_all_routes import get_best_nodes, get_best_net, get_all_best_routes, get_cost, count_routes, get_route
import numpy as np

def update_Q(T,Q,current_state, next_state, alpha):
    current_t = T[current_state][next_state]
    current_q = Q[current_state][next_state]
    
    #updating SARSA
    # best_next_action_val = min(Q[next_state].values())
    # for action in Q[next_state].keys():
    #     if Q[next_state][action] ==  best_next_action_val:
    #         best_next_action = action
    # # print(best_next_action)
    # new_q = current_q + alpha * (current_t + gamma * Q[next_state][best_next_action] - current_q) #for each state, it will choose the minimun furture cost instead of maximum future reward SARSA

    #updating Q-learning
    new_q = current_q + alpha * (current_t + min(Q[next_state].values()) - current_q) #for each state,
                                #it will choose the minimun furture cost instead of maximum future reward.
    Q[current_state][next_state] = new_q
    return Q

def get_key_of_min_value(dic):
        min_val = min(dic.values())
        return [k for k, v in dic.items() if v == min_val]

def Q_routing(T,Q,alpha,epsilon,n_episodes,start,end): #Fill Q table and explore all options
    #--------------e-greedy decay---------------------------------
    # min_epsilon = 0.01
    # max_epsilon = 0.9
    # decay_rate = 0.001
    episode_hops = {}
    
    routes_complete = []
    for i in range(n_episodes):
        routes_complete.append([])

    #T is network info
    for e in range(1,n_episodes+1):     #per ogni episodio
        # print("Episode {0}:".format(e))
        current_state = start
        goal = False
        stored_states = []
	
        #print("Prima dell'update, episodio ", e, "\n",Q)
        while not goal:
            #takes the next hops neighbours for state
            valid_moves = list(Q[current_state].keys())
            
            if len(valid_moves) <= 1:  #se c'è solo un neighbour il prossimo stato è per forza quello
                next_state = valid_moves[0]
            else:
                #scegli la best action tra quelle che in questo stato minimizzano il Q value
                best_action = random.choice(get_key_of_min_value(Q[current_state]))
                if random.random() < epsilon:
                    next_state = best_action
                else:
                    valid_moves.pop(valid_moves.index(best_action))  #togli da valid moves quella che ha come indice la best 
                    					#action scelta a caso prima tra quelle col minor Q value
                    next_state = random.choice(valid_moves)  #scegli a caso tra quelle rimanenti tra le mosse valide
            Q = update_Q(T,Q,current_state, next_state, alpha)  #update Q Table
            current_state = next_state
            # print(next_state)
            stored_states.append(next_state)

            if next_state in end:
                goal = True
        
        
        ##QUI DEVO STAMPARE LA REWARD DI FINE EPISODIO PER UNA COPPIA SRC/DST
        
        #print("Dopo l'update, episodio ",e,"\n", Q)
        nodes = get_best_nodes(Q,start,end) #get best nodes to reach dest
        route = get_route(Q, start, end)
        
        routes_complete[e-1] = route
        
        #print("\nepisodio: ", e, " ", route) 
        
     
    	
        
        
        #     print('Q-table:', Q)
        #     print('Switches', stored_states)
        #     episode_hops[e] = stored_states
        # print('resume',episode_hops)
        # name = '~/ryu/ryu/SDNapps_proac/RoutingGeant/stretch/Graphs_parameters/alpha_'+str(alpha)+'/'+str(it)+'_alpha_'+str(alpha)+'_epsilon_'+str(epsilon)+'_'

        # with open(str(name)+'hops_episodes.json', 'w') as json_file:
        #     json.dump(episode_hops, json_file, indent=1)
        
        #--------------e-greedy decay---------------------------------
        # e += 1
        # epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*e)
        # print epsilon
    return Q, epsilon, routes_complete
