
(clear-all)

(define-model submarine 

(sgp :v t :esc t :egs 1 :show-focus nil :trace-detail low
     :ul t :ult t 
     :epl nil :pct nil
     :needs-mouse t :cursor-noise t
     :default-target-width 40)

(chunk-type play-game state)
(chunk-type fraction numer denom position)

(define-chunks 
    (goal isa play-game state find-numer)
    (find-numer) (read-numer) 
    (find-denom) (attend-denom) (read-denom) 
    (retrieve) (retrieved) (estimate)
    (prepare-mouse) (move-mouse)
    (find-sol) (memorize-sol) (end-choice)
)

(add-dm
 (half isa fraction numer "1" denom "2" position 750))
 

(p find-numerator
    =goal>
        isa        play-game
        state      find-numer
    ?visual-location>
        buffer     empty
  ==>
    +visual-location>
        isa        visual-location
        kind       text
      < screen-y   510
  )

(p cannot-find-numerator
    =goal>
        isa        play-game
        state      find-numer
    ?visual-location>
        buffer     failure
  ==>
    +visual-location>
        isa        visual-location
        kind       text
      < screen-y   510
  )

(p attend-numerator
    =goal>
        isa        play-game
        state      find-numer
    =visual-location>
        isa        visual-location
        kind       text
      < screen-y   510
    ?visual>
        state      free
  ==>
    =goal>
        state      read-numer
    +visual>
        isa        move-attention
        screen-pos =visual-location
  )

(p read-numerator
    =goal>
        isa        play-game
        state      read-numer
    =visual>
        isa        text
        value      =numer
    ?imaginal>
        state      free
  ==>
    =goal>
        state      find-denom
    +imaginal>
        isa        fraction
        numer      =numer
  )

(p find-denominator
    =goal>
        isa        play-game
        state      find-denom
    =imaginal>
  ==>
    =goal>
        state      attend-denom
    +visual-location>
        isa        visual-location
        kind       text
      > screen-y   520
    =imaginal>
  )

(p attend-denominator
    =goal>
        isa        play-game
        state      attend-denom
    =imaginal>
    =visual-location>
    ?visual>
        state      free
  ==>
    =goal>
        state      read-denom
    +visual>
        isa        move-attention
        screen-pos =visual-location
    =imaginal>
  )

(p read-denominator
    =goal>
        isa        play-game
        state      read-denom
    =imaginal>
        isa        fraction
        numer      =numer
        denom      nil
    =visual>
        isa        text
        value      =denom
  ==>
    =goal>
        state      retrieve
    *imaginal>
        denom      =denom
  )

(p retrieve-experience
    =goal>
        isa        play-game
        state      retrieve
    =imaginal>
        isa        fraction
        numer      =numer
        denom      =denom
  ==>
    =goal>
        state      retrieved
    +retrieval>
        isa        fraction
        numer      =numer
        denom      =denom
    =imaginal>
  )

(p retrieval-failure
    =goal>
        isa        play-game
        state      retrieved
    ?retrieval>
        buffer     failure
    =imaginal>
  ==>
    +retrieval>
        isa        fraction
        numer      "1"
        denom      "2"
    =imaginal>
  )

(p retrieval-success
    =goal>
        isa        play-game
        state      retrieved
    =retrieval>
        isa        fraction
        position   =posit
    =imaginal>
        isa        fraction
        numer      =numer
        denom      =denom
  ==>
    =goal>
        state      estimate
    +visual-location>
        isa        visual-location
        kind       line
        color      blue
    *imaginal>
        position   =posit
  )

(p estimate-position
    =goal>
        isa        play-game
        state      estimate
    =imaginal>
        isa        fraction
        position   =posit
    =visual-location>
  ==>
    =goal>
        state      prepare-mouse
    =visual-location>
        isa        visual-location
        screen-x   =posit
    =imaginal>
  )

(p move-mouse
    =goal>
        isa        play-game
        state      prepare-mouse
    =imaginal>
    =visual-location>
    ?manual>
        state      free
  ==>
    =goal>
        state      move-mouse
    +manual>
        isa        move-cursor
        loc        =visual-location
    =imaginal>
  )

(p click-mouse
    =goal>
        isa        play-game
        state      move-mouse
    ?manual>  
        state      free
    =imaginal>
  ==>
    =goal>
        state      find-sol
    +manual>
        isa        click-mouse
    =imaginal>
  )

(p find-target
    =goal>
        isa        play-game
        state      find-sol
    =imaginal>
 ==>
    +visual-location>
        isa        visual-location
        kind       line
        color      red
    =imaginal>
)

(p attend-target
    =goal>
        isa        play-game
        state      find-sol
    =imaginal>
    =visual-location>
        isa        visual-location
        kind       line
        color      red
    ?visual>
        state      free
  ==>
    =goal>
        state      memorize-sol
    +visual>
        isa        move-attention
        screen-pos =visual-location
    =imaginal>
  )

(p memorize-solution
    =goal>
        isa        play-game
        state      memorize-sol
    =visual>
        isa        line
        end1-x     =left
        end2-x     =right 
    =imaginal>
        isa        fraction
      - numer      nil
      - denom      nil
    !bind!         =mid (/ (+ =right =left) 2)
  ==>
    =goal>
        state      end-choice
    *imaginal>
        position   =mid
  )

(p continue-game
    =goal>
        isa        play-game
        state      end-choice
    ?manual>
        state      free
    ?imaginal>
        state      free
 ==>
    =goal>
        state      find-numer
    +manual>
        cmd        press-key
        key        "c"
    -imaginal>
  )

(p end-game
    =goal>
        isa        play-game
        state      end-choice
    ?manual>
        state      free
    ?imaginal>
        state      free
 ==>
    +manual>
        cmd        press-key
        key        "e"
    -imaginal>
  )

(goal-focus goal)

(spp continue-game :u 20)
(spp end-game :u 0)
)
