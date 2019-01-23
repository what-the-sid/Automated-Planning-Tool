(define (problem cookingproblem)
  (:domain dinner)
  (:init
        (garbage)
        (clean)
        (quiet)
  )
  (:goal (and
        (dinner)
        (present)
        (not (garbage))
  ))
)