
# project-jillian-kenny-vahan
project-jillian-kenny-vahan created by GitHub Classroom
**Due: Wednesday 5pm**
- Description: minimum functionality + extensions
- Schedule: timeline with milestones for each week
- Interface: drawings of each screen
- Classes: design of all classes and objects
- Libraries you will use


### Description
Basic platformer game. 

### Modules used
- PyGame
- sys
- os
- csv
- random

### Controls
- In game movement: WASD, Space
- Menus: arrow keys, return key

### Extensions
- Shop system, the ability to purchase more lives in exchange for coins
- Multiple characters
- Multiple levels

### First Milestone
As of Tuesday, 11/29 we have a working character movement, level loading, and a start menu.
The game includes various animations using sprite images. The level loading is done by reading a csv file containing the data for the current level which is generated using program called "Tiled". 
The game contains a lot of essential classes which are used to make the development easier and more clear. 
#### Classes
- Game - main class which is responsible for running the game
- Level - this class is used to generate the level on a screen
- Player - player class
- Tile - this is a parent class for other classes like StaticTile and AnimatedTile which are used to draw tiles on level
- Sky, Clouds, Lava - basic classes for level decoration
- Interface - class for drawing user interface on screen
- StartMenu - class for drawing the start menu

## User's Manual
To run the code you have to first clone the repository to your local computer and navigate to the code folder. After navigating to the folder you should run the main.py file using the command: python3 main.py.


## Screenshots

![Screenshot 1](https://raw.githubusercontent.com/LMU-CMSI-1010/project-jillian-kenny-vahan/main/screenshots/1.png?token=GHSAT0AAAAAABZL74J2YFC3DZULCLURDZY4Y4XSSTA)
![Screenshot 2](https://raw.githubusercontent.com/LMU-CMSI-1010/project-jillian-kenny-vahan/main/screenshots/2.png?token=GHSAT0AAAAAABZL74J2ILQFWET6VVYEZ3WKY4XSSZA)
