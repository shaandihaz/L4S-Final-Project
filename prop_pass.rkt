#lang forge

// a sig to represent a Scene.
// Scenes act as the states involved in the Trace.
sig Scene {
    // the set of Actors ON STAGE/CENTER during this Scene
    actors : set Actor,
    // the set of Props ON STAGE/CENTER during this Scene
    props : set Prop,
    // the position of each Actor during this Scene
    actorPos : set Actor -> Position,
    // the Position of each Prop during this Scene
    propPos : set Prop -> Position
}

// a predicate to ensure that if a given is on stage
// for a scene, then their position during that scene is Center
pred onStageImpliesCenter {
    // TODO: this pred could take a Scene as a pred, or could have a helper
    // that takes a scene as a pred (so there would be a forall kind of thing going on here)
}

// a sig to represent an Actor.
sig Actor {
}

// a sig to represent a Prop.
sig Prop {
}

// a sig to represent a Position.
// this is used for both Actors and Props.
sig Position {}

// this Position specifies OFF STAGE LEFT.
one sig Left extends Position {}

// this Position specifies OFF STAGE RIGHT.
one sig Right extends Position {}

// this Position specifies ON STAGE.
one sig Center extends Position {}

// a pred to ensure that all Positions are either Left, Right, or Center.
// Position acts as an 'Abstract Class' this way.
pred abstractPosition {
    Position = Left + Right + Center
}

// a sig to represent an Event, which is a Scene Transition.
sig Event {
    // the set of Actor/Prop assignments
    assignments : set Actor -> Prop,
    // the Scene before this transition
    pre: one State,
    // the Scene after this transition
    post: one State
}

// a transition to constrain Scene Changes.
transition[Scene] sceneChange[e: Event] {
}

// a constraint for the initial Scene/State of the Trace.
state[Scene] initScene {
}

// a constraint for the final Scene/State of the Trace.
state[Scene] finalScene {
}

