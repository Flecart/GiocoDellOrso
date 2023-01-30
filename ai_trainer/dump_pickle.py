import argparse
import pickle


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='input file', type=str, required=True)
parser.add_argument(
    '-d', '--dump',
    action='store_true',
    help='dump the state', 
    default=False
)
parser.add_argument(
    '--reverse',
    type=bool,
    help='reverse the input file',
    default=False
)
parser.add_argument('--state', help='display valueof the state', default='')

args = parser.parse_args()
input = args.input
state = args.state
with open(input, 'rb') as f:
    data: dict[str, float] = pickle.load(f)
    print(data)
    states = data['states_value'].copy()
    data['states_value'] = None
    for key, value in states.items():
        print(key, value)

    print(data, args)
    if args.dump:
        states = {
            k: v for k, v in sorted(
                states.items(), key=lambda item: item[1],
                reverse=args.reverse
            )
        }
    elif args.state != '':
        print("the value of the state is:")
        print(f"{state}: {data[state]}")
