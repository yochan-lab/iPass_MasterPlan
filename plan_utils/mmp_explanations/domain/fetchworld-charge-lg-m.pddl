(define (domain fetchworld)

(:requirements :strips :typing :action-costs :negative-preconditions)

(:types        location locatable - object
	       box - locatable
	       )

(:predicates   (hand-tucked)
	       (hand-empty)
	       (charged)
               (holding ?obj - box)
               (block-at ?obj - box ?pos - location)
	       (robot-at ?pos - location)
	       )

(:action move
	 :parameters	(?from ?to - location)
	 :precondition 	(and (charged) (robot-at ?from) (hand-tucked))
  	 :effect 	(and (not (charged)) (robot-at ?to) (not (robot-at ?from)))
  	 )

(:action pickup
  	 :parameters	(?obj - box ?loc - location)
  	 :precondition 	(and (charged) (hand-empty) (block-at ?obj ?loc) (robot-at ?loc))
  	 :effect 	(and (not (charged)) (holding ?obj) (not (hand-tucked)) (not (hand-empty)) (not (block-at ?obj ?loc)))
  	 )

(:action putdown
  	 :parameters	(?obj - box ?loc - location)
  	 :precondition 	(and (charged) (holding ?obj) (robot-at ?loc))
  	 :effect 	(and (not (charged)) (not (holding ?obj)) (not (hand-tucked)) (hand-empty) (block-at ?obj ?loc))
  	 )

(:action tuck
  	 :parameters	()
  	 :precondition 	(and (not (hand-tucked)))
  	 :effect 	(and (hand-tucked))
  	 )

(:action charge
  	 :parameters	()
  	 :precondition 	(and (not (charged)))
  	 :effect 	(and (charged))
  	 )

)