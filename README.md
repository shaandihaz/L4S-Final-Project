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

+ _Center_: This sig extends Position, and represents __on stage__

+ _Event_: This sig is used as the parameter to the transitions in the trace. 
It represents a 'Scene Change' or 'Blackout' in theatre terms. Below are the fields of Event:
  - carryOnAssignments (set Actor -> Prop): This relation represents which actors should carry which props __on stage__ in order to transition from the 'pre scene' to the 'post scene'
  - carryOffAssignments (set Actor -> Prop): This relation represents which actors should carry which props __off stage__ in order to transition from the 'pre scene' to the 'post scene'
  - pre (one Scene): The scene before this Event
  - post (one Scene): The Scene after this Event

### Preds
+ _onStageExactlyCenter_
+ _allAccountedFor_
+ _positions_
+ _abstractPosition_
+ _functionalAssignments_

### State
+ _initState_
+ _finalState_


### Transition
+ _sceneChange_
