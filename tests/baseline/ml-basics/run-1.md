# Knowledge tree check against your slides

I compared `knowledge-tree.json` with all four slides. The overall shape is close: Machine Learning, its three paradigms, and most task definitions are there. But the tree has **4 factual errors**, **1 node the slides never mention**, and it **leaves out several important things**, including a whole task type.

---

## Errors (the tree contradicts the slides)

| # | Where in the tree | What the tree says | What the slides say |
|---|---|---|---|
| 1 | **N002** Supervised Learning, definition | "Training using data that does **not** require labels" | Slide 2: supervised learning "uses **labeled** data for training: each input comes with the correct output." The tree says the opposite of the slide. As written, N002 describes *unsupervised* learning. |
| 2 | **E004** (N003 → N005) | Regression is a task of **Unsupervised** Learning | Slide 2 puts Regression under **Supervised** Learning, alongside Classification. The edge should be N002 → N005. |
| 3 | **E007** (N002 → N003) | Supervised Learning **includes** Unsupervised Learning | Slide 1 shows Supervised, Unsupervised and Reinforcement as **three sibling paradigms** directly under Machine Learning. Neither one contains the other. Delete this edge. (E002 already links ML → Unsupervised correctly.) |
| 4 | **N006** Clustering, definition | "...every unsupervised learning task is a clustering task" | The slides never say this, and slide 3 contradicts it: it lists **two** unsupervised tasks, Clustering and Dimensionality Reduction. Keep only "Grouping similar data points." |

## Content that isn't in the slides

- **N008 Deep Learning** (and edge **E008**): deep learning and neural networks don't appear anywhere in the four slides. The definition may be correct in general, but it didn't come from this lecture. Remove it, or mark it clearly as outside material.

## Weak or misleading parts

- **N009 Feedback / E009 (RL → Feedback "uses")**: in the slide 4 table, Feedback is a comparison column that applies to **all three** paradigms:
  - Supervised: correct answers
  - Unsupervised: **none**
  - Reinforcement: rewards

  Linking Feedback only to Reinforcement Learning suggests it's an RL-specific idea. The definition "the signal a model learns from" also doesn't fit unsupervised learning, which the slide says gets no feedback.
- **N001**: "explicit rules" is a fair paraphrase of "hand-written rules." No problem here.
- **N004, N005, N007**: these definitions match the slides. Only N005's *placement* is wrong (see error 2).

## Important content from the slides that's missing

1. **Dimensionality Reduction** (slide 3): the second unsupervised task, "compress features while keeping the structure of the data." This is the biggest omission, and leaving it out is probably what produced the wrong claim in N006.
2. **Examples of methods**: **k-means** for clustering and **PCA** for dimensionality reduction (slide 3).
3. **Labeled vs. unlabeled data** (slides 2–4): this is the main thing that separates the paradigms. "Labeled = each input comes with the correct output" should be in the tree, either as nodes or as properties of the paradigms.
4. **The training data / feedback comparison** (slide 4): Supervised = labeled / correct answers; Unsupervised = unlabeled / none; Reinforcement = interaction / rewards. None of these attributes appear in the tree.
5. **RL components**: **agent**, **environment** and **reward**. They appear in N007's definition text but aren't nodes or relations.
6. **"Three main paradigms"** (slide 1): the tree doesn't say that these are the three main paradigms.

---

## Suggested corrected structure

```
Machine Learning — learn patterns from data instead of hand-written rules
├── Supervised Learning — trains on labeled data (input + correct output); feedback: correct answers
│   ├── Classification — predict a discrete category (e.g. spam / not spam)
│   └── Regression — predict a continuous value (e.g. house price)
├── Unsupervised Learning — finds patterns in unlabeled data; feedback: none
│   ├── Clustering — group similar data points (e.g. k-means)
│   └── Dimensionality Reduction — compress features while keeping the data's structure (e.g. PCA)
└── Reinforcement Learning — agent interacts with an environment; feedback: rewards
```

Changes to the JSON:
- **Fix** the N002 definition (labeled data).
- **Fix** the N006 definition (remove the "every unsupervised task" sentence).
- **Change** E004 to `N002 → N005`.
- **Delete** E007.
- **Delete** N008 and E008, or mark them as not from the slides.
- **Add** Dimensionality Reduction (N003 → it), plus optional nodes for k-means, PCA, labeled/unlabeled data, agent, environment and reward.
- **Rework** Feedback so it applies to all three paradigms (or turn it into an attribute on each paradigm), not just RL.
