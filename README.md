# L4S Final Project

*by Lily Mayo, Mia Santomauro, and Zahid Hasan*

## Our Goal

Our goal was to model the passing and placement of props during a play. The purpose of our model is to guide directors in their blocking decisions. Such decisions include: which actors should carry which props, and where the actors should exit/enter from.

## Model Structure

We used Forge Traces to model our plays. Each play is represented by a Trace. 
The States in the Trace are the __Scene__ sigs. The transitions in the Trace are the __Event__ sigs which are constrained by the __sceneChange__ transition. Below are descriptions of our Sigs, Preds, States, and Transitions.

### Sigs
+ _Scene_: This sig is used to represent the state in our traces. Below are the fields of Scene:
  - actors (set Actor): The set of Actor sigs which should be on stage during this Scene
  - props (set Prop): The set of Prop sigs which should be on stage during this Scene
  - actorPos (set Actor -> Position): The positions of all of the Actor sigs (whether on or off stage) during this Scene
  - propPos (set Prop -> Position): The positions of all of the Prop sigs (whether on or off stage) during this Scene
  
+ _Actor_: This sig is used to represent the actors in the play

+ _Prop_: This sig is used to represent the props in the play

+ _Position_: This sig is used to represent the positions that actors and props can be in

+ _Left_: This sig extends Position, and represents __off stage left__

+ _Right_: This sig extends Position, and represents __off stage right__

+ _Center_: This sig extends Position, and represents __onstage__

+ _Event_: This sig is used as the parameter to the transitions in the trace. 
It represents a 'Scene Change' or 'Blackout' in theatre terms. Below are the fields of Event:
  - carryOnAssignments (set Actor -> Prop): This relation represents which actors should carry which props __on stage__ in order to transition from the 'pre scene' to the 'post scene'
  - carryOffAssignments (set Actor -> Prop): This relation represents which actors should carry which props __off stage__ in order to transition from the 'pre scene' to the 'post scene'
  - pre (one Scene): The scene before this Event
  - post (one Scene): The Scene after this Event

### Preds
+ _onStageExactlyCenter_: a predicate to ensure that the position of any Prop or Actor during the Scene(s) they're onstage for is Center.
+ _allAccountedFor_: a predicate to ensure that all Props and Actors have a Position during all Scenes.
+ _positions_: ensures that _onStageExactlyCenter_ and _allAccountedFor_
+ _abstractPosition_: ensures that there are exactly three Positions: Left, Right, and Center.
+ _functionalAssignments_: ensures that carryOnAsignments and carryOffAsignments are functional (every actor who has a prop, has only one prop) and injective (every prop has only one actor)

### State
+ _initState_: constrains the first Scene in the trace to have no Actors onstage and no Props onstage
+ _finalState_: constrains the last Scene in the trace to have no Actors onstage and no Props onstage

## Model w/ Weights

After creating the first version of our model, we decided to expand upon it. We decided to add weights to our props, and carrying capacities to our actors. We added some sigs and Predicates to reflect this change.

### New/Modified Sigs
+ _ones_: This is a sig that we sued to help represent weights and carrying capacity. You can think of every instance of ones as having a weight of one

+ _Actor_: we added a capacity field, which is a set of ones. The cardinality of this set is the total weight an Actor can carry.

+ _Prop_: we added a weight field, which is a set of ones. The cardinality of this set is the total weight of a prop.

### New Preds
+ _uniqueWeight_: This ensures that every Actor and Prop has a capacity/weight of at least one, and that there is no intersection between their sets (allowing this helps when we need to combine capacities/weights later)

+ _constrainWeight_: This makes sure that the combines weight of the Props does not exceed the Actor's capacity, and that no prop is carried by more than one actor. 


### Transition
+ _sceneChange_: This is where most of our functionality lies. This transition constrains Events so that Actors can only carry props when both the Actor's and Prop's source Position and destination Position Align. The Position must also align with which Props and Actors are designated as being onstage during this Scene (if they are in this Scene's actors or props set respectively)

## Visualization
In addition to our Forge spec, we have included python scripts, as well as a webpage made with HTML/CSS/JS in order to visualize our model! The pipeline is as follows:

1. Use PlayGen.py to generate a play inst
2. Copy and Paste the inst into Forge and run our spec (make sure the active command is `run<|traces|> toRun for [name of your inst]`)
3. Use ParsePlay.py on the xml produced by Forge
4. Open the webpage, and use the file upload button to select the json that was produced by ParsePlay.py
