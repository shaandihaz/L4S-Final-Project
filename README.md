# L4S Final Project

*by Lily Mayo, Mia Santomauro, and Zahid Hasan*

## Our Goal

Our goal was to model the passing and placement of props during a play. The purpose of our model is to guide directors in their blocking decisions. Such decisions include: which actors should carry which props, and where the actors should exit/enter from.

## Model Structure

We used Forge Traces to model our plays. Each play is represented by a Trace. 
The States in the Trace are the Scenes. The transitions in the Trace are the Scene changes. Below are descriptions of our Sigs, Preds, States, and Transitions.

### Sigs
+ _Scene_
+ _Actor_
+ _Prop_
+ _Position_
  - _Left_
  - _Right_
  - _Center_
+ _Event_

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
