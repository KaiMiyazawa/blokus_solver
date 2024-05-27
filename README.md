# blokus_solver
This is log of SMART SCAPE CUP Hackathon Battle.  
The Hackathon was about [Blokus Duo](https://ja.wikipedia.org/wiki/%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF%E3%82%B9).  

We were a team and were required to develop an agent to solve Blokus　well.

---
## Hackathon Schedule  
The schedule for the hackathon was as follows.　　
### 1st day (2024/5/24)  
18:00~20:00 Breakout Time

### 2nd day (2024/5/25)  
10:00~20:00 Develop

### 3rd day (2024/5/26)  
10:00~15:00 Tournament Battle  

---

## Our team's Strategy  
We thought that under the Blockus game rules, a strategy that reduces the number of places where the opponent can place the next block would be strong because it would lead to blocking the opponent's action.  

Thus, we began to develop in the derection of "sticy strategy".  

The specific process is as follows.  
1. List up the moves that are not foul. -> strage as "ok_cases" list.
2. Leave good moves from the "sticy strategy" in "ok_cases"
3. Leave bigger block's moves in "ok_cases"
4. and so on ...  
---
## Result
We finished second. yeah!💪　　

---
## Usage
First, make enviroment
```bash
python3 -m venv ssvenv
source ssvenv/bin/activate
```
Second, update packages in this project.
```bash
pip install -U ./game
pip install -U ./client
```
Finally, enjoy Blokus!
```bash
start_blocksduo sticy sticy
#this command's format ↓
# start_blocksduo {AI1's name} {A2's name}
# this means a battle simulation between AI1 and AI2.
```
