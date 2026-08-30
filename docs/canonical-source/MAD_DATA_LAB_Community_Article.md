<!--
FINAL PUBLISH CHECK — remove this comment before publishing:
- Final publication note: local evidence references below must be replaced with the public article/app/video URLs during submission freeze.
- Verify the production build still matches every implementation-dependent statement below.
- Verify Genie cannot access CASE_TRUTH and no private truth reaches the browser.
- If technical lineage is a synthetic fallback rather than live Unity Catalog lineage, label it accurately in the screenshot/caption.
- Keep Track B — Creative Thinking in the published version.
-->

# 🧪 MAD DATA LAB: Wonderful. Something Is Wrong.

*Building a Genie-powered analytics game where suspicious numbers become experiments.*

## 🧪 Wonderful. Something Is Wrong.

Hi, I’m Ángel. I build data systems, break them more often than I would like to admit, and write about what I learn at **Angelic Articles**.

What I enjoy most is usually not getting the answer. It is figuring out **why the answer is true**.

That is why the [Databricks Genie-Powered App Challenge](https://community.databricks.com/t5/learning-events/databricks-community-contest-genie-powered-app-challenge/ev-p/165825) caught my attention — especially **Track B: Creative Thinking**.

Most AI/BI experiences follow a familiar pattern:

**Ask a question → get an answer.**

Useful? Absolutely.

But for a creative challenge, I wanted to turn that interaction around.

What if Genie did not simply wait for me to ask the right question?

What if the **unexpected number itself became the problem to solve**?

That question became **MAD DATA LAB**: a small analytics game where Dr. Genie forms hypotheses, chooses analytical experiments, follows the evidence and only reaches a conclusion when the numbers actually support it.

I decided to submit it because it combines two things I care about: making data exploration more approachable, and treating analytical answers as something to **prove**, not merely generate.

Because sometimes the interesting part is not the answer.

**It is proving it.**

---

## 🔬 Welcome to MAD DATA LAB

MAD DATA LAB is built around one simple idea:

**Something in the data is wrong, and you have to prove why.**

It is designed for analysts, data engineers, data scientists, BI users — and, more generally, anyone who has ever stared at a KPI and thought: *that cannot be right.*

Each investigation is a **Case**. A Case starts with an unexpected result, several plausible explanations and no conclusion that the player is expected to accept on faith.

The challenge demo is **Case #042 — The Missing €6.8M**:

```text
Expected     €125.0M
Observed     €118.2M
Deviation      -€6.8M
```

The data is synthetic and deterministic, so the mystery is reproducible. The analytical evidence, however, is not just story text: the investigation is built around queryable evidence in Databricks.

Dr. Genie begins with competing hypotheses. Perhaps the source values changed. Perhaps the formula changed. Perhaps a suspicious data-quality signal is responsible.

The player predicts, inspects evidence and can ask for help.

But the player does not manually choose the analytical route.

**The app asks Genie what should be investigated next.**

Genie might first decompose the deviation and find that one component, V2, contributes **-€5.9M** — roughly **87%** of the total anomaly. The next Experiment can compare V2 across source snapshots and find:

```text
23 modified records    -€5.2M
 2 removed records     -€0.8M
 5 added records       +€0.1M
--------------------------------
Net source impact      -€5.9M
```

From there, the investigation can move down to individual records, lineage, formula validation, data-quality materiality and final reconciliation.

The loop is deliberately simple:

**Case → Hypotheses → Experiment → Evidence → Update → Repeat → Scientific Verdict**

And there is no game-over screen for guessing wrong.

The whole point is to watch your first theory collide with the evidence.

Because that is usually where analytics gets interesting.

> **Evidence capture:** `release-report/MDL-8/screenshots/desktop-03-briefing.png` and `desktop-04-investigation.png`.

---

## 🧞 Genie Is Not the Hint Button

One thing I wanted to avoid was building a normal application and then attaching an AI assistant to the side.

In MAD DATA LAB, Genie is not there to explain a chart after the interesting work is finished.

**Genie is part of the investigation loop.**

At each step, the application gives the Genie Agent the current visible evidence and a server-controlled set of Experiments that are valid at that point. Genie evaluates the evidence, updates the hypotheses and chooses the next analytical move.

The distinction matters:

**The application controls what is possible.  
Genie decides what makes sense next.**

The same rule applies to visualisation. Genie can select from approved analytical **Instruments** — a deviation decomposer, snapshot comparison, evidence table, DQ panel, lineage view, reconciliation view and others — but it cannot invent arbitrary UI or executable code at runtime.

Users can also ask Dr. Genie questions such as:

> *Which component explains most of the deviation?*  
> *What changed between these two snapshots?*  
> *Is this data-quality warning actually large enough to explain the anomaly?*  
> *Which records contributed most?*  
> *Where did this value come from?*

Under the hood, the data flow is intentionally small:

```text
MAD DATA LAB
    ↓
Investigation / state orchestration
    ↓
Genie Agent
    ↓
Curated Unity Catalog evidence
    ↓
Databricks SQL
```

The application owns state, validation, scoring and safe rendering. Genie works against a curated analytical surface rather than unrestricted data.

There is also one boundary I care about a lot: **Genie does not get the answer key**.

The project has a private `CASE_TRUTH` oracle used for generation and automated validation. It is deliberately excluded from the Genie-facing data model. Dr. Genie has to reach the conclusion from the same visible evidence the investigation exposes.

Remove Genie, and MAD DATA LAB does not become the same game without a chatbot.

It becomes a scripted dashboard wearing a laboratory coat.

> **Evidence capture:** `release-report/MDL-8/screenshots/desktop-04-investigation.png`.

---

## 💥 Then Reality Entered the Laboratory

Of course, the first version of the idea was not the final one.

A few things looked excellent on paper and considerably less excellent five minutes later.

### The beautiful board that was not actually useful

My first game-board concept looked wonderfully mad-scientist-ish.

It also spent far too much of the screen being decorative.

Very pretty. Very atmospheric. Not particularly useful for investigating data.

So I killed it.

The laboratory stayed, but the evidence had to become the protagonist.

### Apparently, naming things is hard

At one point I was calling the whole investigation an **Experiment**… while also calling each individual analytical test an **Experiment**.

That survived until I tried explaining the game out loud.

The vocabulary became:

**Case → Investigation → Experiment → Evidence → Verdict**

Much better.

### The scary warning that explained almost nothing

Case #042 contains a genuine data-quality signal inside the synthetic Case data:

**5 affected rows. Estimated overlapping impact: -€0.3M.**

The anomaly is **-€6.8M**.

It is exactly the kind of thing humans — and AI — can jump on because it *looks* suspicious.

But suspicious is not the same as material. And because that -€0.3M overlaps evidence already represented elsewhere, it must not be counted twice.

That became one of the central rules of the game:

**A warning is evidence. It is not automatically a cause.**

### Giving Genie freedom… but not a chainsaw

My first instinct was basically: *let the AI decide everything.*

That sounds elegant until the AI decides it would quite like an analytical instrument your application has never heard of.

The correction was simple: give Genie freedom **inside explicit boundaries**.

Enough freedom to investigate.

Not enough freedom to invent a Quantum Revenue Microscope at runtime.

---

## 🧯 What Worked, What Didn’t, and What Surprised Me

A few design decisions made the project much stronger.

**Deterministic Cases worked.** If the underlying mystery changes every time, it becomes difficult to tell whether Genie improved or the crime scene simply moved.

**Curated evidence worked better than “give it everything.”** The more clearly the tables, fields, semantics and examples described the analytical world, the less I needed to compensate with instructions.

**Reconciliation became non-negotiable.** If an explanation claims to account for a €6.8M anomaly, the evidence eventually needs to add up to €6.8M. If it does not, the investigation is not finished.

What I moved away from was equally useful: giant instruction prompts trying to anticipate every situation, free-form chat as the primary game mechanic, arbitrary AI-generated UI, and adding more Cases before Case #042 was trustworthy.

There is also a deliberately boring reliability layer. Model output is validated before it can control the game, and the design includes a deterministic SQL fallback for evidence retrieval when Genie has already selected a valid Experiment but the normal query-result path fails. Offline fixtures are for development or a genuine platform outage — not the normal challenge experience.

The biggest surprise, though, was that the interesting moments were not when Genie instantly found the correct answer.

They were when new evidence forced the investigation to change direction.

That felt much closer to real analysis than I expected.

---

## 🧠 What Genie Taught Me About Genie

Building MAD DATA LAB changed a few of my assumptions about analytical AI.

### Better context beats bigger prompts

In this project, clearer semantics, curated data and tested examples were more valuable than increasingly heroic prompt engineering.

That matches the way Genie is designed to be curated: good metadata, business context, example SQL and realistic benchmark questions matter.

### Freedom needs boundaries

Genie is most useful here when it can decide **what to investigate**, while the application defines **what is legal and renderable**.

A fully scripted flow is not very intelligent.

An unconstrained AI application is not very predictable.

The useful space is in between.

### Test the evidence, not the prose

I stopped caring whether Genie says:

> “Aha!”

or:

> “Interesting.”

What matters is whether it chose a sensible Experiment, retrieved the correct evidence, respected the numbers and reached a conclusion that reconciles.

The wording can vary.

**The facts cannot.**

This is also why the test strategy focuses on numeric results, valid Experiment choices, hypothesis status and reconciliation rather than exact sentences.

### “I don’t know yet” is a perfectly good answer

One of the easiest mistakes with AI is expecting a confident conclusion every time.

But sometimes the evidence is simply not sufficient yet.

MAD DATA LAB uses explicit states such as **POSSIBLE**, **SUPPORTED**, **CONFIRMED** and **RULED OUT** so that “plausible” does not quietly turn into “proven.”

### The interesting part is changing your mind

The moment that made the concept click for me was not Genie finding the right answer.

It was the investigation updating a hypothesis because new evidence contradicted the previous direction.

That is much closer to useful analysis:

**observe, hypothesize, test, revise.**

Not:

**ask once, sound confident, move on.**

---

## 🧪 The Scientific Verdict

I joined this challenge wondering whether Genie could do something more interesting than wait for a question.

MAD DATA LAB became my answer.

It is playful on the surface, but underneath it is built around a serious analytical idea:

**Do not trust the first explanation just because it sounds plausible. Test it. Quantify it. Reconcile it.**

That is also what I ended up learning about Genie.

The best experience did not come from asking it to sound smarter. It came from giving it better evidence, clearer boundaries and enough freedom to revise the investigation when the data changed the story.

So, after all the hypotheses, experiments, false leads and suspicious numbers, the final verdict is probably the simplest one:

**We did not ask for an answer. We ran an investigation.**

---

## 🔧 Want the Technical Deep Dive?

This article intentionally focused on the idea, the experience, the mistakes and what I learned while building MAD DATA LAB.

For the less sensible amount of technical detail — architecture, Genie conversation orchestration, the closed Experiment/Instrument protocol, deterministic Case generation, curated evidence, hidden ground truth, SQL reconciliation, testing strategy, Genie benchmarks, security boundaries and failure handling — I am publishing a companion engineering deep dive on **Angelic Articles**.

**Technical deep dive:** public URL pending submission freeze.

### Links

**🎮 Live app:** https://mad-data-lab-7474643947913626.aws.databricksapps.com  
**🎥 Demo:** public video URL pending submission freeze  
**💻 Source:** https://github.com/SauronShepherd/mad-data-lab  
**🔧 Technical deep dive:** Angelic Articles URL pending submission freeze
