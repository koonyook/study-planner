(deftemplate subject
	(slot name)
	(slot code)
	(multislot prerequisite)
)

(deftemplate subject-level
	(slot code)
	(slot level)
)

(deftemplate link
	(slot pre)
	(slot post)
	(slot level-pre)
	(slot level-post)
)

;(deffacts database			;fact in the database
;	(max-unit 22)
;	
;	(subject
;		(name A1)
;		(code 111)
;		(unit 3)
;		(allowed-term 1)
;		(prerequisite)
;	)
;	(subject
;		(name A2)
;		(code 222)
;		(unit 3)
;		(allowed-term 3)
;		(prerequisite)
;	)
;	(subject
;		(name A3)
;		(code 333)
;		(unit 3)
;		(allowed-term 3)
;		(prerequisite)
;	)
;	(subject
;		(name B1)
;		(code 444)
;		(unit 3)
;		(allowed-term 3)
;		(prerequisite 111 222)
;	)
;	(subject
;		(name B2)
;		(code 555)
;		(unit 3)
;		(allowed-term 3)
;		(prerequisite 333)
;	)
;	(subject
;		(name C1)
;		(code 666)
;		(unit 3)
;		(allowed-term 3)
;		(prerequisite 444)
;	)
;	(subject
;		(name D1)
;		(code 777)
;		(unit 3)
;		(allowed-term 3)
;		(prerequisite 111 333)
;	)
;	(subject
;		(name E1)
;		(code 888)
;		(unit 3)
;		(allowed-term 3)
;		(prerequisite 111)
;	)
;)

;(deffacts input				;fact from user
;	(now-term 2)
;	(learned 204111)
;	(learned 204222)
;)

;rules
;target: answer all prerequisite of a subject
;(defrule get-target
;	(not (target ?))
;	=>
;	(printout t "What is code of target subject?" crlf)
;	(assert (target (read)))
;)

(defrule get-new-target
	(target ?target-code)
	(subject (code ?target-code) (prerequisite $? ?next-code $?))
	(not (must-regis ?next-code))
	=>
	(assert (must-regis ?next-code))
	(printout t "must regis:" ?next-code crlf)
	(assert (target ?next-code))
)

(defrule set-initial-level
	(subject (code ?a-code))
	(not (subject-level (code ?a-code)))
	=>
	(assert (subject-level (code ?a-code) (level -1)))
)

(defrule set-initial-link
	(subject (code ?post) (prerequisite $? ?pre $?))
	(not (link (pre ?pre) (post ?post)))
	=>
	(assert (link (pre ?pre) (post ?post) (level-pre -1) (level-post -1)))
)

(defrule finish-set-initial-link
	(forall
		(subject (code ?a-code))
		(subject-level (code ?a-code))
	)
	(forall
		(subject (code ?post) (prerequisite $? ?pre $?))
		(link (pre ?pre) (post ?post))
	)
	=>
	(assert (already initial))
)

(defrule find-top
	(already initial)
	?subject-fact <- (subject-level (code ?a-code) (level -1))
	(not (exists (subject (code ?) (prerequisite $? ?a-code $?))))
	=>
	(modify ?subject-fact (level 0))
)

(defrule fill-level
	(already initial)
	?subject-fact <- (subject-level (code ?a-code) (level ?base))
	(subject (code ?next-subject) (prerequisite $? ?a-code $?))
	(subject-level (code ?next-subject) (level ?cmp))
	(test (>= ?cmp ?base))
	=>
	(modify ?subject-fact (level (+ ?cmp 1)))
)

(defrule update-link-post
	(subject-level (code ?a-code) (level ?true-level))
	?link-fact <- (link (post ?a-code) (level-post ?old-level))
	(test (< ?old-level ?true-level))
	=>
	(modify ?link-fact (level-post ?true-level))
)
(defrule update-link-pre
	(subject-level (code ?a-code) (level ?true-level))
	?link-fact <- (link (pre ?a-code) (level-pre ?old-level))
	(test (< ?old-level ?true-level))
	=>
	(modify ?link-fact (level-pre ?true-level))
)

(defrule check-finish-fill-level
	(forall
		(link (level-pre ?pre) (level-post ?post))
		(test (> ?pre ?post))		
	)
	;(not (already fill-level))		;this line for debugging
	=>
	(printout t "finish fill level" crlf)
	(assert (already fill-level))
)



;(defrule debug
;	(subject (level nil))
;	=>
;	(printout t "*")
;)
