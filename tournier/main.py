import sys
from tqdm import tqdm
import redis
import os
import chess
import chess.engine
from itertools  import permutations
from uuid import uuid4
import json


CHESS_ENGINES_PATH = '../chess_engines/'
with open('./usefull_engines.json') as f:
    ALL_ENGINES_LIST = json.load(f)['engines']
TIME = 1
DEPTH = None
NODES = None
LIMIT = chess.engine.Limit(time=TIME, depth=DEPTH, nodes=NODES)
QUEUE = redis.Redis(host='localhost', port=8000, db=0)
ITERATIONS = 10
MAX_STEPS = 100
print(ALL_ENGINES_LIST)

def engine_tournament(engine1_path: str, engine2_path: str):
    board = chess.Board()
    print('start creating engins')
    engine1 = chess.engine.SimpleEngine.popen_uci(CHESS_ENGINES_PATH + engine1_path)
    engine2 = chess.engine.SimpleEngine.popen_uci(CHESS_ENGINES_PATH + engine2_path)
    print('end creating engins')
    d1 = {
        'move': [],
        'score': []
    }
    d2 = {
        'move': [],
        'score': []
    }
    for _ in range(MAX_STEPS):
        # with engine1.analysis(board, limit=LIMIT) as analysis:
        #     d1['score'].append([info.get("score") for info in analysis])
        result = engine1.play(board, LIMIT)
        print(result)
        if result.move == None:
            break
        board.push(result.move)
        d1['move'].append(result)
        # with engine2.analysis(board, limit=LIMIT) as analysis:
        #     d2['score'].append([info.get("score") for info in analysis])
        result = engine2.play(board, LIMIT)
        print(result)
        if result.move == None:
            break
        board.push(result.move)
        d2['move'].append(result)
    engine1.quit()
    engine2.quit()
    return d1, d2



def main():
    engines = sys.argv[1:]
    d =list(permutations(ALL_ENGINES_LIST, 2))
    for i in range(ITERATIONS):
        for e1, e2 in tqdm(
            d,  
            desc=f'iteration: {i}/{ITERATIONS}'
        ):
            print(e1, e2)
            d1, d2 = engine_tournament(e1, e2)
            QUEUE.set(
                str(uuid4()), {
                    'engine_1': e1,
                    'engine_2': e2,
                }
            )
    with open('./data.json', 'w') as f:
        json.dump({key: QUEUE.set(key) for key in QUEUE.scan_iter("user:*")}, f)
            
            
if __name__ == '__main__':
    main()

