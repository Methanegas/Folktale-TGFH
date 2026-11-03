from dataclasses import dataclass, field
import random
import sys
import time


def say(text: str, delay: float = 0.008) -> None:
    if not sys.stdout.isatty():
        print(text)
        return
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def choose(prompt: str, options: list[str]) -> int:
    while True:
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        answer = input("> ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer)
        print(f"Enter a number from 1 to {len(options)}.")


@dataclass
class Pool:
    name: str
    maximum: int
    edge: int = 0
    current: int = 0

    def __post_init__(self):
        self.current = self.maximum

    def spend(self, amount: int) -> bool:
        if amount > self.current:
            return False
        self.current -= amount
        return True


@dataclass
class Character:
    name: str
    might: Pool
    speed: Pool
    intellect: Pool

    def pool(self, name: str) -> Pool:
        return getattr(self, name)

    def show(self):
        print(f"\n{self.name}'s pools")
        for pool in (self.might, self.speed, self.intellect):
            print(f"  {pool.name.title():<9} {pool.current}/{pool.maximum}  Edge {pool.edge}")


@dataclass
class Story:
    berren_trust: bool = False
    field_warning: bool = False
    bramble_bond: bool = False
    helped_harl: bool = False
    helped_elseth: bool = False
    helped_nella: bool = False
    learned_mill: bool = False
    tavin_safe: bool = False
    granary_locust_dead: bool = False
    granary_locust_contained: bool = False
    granary_locust_escaped: bool = False
    berren_safe: bool = False
    bramble_safe: bool = False
    stallholder_safe: bool = False
    villagers_sheltered: bool = False
    villagers_gathered: bool = False
    mill_secured: bool = False
    rear_lane_clear: bool = False
    wounded_moved: bool = False
    lookouts_posted: bool = False
    eastern_lane_blocked: bool = False
    food_diversion: bool = False
    preparation: int = 0
    rescued: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)


def task_check(character: Character, pool_name: str, difficulty: int, task: str) -> bool:
    pool = character.pool(pool_name)
    say(f"\n{task} (Difficulty {difficulty}; target {difficulty * 3} on a d20)")
    max_effort = min(3, difficulty)
    while True:
        raw = input(f"Effort to apply, 0-{max_effort} (or 's' to save effort): ").strip().lower()
        if raw == "s":
            effort = 0
            break
        if raw.isdigit() and 0 <= int(raw) <= max_effort:
            effort = int(raw)
            break
        print(f"Enter a number from 0 to {max_effort}, or 's'.")
    effort_cost = 0 if effort == 0 else 3 + (effort - 1) * 2
    cost = max(0, effort_cost - pool.edge)
    if cost > pool.current:
        say(f"That effort would cost {cost} {pool.name} points, but you have {pool.current}. Choose less effort.")
        return task_check(character, pool_name, difficulty, task)
    if cost:
        say(f"Committing {effort} effort will spend {cost} {pool.name} point(s).")
    if not pool.spend(cost):
        return False
    adjusted = max(0, difficulty - effort)
    roll = random.randint(1, 20)
    if sys.stdout.isatty():
        for _ in range(7):
            sys.stdout.write(f"\rRolling: {random.randint(1, 20):2d}\033[K")
            sys.stdout.flush()
            time.sleep(0.07)
        sys.stdout.write(f"\rRoll: {roll:2d}\033[K\n")
    else:
        print(f"Roll: {roll}")
    success = adjusted == 0 or roll >= adjusted * 3
    if roll == 20:
        success = True
    elif roll == 1:
        success = False
    say(f"You spend {cost} {pool.name} point(s). Target: {adjusted * 3}.")
    say("Success." if success else "The attempt fails, and the situation becomes more dangerous.")
    if roll == 20:
        say("A natural 20 turns the attempt into a decisive success.")
    elif roll == 1:
        say("A natural 1 creates a complication, even if you had reduced the difficulty.")
    return success


def recover(character: Character, amount: int, reason: str) -> None:
    say(f"\n{reason}.")
    for pool in (character.might, character.speed, character.intellect):
        restored = min(amount, pool.maximum - pool.current)
        pool.current += restored
        if restored:
            say(f"You recover {restored} {pool.name} point(s).")


def make_character() -> Character:
    name = input("What is your character's name? ").strip() or "Traveler"
    focus = choose("Choose a starting focus:", [
        "Might: 12 pool, 1 Edge",
        "Speed: 12 pool, 1 Edge",
        "Intellect: 12 pool, 1 Edge",
        "Even spread: 10 in each pool, no Edge",
    ])
    pools = {key: Pool(key, 10) for key in ("might", "speed", "intellect")}
    if focus == 1:
        pools["might"] = Pool("might", 12, 1)
    elif focus == 2:
        pools["speed"] = Pool("speed", 12, 1)
    elif focus == 3:
        pools["intellect"] = Pool("intellect", 12, 1)
    return Character(name, **pools)


def road_to_bellwether(s: Story):
    say("\nSESSION ONE: THE FIRST HARVEST")
    say("You have been hired as the wagon’s sole escort to Bellwether. The cargo is flour, vegetables, and two barrels of ale. Your job is simple: keep the cargo safe, help unload, and return with Mara Venn’s signed receipt.")
    say("The wagon rattles along a dry country road between fields of ripening grain. Each rut makes bottles beneath Berren's seat clink. Behind you, a loose corner of canvas snaps against a barrel. Far ahead, a mill roof rises above the fields.")
    say("Berren shifts on the driver's bench and passes back a small sack of apples.")
    say('"Help yourselves. Those are mine. Everything under the canvas belongs to someone who’ll notice."')
    say('He looks back at the road. "Have you been to Bellwether before?"')

    first = choose("How do you spend the journey?", [
        "Talk with Berren about the job and Bellwether",
        "Ask Berren about himself",
        "Ask Berren what made him hire an escort",
        "Stay quiet and enjoy the view",
    ])

    if first == 1:
        s.berren_trust = True
        say("Berren answers readily, eyes on the road. “Mara runs the mill. Fair woman, but she counts every sack twice.”")
        say("He nods toward the village. “Market day brings farmers in from all over. Harl spends most of it arguing over cart space.”")
        say("“There’s a footbridge behind the mill. I go there when the square gets too loud.” He grins. “Mara will say we’re late. Don’t argue. She says it when I arrive early, too.”")
    elif first == 2:
        s.bramble_bond = True
        say("Berren tells you about his room in the town you departed from and his sister, who keeps urging him to find steadier work.")
        say('"Bramble’s my most reliable colleague. Better company than most people, too."')
        say('"She loves apples, but she’s not a fan of strangers. Try offering her one."')
        say('"Flat hand. She’s gentle, but she’s never understood where the apple ends."')
        say("Bramble accepts an apple from your palm.")
    elif first == 3:
        say("Berren scratches his chin.")
        say('"You’d be surprised how many people think a delivery driver can handle bandits, broken axles, and angry merchants all at once."')
        say('"I hired you because I’d rather arrive with my cargo and my teeth intact."')
        say("He laughs, then checks the wagon straps.")
    else:
        say("Berren lets the road fill the silence. The wagon passes fields ready for harvest, their grain moving in the morning breeze.")

    say("\nA short distance from the village, one of the barrels shifts with a heavy knock. Berren stops the wagon so its securing strap can be tightened.")
    say("Berren checks Bramble’s harness while you tighten the cargo strap.")
    say("As you walk around the wagon, you notice a few crushed grain stalks along the roadside. Farther into the field, a narrow strip of grain leans at an odd angle.")
    say("When you point it out, Berren looks across the field. “The farmer won’t thank whoever did that. Nearly ready to cut.” He is more concerned about the barrel. Once the strap is secure, he climbs back onto the bench.")
    say("The damage could be an animal or someone taking a shortcut. There are no clear tracks in the dry soil")

    say("\nAs the wagon starts moving again, Bramble stops. Her ears turn toward the field. For a moment, you hear only the creak of the wagon and flies around its wheels")
    say("Then something rustles among the crops. Several stalks shake together, farther from the road than a person could comfortably reach. Bramble pulls backward against the harness")
    say("Berren gathers the reins. “Easy. Easy, now.” He assumes a deer or loose dog is hiding in the grain and asks you to walk beside Bramble while he encourages her forward.")
    response = choose("How do you respond to the disturbance?", [
        "Walk beside Bramble to keep watch",
        "Investigate the rustling crops",
        "Ask Berren to hold the wagon while you watch the field",
    ])
    if response == 1:
        say("You walk beside Bramble. She settles, but the crops go still and then rustle again farther out. Nothing comes toward the road")
    elif response == 2:
        s.field_warning = True
        say("You find a narrow passage of flattened stalks leading deeper into the field. Some stems are broken above knee height. No tracks are visible")
        if choose("Do you follow the trail farther?", [
            "Examine the nearby damage, then return",
            "Follow the trail deeper into the field",
        ]) == 1:
            say("The nearby damage offers no further clue, and you return to the wagon")
        else:
            say("The passage joins a broader patch of trampled grain, then becomes difficult to distinguish from other crop damage. Nothing appears")
            say("Berren calls from the road, asking whether you found anything and reminding you that the delivery is waiting")
    else:
        say("Berren holds Bramble steady while you watch the field. The rustling stops. A few stalks sway, but nothing emerges. He urges you back aboard")

    say("\nThe fields give way to kitchen gardens, low fences, and houses with doors standing open to the morning air. At the village entrance, Berren greets an older man repairing a gate")
    say('"Morning, Fen." "Wheel still making that noise?" "Only when it turns." The man laughs and steps aside')
    say("The road opens into Bellwether’s busy market square. The mill stands beside a narrow stream, its wheel clattering steadily. Across from it is a broad granary with a loading beam above its doors")
    say('A flour-covered woman points toward the unloading platform. "You’re late." Berren looks up at the sun. "We’re early." "Then you can help unload."')



def village_arrival(s: Story):
    say("\nMara checks the delivery against her ledger. Flour goes beneath the awning, vegetables by the mill, and the ale stays on the wagon.")
    say("The square is busy with small problems. Harl, the constable, is untangling a cart dispute. Elseth the healer tends a farmworker. Nella is trying to catch a runaway chicken.")

    choice = choose("Before the disturbance, how do you spend your time?", [
        "Help Harl clear a cart passage",
        "Offer the healer a hand with the wounded",
        "Help Nella catch the chicken",
        "Help Mara unload and learn the mill layout",
    ])

    if choice == 1:
        s.helped_harl = True
        s.preparation += 1
        say("Harl is trying to move a handcart out of the market passage while two stallholders argue over whose goods are blocking the way.")
        say("You help shift the cart clear. Harl dusts off his hands and gives you a grateful nod.")
        say('"Harl, constable of Bellwether. Though most days I spend more time moving carts than catching criminals."')
        say('He glances toward the eastern road. "still, a clear passage can matter when trouble comes."')

    elif choice == 2:
        s.helped_elseth = True
        s.preparation += 1
        say("Elseth kneels beside a farmworker whose palm has been cut by a broken crate. She asks you to hold a clean cloth while she washes the wound.")
        say("She works carefully, asking the worker how the injury happened and whether anything else hurts.")
        say('"Thank you. Helping someone stay calm is part of treating them."')
        say("She gathers her bandages and gives you a small, reassuring smile.")

    elif choice == 3:
        s.helped_nella = True
        s.preparation += 1
        say("A chicken darts beneath a market stall, scattering eggshells and sending Nella scrambling after it.")
        say("You help guide it toward its basket. It escapes once more before Nella finally catches it.")
        say('"Duchess is usually much worse," Nella says solemnly. Her father thanks you from the egg stall.')
        say("Nella gives the chicken a stern look, as though this has settled the matter.")

    else:
        s.learned_mill = True
        say("Mara leads you through the mill, pointing out the heavy doors, narrow rear lane, and empty grain carts.")
        say('"Damp comes through those stones. Keep the sacks on the boards, or the grain will spoil."')
        say("She shows you the loading beam and pulley above the granary entrance.")
        say('"Tavin checks the bins and handles the loading gear. That pulley makes moving heavy loads easier."')

    say("\nWhile Mara checks the last of the flour, a farmer approaches with broken grain stalks.")
    say('"Something’s been through the east field. The fence is still standing, but a whole strip of grain is flattened."')
    say("You recognize the damage from the roadside. The farmer worries that more fields may be affected.")
    say('Mara directs him toward Harl. "Tell him where. I’ll come look once this is put away."')
    say("Mara calls for her apprentice, Tavin. There is no answer.")
    say("A worker remembers seeing Tavin enter the granary. Mara sets down her ledger.")
    say('"Would you fetch him? Across the square, side door. Tell him I need those bins checked."')

    if s.berren_trust:
        say("Berren offers to keep an eye on Bramble while you cross the square.")


def granary(s: Story, character: Character):
    say("\nThe granary’s main doors are closed, but the smaller side door stands open. A wooden scoop lies on the threshold, grain scattered into the dirt")
    say("From inside comes a scrape, followed by a soft patter of falling grain")
    say("Above the stacked sacks, Tavin crouches behind the loft edge, clutching a bloodied hand. 'Don’t come in.'")
    say("Tavin presses his injured hand against his chest. His face is pale, and his breathing comes in short bursts")
    say('"I heard something behind the sacks. Thought it was a rat." His eyes flick toward the creature. "Then it stood up."')
    say("He grips the loft beam with his uninjured hand.")
    say('"I pulled the ladder up, but the boards are starting to crack. I can’t stay here."')
    say("A shape shifts below him. It rises until its back strikes a beam. Dust falls from the rafters. Hooked limbs unfold, and its mouthparts click toward the doorway")
    say("This creature followed Tavin inside minutes ago. He escaped into the loft and pulled the ladder up after him. He cannot reach the exit without passing it")
    say("The creature is larger than a man, with a long segmented body, two powerful hind legs, and two pairs of clawed arms. Its head is triangular, with compound eyes and a hinged jaw")
    say("It resembles a locust, but its size and shape are unnatural. It is aware of your presence and moves toward the side door")
    say("You notice that there is a suspended load above the creature, held by a pulley. It could be released to fall on the creature, but timing would be critical.")
    say("Next to you stands a grain cart. It could be pushed into the creature’s path, but it may be heavy and awkward to maneuver.")
    say("You have a heartbeat to study the room. The pulley rope is frayed; the cart's wheel is wedged against a loose board; the narrow aisles offer cover but leave little room to turn.")
    if s.learned_mill:
        say("Mara's earlier explanation of the mill layout helps you recognize the safest path between the sacks.")

    studied = choose("Do you take a moment to read the room?", [
        "Study the creature, pulley, and escape routes",
        "Act immediately before it reaches the door",
    ]) == 1
    if studied:
        say("You notice the locust favors its right side, and the pulley rope is already under strain. Tavin watches for your signal.")
    else:
        say("You move before the creature can close the distance.")

    action = choose("How do you get Tavin out?", [
        "Hold the creature’s attention while Tavin climbs down",
        "Use the storage aisles to get behind it",
        "Release the suspended load from the loft",
        "Push a grain cart into the creature’s path",
        "Call to Tavin and coordinate your escape",
    ])
    if action == 1:
        success = task_check(character, "might", max(1, 3 - int(studied)), "Keep the locust focused on you")
    elif action == 2:
        success = task_check(character, "speed", max(1, 2 - int(studied)), "Reach Tavin through the narrow aisles")
    elif action == 3:
        success = task_check(character, "intellect", max(1, 2 - int(studied)), "Release the loading pulley at the right moment")
    elif action == 4:
        success = task_check(character, "might", max(1, 2 - int(studied)), "Push the heavy grain cart into the locust’s path")
    else:
        success = task_check(character, "intellect", max(1, 2 - int(studied)), "Coordinate Tavin’s escape while distracting the creature")

    s.tavin_safe = True
    s.rescued.append("Tavin")
    if success:
        success_outcomes = [
            "You hold the locust's attention while Tavin climbs down. He reaches the door before the creature lunges after him and bursts into the square.",
            "You slip through the narrow aisles and reach Tavin from behind. Together you get clear; the locust turns and scrambles out through the side door.",
            "You release the pulley at just the right moment. The suspended load crashes onto the locust, pinning it beneath the sacks.",
            "You shove the grain cart into the locust's path. It slams into the cart and collapses beneath the impact, leaving the way clear for Tavin.",
            "You call out a careful sequence of moves. Tavin climbs down as you draw the creature toward the doorway, and you both escape into the square.",
        ]
        say(success_outcomes[action - 1])
        if action == 3:
            s.granary_locust_contained = True
        elif action == 4:
            s.granary_locust_dead = True
        else:
            s.granary_locust_escaped = True
    else:
        s.granary_locust_escaped = True
        failure_outcomes = [
            "The locust ignores your attempt to draw it away. Tavin drops from the loft and lands hard, but you pull him through the door as the creature escapes into the square.",
            "A sack shifts underfoot and blocks the aisle. Tavin gets down another way, but the locust slips past you and escapes through the side door.",
            "The pulley catches, then releases too late. Tavin scrambles down while the locust darts past the falling load and escapes into the square.",
            "The cart lurches but stops short of the locust. Tavin reaches the floor and you both get clear as the creature escapes through the side door.",
            "The creature moves before Tavin can follow the plan. He drops from the loft, and you get him out as the locust slips past and escapes into the square.",
        ]
        say(failure_outcomes[action - 1])
    if success:
        say('Outside, Tavin catches his breath, keeping his injured hand close. "Mara told me to check the bins before market. I thought I had time."')
    else:
        say('Outside, Tavin catches his breath, pale and shaken. The rough escape has worsened his injuries; Elseth will need to treat him before he can help again.')
    character.show()
    recover(character, 2, "The square gives you a brief moment to breathe")


def market_attack(s: Story, character: Character):
    say("\nA crash comes from the square. Berren shouts. Bramble screams as one of the creatures clings to the wagon. Across the market, another steps between stalls and pursues fleeing villagers")
    say("A market stall collapses beneath the creature’s weight")
    say("People abandon baskets and handcarts. Someone cries for a child who has been separated from their family")
    if s.field_warning:
        say("The damaged fields you noticed now make terrible sense. You recognize the direction the creatures came from.")
    if s.granary_locust_dead:
        say("The creature you killed in the granary is absent from the attack; your earlier success has bought the square a little time.")
    elif s.granary_locust_contained:
        say("The granary locust remains pinned beneath the suspended load. It has not joined the attack, though the sacks may not hold forever.")
    say("Harl arrives with three villagers carrying farm tools. He looks toward you, uncertain where to begin")
    if s.granary_locust_escaped:
        say("The wounded granary locust also emerges into the square. Three creatures are now loose among the market stalls")
    say("Berren has fallen, his ankle tangled in a rein. A stallholder is pinned beneath an overturned table. Mara opens the mill to shelter the crowd, but its broad doors must be secured")
    say("You have only moments to act.")

    priority = choose("Where do you act first?", [
        "Free Berren and Bramble from the wagon",
        "Get the pinned stallholder out of the locust’s path",
        "Help Mara shut and brace the mill doors",
    ])
    if priority == 1:
        difficulty = 1 if s.bramble_bond else 2
        if s.berren_trust:
            say("Berren recognizes your voice and follows your instructions without hesitation.")
            difficulty = max(1, difficulty - 1)
        elif s.bramble_bond:
            say("Bramble remembers your offered apple and lets you approach.")
        success = task_check(character, "speed", difficulty, "Free Berren and calm Bramble")
        s.berren_safe = s.bramble_safe = True
        s.rescued.extend(["Berren", "Bramble"])
        say("You cut the rein and pull them clear. " + ("Berren gets up, shaken but able to walk." if success else "The wagon is struck and its cargo scatters, but both are safe."))
    elif priority == 2:
        success = task_check(character, "might", 2, "Lift the overturned market table")
        s.stallholder_safe = True
        s.rescued.append("the stallholder")
        say("You drag the stallholder clear just in time. " + ("Harl guides them toward the mill." if success else "They are hurt, but alive; Elseth begins treating them at once."))
    else:
        success = task_check(character, "might", 2, "Brace the mill doors against the attack")
        s.mill_secured = success
        s.villagers_sheltered = success
        if success:
            say("Mara and Harl pull the heavy doors shut. The first villagers are safe inside")
        else:
            say("The doors hold for now, but the brace slips. Mara keeps people moving while Harl calls for help")
            s.preparation += 1

    if not s.berren_safe:
        say("Berren and Bramble remain in danger beside the wagon")
    if not s.stallholder_safe:
        say("The pinned stallholder remains exposed in the square")
    say("For a few breaths, the square is almost still. A broken wheel creaks. Elseth kneels beside the injured, and the rescued stallholder clutches your sleeve before being led away.")
    say("Then Harl gathers three villagers with farm tools. Elseth treats the wounded. Mara looks toward the fields as more shapes move beyond the last houses")
    if s.berren_safe:
        say("Berren struggles to his feet and begins helping people move away from the wagon")
    if s.stallholder_safe:
        say("The stallholder is carried toward Elseth, who immediately begins treating their injuries")
    if s.mill_secured:
        say("Mara calls from inside the mill, directing villagers toward shelter")
    if s.tavin_safe:
        say("Tavin, despite his injured hand, helps guide people toward the mill")
    say("Harl turns toward you. 'Tell me where you need us. We can’t save everyone if we scatter.'")
    character.show()
    recover(character, 2, "The villagers organize around you")


def preparations(s: Story, character: Character):
    say("\nThe chapel bell begins ringing. A villager at an upper window sees several tall shapes moving beyond the last houses. More appear behind them. The swarm is approaching; Bellwether has minutes to prepare")
    if s.field_warning:
        say("Because you noticed the damaged grain earlier, Harl’s lookouts were already watching the eastern fields")
        s.preparation += 1
    if s.helped_harl:
        say("Harl remembers your help and immediately puts you in charge of coordinating the volunteers")
    if s.helped_elseth:
        say("Elseth asks you to help move the wounded you treated earlier")
    if s.helped_nella:
        say("Nella and her father are already together and ready to follow instructions")
    say("Choose two different preparations")
    prep_options = [
        ("Block the eastern lane", "might", 2, "Build a barricade from carts and timber"),
        ("Clear the mill’s rear lane", "speed", 1, "Open a route to the footbridge"),
        ("Gather villagers early", "intellect", 2, "Organize the market crowd into groups"),
        ("Move the wounded", "might", 2, "Carry the injured into shelter"),
        ("Prepare a food diversion", "intellect", 3, "Set supplies to draw the swarm away"),
        ("Post lookouts", "intellect", 1, "Spot the swarm’s approach routes"),
    ]
    picked = set()
    for _ in range(2):
        available = [item for i, item in enumerate(prep_options) if i not in picked]
        index = choose("Choose a preparation:", [item[0] for item in available]) - 1
        item = available[index]
        picked.add(prep_options.index(item))
        label, pool, difficulty, task = item
        success = task_check(character, pool, difficulty, task)
        s.preparation += 2 if success else 1
        if label == "Block the eastern lane":
            s.eastern_lane_blocked = success
        elif label == "Clear the mill’s rear lane":
            s.rear_lane_clear = success
        elif label == "Gather villagers early":
            s.villagers_gathered = success
        elif label == "Move the wounded":
            s.wounded_moved = success
        elif label == "Prepare a food diversion":
            s.food_diversion = success
        elif label == "Post lookouts":
            s.lookouts_posted = success
        if not success:
            failure_text = {
                "Clear the mill’s rear lane": "The rear lane remains cluttered; the footbridge route will be harder to use.",
                "Gather villagers early": "The crowd is still disorganized, and some villagers may be slow to reach shelter.",
                "Move the wounded": "The wounded remain where they are; Elseth will have to move them during the attack.",
                "Post lookouts": "The lookout posts are not established, leaving the approach less well watched.",
                "Block the eastern lane": "The eastern lane remains open.",
                "Prepare a food diversion": "The supplies are not arranged well enough to draw the swarm.",
            }
            say(failure_text[label])

    if s.berren_safe and s.bramble_safe:
        say("Berren helps move supplies and keeps Bramble close to the mill")
    if s.tavin_safe:
        say("Tavin carries messages between Mara and Harl despite his bandaged hand")
    say("Harl gathers the volunteers while Mara checks the remaining supplies")
    if s.eastern_lane_blocked:
        say("The eastern lane is blocked with carts and timber. The barricade should slow anything approaching from the fields")
    if s.rear_lane_clear:
        say("The rear lane behind the mill is clear. The footbridge offers a possible escape route")
    if s.wounded_moved:
        say("The wounded have been moved into shelter. Elseth checks their bandages before preparing to move again")
    if s.lookouts_posted:
        say("Lookouts take positions near the chapel and the eastern road")
    if s.food_diversion:
        say("The food diversion is ready. Supplies have been placed away from the main shelter")
    if s.villagers_sheltered:
        say("Several families are already inside the mill, waiting for instructions")
    elif s.villagers_gathered:
        say("The villagers are organized into groups and ready to move when called")
    say("The preparations are " + ("organized, with routes and shelter ready." if s.preparation >= 5 else "hurried; some routes remain exposed."))
    say("The chapel bell begins to ring. Beyond the last houses, the fields are moving")


def final_swarm(s: Story, character: Character):
    say("\nEight locusts break from the fields and rush Bellwether. Two have doubled bodies and strike with twice the force. One is missing its arms, but barrels through fences on powerful legs")
    say("The market fills with dust and shouting. Harl calls for the villagers to move. Mara waits at the mill entrance; the footbridge lies behind it, across the stream")

    route = choose("Where do you lead the villagers?", [
        "Withdraw across the stream and regroup beyond the village",
        "Hold the mill as a refuge while villagers get inside",
    ])
    if route == 1:
        difficulty = 2
        if s.rear_lane_clear:
            difficulty -= 1
        if s.lookouts_posted:
            difficulty -= 1
        if s.villagers_gathered:
            difficulty -= 1
        difficulty = max(1, difficulty)
        if s.berren_trust:
            say("Berren remembers the footbridge he mentioned on the road and guides people toward it")
        if s.rear_lane_clear:
            say("The cleared rear lane gives the survivors a direct route to the footbridge")
        if s.lookouts_posted:
            say("The lookouts warn you before a locust reaches the lane")
        success = task_check(character, "speed", difficulty, "Lead the survivors across the footbridge")
        say("The first group reaches the far bank. Behind you, a locust crashes through the market stalls and turns toward the bridge" if success else "The retreat bunches at the narrow crossing. Supplies are lost, and several villagers stumble, but everyone keeps moving")
        second = choose("The bridge is becoming crowded. What do you do?", [
            "Hold the near end while the last villagers cross",
            "Use a distraction to draw the locust away",
        ])
        if second == 1:
            hold_difficulty = 1 if s.lookouts_posted else 2
            held = task_check(character, "might", hold_difficulty, "Hold the bridge approach long enough for the last villagers")
            say("You brace at the bridge entrance. " + ("The last villagers cross, and you follow just before the locust reaches you." if held else "You give ground step by step. The last villagers cross, though the creature tears through the railing behind you."))
        else:
            difficulty = 1 if s.food_diversion else 3
            distracted = task_check(character, "intellect", difficulty, "Create a diversion at the bridge")
            say("The diversion " + ("pulls the locust away long enough for everyone to cross." if distracted else "fails to hold its attention. You abandon the supplies and sprint across with the others."))
    else:
        difficulty = 3
        if s.eastern_lane_blocked:
            difficulty -= 1
        if s.wounded_moved or s.villagers_gathered:
            difficulty -= 1
        difficulty = max(1, difficulty)
        if s.eastern_lane_blocked:
            say("The eastern barricade diverts part of the swarm away from the mill entrance")
        if s.wounded_moved:
            say("The wounded are already inside and out of the immediate path")
        success = task_check(character, "might", difficulty, "Hold the mill doors while villagers take shelter")
        if success:
            s.mill_secured = True
            s.villagers_sheltered = True
            say("The doors slam shut. Villagers brace them from inside as the swarm passes through the square")
        else:
            say("The doors buckle. You pull people back toward the rear lane as locusts strike the entrance")
            if s.rear_lane_clear or s.villagers_sheltered:
                say("Earlier preparations keep the wounded and stragglers from being cut off")
            else:
                say("The retreat is confused; Harl and Mara shout names, trying to account for everyone")
        second = choose("A locust reaches the mill's side entrance. How do you respond?", [
            "Shove a cart across the entrance",
            "Lead the remaining villagers through the rear lane",
        ])
        if second == 1:
            blocked = task_check(character, "might", 2, "Block the side entrance with a cart")
            say("The cart " + ("holds long enough for the doors to be secured." if blocked else "slows the creature, but splinters under its impact. You retreat with the others."))
            s.mill_secured = s.mill_secured or blocked
        else:
            escaped = task_check(character, "speed", 2 if s.rear_lane_clear else 3, "Guide the remaining villagers through the rear lane")
            say("You " + ("get the stragglers out before the locust reaches them." if escaped else "get most of the stragglers out, though the swarm scatters the group beyond the mill."))

    if s.food_diversion:
        say("The prepared food diversion draws several locusts away for a few precious moments")
    say("\nSESSION END")
    known_safe = list(dict.fromkeys(s.rescued))
    if s.villagers_sheltered and s.mill_secured:
        known_safe.append("villagers sheltered in the mill")
    elif s.rear_lane_clear:
        known_safe.append("villagers who reached the footbridge")
    say("Known safe: " + (", ".join(known_safe) if known_safe else "no one is confirmed safe yet"))
    say("Other villagers: their fates are uncertain in the confusion")
    say("Berren survives, clutching the torn delivery receipt" if s.berren_safe else "Berren’s fate is uncertain in the confusion")
    say("Bramble is safe with you and the other survivors" if s.bramble_safe else "Bramble’s fate is uncertain in the confusion")
    say("Tavin is alive and out of the granary" if s.tavin_safe else "Tavin’s fate is uncertain")
    if s.mill_secured:
        say("The mill remains a defensible refuge")
    say("\nThe village falls quiet behind you")
    if s.mill_secured and s.villagers_sheltered:
        say("The mill remains standing. Survivors gather inside, exhausted but alive")
        say("Mara begins counting the missing while Harl organizes the remaining defenders")
    elif s.rear_lane_clear:
        say("The survivors have reached the footbridge. Bellwether lies behind them, lost in dust and movement")
        if s.berren_safe:
            say("Berren looks back toward the mill. 'We can’t leave them there forever.'")
    else:
        say("The survivors scatter beyond the village. Nobody knows how many made it out")
        say("The distant cries from Bellwether slowly fade")
    if s.tavin_safe:
        say("Tavin sits beside Elseth, his injured hand wrapped in clean cloth")
        say('"I thought I had time," he whispers')
    if s.berren_safe:
        say("Berren folds the torn delivery receipt and puts it away")
        say('"I suppose we won’t be collecting payment today."')
    say("The road ahead is uncertain. Somewhere beyond the fields, the swarm continues to gather")
    character.show()


def play():
    print("THE GOSPEL FOR HUNGER")
    say("Story by Violet K")
    say("A delivery to Bellwether should be an ordinary day’s work")
    character = make_character()
    story = Story()
    road_to_bellwether(story)
    village_arrival(story)
    granary(story, character)
    market_attack(story, character)
    preparations(story, character)
    final_swarm(story, character)

if __name__ == "__main__":
    play()
