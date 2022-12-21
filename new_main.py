#
#         honest miner                                    Attacker
#
# step1: mine genesis block                      construct forged TX2 template
# step2: honest miner mine first block           compute avg nonce, forge TX1 in first block,
#                                                       re-mine forged first block dishonestly
# step3: honest start mining second block        mine forged second block(TX2) as long as
#                                                       second block is still not delivered
# step4: broadcast second block if not new       broadcast forged second block if not new
#         BC version delivered                          BC version delivered
import copy
import math
import os
import random
import time
from pandas import DataFrame

import Utilized_functions

blockchain = {}
difficulty = int(input('Input Puzzle Difficulty (0--256)>>  '))
# portion_controlled_by_attacker = int(input('Input percentage computational power the attacker controls (<= 50)>>  '))
Total_attack_attempts = 0
Total_successful_attack_attempts = 0


def honest_mining():
    start_time = time.time()
    new_block = Utilized_functions.get_new_block(blockchain[str(len(blockchain) - 1)]['Header']['Hash'],
                                                 len(blockchain))
    block_hash, block_body = Utilized_functions.mine_block(new_block['Body'], difficulty)
    new_block['Body'] = block_body
    new_block['Header']['Hash'] = block_hash
    add_block_to_ledger(new_block)  # step4: broadcast new block
    elapsed_time = time.time() - start_time
    # print('Honest nodes proposed last block in ' + str(elapsed_time) + ' seconds')
    return elapsed_time


def attack_ledger(time_to_attack):
    if len(blockchain) < 3:
        pass
    else:
        global Total_attack_attempts
        global Total_successful_attack_attempts
        Total_attack_attempts += 1
        time_to_attack = time_to_attack * 2 * portion_controlled_by_attacker / 100
        avg_num_of_attempts = int(get_avg_nonce())
        nonce_a = random.randint(0, avg_num_of_attempts)
        second_forged_block = Utilized_functions.get_forged_block(len(blockchain) - 1,
                                                                  blockchain[str(len(blockchain) - 2)])  # construct forged TX2 template
        start_time = time.time()
        first_forged_block = copy.deepcopy(blockchain[str(len(blockchain) - 2)])
        # print('Attacker is now forging Block number: ' + str(len(blockchain) - 2))
        first_forged_block['Body']['Sample_Transaction']: random.randint(0, 1000000000)  # forge TX1 in first block
        first_forged_block, success_result = Utilized_functions.mine_dishonestly(first_forged_block, nonce_a, difficulty, time_to_attack)  # re-mine forged first block dishonestly

        if success_result:
            # # print('first block forged successfully!')
            # nonce_a = first_forged_block['Body']['Nonce']
            second_forged_block, success_result = Utilized_functions.mine_dishonestly(second_forged_block, nonce_a, difficulty, time_to_attack)  # mine forged second block(TX2)
            elapsed_time = time.time() - start_time
            if success_result and elapsed_time < time_to_attack:
                # print('second block forged successfully!')

                Total_successful_attack_attempts += 1
                # print('Attacker spent ' + str(elapsed_time) + ' seconds trying to forge previous block')

            # else:
            #     print('Attack was unsuccessful within time window')
        # clear_screen()
        # print("Attacker controls: " + str(portion_controlled_by_attacker) + " % of the network")
        # print("Puzzle difficulty is " + str(difficulty) + "/256")
        # print('Length of the longest chain = ' + str(len(blockchain)))
        # print('nonce_a = ' + str(nonce_a))
        # print("Attack attempts = " + str(Total_attack_attempts))
        # print("Attacker was successful in " + str(Total_successful_attack_attempts) + ' time(s)')
        # print("Success attack rate = " + str(Total_successful_attack_attempts / Total_attack_attempts))
        return success_result


def add_block_to_ledger(new_block):
    blockchain[str(new_block['Header']['Block_number'])] = new_block


def get_avg_nonce():
    total_attempts = 0
    number_of_considered_blocks = 0
    for key in blockchain:
        total_attempts += blockchain[key]['Body']['Nonce']
        number_of_considered_blocks += 1
    return math.ceil(total_attempts / number_of_considered_blocks)


def clear_screen():
    os.system('clear')


add_block_to_ledger(Utilized_functions.get_new_block())  # mine genesis block
list_of_experiment_results = []
for dif in range(difficulty):
    list_of_experiment_results.append([])
    refined_attack_results = []
    for portion_controlled_by_attacker in range(45):
        clear_screen()
        print("Attacker controls: " + str(portion_controlled_by_attacker) + " % of the network")
        print("Puzzle difficulty is " + str(dif) + "/256")
        # print('Length of the longest chain = ' + str(len(blockchain)))
        # print("Attack attempts = " + str(Total_attack_attempts))
        # print("Attacker was successful in " + str(Total_successful_attack_attempts) + ' time(s)')

        list_of_experiment_results[dif].append([])
        for number_of_simulated_blocks in range(100):
            window_to_attack = honest_mining()
            success_result = attack_ledger(window_to_attack)
            if success_result:
                list_of_experiment_results[dif][portion_controlled_by_attacker].append(1)
            else:
                list_of_experiment_results[dif][portion_controlled_by_attacker].append(0)
        try:
            print("Success attack rate for above parameters = " + str(sum(list_of_experiment_results[dif][portion_controlled_by_attacker]) / len(list_of_experiment_results[dif][portion_controlled_by_attacker])))
        except Exception as e:
            pass
    portion_measures = []
    for portion_measure in range(len(list_of_experiment_results[dif])):
        target_list = list_of_experiment_results[dif][portion_measure]
        refined_attack_results.append(sum(target_list)/len(target_list))
        portion_measures.append(portion_measure)
    name_of_file = 'Dif' + str(dif) + '.xlsx'
    df = DataFrame({'Attacker_Portion': portion_measures,
                    'Attacker_Success_Rate': refined_attack_results})
    df.to_excel(name_of_file, sheet_name='sheet1', index=False)


