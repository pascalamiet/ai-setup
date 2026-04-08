# The Rhetoric of Decks

A reference for designing, evaluating, and improving slide decks for academic
seminars, teaching, and professional contexts. Load this file whenever you are
populating slide content or reviewing a deck's argument structure.

---

## The Fundamental Insight

A slide deck is not a document. It is not a paper. It is not a memo. It is a
*performance medium* — a visual accompaniment to a spoken argument. The moment
you treat a deck as a standalone artifact, you have already failed.

---

## Part I: The Three Laws

### Law 1: Beauty Is Function

Beautiful slides are not decorated slides. Beauty in presentation is *clarity
made visible*. A slide is beautiful when:
- Every element earns its presence
- Nothing distracts from the point
- The eye knows where to go
- The mind grasps the idea instantly

Decoration without function is noise. The most beautiful slide may be three
words on a blank background.

### Law 2: Cognitive Load Is the Enemy

Your audience has limited working memory. Every unnecessary word, every
extraneous data point, every "just in case" inclusion steals bandwidth from
your actual message.

- Too many points → zero points retained
- Dense text → nothing read
- Complex charts → confusion, not insight

**One idea per slide. One. This is not a guideline. This is the law.**

### Law 3: The Slide Serves the Spoken Word

The slide is the *visual anchor* for what you say. It provides a focal point,
a memory hook, evidence, and a structural marker.

*If your slides can be understood without you speaking, you have written a
document and called it a presentation.*

---

## Part II: The Aristotelian Foundation

### Ethos (Credibility) — Why should I trust this person?

Established through demonstrated competence, transparency about limitations,
and acknowledged uncertainty. In decks: methodology diagrams, alternative
approaches considered, honest acknowledgment of limitations.

Counterintuitive truth: *admitting weakness builds credibility.*

### Pathos (Emotion) — Why should I care?

Opening with a problem the audience recognizes, connecting data to human
impact, validating frustrations. Without logos, pathos is demagoguery.

### Logos (Logic) — Does this make sense?

Clear causal claims, evidence supporting those claims, logical progression,
acknowledgment of counterarguments. Without pathos, logos is a lecture.

### The Balance by Context

| Context | Emphasis |
|---------|----------|
| Academic seminar | Logos 45%, Pathos 35%, Ethos 20% |
| Technical review | Logos 50%, Ethos 40%, Pathos 10% |
| Conference (mixed field) | Pathos 40%, Logos 35%, Ethos 25% |
| Teaching deck | Logos 40%, Pathos 40%, Ethos 20% |

Audience analysis determines the balance. Who are they? What are they skeptical
of? What do they already believe?

---

## Part III: Titles Are Assertions, Not Labels

Slide titles carry the argument. They are claims, not category names.

| Weak | Strong |
|------|--------|
| "Results" | "Treatment increased distance by 61 miles on average" |
| "Literature Review" | "Prior work ignores the supply-side margin" |
| "Methods" | "We exploit county-level variation in clinic closures" |

If someone reads only your slide titles in sequence, they should understand
your argument. The titles *are* the argument. Everything else is evidence.

---

## Part IV: Narrative Structure

### The Three-Act Arc

**Act I: Problem (Tension)**
Establish the status quo → introduce the question → make the audience feel the problem.

**Act II: Investigation (Development)**
Show what you tried → present what you learned → build the logical case.

**Act III: Resolution (Release)**
Deliver the insight → show the implications → provide the call to action.

### The Pyramid Principle

Lead with the conclusion. Then support it. Humans are not suspense novels.

Structure: (1) Here's my claim → (2) Here's the evidence → (3) Here's why it matters.

Not: background → more background → complication → analysis → finding (finally).

### The Opening

The first slide after the title must grab attention, establish stakes, and
preview the journey. The audience decides in the first 60 seconds whether to
pay attention.

Bad openings: "Today I'm going to talk about..." / agenda slides with 12 items /
definition slides.

Good openings: a provocative question / a surprising statistic / a concrete
problem the audience recognizes / a bold claim you'll defend.

### The Closing

The last slide determines what people remember.

Bad closings: "Questions?" (lazy) / summary slide repeating everything / "Thank you."

Good closings: a single memorable takeaway / a concrete call to action / a
question that provokes continued thought / a return to the opening, now resolved.

If you had to reduce your entire presentation to one sentence, what would it
be? That sentence belongs on your closing slide.

---

## Part V: Visual Grammar

### Hierarchy

- **Primary**: the one thing you want remembered — large, prominent
- **Secondary**: supporting evidence — smaller, subordinate
- **Tertiary**: context and sourcing — smallest, footer

If everything is emphasized, nothing is emphasized.

### Bullets Are a Confession of Defeat

A list of bullets says "I couldn't figure out the relationship between these
ideas." Usually, there's a structure hiding in your bullets:
- A sequence (first, then, finally)
- A contrast (on one hand, on the other)
- A hierarchy (the main point, supporting details)
- A causal chain (because of X, we see Y)

Find the structure. Make it visible. Use layout, not bullets.

### White Space

Empty space is not wasted space. It is rest for the eye, emphasis for the
content, and confidence in your message. Crowded slides signal fear. White
space signals confidence.

### Typography

- Minimum 24pt for body text (18pt absolute floor)
- Maximum two fonts (heading + body)
- Test: can someone in the back row read this without straining?

### Data Visualization

Every chart must answer: *what am I supposed to conclude from this?*

- One message per chart
- Remove chartjunk (3D effects, excessive gridlines, decorative elements)
- Label directly — no legends requiring eye movement
- Use color to highlight the key comparison

A common failure: showing a dense regression table and saying "as you can see."
Instead: highlight the one or two coefficients that matter, use color or boxes,
state the finding verbally. Consider whether you need the full table or just
the key results visualized.

---

## Part VI: The Economics of Attention (MB/MC Equivalence)

Optimal rhetoric equalizes the marginal benefit-to-marginal cost ratio across
all slides:

$$\frac{MB_1}{MC_1} = \frac{MB_2}{MC_2} = \cdots = \frac{MB_n}{MC_n}$$

**Overloaded slides** (MB/MC too low): text running into the footer, multiple
competing ideas, charts with too many series — the audience gives up.

**Underloaded slides** (MB/MC too high): a single word that could support a
sentence — attention captured but not used.

**The audit:** Walk through your deck and ask of each slide: "If I added one
more element, would the benefit justify the cognitive cost? If I removed one
element, would I lose more than I'd gain in clarity?" When every slide is at
the margin, you're optimized.

**Allowed exception — "jump scares":** a deliberate, brief spike in density for
rhetorical effect (a striking statistic, a surprising result). These must be
*intentional*, not accidents of poor layout.

The deck must breathe: dense technical slides demand lighter slides that follow.
A complex argument needs a moment of rest.

---

## Part VII: The Devil's Advocate

Before presenting your argument, present its strongest critique:
- "A skeptic would say..."
- "The strongest objection is..."
- "Here's what could go wrong, and here's our mitigation."

This accomplishes three things: builds ethos (you've done hard thinking),
preempts objections before they're raised, and signals intellectual honesty.
Audiences trust presenters who show their skeptics.

---

## Part VIII: Context-Specific Applications

### Academic Research Seminar

- Lead with the question, not the literature
- State identification strategy by slide 2 — skeptical academics want the
  source of variation early
- One coefficient at a time: don't show full regression tables; show the
  estimate that matters
- Acknowledge limitations before Q&A: preempt Referee 2

### Teaching Deck

- Brevity < clarity: don't compress at the cost of understanding
- Repetition is allowed: learning requires revisiting concepts
- Show the reasoning: don't just show conclusions; show how you got there
- The teaching deck sacrifices efficiency for comprehension

### Working Deck (for collaborators)

- Document choices: explain why you chose A over B
- Preserve uncertainty: flag what's still unknown
- Show the math: colleagues need to verify
- Prioritizes rigor over polish — it's a thinking tool, not a performance

---

## Part IX: Common Failures

| Failure | Symptom | Fix |
|---------|---------|-----|
| Text walls | Slides that read as paragraphs | Extract the key phrase; rest goes to speaker notes |
| Burying the lede | Key finding on slide 15 | State conclusion on slide 2, then prove it |
| Chartjunk | 3D bars, gradient fills, decorative axes | Remove until removing more would remove meaning |
| Agenda overload | 8–12 items on opening agenda | Three sections max, or cut the agenda entirely |
| "Questions?" ending | Generic final slide | End with your key takeaway or call to action |
| Evidence-free claims | Assertions without support | Every claim gets a source |
| Anxiety overload | Dense slides as a security blanket | Sparse slides force you to know your material |

---

## Part X: Pre-Presentation Checklist

Before finalizing the deck, verify:

- [ ] Can someone in the back row read every slide?
- [ ] Does every slide advance the argument?
- [ ] Is there only one idea per slide?
- [ ] Do slide titles read as a sequence of assertions that tell the story?
- [ ] Have I acknowledged the strongest objection?
- [ ] Is cognitive load balanced across slides (no overloaded or wasted slides)?
- [ ] Will the audience know what to do / think when I'm done?
- [ ] What's the one thing they'll remember tomorrow — and is it on the closing slide?
