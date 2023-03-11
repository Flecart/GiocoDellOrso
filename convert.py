
end_states = ['1000_________________',
                '0_10__0______________',
                '__0___1_____00_______',
                '______0_____01__0____',
                '____________00__1__0_',
                '________________00_10',
                '_________________0001',
                '______________0__01_0',
                '_______00_____1___0__',
                '____0__10_____0______',
                '_0__1__00____________',
                '01_00________________',
                '000_________________1',]

def convert(state: str) -> int:
    def get_value(char: str):
        if char == '_':
            return 0
        elif char == '0':
            return 1
        elif char == '1':
            return 2
        else:
            raise ValueError("Invalid character")

    val = 0
    for i, ch in enumerate(state):
        val += get_value(ch) * 3 ** i

    return val

s = []

for state in end_states:
    s.append(convert(state))

print(s)