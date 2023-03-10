#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <cstring>
#include <algorithm>
#include <queue>
#include <unordered_set>
#include <unordered_map>
using namespace std;

const int SIZE = 16;
struct pos_t {
	int x, y;
	char type;
    bool operator == (const pos_t& ref) const {
        return ref.x == x && ref.y == y && ref.type == type;
    }
};
vector<pos_t> walls;
pos_t target;
int target_robot_id;
string ROBOT_NAMES = "rbgy";
string DIR_NAMES = "lrdu";
int lefts[SIZE][SIZE], rights[SIZE][SIZE];
int ups[SIZE][SIZE], downs[SIZE][SIZE];
int DIRX[] = {-1, 1, 0, 0};
int DIRY[] = {0, 0, -1, 1};
struct state_t {
	pos_t robots[4];
	inline unsigned compress() {
		unsigned result = 0u;
		for (int i = 0; i < 4; ++i) {
			result <<= 8;
			result |= robots[i].x << 4 | robots[i].y;
		}
		return result;
	}
	state_t() { }
	state_t(unsigned result) {
		for (int i = 4 - 1; i >= 0; --i) {
			robots[i].x = (result >> 4) & 0xf;
			robots[i].y = result & 0xf;
			robots[i].type = ROBOT_NAMES[i];
			result >>= 8;
		}
	}
	void print() {
		for (int i = 0; i < 4; ++i) {
			cout << robots[i].type << robots[i].x << "," << robots[i].y << " ";
		}
		cout << endl;
	}
}init_state;
unordered_map<unsigned, unsigned> previous_steps;
unordered_map<unsigned, int> ops;
queue<unsigned> state_queue[2];
int main() {
	freopen("solver.in", "r", stdin);
	// freopen("solver.out", "w", stdout);
	for (int i = 0; i <= 1; ++i) {
		for (int j = 0; j <= 1; ++j) {
			walls.push_back({SIZE / 2 - j - j, SIZE / 2 - i, 'v'});
			walls.push_back({SIZE / 2 - i, SIZE / 2 - j - j, 'h'});
		}
	}
	for (int i = 0; i < SIZE; ++i) {
		walls.push_back({-1, i, 'v'});
		walls.push_back({SIZE - 1, i, 'v'});
		walls.push_back({i, -1, 'h'});
		walls.push_back({i, SIZE - 1, 'h'});
	}
	while (true) {
		string s2;
		int x, y;
		cin >> s2 >> x >> y;
		pos_t pos = {x, y, (char)tolower(s2[0])};
		if (cin.eof())
			break;
		if (s2 == "v" or s2 == "h") {
			walls.push_back(pos);
		} else if (ROBOT_NAMES.find(s2[0]) != string::npos) {
			init_state.robots[ROBOT_NAMES.find(s2[0])] = pos;
		} else {
			target = pos;
			target_robot_id = ROBOT_NAMES.find(pos.type);
			cout << "target" << ":" << pos.x << "," << pos.y << "@" << pos.type << endl;
		}
	}
	for (int x = 0; x < SIZE; ++x) {
		for (int y = 0; y < SIZE; ++y) {
			for (int k = 0; ; ++k) {
				if (find(walls.begin(), walls.end(), (pos_t){x - k - 1, y, 'v'}) != walls.end()) {
					lefts[x][y] = x - k;
					break;
				}
			}
			for (int k = 0; ; ++k) {
				if (find(walls.begin(), walls.end(), (pos_t){x + k, y, 'v'}) != walls.end()) {
					rights[x][y] = x + k;
					break;
				}
			}
			for (int k = 0; ; ++k) {
				if (find(walls.begin(), walls.end(), (pos_t){x, y - k - 1, 'h'}) != walls.end()) {
					ups[x][y] = y - k;
					break;
				}
			}
			for (int k = 0; ; ++k) {
				if (find(walls.begin(), walls.end(), (pos_t){x, y + k, 'h'}) != walls.end()) {
					downs[x][y] = y + k;
					break;
				}
			}
		}
	}
	unsigned init_z = init_state.compress();
	state_queue[0].push(init_z);
	previous_steps[init_z] = init_z;
	int dist = 0;
	while (!state_queue[0].empty() || !state_queue[1].empty()) {
		for (int i = 0; i <= 1; ++i) {
			while (!state_queue[i].empty()) {
				unsigned z = state_queue[i].front();
				state_queue[i].pop();
				state_t state(z);
				for (int j = 0; j < 4; ++j) {
					for (int dir = 0; dir < 4; ++dir) {
						state_t state2 = state;
						if (dir == 0)
							state2.robots[j].x = lefts[state2.robots[j].x][state2.robots[j].y];
						else if (dir == 1)
							state2.robots[j].x = rights[state2.robots[j].x][state2.robots[j].y];
						else if (dir == 2)
							state2.robots[j].y = ups[state2.robots[j].x][state2.robots[j].y];
						else if (dir == 3)
							state2.robots[j].y = downs[state2.robots[j].x][state2.robots[j].y];
						for (int k = 0; k < 4; ++k) {
							if (k == j) continue;
							if (dir == 0) {
								if (state.robots[k].y == state.robots[j].y && state.robots[k].x < state.robots[j].x && state.robots[k].x >= state2.robots[j].x)
									state2.robots[j].x = state.robots[k].x + 1;
							} else if (dir == 1) {
								if (state.robots[k].y == state.robots[j].y && state.robots[k].x > state.robots[j].x && state.robots[k].x <= state2.robots[j].x)
									state2.robots[j].x = state.robots[k].x - 1;
							} else if (dir == 2) {
								if (state.robots[k].x == state.robots[j].x && state.robots[k].y < state.robots[j].y && state.robots[k].y >= state2.robots[j].y)
									state2.robots[j].y = state.robots[k].y + 1;
							} else if (dir == 3) {
								if (state.robots[k].x == state.robots[j].x && state.robots[k].y > state.robots[j].y && state.robots[k].y <= state2.robots[j].y)
									state2.robots[j].y = state.robots[k].y - 1;
							}
						}
						unsigned state2_z = state2.compress();
						if (previous_steps.find(state2_z) == previous_steps.end()) {
							state_queue[i ^ 1].push(state2_z);
							previous_steps[state2_z] = z;
							ops[state2_z] = j * 4 + dir;
							bool win = false;
							if (target_robot_id == string::npos) {
								for (int k = 0; k < 4; ++k) {
									if (state2.robots[k].x == target.x && state2.robots[k].y == target.y) {
										win = true; break;
									}
								}
							} else {
								win = state2.robots[target_robot_id].x == target.x && state2.robots[target_robot_id].y == target.y;	
							}
							if (win) {
								cout << "Found solution " << state2_z << " in " << dist + 1 << " steps!" << endl;
								vector<string> buffer;
								while (state2_z != init_z) {
									int op = ops[state2_z];
									string s1(1, ROBOT_NAMES[op / 4]);
									string s2(1, DIR_NAMES[op % 4]);
									buffer.push_back(s1 + s2);
									state2_z = previous_steps[state2_z];
								}
								reverse(buffer.begin(), buffer.end());
								for (string s: buffer)
									cout << s << " ";
								return 0;
							}
						}
					}
				}
			}
			dist++;
            if (dist >= 15) { break; }
			cout << "Searching dist " << dist << endl;
		}
	}
	cout << "Found no solution!" << endl;
}
