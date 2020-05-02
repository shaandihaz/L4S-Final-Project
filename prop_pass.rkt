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
pred onStageExactlyCenter {
    all s : Scene | {s.actors = (s.actorPos).Center
    s.props = (s.propPos).Center}
}

-- ensure every actor/prop is given a position in every scene
pred allAccountedFor{
    all s : Scene | {
        (s.actorPos).Position = Actor
        (s.propPos).Position = Prop
        (~(s.actorPos)).(s.actorPos) in iden
        (~(s.propPos)).(s.propPos) in iden
    }       
    //(~(s.actorPos)).(s.actorPos) in iden and  (~(s.propPos)).(s.propPos) in iden
}

pred positions{
    onStageExactlyCenter
    allAccountedFor
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

-- ensures all prop assignments are functional and injective
pred functionalAssignments{
    all e: Event |  {(~(e.carryOnAsignments)).(e.carryOnAsignments) in iden
    ((e.carryOnAsignments)).~(e.carryOnAsignments) in iden
    (~(e.carryOffAsignments)).(e.carryOffAsignments) in iden
    ((e.carryOffAsignments)).~(e.carryOffAsignments) in iden}
}

// a transition to constrain Scene Changes.
transition[Scene] sceneChange[e: Event] {
    e.pre = this
    e.post = this'
    -- the new props are the old ones, minus the ones that were carried off,
    -- plus the ones that were carried on
    props' = props - Actor.(e.carryOffAsignments) + Actor.(e.carryOnAsignments)
    
    -- the new actors must include the ones that were on before minus those who
    -- carried props off plus those who carried props on
    actors - (e.carryOffAsignments).Prop + (e.carryOnAsignments).Prop in actors'
    
    -- carry on pairs the actors and props that were offstage but will be on
    (e.carryOnAsignments).Prop in (actors' - actors)
    Actor.(e.carryOnAsignments) = (props' - props)
    
     -- carry off pairs the actors and props that were onstage but will be off
    (e.carryOffAsignments).Prop in (actors - actors')
    Actor.(e.carryOffAsignments) = (props - props')
    
    -- Ensures that if a given prop/actor pair is assigned, the actor's and prop's source and target positions are the same
    all p : Prop | all a : Actor {
        (p->a in e.carryOffAsignments) or (p->a in e.carryOnAsignments) => a.actorPos' = p.propPos' and a.actorPos = p.propPos
    }
    
    -- ensures that no actors move from LEFT to RIGHT and vice versa
    no actorPos.Left & actorPos'.Right
    no actorPos.Right & actorPos'.Left
}

state[Scene] initState{
    -- constraints for the first state
    no actors
    no props
}

state[Scene] finalState {
    -- constraints for the last state that should hold for a valid solution
    no actors
    no props
}

transition[Scene] model {
    some e: Event | sceneChange[this, this', e]
}

pred interestingModel{
    -- ensure there are some changes
    some carryOnAsignments
    some carryOffAsignments
}

pred toRun{
    positions
    abstractPosition
    functionalAssignments
    interestingModel
}

trace<|Scene, initState, model, finalState|> traces: linear {}

--run<|traces|> toRun for exactly 3 Scene, exactly 2 Actor, exactly 1 Prop, exactly 2 Event, exactly 3 Position

inst tester { 
    Scene = Scene0 + Scene1 + Scene2 + Scene3 + Scene4 + Scene5 + Scene6 + Scene7
    Event = Event0 + Event1 + Event2 + Event3 + Event4 + Event5 + Event6 + Event7
    Actor = Actor0 + Actor1 + Actor2 + Actor3
    Prop = Prop0 + Prop1 + Prop2 + Prop3 + Prop4
    actors = Scene1->Actor1 + Scene1->Actor2 + Scene1->Actor3 + Scene2->Actor0 + Scene2->Actor1 + Scene3->Actor2 + Scene3->Actor3 + Scene4->Actor1 + Scene4->Actor2 + Scene4->Actor3 + Scene5->Actor2 + Scene5->Actor3 + Scene5->Actor0 + Scene6->Actor0 + Scene6->Actor2
}
run<|traces|> toRun for tester