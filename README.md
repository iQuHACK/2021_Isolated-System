# GateState Memory: Train your memory and circuit intuition!

Frederik Hardervig

## Introduction

The barrier of entry into quantum computing can be intimidating, and thus gamifying tools to help train the fundamentals might be a good way engage newer audiences that might know nothing about linear algebra, such as those in high school, early university, or those who simply haven't pursued such topics.

To achieve this, I have built a memory game where players have to match a circuit to its corresponding state, represented through a qSphere. The circuits are randomly generated using IBM's qasm simulator. 

## Elements and rules

When "Play" is pressed, 6 circuit-qsphere pairs are generated and randomly placed unto cards. The play can at most flip two of them at a time, and must identify the pairs by thinking about the state each circuit will generate and where these are located. Once all pairs have been identified, the game ends.

There isn't much strategy apart from remembering where each circuit is located and if you're a cheat, writing them down. However, no cheating will help you determine which state is generated from a given circuit. You'll have to figure that out yourself.

## Generating gates for the game circuits
To generate my circuits, I created the circuit below, which can be measure with n shots to generate n strings that encode a gate each.
![circuit generatot](https://github.com/iQuHACK/2021_Ducktectives/blob/main/Pictures/Generator%20circuit.JPG)

This might seem a bit messy, but I've included a short description below. The two sub-routines that require the most explanation is the ones for q4 and q5, and for q8 and q9. For q4 and q5, since the game uses 3 qubits, we wish to generate |00>, |01>, and |10>, with equal probability, ie.![img](https://i.imgur.com/vzZ6lGY.gif), but NOT 11. We essentially need to create a state where the qubits cannot be 1 at the same time. Thus we firstly observe that each should be 0 two out of three times. Thus we first rotate q4 around the y-axis by ![img](https://i.imgur.com/bhy8bgJ.gif) which we've obtained after a bit of algebra. Then we do an X-flip to instead be 1 two thirds of the time when controlled to apply a hadamard to q5. Finally we revert back. Thus, when q4=0, the controlled gate has been triggered, and q5 is either 0 or 1, leading to |10> or |00> one third of the time respectively, while if q4=1 (which happens one third of the time), the hadarmard was not triggered and we obtain |01>. I don't quite have time to explain q8 and q9.

![explanation](https://github.com/iQuHACK/2021_Ducktectives/blob/main/Pictures/Explanation.png)

## Repository:

The GitHub repository link is [https://github.com/iQuHACK/2021_Ducktectives](https://github.com/iQuHACK/2021_Ducktectives).
Note that running the jupyter notebook on remote machines will not work since PyGame only recognizes local displays.

## Final notes:
### Future improvements
* Buttons to control difficulty (e.g. amount of cards, extended gate-set)
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

