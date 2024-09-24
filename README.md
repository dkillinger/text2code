# Text2Game
## Introduction
A basic python program utilizing regex that transforms screenplays into Ren'Py game code to promote a better development workflow.

When developing any Ren'Py game, independent developers are often tasked with juggling their game's narrative alongside their code, sound, and music. While some independent developers eventually find their preferred workflow, many solo devs give up due to the sheer amount of things they must manage. To help these struggling devs, I decided to create *Text2Game* which gives developer the flexibility of transforming their stories into Ren'Py code. This not only formats all narration/dialogue into the expected syntax, it also: automatically handels Character Object creation, creates scene/show statements when necessary, generates verbose character sprite names, generates practical image names, grants the user the ability to control how the resulting code is generated using *Generation Statements*, and reports on the choices the program made.

## Important Notes
### Why Screenplays?
Some might be confused as to why screenplays are the only style of writing that Text2Code can understand. There a two reasons:
* It was the first style of writing I encountered.
* It is the second best thing to writing code; very objective style of writing.
The style of writing used to create screenplays is very objective compared to more descriptive styles of writing seen in novels or poetry. Furthermore, it is not as tedious as writing Ren'Py code (in my experience).

## Screenplay format
In respect to text2code, there are six main screenplay concentions you must adhere to in order for text2code to make the most of your script. These must be given in the following order:
* Transitions (on a line prepended before a scene header)
* Scene Headers
* Character Names (on a line prepended before dialogue)
* Other text
* Blank Lines (to primarily signal when a character is done talking)

## Render Style Statements
Surrounded by '<>,' these statements determine how images and dialogue is rendered on screen.

