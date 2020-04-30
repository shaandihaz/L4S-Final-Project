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

// a predicate to ensure that if an Actor or prop is on stage
// for a scene, then their position during that scene is Center
pred onStageImpliesCenter {
    all s : Scene | {s.actors in s.actorPos.Center
    s.props in s.propPos.Center}
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
    // the set of Actor/Prop assignments to be carried on
    carryOnAsignments : set Actor -> Prop,
    // the set of Actor/Prop assignments to be carried off
    carryOffAsignments : set Actor -> Prop,
    // the Scene before this transition
    pre: one Scene,
    // the Scene after this transition
    post: one Scene
}

-- ensures all prop assignments are functional
pred functionalAssignments{
    all e: Event |  {(~(e.carryOnAsignments)).(e.carryOnAsignments) in iden
    (~(e.carryOffAsignments)).(e.carryOffAsignments) in iden}
}


// a transition to constrain Scene Changes.
transition[Scene] sceneChange[e: Event] {
    e.pre = this
    e.post = this'
    -- the carry on props are exactly those in the following scene that
    -- weren't in the previous scene
    (e.carryOnAsignments).Prop = props' - props
    -- the carry on actors must be in the following scene but not the previous
    Actor.(e.carryOnAsignments) in actors'  - actors
    -- the opposite for the carry off props
    (e.carryOffAsignments).Prop = props - props'
    Actor.(e.carryOffAsignments) in actors - actors
}

state[Scene] initState{
    -- constraints for the first state

}

state[Scene] finalState {
    -- constraints for the last state that should hold for a valid solution

}

transition[Scene] model {
    some e: Event | sceneChange[this, this', e]
}

pred interestingModel{
    -- ensure there are props and actors in every scene
    all s: Scene |
        ((some e : Event | e.pre = s) and (some e : Event | e.post = s))
        implies
        {some s.props
        some s.actors}
    -- ensure there are some changes
    some carryOnAsignments
    some carryOffAsignments
}

pred toRun{
    onStageImpliesCenter
    abstractPosition
    functionalAssignments
    interestingModel
}

trace<|Scene, initState, model, finalState|> traces: linear {}

run<|traces|> toRun for exactly 10 Scene, exactly 10 Actor, exactly 1 Prop, 11 Event, 3 Position