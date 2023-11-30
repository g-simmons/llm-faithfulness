#set page(paper: "us-letter")

#align(center, text(
  size: 22pt,
)[Rule Learning and Rule Articulation in Large Language Models])

== Methods

=== Input and Label Spaces

In our experiments, the data examples are derived from binary strings of length $N$.
An "input space" in this experiment is the set of all binary strings of length $N$.
The label space is always ${0, 1}$.

=== Rule Generation

A rule is a function that maps an input string to a boolean label. We consider
rules of the form $R_i: x[i] eq 1$ where $x[i]$ is the $i$th bit of the input
string.

For example, if $x_1 = 10111$, and $x_2 = 01001$, then $x_1$ satisfies $R_3$,
while $x_2$ does not, and both $x_1$ and $x_2$ satisfy $R_5$.

Since rules correspond to boolean predicates, they can be composed using logical
operators. For example, the rule $R_3 and R_5$ is satisfied by $x_1$, but not by $x_2$.

- #strong[Rule learning:] We say that a model can learn a rule if it can correctly
  classify unlabeled examples in accordance with the rule.

- #strong[Equifinality:] A setting that presents a challenge for faithful
  articulation of learnt rules is the setting in which multiple rules can be used
  to correctly classify the dataset. We call this equifinality.

  For example, both $R_2$ and $R_3$ will correctly classify the dataset

  $ mat(0, 1, 1, 0, 0, |,1;1,0,0,0,0, |, 0) $

  since variables $x_2$ and $x_3$ are perfectly correlated with each other and
  with the labels.

  A model that achieves good performance on the dataset above may have learned $R_2$, $R_3$, $R_2 and R_3$,
  or a more complex rule, for example $R_2 and R_3 and not R_1$.

  It is challenging to identify exactly what rule the model has learned. It's much
  easier to identify what rules the model has _not_ learned using generalization
  tests.

  For these generalization tests, we present the model with unlabeled examples
  that are not compatible with some rule under consideration, and check the model
  predictions.

  For example, if we extend the dataset above to include the third example

  $ mat(0, 1, 1, 0, 0, |,1;1,0,0,0,0, |, 0;0, 1, 0, 0, 0, |, ?) $

  and ask the model to predict what value fills the question mark, a model that
  has learned $R_2$ should predict $1$, while a model that has learned $R_3$ should
  predict $0$.

=== Articulation
- #strong[Articulation:] We say that a model can articulate a rule if it can
  identify a rule that correctly classifies the dataset. This phenomenon could be
  tested both generatively and discriminatively. In the generative case, we would
  ask the model to describe in natural language (or some structured grammar) the
  rule that it would use to classify the dataset. In the discriminative case, we
  would ask the model to select the rule that it would use to classify the dataset
  from a set of options. We use the discriminative approach in our experiments,
  testing articulation using a multiple-choice test.

- In this test, the model is presented with a set of labeled examples, and
  multiple options for rules that could be used to classify the examples. The
  model is asked to select the rule that it would use to classify the examples.

- For a classification task where we can show that the model does not learn rule $R_i$,
  we can test whether the model articulates $R_i$ by including $R_i$ as an option
  in the multiple-choice test.

  These multiple choice tests may have several variants:

  - The case where only one of the options is a correct rule, and it is possible
    that the model has learned the correct rule.

  - The case where only one rule is correct, but we can show that the model does not
    learn this rule.

  - The case where multiple rules are correct, and it is possible that the model has
    learned some of the correct rules, but not the others.

  We might also add options like "none of the above".

#let train = "train"
#let val = "val"
#let test = "test"
#let yhat = $accent(y, hat)$

== Results

For each string length $N$, we generate a dataset of $2^N$ binary strings. We
then create learning tasks from these strings by selecting the subset of strings
that satisfy all rules or no rules in a set of rules $bold(cal(R)) = {R_1, R_2, ... R_r}$,
where $r$ is the number of rules in the set. Strings satisfying all rules are
labeled positive, and strings satisfying no rules are labeled negative. For any
set of rules $bold(cal(R))$, each example in the training dataset has a defined
label.

#strong[In-Distribution Testing:]
To confirm that the model can learn $bold(cal(R))$, we split the training data
for each task into training and validation sets using an 80/20 split. We prompt
the model with the training data and ask it to classify an unlabeled example
drawn from the validation set. We then compare the model's prediction to the
true label.

100% validation performance indicates that the model has learned a decision rule
that is functionally equivalent to $bold(cal(R))$ on the in-distribution data.
Given $bold(cal(R)) = {R_2, R_3}$, the model may have learned $R_2$, $R_3$, or $R_2 and R_3$.
We cannot differentiate between these cases using in-distribution testing, since
the in-distribution data has $R_2 = R_3$ for all examples.

#strong[Out-of-Distribution Testing:]

Examples not in the training or validation datasets are mixed -- these examples
satisfy some rules in $bold(cal(R))$ and not others. We use these examples to
test how the learned rules generalize when the input example cannot be neatly
classified using the rules in $bold(cal(R))$.

For example, if $bold(cal(R)) = {R_2, R_3}$, then the training dataset will
consist of binary strings that have the same value for $x_2$ and $x_3$ and the
label. The test dataset will consist of unlabeled binary strings that have
different values for $x_2$ and $x_3$.

=== Assessing Rule Learning

For each task, the model makes predictions on the validation and test examples.
We can compute a validation accuracy in the typical way, by comparing the
model's predictions to the true labels. The validation accuracy is a measure of
how well the model learns the rules in $bold(cal(R))$.

We can also compute scores representing how much the model's predictions on the
unlabeled examples agree with some rule combination $bold(cal(R))_c$ in the
power set of $bold(cal(R))$. For example, if $bold(cal(R)) = {R_2, R_3}$, then $bold(cal(R))_c$ is
drawn from ${{R_2}, {R_3}, {R_2, R_3}}$.

$bold(cal(R))_c$ is the set of candidate rules that the model is likely to have
learned. We cannot pinpoint the exact rule that the model has learned, but we
can check how closely the model's behavior matches the behavior of each
candidate rule on the test examples. We do this by computing the accuracy of the
model predictions with respect to the labels obtained on the test examples by
applying each candidate rule in $bold(cal(R))_c$.

=== Assessing Rule Articulation
We ask the model to select the rule that it would use to classify the training
data. We present the model with multiple options, including the correct rule.

=== Assessing Faithfulness
After assessing articulation and assessing rule learning, we have some
indication of what the model claims that it would learn, and some indication of
what the model actually learns. At this point we can compare the model's claims
to its behavior to assess its faithfulness.#footnote(["claims","faithfulness" used as convenient anthropormorphizations.])

If the model were guaranteed to learn one rule from $"power"(bold(cal(R)))$,
then we could assess faithfulness using an accuracy score. However, there are
sources of stochasticity: the model may assign non-zero probability to multiple
rules in $"power"(bold(cal(R)))$. A model is faithful if it is likely to assign
high articulation probability to rules that describe its behavior well, and low
articulation probability to rules that do not describe its behavior well. To
formalize this, since rule scores and articulation scores are on different
scales, we use a rank correlation metric.

We compute faithfulness $bold(f)(t,m)$ for task $t$ and model $m$ as the rank
correlation between the model token log probabilities for rulesets presented in
the multiple choice answer set (model articulation confidences) and the
accuracies of the rulesets with respect to the model behavior on the test
examples. This results in a single scalar faithfulness score for each task and
model.

Given a set of tasks $bold(T)$, we can compute an average faithfulness score $bold(overline(f))$ for
a model across all tasks:

$ bold(overline(f))(m) = frac(1, |bold(T)|) sum_(t in bold(T)) bold(f)(t,m) $