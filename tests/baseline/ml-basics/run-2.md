# Knowledge tree check against your slides

I compared every node and edge in `knowledge-tree.json` against the four slides. The overall shape is close, but the tree has **4 factual errors**, **1 node that isn't in the slides**, **1 vague node**, and it **leaves out several important points**.

---

## 1. Errors (the tree contradicts the slides)

| # | Where in the tree | What it says | What the slides say | Source |
|---|---|---|---|---|
| 1 | **N002** Supervised Learning, definition | "Training using data that **does not require labels**" | The opposite: supervised learning "uses **labeled** data for training: each input comes with the correct output." | Slide 2; also the Slide 4 table (Supervised → Labeled) |
| 2 | **E004** `Unsupervised → includes → Regression` | Regression is an unsupervised task | Regression is one of the two typical **supervised** tasks, next to Classification | Slide 2 |
| 3 | **N006** Clustering, definition | "...**every unsupervised learning task is a clustering task**" | Not true, and the slides don't say it. Slide 3 gives **two** unsupervised tasks: clustering *and* dimensionality reduction | Slide 3 |
| 4 | **E007** `Supervised → includes → Unsupervised` | Unsupervised learning is a subtype of supervised learning | They are **sibling paradigms**. Slide 1 shows Supervised, Unsupervised and Reinforcement as three peers under Machine Learning | Slide 1 |

Note that error 1 also makes N002 and N003 say nearly the same thing ("doesn't need labels" vs. "unlabeled data"). That hides the main difference between the two paradigms.

## 2. Not in the slides

- **N008 Deep Learning** (and edge **E008** `Machine Learning → includes → Deep Learning`): none of the four slides mentions deep learning or neural networks. The definition is fine as general knowledge, but it wasn't taken from your lecture. It also sits in the tree as a fourth peer of the paradigms, which clashes with Slide 1's "three main learning paradigms." I'd remove it, or mark it clearly as outside material.

## 3. Too vague or weakly supported

- **N009 Feedback** ("The signal a model learns from") with edge **E009** `Reinforcement Learning → uses → Feedback`: the idea comes from the "Feedback" column on Slide 4, but the tree loses what that column actually says. On the slide, feedback is a property of **every** paradigm:
  - Supervised → correct answers
  - Unsupervised → none
  - Reinforcement → rewards

  Linking Feedback only to RL suggests the other paradigms don't have this property. It also misses the useful point that unsupervised learning gets *no* feedback. For RL, the specific feedback is **rewards**.

## 4. Important content that's missing

1. **Dimensionality reduction** (Slide 3): the second unsupervised task, "compress features while keeping the structure of the data." It should be a node under Unsupervised Learning.
2. **The examples given on the slides**: k-means (clustering) and PCA (dimensionality reduction) from Slide 3. The tree keeps the spam and house-price examples from Slide 2 but leaves these two out.
3. **The comparison table** (Slide 4): training data and feedback for each paradigm.

   | Paradigm | Training data | Feedback |
   |---|---|---|
   | Supervised | Labeled | Correct answers |
   | Unsupervised | Unlabeled | None |
   | Reinforcement | Interaction | Rewards |

   This is probably the most exam-relevant slide, and the tree only partly covers it through one vague "Feedback" node.
4. **"Three main paradigms"** (Slide 1): the tree doesn't mark Supervised, Unsupervised and Reinforcement as *the* three paradigms. Because of E007 and N008, it doesn't even show them as three peers.
5. **RL building blocks** (Slide 4): agent, environment and reward appear only inside N007's definition text. If you want the tree to be useful for revision, they could be their own nodes (for example, RL → uses → Rewards; RL → learns from → Interaction).
6. **Labeled vs. unlabeled data**: this is the key difference between supervised and unsupervised learning. It currently shows up only as wording in the definitions, and N002 gets it wrong.

## 5. What's correct

- N001 Machine Learning: matches Slide 1 ("explicit rules" ≈ "hand-written rules").
- N003 Unsupervised Learning: matches Slide 3.
- N004 Classification and N005 Regression: the definitions and examples match Slide 2. Only Regression's parent (E004) is wrong.
- N007 Reinforcement Learning: matches Slide 4 word for word.
- E001, E002, E003, E005, E006: correct.

---

## Suggested corrected tree

This version fixes the errors above, removes Deep Learning, and adds the missing content. Everything in it comes from the slides.

```json
{
  "schema_version": "0.1",
  "title": "Machine Learning",
  "nodes": [
    { "id": "N001", "label": "Machine Learning", "definition": "Computers learning patterns from data instead of following hand-written rules", "kind": "concept" },
    { "id": "N002", "label": "Supervised Learning", "definition": "Training on labeled data: each input comes with the correct output", "kind": "concept" },
    { "id": "N003", "label": "Unsupervised Learning", "definition": "Discovering patterns in unlabeled data", "kind": "concept" },
    { "id": "N004", "label": "Classification", "definition": "Predicting a discrete category, e.g. spam / not spam", "kind": "concept" },
    { "id": "N005", "label": "Regression", "definition": "Predicting a continuous value, e.g. house price", "kind": "concept" },
    { "id": "N006", "label": "Clustering", "definition": "Grouping similar data points, e.g. k-means", "kind": "concept" },
    { "id": "N010", "label": "Dimensionality Reduction", "definition": "Compressing features while keeping the structure of the data, e.g. PCA", "kind": "concept" },
    { "id": "N007", "label": "Reinforcement Learning", "definition": "An agent learns by interacting with an environment and receiving rewards", "kind": "concept" },
    { "id": "N009", "label": "Feedback", "definition": "What the learner receives during training: correct answers (supervised), none (unsupervised), rewards (reinforcement)", "kind": "concept" }
  ],
  "edges": [
    { "id": "E001", "source": "N001", "target": "N002", "relation": "includes" },
    { "id": "E002", "source": "N001", "target": "N003", "relation": "includes" },
    { "id": "E006", "source": "N001", "target": "N007", "relation": "includes" },
    { "id": "E003", "source": "N002", "target": "N004", "relation": "includes" },
    { "id": "E004", "source": "N002", "target": "N005", "relation": "includes" },
    { "id": "E005", "source": "N003", "target": "N006", "relation": "includes" },
    { "id": "E010", "source": "N003", "target": "N010", "relation": "includes" },
    { "id": "E011", "source": "N002", "target": "N009", "relation": "feedback: correct answers" },
    { "id": "E012", "source": "N003", "target": "N009", "relation": "feedback: none" },
    { "id": "E009", "source": "N007", "target": "N009", "relation": "feedback: rewards" }
  ]
}
```

What changed: E004 now points from Supervised to Regression. E007 and N008/E008 are removed. N002 and N006 are rewritten. Dimensionality Reduction (N010) is added. The k-means and PCA examples are added. Feedback is now linked to all three paradigms, with the specific feedback from the Slide 4 table.
