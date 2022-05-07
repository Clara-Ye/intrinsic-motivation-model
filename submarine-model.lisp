
(clear-all)

(define-model submarine 

(sgp :esc t :v nil :trace-detail low
     :model-warnings nil :style-warnings nil
     :show-focus nil
     :ul t :egs 1 :ult nil
     :mp 1.0 :rt -0.2 :act nil
     :epl nil :pct nil
     :needs-mouse t :cursor-noise t
     :default-target-width 10)

(chunk-type play-game state)
(chunk-type integer string)
(chunk-type fraction numer denom position)

(define-chunks 
    (first-goal isa play-game state find-numer)
    (second-goal isa play-game state find-sol)
    (find-numer) (read-numer) (encode-numer)
    (find-denom) (read-denom) (encode-denom)
    (retrieve) (retrieved) (estimate)
    (prepare-mouse) (move-mouse)
    (find-sol) (memorize-sol) 
    (end-choice) (wait) (quit)
)

(add-dm
    (one   isa integer  string "1")
    (two   isa integer  string "2")
    (three isa integer  string "3")
    (four  isa integer  string "4")
    (five  isa integer  string "5")
    (six   isa integer  string "6")
    (seven isa integer  string "7")
    (eight isa integer  string "8")
    (nine  isa integer  string "9")
    (ten   isa integer  string "10")
    (half  isa fraction  numer one  denom two  position 750))
 

(p find-numerator
    =goal>
        isa        play-game
        state      find-numer
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
  ==>
    =goal>
        state      encode-numer
    +retrieval>
        isa        integer
        string     =numer
  )

(p encode-numerator
    =goal>
        isa        play-game
        state      encode-numer
    =retrieval>
    ?imaginal>
        state      free
  ==>
    =goal>
        state      find-denom
    +imaginal>
        isa        fraction
        numer      =retrieval
  )

(p find-denominator
    =goal>
        isa        play-game
        state      find-denom
    =imaginal>
  ==>
    +visual-location>
        isa        visual-location
        kind       text
      > screen-y   520
    =imaginal>
  )

(p attend-denominator
    =goal>
        isa        play-game
        state      find-denom
    =imaginal>
    =visual-location>
        isa        visual-location
        kind       text
      > screen-y   520
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
        state      encode-denom
    +retrieval>
        isa        integer
        string     =denom
    =imaginal>
  )

(p encode-denominator
    =goal>
        isa        play-game
        state      encode-denom
    =imaginal>
        isa        fraction
        numer      =numer
        denom      nil
    =retrieval>
  ==>
    =goal>
        state      retrieve
    =imaginal>
        denom      =retrieval
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
    =goal>
        state      estimate
    +visual-location>
        isa        visual-location
        kind       line
        color      blue
    =imaginal>
        position   750
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
    =imaginal>
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
        state      wait
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
        state      wait
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
    =goal>
        state      quit
    +manual>
        cmd        press-key
        key        "e"
    -imaginal>
  )

(spp attend-numerator :u 20)
(spp attend-target :u 20)
(spp continue-game :u 40)
(spp end-game :u 0 :fixed-utility t)

(set-base-levels 
  (one 10)  (two   10) (three 10) (four 10) (five 10)
  (six 10)  (seven 10) (eight 10) (nine 10) (ten  10))

(set-similarities
  (one   two   -0.1) (two   three -0.1) (three four  -0.1)
  (four  five  -0.1) (five  six   -0.1) (six   seven -0.1) 
  (seven eight -0.1) (eight nine  -0.1) (nine  ten   -0.1)
  (one   three -0.2) (two   four  -0.2) (three five  -0.2) 
  (four  six   -0.2) (five  seven -0.2) (six   eight -0.2) 
  (seven nine  -0.2) (eight ten   -0.2) 
  (one   four  -0.3) (two   five  -0.3) (three six   -0.3) (four seven -0.3) 
  (five  eight -0.3) (six   nine  -0.3) (seven ten   -0.3)
  (one   five  -0.4) (two   six   -0.4) (three seven -0.4) 
  (four  eight -0.4) (five  nine  -0.4) (six   ten   -0.4)
  (one   six   -0.5) (two   seven -0.5) (three eight -0.5) 
  (four  nine  -0.5) (five  ten   -0.5)
  (one   seven -0.6) (two   eight -0.6) (three nine  -0.6) (four ten   -0.6)
  (one   eight -0.7) (two   nine  -0.7) (three ten   -0.7)
  (one   nine  -0.8) (two   ten   -0.8)
  (one   ten   -0.9))

)