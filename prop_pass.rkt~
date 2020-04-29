#lang forge

sig Scene {
    actors : set Actor,
    props : set Prop,
    actorPos : set Actor -> Position,
    propPos : set Prop -> Position
}

sig Actor {
}

sig Prop {
}

sig Position {}

one sig Left extends Position {}

one sig Right extends Position {}

one sig Center extends Position {}

pred abstractPosition {
    Position = Left + Right + Center
}

sig Event {
    assignments : set Actor -> Prop,
    pre: one State,
    post: one State
}

transition[Scene] sceneChange[e: Event] {
}

state[Scene] initState {
}

state[Scene] finalState {
}

