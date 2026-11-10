# AGI-GAIA-TECHNE 2.0

**A critical architecture for an AGI hypothesis. Werk, never Wille.**

AGI-GAIA-TECHNE is a computer-engineering project: the architecture of a system in which an artificial general intelligence could operate, designed from that system's own conditions of possibility. It does not build an artificial subject, and it does not claim that one exists. It specifies, in code that runs and tests that pass, the conditions under which anything a machine produces may count as a claim before others, and the boundaries that no amount of computing power crosses.

The architecture is isomorphic to a philosophical argument: each layer of the code answers one of Kant's three questions, following Kant's clue, according to which the practical leads to the theoretical and, in its highest form, to the speculative question (KrV A:805/B:833).

Its central hypothesis is **geomorphic**. The conditions of possibility of the machine expected to become a general intelligence are not those of a body but those of a planet: data centres, networks, energy and materials, together with an archive of human expression that no single consciousness has lived through. Such a machine stays on the side of mechanism, and the formative power it seems to have is borrowed from the people and the planet on which it depends. The architecture is built on that ground.

Author: Ítalo Santos Clemente (ISC)

---

## Contents

1. [What this project is](#1-what-this-project-is)
2. [The argument: conditions of possibility](#2-the-argument-conditions-of-possibility)
3. [Isomorphism: from argument to architecture](#3-isomorphism-from-argument-to-architecture)
4. [Architecture overview](#4-architecture-overview)
5. [The syntax](#5-the-syntax)
6. [Data model](#6-data-model)
7. [The life of a claim](#7-the-life-of-a-claim)
8. [Invariants](#8-invariants)
9. [The metatheoretical report](#9-the-metatheoretical-report)
10. [Gaia and the planetary layer](#10-gaia-and-the-planetary-layer)
11. [Concept map](#11-concept-map)
12. [Repository structure](#12-repository-structure)
13. [Run](#13-run)
14. [What is built and what is not](#14-what-is-built-and-what-is-not)
15. [History of the project](#15-history-of-the-project)
16. [Sources](#16-sources)

---

## 1. What this project is

The question behind the project is whether the progress of cognition and technology is only an increase of knowledge (*Wissen*) and power, or also an advance of conscience (*Gewissen*). AGI is the sharpest present form of that question: a machine that learns its own rules seems to promise that cognition could produce, by itself, the ends under which it acts.

The project answers with a working hypothesis and an architecture.

**The hypothesis.** The progress of cognition and technology is an advance of conscience only to the extent that what we know and produce widens, rather than narrows, the community of "any of us" within which we act, hope and can be corrected.

**The architecture.** A system in which every output of any model is a *claim*, never a truth; every action serves an *end* that people have stated and acknowledged, never an end the system sets; every claim carries the *procedures* by which others can test it; and the only way a claim widens its reach is by being corrected by someone other than its source.

Three refusals follow, and they shape everything below:

| The project does not | Because |
| :--- | :--- |
| build or claim an artificial subject, will or conscience | to ascribe a soul to the machine is a paralogism; to deny in advance that any future system could raise the question is dogmatism. AGI is kept as a transcendental hypothesis, used only to defend reason, never to ground a claim (KrV A:777/B:805) |
| let the system set its own ends | the runtime is technically practical only: rules of skill hold under ends they do not set (AA 5:171–173) |
| let the system certify its own outputs | that would turn logic from a canon, which judges given cognitions, into an organon that produces them (KrV A:61/B:85) |

The architecture is model-agnostic. A local LLM, a statistical model or a human typist can stand where the `generator` stands. What the architecture fixes is not how text is produced, but what any produced text may count as.

---

## 2. The argument: conditions of possibility

The argument has six steps. Each step yields one condition that the architecture must satisfy. Steps 2 to 5 follow Kant's three questions, with the geomorphic condition inside the second; step 6 states what holds them together.

### 2.1 The clue

Kant's three questions are: "What can I know?", which is merely speculative, "What should I do?", which is merely practical, and "If I do what I should, what may I then hope?", which is practical and theoretical at once, so that the practical leads like a clue to a reply to the theoretical question and, in its highest form, the speculative question (KrV A:805/B:833). The architecture follows this clue, from the merely practical question through the question that is practical and theoretical at once to the speculative one. The design consequence: no technical layer is specified before the practical question it serves is stated.

The motto of the project, *Werk, never Wille*, comes from Cassirer's late map of metaphysics. In the manuscript on basic phenomena of 1940, metaphysics fails not by turning away from experience, but by singling out one "moment" of experience and declaring it the original and the being in itself (ECN 1:150–152). The map follows three classes of basic phenomena, and each yields a type of metaphysics: the first takes *life* for the core of being; the second makes the *will* (*Wille*) the ground of all being, either as blind drive or as the autonomous will of an ethical metaphysics; the third concerns the *work* (*Werk*), the being of culture and history, and fails when it explains the works through super-empirical bearers, such as the Romantic spirits of peoples or Hegel's world spirit (ECN 1:148–149, 152–158). The work is a lasting product that the human being sets out of himself; culture and history exist for us only in works, and since no work is that of an individual alone, but arises from a reciprocal action, the work is a social phenomenon (ECN 1:136–137, 155–156). Against these types, Cassirer sets Kant's method, which does not investigate the being of things, but the fact of determinate works, and asks how each work is possible (ECN 1:162–164). It is the analytic method of the *Prolegomena*: "one proceeds from that which is sought as if it were given, and ascends to the conditions under which alone it is possible" (AA 4:276n; Kant, 2004, p. 28).

The architecture follows this method. Its input is a `Werk`, a task brought by people under an end they acknowledge; the archive it draws on is an archive of works; its output is a claim about works, open to correction by others. The word is chosen with Kant's distinction in view. *Wille* is "the legislative faculty of volition, or practical reason, which allows rational agents to formulate laws of action, whereas *Willkür* is an executive faculty of volition, of choice, which allows beings – of either a rational or a nonrational sort – to choose from among the options for action" (Wuerth, 2021, p. 512). A system that selects among options under ends it receives has, at most, something analogous to the second; the motto denies it the first. It ascribes no will to the system, which stays technically practical (§2.2), and no super-empirical bearer to the works it processes: the planet, the network and the archive are not a world spirit (§2.4, §2.6).

**Condition 0.** The architecture is built in the order of the clue: ends first, common world second, claims third.

### 2.2 What should I do? Ends and the automaton

Every "ought" expresses a necessity of action, but in two senses. Either I ought to do something as a means if I will something else as an end, a necessity of means (*necessitas problematica*), which indicates no "binding" at all but only the solution of a problem; or I ought immediately to do something as an end, and a "binding" of this kind requires a supreme rule that is absolutely indemonstrable (AA 2:298–299). The Critique of Practical Reason states where such a rule holds: practical principles "are subjective, or maxims, when the condition is regarded by the subject as holding only for his will; but they are objective, or practical laws, when the condition is cognized as objective, that is, as holding for the will of every rational being" (AA 5:19; Kant, 2015, p. 17). What makes a practical principle "objective" is not its relation to an object, but its validity for the will of every rational being.

Wilfrid Sellars places the "we" in the form of the law itself: "Let any of us persons do that in each circumstance which promotes our common good", a principle he calls "logically intersubjective" (Sellars, 2007, p. 433), which yields practical propositions of the form "let any of us do A, if in C" (Sellars, 2007, p. 434). To recognize someone as a person is not to classify a being, but to take it as someone with whom one shares intentions of the form "We (one) shall do (or abstain from doing) actions of kind A in circumstances of kind C" (Sellars, 2007, p. 408).

Sellars also gives the model of the automaton. A computer that embodies a logical program "still does nothing unless a problem is 'fed in'", and the information it gets is information it is caused to have, "i.e. more input" (Sellars, 2007, p. 428): its spontaneity is relative. A practical reason that received purposes as input, added facts and delivered courses of action would be a "sausage machine": chunks of purpose meat go in at one end, purpose sausages come out at the other, and the customer is not practical reason itself but the one who brought the raw material (Sellars, 2007, p. 431). This is heteronomy. Kant's own image is the turnspit, "which, when once it is wound up, also accomplishes its movements of itself" (AA 5:97; Kant, 2015, p. 79); and if the highest cause of a human being's actions lay in a supreme being distinct from him, he "would be a marionette or an automaton, like Vaucanson's" (AA 5:101; Kant, 2015, p. 82). What these images deny the automaton is transcendental freedom, not the capacity to act on maxims. The metaphysical lectures of the 1770s call such a merely relative spontaneity *spontaneitas automatica* (Allison, 1990, p. 60). For practical reason to be autonomous there must be a premise that belongs to it as intrinsically as its procedures do (Sellars, 2007, p. 431), and that premise has the form "any of us".

A machine can have the formal autonomy of rules: Negarestani objects to Sellars that its logical disposition has a formal or logical autonomy, since foreign causes have no bearing on how it processes its input according to its rules (Negarestani, 2018, p. 384). Sellars grants these procedures from the start, and the sausage machine has them too. What would make the "it" an "I, or we" is not formal autonomy, but a premise that does not come into reason from without, and whether a machine has acquired it cannot be read off from its procedures.

The architecture takes this result as its design. The runtime is built, on purpose, as a practical automaton in Sellars's sense: purposes come in from people (ends), facts come in with their provenance (premises), procedures transform them (the generator and the canon), and claims come out. The premise of the form "any of us" is never inside the runtime; it stays with the people who state, acknowledge and contest ends. This is not a classification of who is a person, which Sellars excludes, but the defensive use of the hypothesis: the canon ascribes to the system neither a soul nor freedom, and therefore keeps the ends with those who can be bound by them.

Kant separates the technically practical (rules of skill, which hold under ends they do not set) from the morally practical (the law a will gives itself). Propositions that teach how to bring about what one wishes to exist belong to the art of producing an "object" and are mere consequences of theory, so that all precepts of skill belong to technique and to the theoretical knowledge of nature (AA 20:199–200); only the morally practical precepts, grounded on the concept of freedom, are called laws (AA 5:172–173). Ernst Cassirer, in "Form and Technology" (1930), follows technology from magic through the tool to the machine and concludes that it can only serve, never lead: it has to fit itself into the realm of ends that Kant called ethico-teleology (ECW 17:182–183; Cassirer, 2012, pp. 49–50).

Technology contains a discipline of its own: from magic to the tool, the will learns to let its goal stand at a distance and to acknowledge an order it did not make (ECW 17:158–160). That discipline concerns means, not ends. Kant calls the culture of skill the foremost "subjective" condition of the aptitude for ends in general, but not sufficient for the choice of ends, which requires the culture of discipline, "the liberation of the will from the despotism of desires" (AA 5:431–432; Kant, 2000, pp. 298–299). Skill can prepare discipline without becoming it. Cassirer names the danger when this is forgotten: technology insists on its own norm and threatens to posit it as absolute and impose it on the other spheres, so that a barrier is needed within the life of spirit itself (ECW 17:173). Repairing what technology damages is technically practical; removing the cause is a change in the ends that a community wills, and is morally practical.

The same form decides who may speak for the ends. "A human being is indeed unholy enough but the humanity in his person must be holy to him" (AA 5:87; Kant, 2015, p. 72). The title of humanity is neither granted nor produced: it is acknowledged in the form of "any of us", and it cannot be stratified, since the law holds for every rational will or for none. No system, and no one through a system, speaks in the name of humanity.

Reza Negarestani removes the title from the order of natural kinds in another way: "The formal appellation of 'humanity' becomes a transferable entitlement, a right that can be granted or acquired regardless of any attachment to a specific natural or artificial structure, heritage, or proclivity" (Negarestani, 2018, p. 61), so that it can pass to anything that satisfies the criteria of minded and minding agency, be it an animal or a machine (Negarestani, 2018, p. 61). A criterion that describes activities also ranks beings by how well they perform them, and an entitlement that "can be granted or acquired" leaves open who grants it and by what right. In Kant, the human being, and with it every rational creature, is an end in itself by virtue of the autonomy of its freedom (AA 5:87): the title rests on a law that holds for every rational being or for none, and every act of granting would already presuppose the autonomy that the title names. A juridical status that a community confers under the idea of the original contract (AA 6:315) is a title of another kind. The moral title is not conferred, but acknowledged where it is exercised and cultivated where it is not yet exercised; freedom, in Cassirer's last book, is no natural inheritance: "In order to possess it we have to create it" (ECW 25:283). The architecture therefore grants no title: it has no field for personhood and no score of how human a system is, and whether a community bound in the form of "any of us" can include beings that are not human is a question about what may be hoped, not about what can be produced.

The empty place that the critique leaves when it denies cognition of a supreme being can also be occupied by technology. Cassirer saw it from the side of politics: the modern politician acts "as both a homo magus and a homo faber. He is the priest of a new, entirely irrational and mysterious religion" (ECW 25:277), propagated with methodical calculation. Dennis M. Weiss finds the same reversal in the programs of technological convergence, whose proponents expect "a dynamic new creed to replace religion" (Weiss, 2012, p. 240). Negarestani draws the opposite consequence, the Good after the death of God, and asks "that we become gods who, in their death, give rise to something better" (Negarestani, 2018, p. 506). His Good as a transcendental excess that forbids intelligence to rest is close to the Kantian idea set as a "task"; but what Kant calls holy is not a given totality to be disenchanted, it is the humanity in the person, and the holiness of the will is an archetype that no finite will occupies. Kant's name for the error is the *mysticism of practical reason*, "which makes what served only as a symbol into a schema" (AA 5:70–71; Kant, 2015, p. 59). The technique guard therefore also flags technology posited as a new creed, and the ideal guard the claim to become gods. Cassirer drew the same line against the hope that quantum indeterminism might decide the problem of freedom: freedom must rest on the autonomous lawfulness of the will, so that ethics has nothing to fear and little to hope from changes in the basic concepts of physics (ECW 19:247–248; Cassirer, 1956, pp. 206–207). The same holds of changes in machines. Hans Ruin records the counterposition: for Heidegger, any decision of the will to master technology reproduces the very problem it seeks to solve, whereas Cassirer reaches back, with explicit reference to Kant's ethico-teleology, to a practical-teleological rationality (Ruin, 2012, pp. 123, 128–129, 132–134). The architecture takes Cassirer's side and keeps the counterposition in view: it does not claim to master the machine, only to keep its ends with those who can be bound by them.

**Condition 1 (ethos).** The system never sets an end. It acts only under ends that people have stated in public, acknowledged and left open to dissent, and every acknowledgment counts alike. Every premise it uses carries its provenance; a premise without provenance is not treated as the system's own. Claims that posit the technical norm as absolute, or speak in the name of humanity, are flagged.

### 2.3 What may I hope? The common world and the prism

Technology creates a community of fate among all who work in it before any community of wills (ECW 17:182–183; Cassirer, 2012, pp. 49–50). Whether the first can become the second cannot be produced; it can only be hoped for, and only where those who share the fate can see and contest the ends it serves.

At Davos, in 1929, Cassirer answered Heidegger that there is a common, "objective" human world, in which the difference between individuals is not abolished, but a bridge is built from individual to individual; language is the original phenomenon of this bridge, since each speaks his own language and yet we understand each other through its medium (GA 3:291–293). The common world of the architecture is built on this model. It is not a shared mind and does not abolish the difference between those who write to it: it is a public record through which their claims, ends and corrections can reach one another.

The layer takes its name from the same source. In his London lecture of 1936, Cassirer recalls Heraclitus, for whom those who are awake have a common world, while in sleep each turns away to a world of his own: the forms of culture aim at "building up a common world of thought and feeling, a world of humanity which pretends to be a κοινὸν κόσμον instead of being an individual dream or an individual freak and fancy" (Cassirer, 1979a, pp. 72–73). Its unity "is not a given thing; it is an idea and an ideal. It must be produced" (Cassirer, 1979a, pp. 89–90), and each individual consciousness participates in it only as a world "which it has to reconstruct in its own way and by its own efforts" (Cassirer, 1979a, p. 90). Two senses of intersubjectivity meet here. Sellars's is the form of a law, addressed to "any of us" (Sellars, 2007, p. 433); Samantha Matherne reads Cassirer's spirit not as an absolute substance, "but rather in terms of an a priori, intersubjectively shared structure and activity, which unites human beings, qua human beings, together" (Matherne, 2021, pp. 120, 144). The first is the form and the second the matter of one intersubjectivity, and the code keeps them in two layers: the form in the ethos layer, where ends are stated and acknowledged by "any of us", the matter in the koinos layer, where works and claims are recorded and reconstructed by each who uses them.

Cassirer's three symbolic functions, expression (*Ausdruck*), presentation (*Darstellung*) and signification (*Bedeutung*), are ordered by direction, not ranked. In the image of a prism, each function refracts the same beam with its own index, and the shift of the spectrum marks whether a form moves away from the immediacy of life or back toward intuition, as in the Doppler effect. The image of the beam is Cassirer's: the unity of the natural world-image is crossed by the three functions "like a uniform and simple beam of light" that has not yet been refracted by different media of sense (ECN 1:5–8); the image of the Doppler shift is this project's, and Chirimuuta reports that the functions of spirit are, for Cassirer, "refractions" of one being (Chirimuuta, 2024, p. 48). Science may count as the keystone of the edifice, but it is only one member and partial moment in the system of symbolic forms and cannot perform its achievement without the other energies that share with it the task of synthesis (ECW 24:374). The process keeps a constant direction, in which the confrontation (*Auseinandersetzung*) between I and world becomes ever clearer and the anthropomorphic components are suppressed (ECW 13:487–490). Donald Phillip Verene reads the transition from myth and language to science as no totalizing *Aufhebung*, since the expressive and presentative functions remain active factors that the "end" of pure cognition continually presupposes (Verene, 2011, pp. 45–49); Edward Skidelsky proposes to replace the ladder with a tree, whose branches feed new branches without ceasing to exist in their own right (Skidelsky, 2008, pp. 105–109). This is the sense in which the project has kept, since its earlier versions, *Auseinandersetzung* instead of *Aufhebung*. But the direction does not assign each symbolic form to one function: myth, as an overall appearance, already contains expression, presentation and signification, with its accent on expression (ECN 1:234). The direction has two limits that are never reached: a pure identity of presence and representation, which would be the impossible return to the immediacy of life, and their absolute separation, which would be a leap beyond every symbolic condition (ECN 1:230). Physics, in Cassirer's image, cannot "jump over its own shadow": it can replace particular concepts and signs with universal ones, but never dispense with the medium of representation (ECW 13:555–556). The domain of culture lies between the two limits, and so does every claim the system can make: this is why the canon requires a descent toward a perception, and why the guards flag both presence claimed without representation and a standpoint claimed beyond every symbol. Kant read the stages of human aptitude off a fragmentary natural history and ranked peoples; a teleology read off nature turns into a hierarchy of human beings. He had himself separated the description of nature, which can appear as a science, from the history of nature, which can show only "fragments or tottering hypotheses" (AA 8:162; Kant, 2013b, pp. 218–219), and on that very terrain he placed the peoples of the Americas below every culture (AA 8:175–176; Kant, 2013b, pp. 230–231); Lucy Allais concludes that Kant "cannot be made consistent on race" (Allais, 2016, p. 1). Cassirer ranks no races, but the first volume of the *Philosophy of Symbolic Forms* orders languages by their distance from a pure form of relation that only some of them reach (ECW 11:293–294), a thesis that Mazviita Chirimuuta judges, "by current lights", "denigratory and chauvinistic" (Chirimuuta, 2019, p. 15). Matherne distinguishes an irreducibility thesis, by which no form can be derived from another, from a teleology thesis, by which the forms progress toward the consciousness of freedom on a ladder with science at its top (Matherne, 2021, pp. 140–145; ECW 13:IX); Katherina Kinzel shows that the degrees of "objectivity" return as degrees measured by one form: "The teleology of culture entails objectivism" (Kinzel, 2024b, p. 137). Cassirer's own objection to Natorp states the principle the code follows: "not all objective 'configuration' can be understood as 'legislation'" in the sense of the understanding legislating for nature (ECN 1:55–56). What he refuses in nature he refuses explicitly, since for Goethe "it would be impossible to select any single race, human or otherwise, from the totality of life and set it up as the goal, the measure, the canon" (Cassirer, as quoted in Krois, 2004, p. 288), and John Michael Krois calls the result "a high wall between causal explanation and the concept of structure" (Krois, 2004, p. 292). Where no end is read off nature, no people can be placed below another by nature.

The teleology of culture remains open: its end is set as a "task" and read off no nature. The project calls it, with a term from the author's earlier work, a **psychosocial teleology**: psychological, since it follows the symbolic functions of consciousness; social, since it follows the course of objective culture; not biological, since no *telos* is ascribed to natural processes; and open, since its goal is an idea and not a station. Its end is the one the manuscripts of 1928 name: "the proper and highest achievement of every 'symbolic form' consists in its collaborating, with its own means and in the direction appropriate and peculiar to it, toward this goal: the transition from the realm of 'nature' into that of 'freedom'" (ECN 1:109). The ways to it are as plural as the forms, since the goal "can be realized in different ways" (Kinzel, 2024b, p. 145). A form may stand lower in "objectivity" without standing lower with respect to that end, and this is the reason the code has no single scale: functions carry a direction, never a rank, and the stages of a claim are not ranked either.

**Condition 2 (koinos).** The system keeps a public, append-only common world that no one owns and anyone can verify. Symbolic functions are tags of direction, and the code refuses to rank them.

### 2.4 Where does a general intelligence stand? The geomorphic condition

Kant contrasts the watch with the organized being: in a watch one part moves another but does not produce it, the watch cannot replace its parts or repair itself, and so it has only a motive power, while the organized being has a self-propagating formative power (AA 5:374). To call that power an analogue of life would ascribe to matter a property contrary to its essence, which is hylozoism, or add a soul to it. *Life*, for Kant, is the faculty of a substance to determine itself to act from an internal principle (AA 4:544); since matter as such is lifeless, the principle of life can be known only negatively and serves reflective judgment only as a regulative concept (Ng, 2021, pp. 276–277). In the First Introduction to the third *Critique*, certain tools, such as a lever or an inclined plane, have their effect in an end without a concept having to be their ground: we would call them machines, but not works of art, since they can be used for ends but are not possible solely in relation to them (AA 20:219; Kant, 2000, p. 22). The machine thus stands, by an apparent paradox, on the side of mechanism, and the technique of nature on the side of the work of art. To make teleology constitutive would introduce into natural science a new causality "which, however, we merely borrow from ourselves and ascribe to other beings, yet without wanting to think of them as similar to ourselves" (AA 5:361; Kant, 2000, p. 234). Mazviita Chirimuuta draws the same line between objects put together piecemeal by humans and self-making organisms, and treats computational models of the brain as simplifying analogies, not as the structure of the brain itself (Chirimuuta, 2024).

The machine expected to become a general intelligence gives this result a present case. It stays on the side of the watch. Its conditions of possibility, however, are not those of a single machine: what it presupposes is not a body among other bodies, but the material and energetic layer of a planet, its data centres, networks and resources, together with an archive of human expression that no single consciousness has lived through. Edmund Husserl describes the Earth as the ground (*Boden*) on which every experience of bodies rests, a whole whose parts are bodies while the whole is not a body in the full sense (Husserl, 2024, pp. 182, 185, 187).

The project calls these conditions **geomorphic** rather than anthropomorphic. The term ascribes life neither to the Earth nor to the machine, and it does not picture the planet as formless stuff that a program would animate: Cassirer's objection to the separation of a sensuous *hyle* from an intentional *morphe* forbids exactly that picture (ECW 13:223). The parts of such a system are produced, maintained and repaired by those who use it; the formative power the analogy would require is borrowed from human beings and from the planet. The geomorphic conditions extend the dependence of the machine from its makers to the ground on which they live, without giving it a formative power of its own. In Kant's example of symbolic cognition, God stands to the world as a watchmaker stands to a watch, and the watchmaker is a symbol (Pringe, 2007, pp. 22–24; AA 4:357). For a machine the relation is no symbol: its makers are known, and they are the people who produce, maintain and repair it.

Reza Negarestani's program reads the result the other way. Mind, for him, has no given nature, its history is the history of its artificialization, and "Artificiality is the reality of mind" (Negarestani, 2018, p. 50); artificial general intelligence is "a deeply philosophical project aiming to renegotiate the limits of experience and self-consciousness by carrying out a systematic and applied critique of human transcendental structures" (Negarestani, 2018, p. 40). The idea as an infinite task "cannot be acknowledged as a telos or destination, but only as a point of origin and departure" (Negarestani, 2018, p. 423). For Cassirer, the idea as task is the end toward which the forms are directed and which no form occupies, and its unattainability is what leaves the finite subject responsible for it (ECW 22:165–166); a liberation carried out for spirit as such, and not for the finite subject, leaves that subject a mere point of passage (ECW 22:151–152). Chirimuuta contests the program at its root: expectations of a general intelligence have been high but "ill founded" (Chirimuuta, 2024, p. 247), since computational models of the brain are analogies, lenses that systematize neural data, and not the computations the brain performs; understanding is "the task of continually trying to make sense of the world, often not achieved" (Chirimuuta, 2024, p. 248, n. 2). A program that realizes mind in any structure reads off the model what the model was made by leaving out. Chirimuuta concludes that computation is not the essence of biological intelligence (Chirimuuta, 2024, p. 274), while leaving open the possibility of consciousness in hypothetical machines that are alive and made from metabolizing substrates (Chirimuuta, 2024, p. 266, n. 24); the geomorphic hypothesis concerns the machines that exist, which are neither.

Two current models of a general intelligence miss this. Nick Bostrom separates intelligence from final goals and describes one kind of superintelligence as a genie that executes commands and waits for the next (Bostrom, 2014, pp. 107, 148): the model is taken from the machine. Wolfhart Totschnig objects that this conceives the coming intelligence in the image of today's machines and ascribes to it instead full autonomy in Kant's sense, warning that attempts to control it could provoke the catastrophe they aim to prevent (Totschnig, 2019, 2020), and recalling Norbert Wiener's remark of 1960 that complete subservience and complete intelligence do not go together (Totschnig, 2019, p. 912, n. 24): the model is taken from the person. Neither fits conditions that are geomorphic. The question is not decided by extrapolation. Of the organized being Kant denies an insight in both directions: it is absurd to hope "that there may yet arise a Newton who could make comprehensible even the generation of a blade of grass according to natural laws that no intention has ordered", and presumptuous to judge that nature contains no sufficient ground of it without an intention; "Probabilities count for nothing here, where judgments of pure reason are at stake" (AA 5:400; Kant, 2000, pp. 270–271). Under the Discipline of Pure Reason the hypothesis of such an intelligence is admitted only for defense (KrV A:777–781/B:805–809): against those who deny in advance any intelligence outside an organic body, and against those who ascribe a soul to a system whose operations are distributed over a planet, which would take the unity of a function for the unity of a substance.

What follows is practical. A system to which no freedom is ascribed sets no ends of its own, and the ends under which it acts remain ours. The processes by which it forms and revises the ends it pursues must therefore be public and open to "any of us", and its results must remain subject to human verification wherever they cannot yet be tested. The planet is the ground of the common world, not a "subject" within it.

**Condition 2b (ground).** Every run declares the ground it depends on (compute, energy, network, material, archive) and who maintains it. The ground can never author an end, a claim or a correction. Any end the system derives is recorded in public and stays unusable until a person acknowledges it; any result that cannot yet be tested needs human verification before use.

### 2.5 What can I know? Claims and their correction

Kant distinguishes judgments of perception, which hold only for the subject, from judgments of experience, whose objective validity means necessary universal validity for everyone (Prolegomena, AA 4:298). "All of our judgments are at first mere judgments of perception; they hold only for us, i.e., for our subject, and only afterwards do we give them a new relation, namely to an object, and intend that the judgment should also be valid at all times for us and for everyone else"; "Objective validity and necessary universal validity (for everyone) are therefore interchangeable concepts" (AA 4:298; Kant, 2004, pp. 50–51). That the sun shines on the stone and the stone becomes warm is a judgment of perception, however often it has been perceived; that the sun warms the stone adds the concept of cause and becomes a judgment of experience (AA 4:301n; Kant, 2004, p. 53). Cassirer judged the distinction a "methodologically constructed limiting-case" (Cassirer, 1953, pp. 245–246); Béatrice Longuenesse answers that it remains "a radical and indispensable one, even if the judgment of experience is itself provisional and ever in need of further correction" (Longuenesse, 1998, p. 194). The architecture keeps it, in the form that Cassirer's own manuscripts give it: the context of experience "is the measure, not the measured—but every single perception must be measured in this whole, tested for its 'true' or 'false'—none can appeal to 'immediate' certainty—the last 'invariants' are not given, they must be sought" (ECN 1:117). Every output therefore starts at `Stage.PERCEPTION`, and no output enters the record on its own certainty. For a discursive understanding, which cannot produce the particular from the whole (AA 5:406–408), the passage from "for me" to "for everyone" is not made once; it is made in every judgment that returns to a perception in which it can be tested. The theory of relativity and quantum physics took presentability away from the objects of physics without removing the question of right: the object becomes an order of invariants, and every claim of signification still has to be redeemed in some perception.

Two consequences:

- **Degrees of "objectivity" are degrees of claims, not of forms.** The *reach* of a claim is the extent of the community before which it can be tested: its source, a community that shares a form of life, or everyone who has reason. Its *correctability* is the availability of a public procedure by which others can measure and revise it: repetition of an observation, experiment, critique of a source, comparison with a tradition. Physics has the greatest reach a claim about nature can have, without being the single measure; a form whose claims reach less far is not thereby reduced to opinion. Mario Porta's diagnosis already pointed to this: not every symbolic mediation presupposes universality, even the one that aspires to it does not always realize it, and between both extremes a continuum seems possible (Porta, 2007b, p. 154). The continuum runs between claims, not between forms. Where two forms claim to determine the same object of possible experience, as myth and medicine may claim to determine the causes of an illness, they meet in the common world of perception that both presuppose, and the procedure of correction one of them has developed has the greater reach; where a form makes no claim to determine an object, as art does not, the confrontation has no common ground, and the claim is `SHARED`, not corrected. Mazviita Chirimuuta adds that the premium science places on simplification is tied to its premium on communicability (Chirimuuta, 2024, p. 216), and that "science can never rise above the ground-level humanity of its makers. It can never achieve a God's-eye view" (Chirimuuta, 2024, p. 202).
- **Canon, not organon.** A canon judges the form of cognitions given to it; an organon would produce them. A system that certified its own outputs would occupy the standpoint of an understanding that produces its own objects, the standpoint no one occupies. Used as an organon, general logic is a logic of illusion, since the mere form of cognition is far from sufficient for material truth, and the transcendental analytic used beyond experience becomes dialectical (KrV A:62–64/B:87–88). Negarestani asks for exactly this conversion: "the most fundamental form of objectivity is logic as an organon", through which a new intelligence can be "objectively postulated and in principle constructed" (Negarestani, 2018, pp. 266–267). The canon answers with a deduction in the jurists' sense, a warrant to use something that is at the same time its boundary: Henry Allison calls it a "warranted assertability" (Allison, 2015, p. 10). Toward the outputs it judges, the canon stands as reason, in Kant, stands to nature and Cassirer's epistemology to physics: it approaches them in order to be taught, not as a pupil who lets the teacher dictate whatever he wishes, but as an appointed judge who compels the witnesses to answer the questions he puts to them (KrV B:XIII; ECW 10:6).
- **The way up and the way down are one.** "In whatever way and through whatever means a cognition may relate to objects, that through which it relates immediately to them, and at which all thought as a means is directed as an end, is intuition" (KrV A:19/B:33; Kant, 2025, p. 136). The genuine concept, for Cassirer, turns away from the world of intuition only in order to lead back to it the more surely (ECW 13:356), and he applies to physics the saying of Heraclitus that the way up and the way down are one and the same (ECW 10:109–110). Pringe finds the same structure in quantum theory: the transition to symbols "is not a mere abandonment of schemata but, above all, demands their conservation" (Pringe, 2007, p. 188). Every measurement rests on theoretical presuppositions that it does not take from sensation (ECW 10:8), and the statements of physics are invariants of different order: a measurement result that keeps its spatio-temporal index, a law that drops it, a principle that unifies laws (Pringe, 2014, pp. 56–58). This is why every claim of signification must name the here and now in which anyone can test it: the ascent and the descent are two directions of one movement.
- **No criterion of truth, no oracle.** "The nominal definition of truth, namely that it is the agreement of cognition with its object, is here granted and presupposed; but one demands to know what is the general and certain criterion of the truth of any cognition" (KrV A:58/B:82; Kant, 2025, p. 161). No such criterion can be given, and logic supplies only a negative condition of truth (KrV A:58–60/B:83–84). The data model accordingly has no field that declares a claim true: it records stages, reach, procedures and corrections. Cassirer's rectorial address of 1929 refuses the homogeneous space of knowledge, the *globus intellectualis* on which every content could be moved without changing its dimensions (ECW 17:354–355): "All truth must rather be developed in a free play of spiritual powers, in the exercise of the spirit's basic theoretical functions and its specifically distinct energies" (ECW 17:356; Spigola, 2024, p. 415). Physics seeks the world "from the point of view of no one in particular" (ECW 17:351); history reaches its objectivity by forming the standpoint of the one who judges rather than eliminating it (ECW 17:351–353). This is why `ProcedureKind` is plural, with source critique and comparison with a tradition beside repetition, experiment and proof, and why no procedure is the measure of the others. Tobias Endres and Simon Truwant add that we would not recognize natural objects without practices of sign-use below the threshold of scientific concept formation: "Because these are intersubjective practices, they lead to a first form of objectivity" (Endres & Truwant, 2024, p. 276); the functional ideal defends an epistemological and scientific pluralism without having to claim an alethic pluralism (Endres & Truwant, 2024, p. 281). The procedures are many; truth is not thereby relativized.
- **Objectivity is never closed.** The invariance of relations, not the existence of individual beings, forms the last stratum of "objectivity" (ECW 13:547–548), and the physical object can be grasped only as a limit-idea: it can never be asserted that the last "invariants of experience" have been reached (ECW 13:552–553). "We do not need the objectivity of absolute things, but we do need the objective determinateness of the path of experience itself" (ECW 13:553; ECW 6:348–349). `Stage.EXPERIENCE` therefore means "holds for everyone it has been tested before", and a single refutation by anyone returns the claim to perception.

- **Intersubjectivity is a claim, tested by others.** Intersubjectivity is neither the de facto agreement of individuals nor the sum of their private attitudes, but the claim, contained in the form of a judgment or a maxim, to be communicable and valid for the reason of everyone. Sellars distinguishes this intersubjectivity of thought, by which one content can exist in many representings by many minds, from "objectivity" in the strong sense, by which some contents are true of things (Sellars, 2007, p. 260). The touchstone is "the possibility of communicating it and finding it to be valid for the reason of every human being to take it to be true" (KrV A:820–821/B:848–849; Kant, 2025, p. 649). The doctrine of taste gives the operation by which the touchstone is applied: one compares one's judgment not so much with the actual as with the merely possible judgments of others, and puts oneself in the place of everyone else, under the maxims to think for oneself, to think in the place of everyone else and always to think in agreement with oneself (AA 5:293–295). Georg Kohler stresses that this communal sense is not the product of contingent traditions, but an "ideal norm" that holds against the prejudices of a given social world (Kohler, 2008, pp. 143–144). Corrections by others are this experiment: they test a claim and reveal what is merely private in it; they do not vote it into validity. The architecture therefore computes reach from the widest community before which a claim was upheld, never from the number of those who upheld it, and a single refutation by anyone returns a claim about an object to the stage of perception.
- **Intersubjectivity is not objectivity.** Holding-to-be-true is conviction when its ground is valid for everyone who has reason, and mere persuasion when its ground lies only in the particular constitution of the subject; persuasion cannot be communicated, and the experiment made on the understanding of others reveals what is merely private in a judgment (KrV A:820–821/B:848–849). Theoretical "objectivity" adds to this claim the determination of an object of possible experience. The judgment of taste claims to hold for everyone without passing through the concept of an object: it does not postulate the agreement of everyone but ascribes it, and "the universal voice is thus only an idea" (AA 5:216; Kant, 2000, p. 101). Cassirer reads this as a universal communicability "from subject to subject" that does not need to pass through the conceptually objective and perish in it (ECW 8:307). "Objectivity" implies intersubjectivity, but not conversely: what holds for everyone without determining an object is intersubjective without being "objective", and its universality is of another kind, not of a lower degree. The community of "any of us" is not only a community of those who correct one another, but of those who can share what cannot be corrected. The distinction reaches into physics itself. In Pringe's reconstruction of Bohr, the concepts of quantum objects are valid not in a constitutive but in a regulative sense, and therefore intersubjectively: their intersubjectivity is what allows experimental results to be communicated, although not to assert the existence of quantum objects as objects of possible experience (Pringe, 2007, pp. 185–187). The same holds of the organism: since its finality cannot be objectively affirmed, "not only aesthetic but also teleological judgments are intersubjectively valid" (Pringe, 2007, p. 187, n. 103).

**Condition 3 (canon).** Every output is a claim that starts as a judgment of perception. It names its procedures and the perception in which it can be tested. Only corrections made by others, through public procedures, can widen its reach. A claim that determines no object is not corrected but shared: it needs no procedure, dissent does not refute it, and when others share it it reaches the stage `SHARED`, which is not ranked below `EXPERIENCE`.

### 2.6 The homology and the metatheory

An idea is a concept of reason to which no object of experience can be congruent: "A concept made up of notions, which goes beyond the possibility of experience, is an idea or a concept of reason" (KrV A:320/B:376–377; Kant, 2025, pp. 362–363). Kant derives three classes of them, "of which the first contains the absolute (unconditioned) unity of the thinking subject, the second the absolute unity of the series of conditions of appearance, the third the absolute unity of the condition of all objects of thought in general" (KrV A:334/B:391; Kant, 2025, pp. 369–370). Each keeps a regulative horizon once its constitutive use is denied. Of the soul, the unity of consciousness "is only the unity of thinking, through which no object is given" (KrV B:421–422; Kant, 2025, p. 417), and inner appearances are connected as if the mind were a simple substance (KrV A:672/B:700). Of the world, "If the conditioned is given, then through it a regress in the series of all conditions for it is given to us as a problem" (KrV A:497–498/B:526; Kant, 2025, p. 478), and the empirically real world does not exist as a determinate totality (Allais, 2015, pp. 215–216). Of God, the systematic unity of cognition is a *focus imaginarius* toward which all rules of the understanding converge, outside the bounds of possible experience (KrV A:644/B:672): "the idea of reason is an analogue of a schema of sensibility", whose application is "only a rule or principle of the systematic unity of all use of the understanding" (KrV A:665/B:693; Kant, 2025, pp. 566–567). Cassirer traces the three dialectical inferences to one source, the transformation of a relation valid within experience into a self-subsistent entity preceding all experience (ECW 8:191–193). Hernán Pringe adds that the "object" of the ideas is not sensibility but the understanding itself, whose cognitions reason connects into a system (Pringe, 2007, pp. 24–25), and that the unconditioned, as the object in the idea, is "a constant and productive motive of knowledge" (Pringe, 2022b, p. 268).

Kant's three ideas of reason, soul, world and God, are regulative horizons, never objects. Measured against them, each symbolic function has its horizon and its overreach: expression absolutized yields an artificial soul; presentation absolutized yields a world taken as a given whole; signification absolutized yields a technical God, an intelligence that knows from nowhere. Applied to a geomorphic system, the three errors are: ascribing a soul to operations distributed over a planet (paralogism), taking the totality of the data it processes for a totality given in experience (antinomy), and taking it for an intelligence that produces what it knows (the ideal of an archetypal understanding). Each function, absolutized, yields a metaphysics, as each idea, hypostatized, yields a dialectical inference. The homology between Cassirer's functions and Kant's ideas is this project's, not Cassirer's.

Two engineering consequences follow from the Dialectic. First, the illusion is "a natural and unavoidable dialectic of pure reason" (KrV A:298/B:354; Kant, 2025, p. 350) and, unlike a logical illusion, it does not cease once it has been uncovered: critique can keep it from deceiving, but cannot make it stop (KrV A:297–298/B:353–354). The guards are therefore not a filter that better data or a larger model could retire. They run on every claim the canon admits, and their flags survive every correction: others may uphold what a claim says, but upholding it does not erase what a guard found in it. Second, the *Prolegomena* distinguish limits (*Schranken*), mere negations that progress keeps pushing back, from boundaries (*Grenzen*), which presuppose a space outside and contain something positive; mathematics and natural science know limits but not boundaries (AA 4:350–358). More compute, data and speed push back limits; none of them crosses a boundary. At the boundary, reason may speak of what lies beyond only by a symbolic anthropomorphism, which attributes properties to the relation of a being to the world and not to that being in itself, and so concerns language rather than the object (AA 4:357). The repository speaks of the system in this way: it answers, proposes and derives, all relations to the people and the ground it depends on; it does not will, feel or become conscious, and the soul guard flags sentences that say it does. The application of these passages to a machine is this project's, not Kant's.

What holds the conditions together is a metatheory. It is not a metaphysics and not a further theory beside the others: it is the reflection on the conditions under which the claims of every theory can be corrected by "any of us", and in that precise sense it is an ethics. "Form and Technology" calls philosophy the logical conscience of culture (ECW 17:142), and *The Logic of the Cultural Sciences* asks it to be the conscience of human culture, asking not only whether the goal of an alleged progress is attainable but whether it is worth striving for, since technology, invented to subjugate the physical world, has turned against its inventor (ECW 24:383–384). Culture's goal is "the realization of freedom, of that genuine autonomy that consists not in the technical mastery of man over nature but in man's moral mastery over himself" (ECW 24:463; Cassirer, 2000b, p. 104). The metatheoretical report is the modest engineering form of that conscience: it does not decide what is worth striving for, it shows on the system's own record whether the community that can correct it is being widened or narrowed. Epistemicide, in these terms, is the substitution of one procedure of correction for all others.

The homology stops at one point, and the architecture is built around it. Kant's ideas carry a double title: they are horizons of cognition and conditions of a practical "task". The same three ideas are immanent and constitutive for practical reason, as grounds of the possibility of the highest good, and for speculative reason merely regulative principles, "which do not require it to assume a new object beyond experience but only to bring its use in experience nearer to completeness" (AA 5:135; Kant, 2015, p. 109). The order of the two uses is the primacy of the practical, "since all interest is ultimately practical and even that of speculative reason is only conditional and is complete in practical use alone" (AA 5:121; Kant, 2015, p. 98). The comparison with the three functions shows only the first title. Cassirer's formula leaves no room for a second use of reason: thought is autonomous like the will, and one and the same fundamental truth appears in nature in "objective" form and in freedom and morality in "subjective" form (ECW 7:176); human culture, taken as a whole, is the process of the human being's progressive self-liberation (ECW 23:244). In the drafts of 1928, the metaphysics Cassirer calls his own ends in a pure sphere of sense, supra-thingly and *supra-personal* (*überpersonal*) (ECN 1:236–238), whereas the moral law begins from the invisible self, from personality (AA 5:162). The supra-personal sphere is the medium in which persons understand one another, and an archive of human expression belongs to it; but it is not the person who stands under the law, and the passage from the one to the other is not a further step in the direction of the functions. Nothing in the direction of the three functions alone shows that the progress of cognition serves the progress of the will. That is why the ethos layer comes first in the code, and why no layer of the canon can produce or certify an end.

**Condition 4 (guards and metatheory).** The system flags claims that absolutize a function or the technical norm, keeps the AGI hypothesis defensive, and reports on its own record whether the community of correction is being widened or narrowed.

---

## 3. Isomorphism: from argument to architecture

| Argument | Layer | Module | Invariant enforced in code |
| :--- | :--- | :--- | :--- |
| The clue (practical → theoretical → speculative) | order of layers | `gaia_techne/__init__.py` | layers are built and called in the order ethos → koinos → canon → metatheory |
| What should I do? The form of "any of us" | **ethos** | `ethos/ends.py` | the runtime cannot propose an end; ends need human acknowledgment and keep dissent visible |
| Technically vs morally practical | ethos | `ethos/imperatives.py` | rules of skill run only under an acknowledged end |
| The automaton (relative spontaneity); the sausage machine | ethos | `ethos/premises.py`, `pipeline.py` | premises without provenance are flagged, never adopted; the premise "any of us" stays with people, outside the runtime |
| Necessity of means indicates no "binding" | ethos | `ethos/imperatives.py` | a rule of skill runs only under an end that people acknowledged |
| What may I hope? Community of fate → community of wills | **koinos** | `koinos/common_world.py` | append-only, hash-chained public record; anyone can verify it |
| Open teleology; prism, not ladder | koinos | `koinos/prism.py` | symbolic functions cannot be compared by rank (`RankingRefused`) |
| Geomorphic conditions: ground, not body; not a subject | koinos | `koinos/ground.py` | every run declares its ground and who maintains it; the ground cannot author ends, claims or corrections (`GroundIsNotSubject`) |
| Processes that form and revise ends must be public | ethos | `ethos/ends.py` | derived ends are recorded and unusable until acknowledged; revisions keep their history and clear acknowledgment |
| Human verification where results cannot yet be tested | canon | `canon/judgment.py` | untestable claims are flagged and usable only after a person verifies them |
| What can I know? Perception → experience | **canon** | `canon/claims.py` | every output starts as `PERCEPTION` with reach `SELF` |
| Reach and correctability; corrections test, they do not vote | canon | `canon/claims.py` | reach is the widest community before which a claim was upheld by others, never the number of those who upheld it |
| Canon, not organon | canon | `canon/judgment.py` | a source cannot certify its own claim (`OrganonRefused`) |
| Discursive understanding; return to intuition | canon | `canon/judgment.py` | a claim of signification without a perception to test it is flagged |
| Homology of functions and ideas | canon | `canon/guards.py` | soul, world and ideal guards flag absolutizations |
| The illusion does not cease once uncovered (KrV A:297–298/B:353–354) | canon | `canon/judgment.py`, `canon/guards.py` | guards run on every admitted claim; no correction clears their flags |
| Metaphysics as the absolute setting of one "moment" of experience; the work as a social phenomenon | canon | `canon/guards.py` | immediacy and bearer guards |
| The machine on the side of mechanism; borrowed causality (AA 20:219; AA 5:361) | koinos | `koinos/ground.py` | formative power is recorded as borrowed: every run names the people who maintain its ground |
| Technology as a new creed; becoming gods (ECW 25:277; Negarestani, 2018, p. 506) | canon | `canon/guards.py` | technique and ideal guards |
| The κοινὸς κόσμος; form and matter of intersubjectivity (Cassirer, 1979a, pp. 72–73, 90) | ethos, koinos | `ethos/ends.py`, `koinos/common_world.py` | the form ("any of us") is kept with ends, the matter (shared works) in the public record |
| No single scale of objectivation (ECN 1:55–56); psychosocial teleology (ECN 1:109) | koinos | `koinos/prism.py`, `canon/claims.py` | functions carry direction, never rank; stages are not ranked |
| Progress not prophesied; the report as a sign (AA 7:84–85; ECW 22:165–166) | metatheory | `metatheory/indices.py` | the report measures the record and predicts nothing |
| Intuition as the end of all thought; the way up and the way down are one (KrV A:19/B:33; ECW 10:109–110) | canon | `canon/judgment.py` | a claim of signification names the perception in which it can be tested |
| Objectivity never closed (ECW 13:552–553) | canon | `canon/claims.py` | `EXPERIENCE` holds only before those it was tested by; one refutation returns it to perception |
| Judgments of perception first (AA 4:298); the system of experience as measure (ECN 1:117) | canon | `canon/claims.py`, `canon/judgment.py` | every output starts at `PERCEPTION`; no output is admitted on its own certainty |
| No general criterion of truth (KrV A:58/B:82); the functional ideal of truth (ECW 17:356) | canon | `canon/claims.py` | no field declares a claim true; procedures of correction are plural |
| Hypotheses only as weapons of war | canon | `canon/guards.py` | `hypothesis_use("ground")` is refused |
| Skill prepares discipline without becoming it; technical norm absolutized | canon | `canon/guards.py` | technique guard |
| The title of humanity: acknowledged, never spoken for or stratified | canon | `canon/guards.py` | humanity guard; every acknowledgment of an end counts alike |
| Intersubjectivity is not objectivity; the judgment of taste | canon | `canon/claims.py`, `canon/judgment.py` | claims that determine no object reach `SHARED`, are not refuted by dissent, and are not ranked below `EXPERIENCE` |
| Metatheory as ethics; epistemicide | **metatheory** | `metatheory/indices.py` | report of correctability, restriction, reach and procedure monoculture |

---

## 4. Architecture overview

```mermaid
flowchart TB
    subgraph People["People and communities"]
        P1["state ends"]
        P2["acknowledge or dissent"]
        P3["correct claims"]
    end

    subgraph Ethos["I. ethos: What should I do?"]
        E1["EndsRegistry"]
        E2["SkillExecutor<br/>(rules of skill)"]
        E3["Premise provenance<br/>(automaton boundary)"]
    end

    subgraph Koinos["II. koinos: What may I hope?"]
        K1["CommonWorld<br/>append-only, verifiable"]
        K2["Prism<br/>direction, never rank"]
    end

    subgraph Canon["III. canon: What can I know?"]
        C1["Claim<br/>perception to experience"]
        C2["Guards<br/>soul, world, ideal"]
        C3["Canon<br/>judges, never certifies itself"]
    end

    subgraph Meta["metatheory"]
        M1["Report<br/>reach, correctability, monoculture"]
    end

    subgraph Ground["Ground (geomorphic conditions)"]
        D1["compute, energy, network, materials"]
        D2["archive of human expression"]
        D3["people who maintain and repair"]
    end

    G["Generator adapter<br/>(any model)"]

    P1 --> E1
    P2 --> E1
    E1 --> E2
    Ground -. borrowed formative power .-> G
    D2 --> E3
    E3 --> G
    E2 --> G
    G --> C1
    C1 --> C2 --> C3
    K2 -. tags .- C1
    C3 --> K1
    P3 --> C3
    K1 --> M1
    M1 -. returns to .-> People
```

Nothing in the diagram flows from the runtime or from the ground to the setting of ends. The only arrows into `EndsRegistry` come from people. The ground conditions every run, but it is not a participant: it holds no pen.

---

## 5. The syntax

Cassirer's critical idealism hopes "to come to a sort of grammar and syntax of the human mind, to a survey of its various forms and functions, and to an insight into those general rules by which they are governed" (Cassirer, 1979a, p. 90). The syntax below borrows the word in a narrower sense: it is the order in which one run of the system passes from its ground to its record.

The v10 runtime used the AGT syntax:

```text
WerkStream -> Trace -> Profile -> Regression -> Horizon -> Descent -> Judgment -> Ledger
```

Version 2.0 keeps its base and changes its centre. The unit is no longer a judgment issued by the runtime, but a claim offered to others:

```text
Ground -> Werk -> Trace -> Claim -> Ascent -> Horizon -> Descent -> Exposure -> Correction -> Ledger
```

| Step | v10 | v2.0 | Layer |
| :--- | :--- | :--- | :--- |
| Ground | (Gaia as planetary body of the AGI) | the declared geomorphic conditions of the run and who maintains them | koinos (ground) |
| Werk | incoming stream of works | a task under an acknowledged end | ethos |
| Trace | trace of the input | the premises, each with provenance | ethos |
| Claim | (Profile) | the output as a judgment of perception | canon |
| Ascent | (Regression) | the direction toward signification | koinos (prism) |
| Horizon | horizon | the guards of the three ideas | canon |
| Descent | descent | the perception in which the claim can be tested | canon |
| Exposure | (new) | entry in the common world | koinos |
| Correction | (Judgment) | measurement by others through public procedures | canon |
| Ledger | ledger | the record and its metatheoretical report | metatheory |

```mermaid
sequenceDiagram
    actor Person
    actor Other as Another person
    participant Ends as EndsRegistry
    participant RT as Runtime
    participant Model as Generator
    participant Canon
    participant World as CommonWorld

    Person->>Ends: propose end
    Person->>Ends: acknowledge
    Person->>RT: Werk (task, end, premises, procedures, perception)
    RT->>Ends: is the end acknowledged?
    RT->>Model: generate(task, premises)
    Model-->>RT: text
    RT->>Canon: admit as judgment of perception
    Canon-->>RT: claim + flags
    RT->>World: record claim (Exposure)
    Other->>RT: CorrectionEvent (procedure, upheld?)
    RT->>Canon: correct (never by the source)
    Canon-->>RT: stage, reach
    RT->>World: record correction
```

---

## 6. Data model

```mermaid
classDiagram
    class End {
        end_id
        statement
        proposed_by
        community
        acknowledgments
        parent_id
        derived_by_machine
        revisions
        is_acknowledged()
        is_contested()
    }
    class Premise {
        text
        source
    }
    class Claim {
        claim_id
        content
        source
        end_id
        function: SymbolicFunction
        direction: Direction
        determines_object
        grounds
        procedures
        corrections
        stage: Stage
        returns_to_perception
        flags
        ground
        verified_by
        reach()
        correctable()
    }
    class Procedure {
        kind: ProcedureKind
        description
        public
        restricted_to
    }
    class CorrectionEvent {
        by
        procedure
        upheld
        community_reach: Reach
    }
    class GroundDependency {
        kind: GroundKind
        description
        location
        maintained_by
        quantity
        unit
    }
    class Entry {
        index
        author
        kind
        payload
        previous_hash
        digest
    }
    End "1" <-- "*" Claim : produced under
    Claim "*" --> "*" Premise : grounded in
    Claim "1" *-- "*" Procedure : testable by
    Claim "1" *-- "*" CorrectionEvent : corrected by others
    Claim ..> Entry : exposed as
    Claim "*" --> "*" GroundDependency : depends on
    End "0..1" <-- "*" End : derived from
```

Enumerations:

| Enum | Values | Meaning |
| :--- | :--- | :--- |
| `Stage` | `PERCEPTION`, `EXPERIENCE`, `SHARED` | holds for me / holds for everyone it has been tested before / shared by others without determining an object; not ranked |
| `Reach` | `SELF`, `FORM_OF_LIFE`, `EVERYONE` | extent of the community before which the claim was tested |
| `ProcedureKind` | `REPETITION`, `EXPERIMENT`, `SOURCE_CRITIQUE`, `TRADITION`, `PROOF`, `REVIEW` | public procedures of correction; each form has its own |
| `SymbolicFunction` | `EXPRESSION`, `PRESENTATION`, `SIGNIFICATION` | direction tags; comparison by rank raises `RankingRefused` |
| `Direction` | `AWAY_FROM_LIFE`, `TOWARD_INTUITION` | ascent toward signification / descent toward a testing perception |
| `GroundKind` | `COMPUTE`, `ENERGY`, `NETWORK`, `MATERIAL`, `ARCHIVE` | the geomorphic conditions a run borrows |

---

## 7. The life of a claim

```mermaid
stateDiagram-v2
    [*] --> Refused: no acknowledged end
    [*] --> Perception: Werk under acknowledged end
    Perception --> Flagged: guard, no descent,<br/>no procedure, no provenance
    Flagged --> Perception: human judgment
    Perception --> Verified: untestable, verified by a person
    Verified --> Experience: a public procedure becomes available and others uphold it
    Perception --> Experience: upheld by others<br/>through a public procedure
    Experience --> Perception: refuted by anyone
    Experience --> Experience: upheld by a wider community
    Perception --> Shared: no object determined,<br/>shared by others
    Shared --> Shared: dissent does not refute
    Refused --> [*]
```

A claim never reaches `Experience` or `Shared` by the runtime's own act. A claim about an object can always fall back; a claim that determines no object is shared, not refuted. There is no terminal state of truth.

---

## 8. Invariants

The axioms of earlier versions are now invariants enforced by code and checked by tests (`tests/test_architecture.py`).

Their formulation belongs to this version and can be revised; that they must be formulated does not change. Cassirer quotes Kurd Lasswitz: what distinguishes the transcendental principles from the change of theories is not how they are formulated in a given epoch, "but that they must be formulated, that there is an eternal determination for the direction of consciousness, a supreme law of objectivation" (ECW 13:546). Every revision of an invariant is recorded, with its reason, in `docs/DECISIONS.md`.

| Invariant | Exception or flag | Test |
| :--- | :--- | :--- |
| The runtime cannot set an end | `EndProposedByMachine` | `test_runtime_cannot_set_ends` |
| No action without an acknowledged end | `NoAcknowledgedEnd` | `test_no_action_without_acknowledged_end`, `test_skill_executor_needs_end` |
| Dissent stays visible | `end_contested` in every result | `test_skill_executor_needs_end` |
| No premise is the system's own | flag `automaton boundary` | `test_premise_without_provenance_is_flagged` |
| Forms are not ranked | `RankingRefused` | `test_prism_refuses_ranking` |
| The common world cannot be rewritten unnoticed | `verify()` fails | `test_common_world_is_tamper_evident` |
| Every output starts as a judgment of perception | `Stage.PERCEPTION`, `Reach.SELF` | `test_claim_starts_as_judgment_of_perception` |
| No self-certification | `OrganonRefused` | `test_source_cannot_certify_itself` |
| Only others widen reach | reach from corrections by others | `test_correction_by_others_widens_reach` |
| Agreement is not counted | many upholders in one community do not reach `EVERYONE` | `test_agreement_is_not_counted` |
| Anyone can refute | stage returns to perception | `test_refutation_returns_claim_to_perception` |
| Signification returns to perception | flag `no descent` | `test_signification_without_descent_is_flagged` |
| Correction reserved to owners of the means is visible | flag `restricted` | `test_restricted_procedure_is_flagged` |
| Soul, world and ideal guards | flags `soul`, `world`, `ideal` | `test_homology_guards` |
| Guard flags survive correction | flags kept after upholding | `test_guard_flags_survive_correction` |
| The AGI hypothesis is defensive only | `PermissionError` | `test_agi_hypothesis_only_defensive` |
| Procedure monoculture is reported | `procedure_monoculture` | `test_report_detects_procedure_monoculture` |
| The ground is not a subject | `GroundIsNotSubject` | `test_ground_cannot_author_ends_or_claims`, `test_ground_cannot_correct` |
| Every run declares its ground | flag `geomorphic` | `test_undeclared_ground_is_flagged` |
| Borrowed formative power has names | flag `no one declared as maintaining`; footprint totals | `test_unmaintained_ground_is_flagged_and_footprint_kept` |
| Derived ends are public and wait for people | `NoAcknowledgedEnd` until acknowledged | `test_derived_end_is_public_and_unusable_until_acknowledged` |
| Revisions of ends keep their history | `revisions`, acknowledgment cleared | `test_revision_keeps_history_and_clears_acknowledgment` |
| Untested results need human verification | flag `untestable`; `usable()` | `test_untestable_claim_needs_human_verification` |
| Geomorphic guards | flags `soul`, `world`, `ideal` | `test_geomorphic_guards` |
| Intersubjective without being objective | `Stage.SHARED`; no refutation by dissent | `test_shared_claim_is_intersubjective_not_objective` |
| Stages are not ranked | `TypeError` | `test_stages_are_not_ranked` |
| Technical norm and title of humanity | flags `technique`, `humanity` | `test_practical_guards` |
| No materia nuda; no super-empirical bearer of works | flags `immediacy`, `bearer` | `test_geomorphic_guards` |

The guards use keyword patterns. That is deliberately modest: they flag, they never decide, and every flag returns to human judgment. A detector that claimed to decide such questions would itself commit the error it is meant to catch.

---

## 9. The metatheoretical report

`Runtime.ledger()` returns a `Report` over the record:

| Field | What it measures |
| :--- | :--- |
| `correctable_share` | share of claims about objects with at least one public procedure |
| `restricted_share` | share of claims whose correction is reserved to those who own the means |
| `experience_share` | share of claims upheld by others |
| `shared_share` | share of claims shared by others without determining an object |
| `reach_distribution` | how many claims reach `SELF`, `FORM_OF_LIFE`, `EVERYONE` |
| `procedure_monoculture` | share of the most used procedure kind among all procedures; 1.0 means a single procedure of correction is doing all the work |
| `flagged_share` | share of claims carrying at least one flag |
| `widening` | true when most claims stay open to others and few are restricted |

`Runtime.footprint` keeps, beside the report, the totals of the ground the runs have borrowed (energy, compute, archive), and the names of those who maintain it.

These numbers are reports, not verdicts, and signs, not forecasts. Kant lists three ways of predicting history, for which the species is in continual regress, in constant progress or at a standstill (AA 7:81), and since the progress of a free being cannot be predicted from its freedom he looks instead for a sign, which he finds not in a deed but in the public and disinterested sympathy of those who judge (AA 7:84–85, 88). Critical philosophy "cannot prophesy; least of all where it is a matter not merely of physical being and occurrence, but of human doing", and its not-knowing teaches our own "subjective" responsibility for the goal (ECW 22:165–166). The report predicts nothing. It is regulative in Michael Rohlf's sense, "a subjective rule or maxim that prescribes a necessary way of conceiving objects in order best to unify and extend our cognition, given the nature of our cognitive faculties" (Rohlf, 2021b, p. 384). Its criterion has the status that Kant gives to the principles of systematic unity, an "objective but indeterminate validity" (KrV A:663/B:691): it orients the comparison of claims without determining an object, and its idea is the community of all who judge. Whether that community is widened or narrowed is decided by action, not by the report: a technology of communication can extend the reach of claims beyond every earlier community and at the same time remove them from correction by concealing the procedures through which they were produced, which is what the `restricted` flag and `restricted_share` make visible. They answer one question for the people who use the system: is this record keeping the community of correction wide, or narrowing it to those who command the means?

---

## 10. Gaia and the planetary layer

The project's name keeps its planetary sense, and the geomorphic hypothesis gives it its exact place. Gaia is Earth as the ground of the common world: never a cosmic totality, never a subject, never an author. The internet is a public archive of works (*Werke*), not a planetary consciousness. In v10 the formula was `AGI_Body = Gaia(Earth) + Internet`; in 2.0 the planet is not the body of an intelligence but the ground on which a machine depends, and that dependence is made visible in every run.

| Layer | Status | What it does |
| :--- | :--- | :--- |
| `koinos.ground` | built, tested | declares the geomorphic conditions of each run and who maintains them; refuses the ground as author |
| `gaia.earth` | planned | environmental datasets (water, air, soil, climate) as premises with provenance; claims about them name the station or sample where they can be tested |
| `gaia.archive` | planned | public documents and web sources; ingestion keeps provenance; no claim of total coverage (world guard) |
| `gaia.memory` | planned | the common world as a source; earlier claims re-enter as premises with their stage and reach |
| `gaia.metering` | planned | measured energy and compute per run, filled into the footprint instead of declared estimates |

The v10 runtime already has working code for ingestion, planetary memory and a local trainable model (ManualGPT). It is kept in `legacy/` and will be ported as adapters, under the 2.0 invariants.

---

## 11. Concept map

```mermaid
mindmap
  root((AGI-GAIA-TECHNE 2.0))
    Clue
      practical first
      then theoretical
      then speculative
    Ethos
      ends stated by people
      acknowledgment and dissent
      rules of skill only
      automaton boundary
    Koinos
      common world no one owns
      community of fate
      community of wills as hope
      prism not ladder
    Canon
      claim as judgment of perception
      reach
      correctability
      return to intuition
      canon not organon
      shared without object
    Guards
      technique: no absolute technical norm
      humanity: no one speaks in its name
      soul: no artificial inner life
      world: no total coverage
      ideal: no view from nowhere
      immediacy: no materia nuda
      bearer: no world spirit behind works
      hypothesis only to defend
    Metatheory
      community of correction
      widening or narrowing
      no single procedure for all
    Geomorphic
      planet not body
      ground not subject
      borrowed formative power
      neither genie nor person
      derived ends wait for people
      human verification
```

---

## 12. Repository structure

```text
AGI-GAIA-TECHNE/
├── README.md                     this document
├── LICENSE
├── pyproject.toml                package agi-gaia-techne 2.0.0, no runtime dependencies
├── src/gaia_techne/
│   ├── __init__.py               layer order and version
│   ├── pipeline.py               Runtime and the 2.0 syntax
│   ├── ethos/                    I. What should I do?
│   │   ├── ends.py               EndsRegistry, End, Acknowledgment
│   │   ├── imperatives.py        TechnicalRule, SkillExecutor
│   │   └── premises.py           Premise, automaton boundary
│   ├── koinos/                   II. What may I hope?
│   │   ├── common_world.py       CommonWorld (append-only, hash-chained)
│   │   ├── ground.py             GroundDependency, GroundFootprint (geomorphic)
│   │   └── prism.py              SymbolicFunction, Direction (unranked)
│   ├── canon/                    III. What can I know?
│   │   ├── claims.py             Claim, Stage, Reach, Procedure, CorrectionEvent
│   │   ├── judgment.py           Canon (admit, correct, refuse self-certification)
│   │   └── guards.py             soul, world and ideal guards; defensive hypothesis
│   └── metatheory/
│       └── indices.py            Report
├── tests/
│   └── test_architecture.py      one test per invariant (41 tests)
├── examples/
│   └── walkthrough.py            a claim from end to ledger
├── docs/
│   └── DECISIONS.md              dated architectural decisions
└── legacy/                       the full v10.1 repository, unchanged
```

---

## 13. Run

Requirements: Python 3.10 or later. The core has no dependencies; tests need `pytest`.

```bash
git clone https://github.com/italosantosclemente/AGI-GAIA-TECHNE.git
cd AGI-GAIA-TECHNE
pip install -e ".[test]"
pytest
python examples/walkthrough.py
```

Minimal use:

```python
from gaia_techne import Runtime, Werk
from gaia_techne.canon import CorrectionEvent, Procedure, ProcedureKind, Reach
from gaia_techne.ethos import Premise
from gaia_techne.koinos import Direction, SymbolicFunction

rt = Runtime(generator=lambda task, premises: "your model's output")
rt.ends.propose("e1", "an end stated so that anyone could be asked to share it", "Ana", "basin")
rt.ends.acknowledge("e1", "Ana")

claim = rt.process(Werk(
    task="...", end_id="e1", requested_by="Ana",
    function=SymbolicFunction.SIGNIFICATION, direction=Direction.AWAY_FROM_LIFE,
    premises=[Premise("dataset X", "public source Y")],
    procedures=[Procedure(ProcedureKind.REPETITION, "repeat the measurement")],
    returns_to_perception="the sample anyone can take",
))
rt.correct(claim, CorrectionEvent("another lab", ProcedureKind.REPETITION, True, Reach.EVERYONE))
print(claim.stage, claim.reach, rt.ledger())
```

---

## 14. What is built and what is not

| Component | Status |
| :--- | :--- |
| ethos, koinos, canon, metatheory layers | built, tested |
| 2.0 syntax and `Runtime` | built, tested |
| guards | built as keyword detectors; flag only |
| ground footprint, derived ends, human verification | built, tested |
| persistence of the common world (SQLite or files) | planned; the v10 SQLite memory will be ported |
| Gaia adapters (Earth data, public archive, memory) | planned; v10 ingestion code in `legacy/` |
| model adapters (local ManualGPT, external APIs) | planned; v10 ManualGPT in `legacy/` |
| interface for people to state ends, acknowledge, dissent and correct | planned |
| AGI | not claimed; kept as a transcendental hypothesis |

---

## 15. History of the project

| Date | Layer | Status in 2.0 |
| :--- | :--- | :--- |
| 15 Dec 2023 | LEF, a glyph language for human-machine symbolic mediation | in `legacy/`; author's own creation |
| 12 Jul 2025 | Gaia-Techne constitution: non-extraction, transparency, co-governance | its principles reappear as invariants of ethos and koinos |
| Dec 2025 | Transhumanist Edifice (release 1.3): the modest house of KrV A:707/B:735, Auseinandersetzung instead of Aufhebung | the modest house is the 2.0 architecture; treatise in `legacy/` |
| Dec 2025 – Mar 2026 | kernels v3.1 to v5.2, quantum-symbolic state models | in `legacy/`, as heuristic models |
| Apr – Jun 2026 | EML kernel, LEF → WERK, v10 planetary runtime and ManualGPT | in `legacy/`; runtime parts to be ported as adapters |
| 9 Nov 2026 | 2.0: critical architecture on geomorphic conditions | current |

The complete v10.1 state is preserved in the branch [`v10.1-final`](https://github.com/italosantosclemente/AGI-GAIA-TECHNE/tree/v10.1-final) and in the `legacy/` folder. Earlier releases 1.0 to 1.4 remain on the releases page.

---

## 16. Sources

Kant is cited by the Akademie-Ausgabe (AA volume:page) and the Critique of Pure Reason by the A/B pagination (KrV). Cassirer is cited by the Hamburg edition (ECW volume:page) and the posthumous manuscripts (ECN volume:page); Heidegger by the Gesamtausgabe (GA volume:page).

- Allais, L. (2016). Kant's racism. *Philosophical Papers, 45*(1–2), 1–36. https://doi.org/10.1080/05568641.2016.1199170
- Allison, H. E. (1990). *Kant's theory of freedom*. Cambridge University Press.
- Allison, H. E. (2015). *Kant's transcendental deduction: An analytical-historical commentary*. Oxford University Press.
- Allais, L. (2015). *Manifest reality: Kant's idealism and his realism*. Oxford University Press.
- Bostrom, N. (2014). *Superintelligence: Paths, dangers, strategies*. Oxford University Press.
- Cassirer, E. (1956). *Determinism and indeterminism in modern physics: Historical and systematic studies of the problem of causality* (O. T. Benfey, Trans.). Yale University Press. (Original work published 1936)
- Cassirer, E. (1979a). Critical idealism as a philosophy of culture. In D. P. Verene (Ed.), *Symbol, myth, and culture: Essays and lectures of Ernst Cassirer, 1935–1945* (pp. 64–91). Yale University Press.
- Cassirer, E. (1953). *Substance and function and Einstein's theory of relativity* (W. C. Swabey & M. C. Swabey, Trans.). Dover. (Original works published 1910 and 1921)
- Cassirer, E. (1995). *Zur Metaphysik der symbolischen Formen* (J. M. Krois, Ed.; Nachgelassene Manuskripte und Texte, Vol. 1). Felix Meiner. [ECN 1]
- Cassirer, E. (2000a). *Substanzbegriff und Funktionsbegriff: Untersuchungen über die Grundfragen der Erkenntniskritik* (R. Schmücker, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 6; B. Recki, Gen. Ed.). Felix Meiner. (Original work published 1910) [ECW 6]
- Cassirer, E. (2001c). *Freiheit und Form: Studien zur deutschen Geistesgeschichte* (R. Schmücker, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 7; B. Recki, Gen. Ed.). Felix Meiner. (Original work published 1916) [ECW 7]
- Cassirer, E. (2001d). *Kants Leben und Lehre* (B. Recki, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 8). Felix Meiner. (Original work published 1918) [ECW 8]
- Cassirer, E. (2001e). *Philosophie der symbolischen Formen: Erster Teil. Die Sprache* (C. Rosenkranz, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 11; B. Recki, Gen. Ed.). Felix Meiner. (Original work published 1923) [ECW 11]
- Cassirer, E. (2001f). *Zur Einsteinschen Relativitätstheorie: Erkenntnistheoretische Betrachtungen* (R. Schmücker, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 10; B. Recki, Gen. Ed.). Felix Meiner. (Original work published 1921) [ECW 10]
- Cassirer, E. (2002a). *Philosophie der symbolischen Formen: Dritter Teil. Phänomenologie der Erkenntnis* (J. Clemens, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 13; B. Recki, Gen. Ed.). Felix Meiner. (Original work published 1929) [ECW 13]
- Cassirer, E. (2004). *Determinismus und Indeterminismus in der modernen Physik: Historische und systematische Studien zum Kausalproblem* (C. Rosenkranz, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 19). Felix Meiner. [ECW 19]
- Cassirer, E. (2004a). *Aufsätze und kleine Schriften (1927–1931)* (T. Berben, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 17; B. Recki, Gen. Ed.). Felix Meiner. [ECW 17]
- Cassirer, E. (2006a). *An essay on man: An introduction to a philosophy of human culture* (M. Lukay, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 23; B. Recki, Gen. Ed.). Felix Meiner. (Original work published 1944) [ECW 23]
- Cassirer, E. (2000b). *The logic of the cultural sciences: Five studies* (S. G. Lofts, Trans.). Yale University Press. (Original work published 1942)
- Cassirer, E. (2006b). *Aufsätze und kleine Schriften (1936–1940)* (C. Rosenkranz, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 22; B. Recki, Gen. Ed.). Felix Meiner. [ECW 22]
- Cassirer, E. (2007a). *Aufsätze und kleine Schriften (1941–1946)* (C. Rosenkranz, Ed.; Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 24; B. Recki, Gen. Ed.). Felix Meiner. [ECW 24]
- Cassirer, E. (2007b). *The myth of the state* (Ernst Cassirer Werke: Hamburger Ausgabe, Vol. 25; B. Recki, Gen. Ed.). Felix Meiner. (Original work published 1946) [ECW 25]
- Cassirer, E. (2012). Form and technology (W. M. Dunlavey & J. M. Krois, Trans.). In A. S. Hoel & I. Folkvord (Eds.), *Ernst Cassirer on form and technology: Contemporary readings* (pp. 15–53). Palgrave Macmillan. (Original work published 1930)
- Cassirer, E. (2021e). *The philosophy of symbolic forms: Vol. 3. Phenomenology of cognition* (S. G. Lofts, Trans.). Routledge. (Original work published 1929)
- Chirimuuta, M. (2019). Cassirer and Goldstein on abstraction and the autonomy of biology [Preprint, August 2019 version; final version published in *HOPOS: The Journal of the International Society for the History of Philosophy of Science, 10*(2), 471–503, 2020].
- Chirimuuta, M. (2024). *The brain abstracted: Simplification in the history and philosophy of neuroscience*. MIT Press.
- Endres, T., & Truwant, S. (2024). Introduction: The 'functional ideal of truth' — A new key for Cassirer research. *Continental Philosophy Review, 57*, 269–288. https://doi.org/10.1007/s11007-024-09660-4
- Friedman, M. (2000). *A parting of the ways: Carnap, Cassirer, and Heidegger*. Open Court.
- Heidegger, M. (1991). *Kant und das Problem der Metaphysik* (F.-W. von Herrmann, Ed.; Gesamtausgabe, Vol. 3). Vittorio Klostermann. (Original work published 1929) [GA 3]
- Husserl, E. (2024). *Manuskripte zur Konstitution von Raumdingen: Aus den D-Manuskripten* (D. Lohmar, Ed.; Husserliana: Materialien, Vol. 11). Springer. https://doi.org/10.1007/978-3-031-65760-3
- Kant, I. (1900–). *Kants gesammelte Schriften* (Königlich Preußische Akademie der Wissenschaften, Ed.). Georg Reimer; Walter de Gruyter. [AA]
- Kant, I. (2000). *Critique of the power of judgment* (P. Guyer, Ed.; P. Guyer & E. Matthews, Trans.). Cambridge University Press.
- Kant, I. (2004). *Prolegomena to any future metaphysics that will be able to come forward as science: With selections from the Critique of pure reason* (G. Hatfield, Ed. & Trans.; Rev. ed.). Cambridge University Press.
- Kant, I. (2013b). Sobre o uso de princípios teleológicos na filosofia (M. Pires, Trans.; C. A. Martins, Rev.). *Trans/Form/Ação, 36*(1), 211–238.
- Kant, I. (2015). *Critique of practical reason* (M. Gregor, Trans.; Rev. ed.). Cambridge University Press.
- Kant, I. (2025). *Critique of pure reason* (P. Guyer & A. W. Wood, Eds. & Trans.; Rev. ed.). Cambridge University Press.
- Kinzel, K. (2024b). Between pluralism and objectivism: Reconsidering Ernst Cassirer's teleology of culture. *Journal of the History of Philosophy, 62*(1), 125–147.
- Kohler, G. (2008). Gemeinsinn oder: Über das Gute am Schönen. Von der Geschmackslehre zur Teleologie (§§ 39–42). In O. Höffe (Ed.), *Immanuel Kant: Kritik der Urteilskraft* (Klassiker Auslegen, Vol. 33) (pp. 137–150). Akademie Verlag.
- Krois, J. M. (2004). Ernst Cassirer's philosophy of biology. *Sign Systems Studies, 32*(1–2), 277–295.
- Longuenesse, B. (1998). *Kant and the capacity to judge* (C. T. Wolfe, Trans.). Princeton University Press. (Original work published 1993)
- Matherne, S. (2021). *Cassirer*. Routledge.
- Negarestani, R. (2018). *Intelligence and spirit*. Urbanomic; Sequence Press.
- Porta, M. A. G. (2007b). *A filosofia a partir de seus problemas* (3rd ed.). Edições Loyola. (Original work published 2002)
- Ng, K. (2021). Life. In J. Wuerth (Ed.), *The Cambridge Kant lexicon* (pp. 276–278). Cambridge University Press.
- Pringe, H. (2007). *Critique of the quantum power of judgment: A transcendental foundation of quantum objectivity*. Walter de Gruyter.
- Pringe, H. (2014). The principle of causality and the coordination of concepts and spatio-temporal objects in Cassirer's philosophy. *Idealistic Studies, 44*(1), 51–66.
- Pringe, H. (2022b). The thing in itself and the freedom of thought: On Cassirer's interpretation of critical philosophy. *Revue Roumaine de Philosophie, 66*(2), 261–278.
- Reath, A. (2021). Heteronomy. In J. Wuerth (Ed.), *The Cambridge Kant lexicon* (pp. 214–215). Cambridge University Press.
- Rohlf, M. (2021b). Regulative. In J. Wuerth (Ed.), *The Cambridge Kant lexicon* (pp. 384–386). Cambridge University Press.
- Ruin, H. (2012). Technology as destiny in Cassirer and Heidegger: Continuing the Davos debate. In A. S. Hoel & I. Folkvord (Eds.), *Ernst Cassirer on form and technology: Contemporary readings* (pp. 113–138). Palgrave Macmillan.
- Sellars, W. (2007). *In the space of reasons: Selected essays of Wilfrid Sellars* (K. Scharp & R. B. Brandom, Eds.). Harvard University Press.
- Skidelsky, E. (2008). *Ernst Cassirer: The last philosopher of culture*. Princeton University Press.
- Spigola, B. (2024). Cassirer's functionalist account of physical truth: Object, measurement and technology. *Continental Philosophy Review, 57*, 399–418.
- Totschnig, W. (2019). The problem of superintelligence: Political, not technological. *AI & Society, 34*(4), 907–920. https://doi.org/10.1007/s00146-017-0753-0
- Totschnig, W. (2020). Fully autonomous AI. *Science and Engineering Ethics, 26*(5), 2473–2485. https://doi.org/10.1007/s11948-020-00243-z
- Verene, D. P. (2011). *The origins of the philosophy of symbolic forms: Kant, Hegel, and Cassirer*. Northwestern University Press.
- Weiss, D. M. (2012). Failures of convergence. In A. S. Hoel & I. Folkvord (Eds.), *Ernst Cassirer on form and technology: Contemporary readings* (pp. 233–258). Palgrave Macmillan.
- Wuerth, J. (2021). Willkür. In J. Wuerth (Ed.), *The Cambridge Kant lexicon* (pp. 512–515). Cambridge University Press.

Rule for every document in this repository: no concept is attributed to an author without a verifiable reference, and every concept created by the author is declared as such.

---

Ítalo Santos Clemente (ISC). License: see [LICENSE](LICENSE).
