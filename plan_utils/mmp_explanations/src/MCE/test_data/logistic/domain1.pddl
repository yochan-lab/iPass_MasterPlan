(define (domain logistics)
  (:requirements :strips :typing)
  (:types truck
          airplane - vehicle
          package
          vehicle - physobj
          airport
          location - place
          city
          place
          physobj - object)

  (:predicates  (in-city ?loc - place ?city - city)
        (at ?obj - physobj ?loc - place)
        (in ?pkg - package ?veh - vehicle))

(:action LOAD-AIRPLANE
:parameters (?pkg - package ?airplane - airplane ?loc - place)
:precondition
(and
( at ?pkg ?loc )
)
:effect
(and


)
)

(:action UNLOAD-TRUCK
:parameters (?pkg - package ?truck - truck ?loc - place)
:precondition
(and
( in ?pkg ?truck )
)
:effect
(and


)
)

(:action UNLOAD-AIRPLANE
:parameters (?pkg - package ?airplane - airplane ?loc - place)
:precondition
(and
( in ?pkg ?airplane )
( at ?airplane ?loc )
)
:effect
(and

(not ( in ?pkg ?airplane ))
)
)

(:action FLY-AIRPLANE
:parameters (?airplane - airplane ?loc-from - airport ?loc-to - airport)
:precondition
(and
( at ?airplane ?loc-from )
)
:effect
(and

(not ( at ?airplane ?loc-from ))
)
)

(:action DRIVE-TRUCK
:parameters (?truck - truck ?loc-from - place ?loc-to - place ?city - city)
:precondition
(and
( at ?truck ?loc-from )
( in-city ?loc-to ?city )
)
:effect
(and

(not ( at ?truck ?loc-from ))
)
)

(:action LOAD-TRUCK
:parameters (?pkg - package ?truck - truck ?loc - place)
:precondition
(and
( at ?pkg ?loc )
( at ?truck ?loc )
)
:effect
(and
( in ?pkg ?truck )
(not ( at ?pkg ?loc ))
)
)


)
