
_Organizer's note:_ this project won the **creativity award** in iQuHACK 2020.

---

# GateState Memory: Train your memory and circuit intuition!

Frederik Hardervig

## Introduction

The barrier of entry into quantum computing can be intimidating, and thus gamifying tools to help train the fundamentals might be a good way engage newer audiences that might know nothing about linear algebra, such as those in high school, early university, or those who simply haven't pursued such topics.

To achieve this, I have built a memory game where players have to match a circuit to its corresponding state, represented through a qSphere. The circuits are randomly generated using IonQ's simulator or QPU backend.

## Elements and rules

When "Play" is pressed, 6 circuit-qsphere pairs are generated and randomly placed unto cards. The play can at most flip two of them at a time, and must identify the pairs by thinking about the state each circuit will generate and where these are located. Once all pairs have been identified, the game ends.

There isn't much strategy apart from remembering where each circuit is located and if you're a cheat, writing them down. However, no cheating will help you determine which state is generated from a given circuit. You'll have to figure that out yourself.


## Repository:

The GitHub repository link is [https://github.com/iQuHACK/2021_Ducktectives](https://github.com/iQuHACK/2021_Ducktectives).
Note that running the jupyter notebook on remote machines will not work since PyGame only recognizes local displays.

## Final notes:
### Future improvements
* Buttons to control difficulty
* Better scaling of picture on cards
* Crop qsphere to be larger on cards
* Show the matching pair for 2 seconds before removing
* Add gamemodes: Speed-run, Fewest moves, Limited guesses
* Scoreboard
* More polished main menu
* Option to just classically generate the circuits to improve loading time

## Notable Features:
*   The cirquits themselves are randomly generated using a quantum circuit, that is adaptable through some parameters.
*   There will never be generated two circuits that result in the same statevector.
*   The difficulty of the game rapidly scales and can provide a challenge even for hardened veterans.

