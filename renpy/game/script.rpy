# =============================================================================
# THE LAST TRAIN NEVER CAME  —  Ren'Py edition
# A short narrative exploration game. Played as Kali, with cold "flashes" into
# Emy's unspoken interior.
#
# HOW TO RUN:
#   1. Download Ren'Py (free) from https://www.renpy.org/  and install it.
#   2. In the Ren'Py launcher, click "Create New Project", name it anything,
#      finish the wizard. This makes a folder with a "game" subfolder.
#   3. Replace that project's  game/script.rpy  with THIS file.
#   4. Back in the launcher, select the project and press "Launch Project".
#
# HOW TO TURN IT INTO AN APP:
#   In the launcher, pick the project -> "Build Distributions" -> tick
#   Windows / Mac / Linux (or set up Android), then "Build". You get real,
#   double-clickable apps. ("Build Web" makes an online version.)
#
# ART & MUSIC are placeholders (colored shapes + silence) so it runs with zero
# extra files. Replace the `image` lines and the commented `play music` line
# whenever you have real art/audio. Everything you'd want to rewrite (dialogue,
# choices, endings) is plain text below — edit freely.
# =============================================================================


# ----- CHARACTERS -----------------------------------------------------------
# Spoken voices.
define k  = Character("Kali", color="#d9a55b", what_color="#e7e2d4")
define e  = Character("Emy",  color="#6f8466", what_color="#e7e2d4")
# Emy's unspoken interior (the "flash"). Cold blue, italic.
define ef = Character("Emy — unspoken", color="#9cc0e8",
                      what_color="#b6d2ee", what_italic=True)
# Kali's first-person narration uses plain narrator lines ("like this").


# ----- ART (built at runtime from Ren'Py displayables — no image files) ------
# These take advantage of Ren'Py's GPU compositing: blurred gradients, particle
# rain, animated mist and lightning. Swap any `image` for a PNG when you have
# real art (e.g.  image bg station = "station.png").

# Background: a dim, ruined station. We fake a smooth twilight by stacking color
# bands and blurring them heavily, then darkening the whole thing a touch.
image bg station = Transform(
    Composite(
        (1280, 720),
        (0,   0),   Solid("#0d1411"),                      # base green-black
        (0,   0),   Solid("#1c2c46", xysize=(1280, 300)),  # cold twilight at top
        (0, 430),   Solid("#3a2a1c", xysize=(1280, 140)),  # faint amber midband
        (0, 540),   Solid("#06080a", xysize=(1280, 180)),  # dark floor
    ),
    blur=70, matrixcolor=BrightnessMatrix(-0.04) * SaturationMatrix(0.92),
)

# Character figures, composited from simple parts so they read as people.
#   Emy : medium brown hair, mossy coat.
#   Kali: short black hair, clear glasses, dusk-violet coat.
# NOTE: distinct image tags ("emy_fig" / "kali_fig") so BOTH stay on screen.
# (defined with ATL so they gently "breathe" — note the offset timings.)
image emy_fig:
    Composite(
        (110, 270),
        (7,  60),  Solid("#45503f", xysize=(96, 210)),   # coat
        (28,  4),  Solid("#5a3f26", xysize=(54, 78)),    # brown hair (behind)
        (33, 10),  Solid("#d3a87f", xysize=(44, 56)),    # face
        (30, 10),  Solid("#5a3f26", xysize=(50, 17)),    # swept fringe
    )
    xalign 0.30 yalign 1.0 zoom 1.05
    block:
        ease 2.3 yoffset -4
        ease 2.3 yoffset 0
        repeat
image kali_fig:
    Composite(
        (110, 270),
        (7,  60),  Solid("#4a4250", xysize=(96, 210)),   # dusk-violet coat
        (33, 12),  Solid("#dcb491", xysize=(44, 56)),    # face
        (30,  4),  Solid("#161620", xysize=(50, 26)),    # short black hair
        (34, 30),  Solid("#cfe0ee", xysize=(40, 4)),     # glasses bridge/frame
    )
    xalign 0.70 yalign 1.0 zoom 1.05
    block:
        ease 2.7 yoffset -4
        ease 2.7 yoffset 0
        repeat

# Full-screen cold wash used during Emy flashes (with a blurred glow).
image flash_tint = Transform(Solid("#3a6abe"), alpha=0.22, blur=8)

# --- Atmosphere pieces ------------------------------------------------------
# A single thin rain streak; SnowBlossom spawns many and animates them falling.
image rain_drop = Solid("#aac3dc", xysize=(2, 16))
image rain = SnowBlossom(
    Transform("rain_drop", alpha=0.5),
    count=150, border=40,
    xspeed=(40, 70), yspeed=(900, 1200), fast=True,
)
# A heavier, closer rain layer for depth.
image rain_near = SnowBlossom(
    Transform(Solid("#c2d6ea", xysize=(3, 26)), alpha=0.35),
    count=50, border=40,
    xspeed=(60, 90), yspeed=(1300, 1600), fast=True,
)

# Cold mist pooling at the floor, blurred soft, drifting sideways.
image mist:
    Solid("#8aa099", xysize=(1700, 220))
    blur 45
    alpha 0.12
    yalign 1.04
    block:
        xoffset -70
        linear 16.0 xoffset 70
        linear 16.0 xoffset -70
        repeat

# Slow amber dust / spores drifting down through the lantern light.
image dust = SnowBlossom(
    Transform(Solid("#d9a55b", xysize=(3, 3)), alpha=0.35),
    count=40, border=20,
    xspeed=(-18, 18), yspeed=(18, 45), fast=True,
)

# Soft vignette: a dark frame, blurred heavily so the edges fall into shadow.
image vignette = Transform(
    Composite(
        (1280, 720),
        (0,   0),    Solid("#000000", xysize=(1280, 150)),
        (0,   570),  Solid("#000000", xysize=(1280, 150)),
        (0,   0),    Solid("#000000", xysize=(170, 720)),
        (1110, 0),   Solid("#000000", xysize=(170, 720)),
    ),
    blur=85, alpha=0.55,
)

# Distant lightning: long random waits, then a quick cold double-flash.
image lightning:
    Solid("#9ab4dc")
    alpha 0.0
    block:
        choice:
            18.0
        choice:
            27.0
        choice:
            36.0
        ease 0.05 alpha 0.5
        ease 0.06 alpha 0.05
        ease 0.05 alpha 0.65
        ease 0.55 alpha 0.0
        repeat

# The atmosphere overlay: rain + mist + lightning + a cool color wash. Shown
# for the whole game so it carries across every scene.
screen atmosphere():
    zorder 60
    add "lightning"
    add "dust"
    add "rain"
    add "rain_near"
    add "mist"
    add Solid("#16263a") alpha 0.10        # unifying cool grade
    add "vignette"                          # darken the edges last

# Small music on/off button in the corner (uses Ren'Py's built-in mute).
screen music_toggle():
    zorder 70
    textbutton "♪":
        xalign 0.98 yalign 0.02
        background None
        padding (12, 10)
        text_size 22
        text_idle_color "#8d918d"
        text_hover_color "#d9a55b"
        action Preference("music mute", "toggle")


# ----- STATE ----------------------------------------------------------------
default warmth      = 0      # accumulates from objects + choices
default flags       = set()  # remembered choices ("door_closed", "kissed", ...)
default seen        = set()  # which objects have been examined
default choices_made = 0     # door + fire
default a1_count    = 0      # number of Act 1 objects examined
default a2_count    = 0      # number of Act 2 objects examined

# Once warmth >= this AND she held your hand, the kiss unlocks.
define KISS_THRESHOLD = 6


# ----- A small helper for the flash effect ----------------------------------
# Usage:  call flash("...Emy's private thought...")
label flash(line):
    show flash_tint with Dissolve(0.3)
    ef "[line]"
    hide flash_tint with Dissolve(0.5)
    return


# ===========================================================================
#   START
# ===========================================================================
label start:
    scene bg station with fade
    show screen atmosphere      # rain, mist, lightning, color grade (whole game)
    show screen music_toggle    # corner ♪ button (mute/unmute)

    # Soft music. Drop a track at  game/audio/theme.ogg  and it plays + loops.
    # Guarded so the game still runs if you haven't added the file yet.
    if renpy.loadable("audio/theme.ogg"):
        play music "audio/theme.ogg" fadein 3.0

    show emy_fig
    show kali_fig with dissolve

    # --- OPENING (Kali POV; the conceit of the flashes is set up here) ------
    "The platform clock died at 11:54. I keep checking it anyway. Hope's a stubborn little muscle; mine never learned to quit."
    "Rain on a roof that's mostly gone now. Moss in the seams of the tiles. And her — Emy — three steps ahead of me, the way she always walks. Close enough to protect. Far enough to bolt."
    k "Well. The schedule says the last train left a long time before either of us was born."
    e "Then why'd you read the schedule."
    k "Hope's a hard habit."
    e "Yeah. Heard it kills people."
    call flash("I shouldn't've said that. She reads dead schedules for the same dumb reason I read exit signs. I just can't make it come out soft.")
    "There it is again. That half-second where I swear I can feel the inside of her — like the wall's got a hairline crack and the light leaks through before she patches it."
    k "We're stuck here till the light. Might as well get to know the place."
    e "...Fine. But I'm not singing campfire songs."
    "(I'm Kali. This is my night to walk — examine what catches my eye, talk when I'm ready. And every so often I'll catch a flash of her: the parts she keeps behind her teeth.)"

    jump explore_act1


# ===========================================================================
#   ACT 1 — first sweep of the station
# ===========================================================================
label explore_act1:
    menu:
        "Look around the station. The night is long; there's no wrong pace."

        "The cracked bench" if "bench" not in seen:
            $ seen.add("bench")
            $ a1_count += 1
            $ warmth += 0
            call obj_bench
            jump explore_act1

        "The faded travel poster" if "poster" not in seen:
            $ seen.add("poster")
            $ a1_count += 1
            $ warmth += 1
            call obj_poster
            jump explore_act1

        "The dead radio" if "radio" not in seen:
            $ seen.add("radio")
            $ a1_count += 1
            $ warmth += 1
            call obj_radio
            jump explore_act1

        "Kali's pack" if "pack" not in seen:
            $ seen.add("pack")
            $ a1_count += 1
            $ warmth += 1
            call obj_pack
            jump explore_act1

        "The shard of mirror" if "mirror" not in seen:
            $ seen.add("mirror")
            $ a1_count += 1
            $ warmth += 1
            call obj_mirror
            jump explore_act1

        "The jammed service door" if "door" not in seen:
            $ seen.add("door")
            $ a1_count += 1
            call choice_door
            jump explore_act1

        "The rusted barrel" if "fire" not in seen:
            $ seen.add("fire")
            $ a1_count += 1
            call choice_fire
            jump explore_act1

        "Let the night settle in around you." if choices_made >= 2 and a1_count >= 6:
            jump act2_intro

    jump explore_act1


# ----- Act 1 objects --------------------------------------------------------
label obj_bench:
    "A bench grown soft with rot. Someone carved two sets of initials into it once, then scratched one out. I run my thumb over the scar of it."
    e "People used to wait here. Real polite about it. Lined up. Trusted the thing would come."
    k "You say 'trusted' like it's a disease."
    e "Isn't it? You trust a train. Train stops coming. Now you're just a person standing in the cold, holding a ticket."
    k "Or you're a person who got to believe in something, right up until you didn't. That's not nothing."
    e "..."
    call flash("She still believes in things. I can see her doing it — right now, believing in me. It's the scariest thing I've ever had to stand next to and not flinch away from.")
    e "Sit down before you fall down. You've been on that foot all day."
    return

label obj_poster:
    "A peeling poster. A coastline that probably doesn't exist anymore. 'THE SEA IS CLOSER THAN YOU THINK.'"
    k "I've never seen it. The sea. Have you?"
    e "Once. From far. It was gray and it was loud and it didn't care about us at all."
    k "That sounds kind of perfect."
    e "...It kind of was."
    k "Take me sometime. When the roads are quieter."
    e "The roads are never gonna be quieter, Kali."
    k "Then take me when they're loud. I don't mind, if it's with you."
    "She looks at the poster very hard, so she doesn't have to look at me."
    call flash("Take you to the sea. Like I get to make plans. Like wanting something out loud doesn't just hand the world a list of what to take from me. ...I'd carry you the whole way, though. I'd never say it. But I would.")
    return

label obj_radio:
    "A handheld radio, half its case gone. I thumb the wheel out of habit. Static, then almost-music, then static."
    k "Wait— go back. There. You hear that?"
    e "It's noise."
    k "It's a song. Somebody, somewhere, is still playing a song. That means somebody's still out there."
    e "Or it's a tape on a loop in an empty room, playing for no one."
    k "God, you're exhausting."
    e "I'm careful. There's a difference."
    k "Is there? From in here it looks like the same coat."
    "She turns the volume down to almost-nothing and lets the almost-music stay. A small mercy. For who, neither of us says."
    call flash("It's a tape on a loop in an empty room. I know that. I turned it down so it'd keep playing anyway — because she smiled at it for one second. That's the whole truth I keep behind the careful.")
    return

label obj_pack:
    "Kali's pack — my pack — slumped against the wall. The zipper's broken; I've tied it with a bootlace."
    e "You carry too much. You'll wreck your back hauling other people's junk."
    k "It's not junk. Look— this is from the kid in the river town. This, the old man traded me for stitches."
    e "So you carry strangers around with you."
    k "I carry proof. That I met them. That they were real and they were kind and the world had them in it for a while."
    e "And when the pack gets too heavy?"
    k "Then I guess I find someone to share the weight."
    "She's not looking at the pack when she says the next part. She's looking at me."
    call flash("Share the weight. Her name was right there in my mouth. I swallowed it, like always. Names are just one more thing the world knows to come back for.")
    return

label obj_mirror:
    "A long shard of mirror wedged in a ticket window. I can see half my face in it. We both can."
    k "There. That's us. The whole population of the world, far as we know."
    e "Population's down. One of us looks like hell."
    k "You look tired, Emy. Not the same thing."
    e "What's the difference."
    k "Tired means you've still got somewhere to get to. People who give up stop looking tired. They look... finished. You're not finished."
    e "How do you know."
    k "Because you keep checking that I'm still behind you. Every twenty steps. All day."
    e "...I do not."
    k "You did it twice while we've been standing here."
    call flash("Three times. She missed one. I check because the day she's not behind me is the day I forget how to keep walking. I'd rather not learn what that's like.")
    return


# ----- Act 1 choices --------------------------------------------------------
label choice_door:
    "A service door, swollen in its frame. Half-open. Cold air pours through it like water. I could force it shut. I could leave it."
    e "Your call, Kali. Leave it open so we can run if we have to... or shut it, and it's just the two of us in here till morning."
    menu:
        "Force it shut. \"Nothing's getting in tonight. Including the cold.\"":
            $ flags.add("door_closed")
            $ warmth += 1
            "It takes both of us, shoulders to the wood. The door groans home. The cold stops moving. The room gets very quiet, and very small, and only ours."
            k "...Just us, then."
            e "Just us. Don't make it weird."
            call flash("Just us. Sealed in. No road out and — God help me — I'm not looking for one. First time in years the want's louder than the fear. Don't make it weird, she says. I'm the one making it weird.")
            k "Too late."

        "Leave it open. \"I like knowing the way out.\"":
            $ flags.add("door_open")
            "I leave it. The cold keeps its road through the room. Emy plants herself where she can see it — the dark rectangle of out-there."
            k "You always need a door, huh."
            e "I always need to know I could go. Doesn't mean I will."
            call flash("She left it open. For me. Didn't even make me ask. She figured out the shape of my fear and built the room around it. Nobody's ever done that. I don't have a word for what it does to me.")
            k "Okay. As long as you know you don't have to."

    $ choices_made += 1
    return

label choice_fire:
    "An old burn barrel. There's enough dry scrap for one small fire. Maybe enough warmth for one of us to actually sleep."
    e "One fire. Barely enough scrap for it. Enough warmth for one of us to really sleep, maybe. ...Your call. You're better at calls than me."
    menu:
        "\"We split it. Both half-cold beats one of us alone.\"":
            $ flags.add("fire_shared")
            $ warmth += 1
            "We build it small and sit close, close enough that the question of how close stops being a question. The fire ticks. Our shoulders end up touching. Neither of us moves away."
            k "See? Half-cold's not so bad."
            call flash("Her shoulder against mine. I could map the exact line of it with my eyes shut. I keep thinking move, you'll wreck it, and my body keeps refusing the order. For once I let it lose the argument.")
            e "...It's bearable."
            k "High praise, coming from you."

        "\"You take it, Emy. Sleep — I've got the watch.\"":
            $ flags.add("fire_gave")
            $ warmth += 1
            "She folds down by the barrel, smaller than she'd ever let herself look awake. I take the dark just past the firelight and keep my eyes on the door. On her. Mostly on her."
            e "(half-asleep) ...You're staring."
            k "I'm keeping watch."
            e "Mm. 'm cold."
            call flash("She stayed close. She's keeping watch over me like I'm something worth guarding. When did I get soft enough to let someone do that... and why don't I want it to stop.")
            "I shift in until the fire's warmth and mine reach her at the same time. Some kindnesses you don't announce."

        "\"Take it. I'll be alright over here.\" (sit apart)":
            $ flags.add("fire_apart")
            $ warmth -= 1
            "I give her the fire and take the far wall — a careful stretch of cold floor I put there on purpose. I'm so tired of being the only one reaching. Tonight I let the gap be a gap."
            e "...You don't have to sit all the way over there."
            k "I'm alright where I am."
            call flash("She pulled back. She finally pulled back. I do this — I teach people to stop trying, then I'm gutted when they learn. The worst part isn't the cold. It's how much of me was begging her to argue.")

    $ choices_made += 1
    return


# ===========================================================================
#   ACT 2 — the night deepens
# ===========================================================================
label act2_intro:
    "The cold settles in for real. The dark gets older. Somewhere a beam ticks as the temperature drops, and the station gives up a few more of its secrets — shapes I didn't see before, or wasn't ready to."
    e "...It's a long way still, till morning."
    k "Good. I'm not done with tonight yet."
    call flash("Neither am I. God help me — I don't want this one to end. First time in years I've wanted the dark to last a little longer.")
    jump explore_act2

label explore_act2:
    menu:
        "New shapes in the dark now. Go and look."

        "The ticket-window ledger" if "ledger" not in seen:
            $ seen.add("ledger")
            $ a2_count += 1
            $ warmth += 1
            call obj_ledger
            jump explore_act2

        "A child's shoe" if "shoe" not in seen:
            $ seen.add("shoe")
            $ a2_count += 1
            $ warmth += 1
            call obj_shoe
            jump explore_act2

        "The broken skylight" if "skylight" not in seen:
            $ seen.add("skylight")
            $ a2_count += 1
            $ warmth += 1
            call obj_skylight
            jump explore_act2

        "Emy's folding knife" if "knife" not in seen:
            $ seen.add("knife")
            $ a2_count += 1
            $ warmth += 1
            call obj_knife
            jump explore_act2

        "A dented flask" if "flask" not in seen:
            $ seen.add("flask")
            $ a2_count += 1
            $ warmth += 1
            call obj_flask
            jump explore_act2

        "Sit with her." if a2_count >= 3:
            jump beat_hands

    jump explore_act2


# ----- Act 2 objects --------------------------------------------------------
label obj_ledger:
    "Behind the cracked ticket glass, a ledger swollen fat with damp. Columns of names. Destinations. Every line is someone who stood right where we're standing and believed they were going somewhere."
    k "Look how many. All these people. All these somewheres."
    e "All gone now. Names in a wet book nobody'll ever read."
    k "We're reading it."
    e "...Yeah. I guess we are."
    call flash("She does that. Finds the one thread of not-pointless in a thing and pulls until it holds my weight too. I walked in here sure the world was just a graveyard. She keeps quietly turning it back into a place where people lived.")
    "I write two names, small, in the margin where the paper's still dry. They'll be gone by morning. I write them anyway."
    e "...Leave a little room. In case we come back."
    return

label obj_shoe:
    "A child's shoe on its side under the bench. Small. The laces still tied in a careful double knot somebody must have learned the slow way."
    e "..."
    k "Hey. You okay?"
    e "Fine. It's just a shoe."
    call flash("It is not just a shoe. It's a person who got tied into their laces by somebody who loved them, on a morning that ended like all the mornings ended. I don't have words for that don't crack open, so I hand her 'fine.'")
    k "We don't have to look at it."
    e "No. Somebody should. Somebody should look at the small things and not flinch. It's the only funeral most of them ever got."
    "She sets the shoe upright, careful, the way you'd straighten something on a grave. Something in my chest goes tight and bright and dangerous, and I have to look away first."
    return

label obj_skylight:
    "A jagged hole torn in the roof. Through it, impossibly, stars — more than the dead cities ever let us see. The dark up there doesn't know a thing ended down here."
    k "There's the one thing the world couldn't ruin. Too far away to get the news."
    e "Make a wish, then. Isn't that the deal."
    k "You first."
    e "I don't wish. Wishing's just disappointment with extra steps."
    call flash("I wished. Of course I wished. I wished for exactly what's standing next to me to still be standing next to me when the light comes up. I'd never say it out loud. Saying it out loud is how the world learns what to take.")
    k "Okay. Then I'll wish loud enough for the both of us."
    e "...Don't waste it on me."
    k "Too late. Already did."
    return

label obj_knife:
    "She's got an old folding knife she keeps touching when she thinks I'm not looking. Bone handle, worn pale where her thumb sits. The one thing she carries that isn't strictly for surviving."
    k "Can I?"
    e "...Careful. It's sharp."
    "She sets it in my hand. From Emy, this is practically handing me her diary."
    k "Whose was it?"
    e "Someone's. Before. They taught me how to hold it so I'd never have to need anybody to keep me safe."
    call flash("And it worked. I never needed anybody. That was the whole point, and the whole prison. Then she walks in and I catch myself wanting to need her, and the knife hasn't got one useful thing to say about that.")
    k "They'd be glad it kept you safe."
    e "Yeah. Funny thing is — lately I keep forgetting to reach for it."
    k "Yeah? Why's that."
    e "...You know why. Don't make me say it."
    return

label obj_flask:
    "A dented steel flask in a locker, somehow still sealed. She sniffs it, makes a face, takes a swig anyway, and hands it over. Some firewater that outlived the end of everything."
    k "God, that's awful."
    e "Best awful thing for miles."
    k "(coughs) To the last train. May it stay good and gone."
    e "To the last train."
    call flash("She's loose now, warm, laughing at the burn of it, and I could watch her laugh until the world starts itself over. I'm in so much trouble. The good kind. The kind I'd forgotten was even on the menu.")
    e "...You're easier to be around than anybody's got a right to be, you know that?"
    k "That a compliment?"
    e "It's the closest I've got. Take it before I take it back."
    return


# ===========================================================================
#   LATE BEATS — the hand, then (if warm) the kiss
# ===========================================================================
label beat_hands:
    "Later. The fire's low, or the cold's deep — depends which way the night went. We're quiet in the kind of way that's louder than talking."
    call flash("Do it. Just do it. Put your hand where she can find it. She's spent all night building me rooms with the doors left open — she did the brave part already. The least I can do is leave one thing of mine out in the cold and not snatch it back.")
    "And then — I feel it before I see it. Emy's hand sliding onto the floor in the space between us. Palm up. Not reaching. Just there. From her, that's not a gesture. That's a held breath she's deciding not to take back."

    menu:
        "Take her hand.":
            $ flags.add("hand_held")
            $ warmth += 2
            "I put my hand in hers and don't say anything clever about it, so she'll know it's not a joke I'm setting up."
            e "Don't. I'll lose my nerve."
            k "Okay. I've got it, then. The nerve. I'll hold onto it for you."
            call flash("She took it. She didn't make me explain, didn't make it a thing. I put my hand out like a dare to myself and she just... met it. Like it was always going to be easy. Maybe — maybe it gets to be easy.")
            "And she holds on. All the rest of the night, through every long hour of it, she holds on."

        "Reach — then falter, afraid to get it wrong.":
            $ flags.add("hand_almost")
            "My fingers get close enough to feel the warmth coming off her skin. Then some old caution of mine — don't startle her, don't want it too loud — stalls my hand an inch short."
            call flash("She almost did. I felt her get close. Then nothing. ...Maybe I read it wrong. Maybe a hand on the floor is just a hand, and I'm the fool who made it mean the whole world.")
            k "I'm here. I'm not going anywhere. Whenever you're ready — even if ready's not tonight."
            e "...Yeah."

        "Leave it lying there. Look at the fire.":
            $ flags.add("hand_none")
            $ warmth -= 1
            "I look at the fire instead. I tell myself it's kinder not to crowd her. I'm not sure I believe me."
            call flash("She left it there. Left me there — hand out in the cold like an idiot. I knew better. I always know better. Doesn't stop it from carving something out of me that won't grow back the same.")
            "After a while, quietly, Emy takes her hand back and folds it into her sleeve. Neither of us says the other thing. The night gets longer."

    # The kiss only opens if she held your hand and the night ran warm.
    if "hand_held" in flags and warmth >= KISS_THRESHOLD:
        jump beat_kiss
    jump the_ending


label beat_kiss:
    "Her hand is still warm in mine. Neither of us has let go, and the space between our shoulders has quietly become no space at all. She looks up. The firelight does something to her face the daylight never gets to."
    call flash("She's close. She's so close. Every alarm I own is screaming run, exit, protect it — and underneath all of them, quiet and certain, is the one voice I never let myself hear, saying: stay. Just this once. Stay.")
    "Emy doesn't pull back. She just waits, breath caught, letting me be the one to decide. Trusting me with the deciding — which, from her, is the whole confession."

    menu:
        "Close the distance. Kiss her.":
            $ flags.add("kissed")
            $ warmth += 2
            "I lean in slow, giving her every chance in the world to stop me. She doesn't take a single one. Her mouth is chapped and warm and it trembles, just slightly, like the rest of her has finally caught up to what she wanted all along."
            "It isn't fireworks. It's quieter than that, and better — two people who outlived the end of the world deciding the world isn't over yet. When we part, she keeps her forehead against mine and won't open her eyes."
            e "...Okay. Okay. Wow. Don't let that go to your head."
            k "Way too late."
            call flash("Whole life I waited for the other shoe to drop. Turns out sometimes the thing coming for you in the dark is just someone who loves you, and the only thing she takes is the being-alone. Take it. It's yours. I don't want it back.")
            e "Hey. Kali. ...I'm glad it was you. At the end of the line. Out of the whole ruined world — I'm glad it was you."

        "Stay close — just hold her tonight.":
            $ flags.add("held_close")
            $ warmth += 1
            "I don't close the last inch. Not tonight. Instead I pull her in against me, and her head finds the curve of my neck like it had been hunting for that exact spot for years."
            k "We've got time. I'd rather get this right than get it fast."
            e "...Yeah. Yeah, okay. This. This is good."
            call flash("She didn't push. She never pushes. She just made a place for me and let me be the one to step into it. Whatever this is — I think it's the first thing I've ever been brave enough to want to keep.")

    jump the_ending


# ===========================================================================
#   ENDINGS — five outcomes from warmth + flags
# ===========================================================================
label the_ending:
    python:
        if "kissed" in flags and warmth >= 9:
            ending_key = "radiant"
        elif "kissed" in flags or "held_close" in flags or ("hand_held" in flags and warmth >= 7):
            ending_key = "hopeful"
        elif "hand_none" in flags and "fire_apart" in flags and warmth <= 3:
            ending_key = "severed"
        elif "hand_none" in flags or warmth <= 3:
            ending_key = "distant"
        else:
            ending_key = "bittersweet"
    scene bg station with fade
    jump expression "ending_" + ending_key


label ending_radiant:
    "The World, Beginning Again {i}(radiant){/i}"
    "I don't sleep, and for once I don't want to. She's curled into me, the knife forgotten in her pack for the first time since I've known her, her breath slow and warm against my throat."
    "When the light comes up — gray, then gold, then a gold I've never seen the likes of — she stirs and looks at me like she's checking I'm real, decides that I am, and gives me the smile she's been hiding behind sarcasm since the day we met."
    e "The sea. You wanted to see it. Let's go ruin it by actually looking at the thing."
    "We leave the station hand in hand and we don't look back at the dead clock. Let it stay 11:54 forever; we're not waiting on anything anymore. The last train never came — and thank God it didn't, because we might have climbed aboard, and then we'd never have learned that the end of the line was only ever the beginning of us."
    jump the_end

label ending_hopeful:
    "Morning, and a Direction {i}(hopeful){/i}"
    "The light comes up gray and then, for a moment, gold. I wake with her hand still in mine and her breath against my collar, and for one whole minute I don't reach for a single reason this can't last."
    k "The sea. You never did take me. Let's go find out if the poster lied."
    "She huffs a laugh into my shoulder — and then she nods. The train never came. Walking out into the wet, bright ruin of the morning, I understand we both stopped waiting for it somewhere in the night, and started, instead, going somewhere on purpose. Together. It is not safe. It was never going to be safe. But it's ours now, and we're choosing it with our eyes open."
    jump the_end

label ending_bittersweet:
    "What the Night Held {i}(bittersweet){/i}"
    "I don't sleep, not really. I watch her instead, and the watching feels like a confession my mouth won't agree to make."
    "By morning the words are still behind my teeth, where they live. But she catches my eye on the way out, and there's no blame in it — just that patient, knowing softness of hers, like she's decided to wait for a train she's almost sure will come."
    k "Walk with me a while?"
    e "Yeah. A while."
    "It isn't everything. It isn't nothing. We walk out side by side into the cold, close enough that our shadows touch, and I let that be the truth I can carry today."
    jump the_end

label ending_distant:
    "The Long Way Apart {i}(distant){/i}"
    "Morning finds us on opposite sides of a cold room, exactly as careful as when the night began."
    "She gathers her pack without a word and ties the broken zipper with her bootlace. At the door she pauses, and for a second it looks like she might finally say the thing. She doesn't. I don't either. That was always the easier silence to keep."
    e "Take care of yourself, Kali."
    "\"You too.\" And I mean it — I mean it so much it aches, which is exactly why I can't manage anything else. I watch her go out into the gray. All night I wondered which of us would end up needing the way out. I never once thought it would be her walking through it, and me letting her."
    jump the_end

label ending_severed:
    "Two Roads in the Dark {i}(severed){/i}"
    "We pass the night like two stones in the same cold riverbed — close together, touching nothing."
    "I tell myself I tried. I'm not sure it's true. Somewhere in the dark I stopped reaching, and she let me, because letting people go is the one thing she has truly mastered."
    "By morning she's already at the threshold when I wake — pack on her shoulder, knife back in her hand like the old days never paused."
    e "Easier this way."
    "And maybe she's right. Maybe two people who can't make their mouths say the words are just two more things the world quietly wears down to nothing. She goes one way down the dead track. After a while, I go the other. The station keeps its silence. It has had a great deal of practice."
    jump the_end


label the_end:
    "{i}For someone who makes the dark feel survivable.{/i}"
    return
