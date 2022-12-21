import hashlib
import json
import random
import sys
import time

simulation_is_done = False
maximum_int = sys.maxsize


def produce_hash(entity):
    h = hashlib.sha256()
    encoded = json.dumps(entity, sort_keys=True).encode('UTF-8')
    h.update(encoded)
    return h.hexdigest()


def puzzle_solution_is_correct(solution, difficulty):
    integer_solution = int(solution, 16)
    diff = 2 ** (256 - difficulty)
    correct = integer_solution <= diff
    return correct
    # return solution[0:difficulty] == '0' * difficulty


def mine_block(block_body, difficulty):
    block_hash = produce_hash(block_body)
    while not puzzle_solution_is_correct(block_hash, difficulty):
        block_body['Nonce'] += 1
        block_hash = produce_hash(block_body)
    return block_hash, block_body


def update_nonce_collatz(nonce_a, tried_one_already):
    if nonce_a % 2 == 0:
        to_be_returned = nonce_a / 2
    else:
        to_be_returned = (3 * nonce_a) + 1
    if to_be_returned == 1 and tried_one_already:
        to_be_returned = random.randint(5, maximum_int)
    return to_be_returned


def mine_dishonestly(forged_block, nonce_a, difficulty, time_to_attack):
    quit_attack_time = time.time() + time_to_attack
    hash_of_forged_block = produce_hash(forged_block['Body'])
    success = True
    tried_one_already = False
    while not puzzle_solution_is_correct(hash_of_forged_block, difficulty):
        nonce_a = update_nonce_collatz(nonce_a, tried_one_already)
        if nonce_a == 1:
            tried_one_already = True
        forged_block['Body']['Nonce'] = nonce_a
        hash_of_forged_block = produce_hash(forged_block['Body'])
        if quit_attack_time < time.time():
            success = False
            return {}, success
    forged_block['Header']['Miner_id'] = 'Attacker'
    forged_block['Header']['Hash'] = hash_of_forged_block
    return forged_block, success


def get_new_block(previous_hash=None, block_number=0):
    body = {'Sample_Transaction': random.randint(0, 1000000000),
            'Previous_hash': previous_hash,
            'Nonce': 0}
    block = {'Header': {'Type': 'New_block',
                        'Miner_id': 'Honest',
                        'Block_number': block_number,
                        'Generation_time': time.time(),
                        'Hash': produce_hash(body)},
             'Body': body}
    return block


def get_forged_block(block_number, previous_hash):
    body = {'forged_Transaction': random.randint(0, 1000000000),
            'Previous_hash': previous_hash,
            'Nonce': 0}
    block = {'Header': {'Type': 'New_block',
                        'Miner_id': 'Attacker',
                        'Block_number': block_number,
                        'Generation_time': None,
                        'Hash': None},
             'Body': body}
    return block
