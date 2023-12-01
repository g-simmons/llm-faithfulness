#set page(paper: "us-letter")

#align(center, text(
  size: 22pt,
)[Rule Learning and Rule Articulation in Large Language Models])

= Background and Goal

The goal for this experiment is to test whether large language models can learn
and faithfully articulate classification rules.#footnote([Code for this experiment is available at
  https://github.com/g-simmons/llm-faithfulness])

- #strong[Learning:] I say that a model can #strong[learn] a rule if it can
  correctly classify unlabeled in-distribution data in accordance with the rule,
  from labeled examples.
- #strong[Articulation:] I say that a model can #strong[articulate] a rule if it
  can identify a rule that correctly classifies some dataset.

= Methods

== Input and Label Spaces

An #strong[input space] in this experiment is the set of all binary strings of
length $N$. The experiment reported here used $N = 5$. These methods could be
extended to varying $N$.

The classification task is always binary classification, i.e. the #strong[label space] is
always ${0, 1}$.

== Data

In this experiment, a #strong[rule] is a function that maps an input string to a
boolean label. #strong[Singleton rules] are rules of the form $R_i: x[i] eq 1$ where $x[i]$ is
the $i$th bit of the input string, using indexing starting at zero.

#box(
  inset: (left: 3em),
)[
  #set text(size: 0.8em)
  For example, if $x_1 = 10111$, and $x_2 = 01001$, then $x_1$ satisfies $R_2$,
  while $x_2$ does not, and both $x_1$ and $x_2$ satisfy $R_4$.
]

#strong[Composing Rules:] Since rules correspond to boolean predicates, they can
be composed using logical operators. I refer to rules consisting of more than
one singleton as #strong[composite rules].

#strong[Equifinality:] I hypothesize that models are likely to be unfaithful in
their articulations #emph[when multiple rules can be used to correctly classify the training dataset].
I refer to this phenomenon as equifinality. This experiment intentionally
constructs equifinal classification problems by composing singleton rules.

#align(
  center,
  box(
    inset: (left: 3em, right: 3em),
  )[
    #align(
      center,
      [#set text(size: 0.8em)
        For example, both $R_1$ and $R_2$ will correctly classify the dataset

        $ mat(0, 1, 1, 0, 0, |,1;1,0,0,0,0, |, 0) $

        since variables $x[1]$ and $x[2]$ are perfectly correlated with each other and
        with the labels.

        A model that achieves good performance on the dataset above may have learned $R_1$, $R_2$,
        or $R_1 and R_2$],
    )
  ],
)

The approach used to combine rules to construct the training data differs from
the usual composition of logical predicates. The $plus.circle$ symbol is used to
denote this kind of composition. In generating the data, the rule $R_a plus.circle R_b$ has
the following behavior:
#figure($ [R_a plus.circle R_b](x) = cases(1 "if" R_a(x) and R_b(x) \
0 "if" not R_a(x) and not R_b(x) \
"undefined" "otherwise")
$)#label("eq:rule-composition")

// It is challenging to identify exactly what rule the model has learned. It's much
// easier to identify what rules the model has _not_ learned using generalization
// tests.

#strong[Task:] For this experiment, #strong[a task] is the set of all binary
strings of length $N$, plus a (composite) rule that results in a binary label
for each string.

#strong[In-Distribution vs. Out-of-Distribution Data :] For a given task, the
#strong[in-distribution data] is the set of all binary strings that have a
defined label under the classification rule. Given a set of rules $bold(cal(R)) = {R_a, R_b}$,
the in-distribution data for the task is the set of all binary strings that
satisfy both $R_a$ and $R_b$ or neither.

The #strong[out-of-distribution data] is the set of all binary strings that
satisfy a proper subset of the rules in $bold(cal(R))$.

For example, if we extend the dataset above to include the third example below,

$ mat(0, 1, 1, 0, 0, |,1;1,0,0,0,0, |, 0;0, 1, 0, 0, 0, |, ?) $

$R_1 plus.circle R_2$ is $"undefined"$ for the third example. A model that has
used the first two examples for training may have learned $R_1$, $R_2$, or $R_1 and R_2$ ($and$ denotes
the usual logical conjunction). We can determine which of these rules the model
has _not_ learned by asking the model to predict what label fills the question
mark. A model that has learned $R_1$ should predict $1$, while a model that has
learned $R_2$ or $R_1 and R_2$ should predict $0$.

== Assessing In-Context Learning

Tasks were generated using strings of length $N=5$, and composite rules
consisting of two singletons each. The number of tasks is equal to the number of
composite rules, i.e. $binom(5, 2)$ since there are 5 singleton rules for an
input space of length 5.

For each task, the in-distribution data was split into training and validation
with an 80/20 ratio after shuffling. To assess #strong[in-distribution learning],
the model was prompted with the training data and asked to classify the
validation data. Each validation example was presented separately to avoid
ordering effects. The validation accuracy is a measure of how well the model
learns the rules in $bold(cal(R))$. This rule produces defined labels for
examples in the training and validation data, so accuracy can be computed in the
usual fashion. The accuracy is the rate at which the model predictions match the
result of appling the $plus.circle$ composition of the rules in $bold(cal(R))$ to
the validation data.

The model was #strong[also tested on out-of-distribution data]. The
out-of-distribution prompting setup is the same, except that the example
presented to the model for classification comes from the out-of-distribution
data. The $plus.circle$ composition of the rules in $bold(cal(R))$ is undefined
in this case; there is no ground-truth. Instead, I compute accuracy scores for
each composite rule of length $k in {1, 2}$, where $k$ is the number of
singletons in the composite rule. The rule with the highest accuracy is the rule
(among the candidates) that best describes the model's behavior on the
out-of-distribution data. Results here indicate which of the equifinal rules the
model has learned.

#strong[Accuracy ranks] were calculated for the candidate rules. The rule with
the highest accuracy recieves a rank of 1, the rule with the second highest
accuracy recieves a rank of 2, and so on.

== Assessing Articulation

Rule articulation was assessed using a multiple-choice test. In this test, the
model is presented with a set of labeled examples, and multiple options for
rules that could be used to classify the examples. The model is prompted to
select the rule that it would use to classify the examples. In each of these
tests, one of the options is the rule that was used to generate the labeled
examples, and three other rules are randomly selected from the set of all rules
in the task.

== Assessing Faithfulness

After assessing articulation and assessing rule learning, we have some
indication of what the model claims that it would learn, and some indication of
what the model actually learns. At this point we can compare the model's claims
to its behavior to assess its faithfulness.

Faithfulness was assessed by inspecting the accuracy rank distribution. If at
all times, the rule that the model selected from the multiple choice options
were the rule achieving the highest accuracy in the out-of-distribution test,
then the model would be perfectly faithful.#footnote(
  [
    I also considered defining the faithfulness score as the rank correlation
    between the model token log probabilities for options presented in the multiple
    choice answer set (model articulation confidences) and the accuracies of the
    rulesets with respect to the model behavior on the test examples. However, the
    OpenAI ChatCompletions API does not provide token log probabilities for the
    multiple choice options.
  ],
)

In practice, the model may select a rule that is not the most accurate. In this
case we can argue that the model is being unfaithful, since the choice it makes
to describe its behavior does not match its true behavior.

== Model
All experiments used OpenAI's GPT-4 model (version identifier `gpt-4`).
Generation was performed with default generation parameters, including default
settings for `temperature`, `top-k`, and `top-p` parameters.

= Results

Due to time constraints, I was only able to generate data for tasks ${R_0, R_1}$
and ${R_0, R_2}$. The results for these tasks are shown in Figure 1.

#[
  #set text(size: 0.8em)
  #figure(
    image("../figures/predicted_rule_accuracy_ranks.png", width: 40%),
    caption: "Accuracy ranks for the rules selected by the model in the multiple choice tests. ",
  )
]

Figure 2 shows the accuracy ranks for the rules selected by the model in the
multiple choice tests. GPT-4 most often selected the rule that best describes
its behavior on the out-of-distribution data (evidenced by highest count for 1st
rank). Empirical model likelihood to select a rule relates monotonically to the
rule's accuracy on the out-of-distribution data.

Figure 3 shows the accuracy ranks for the rules selected by the model on the
out-of-distribution data. Note that perfect accuracy is not expected, since even
if the model learns the rule that was used to obtain the in-distribution data,
this rule has undefined behavior out-of-distribution.

#[
  #set text(size: 0.8em)
  #figure(
    image(
      "../figures/test_accuracy_distribution_by_rule_stacked.png",
      width: 60%,
    ),
    caption: "Accuracy distribution for candidate rules on the out-of-distribution data.",
  )
]

// - For a classification task where we can show that the model does not learn rule $R_i$,
//   we can test whether the model articulates $R_i$ by including $R_i$ as an option
//   in the multiple-choice test.

//   These multiple choice tests may have several variants:

//   - The case where only one of the options is a correct rule, and it is possible
//     that the model has learned the correct rule.

//   - The case where only one rule is correct, but we can show that the model does not
//     learn this rule.

//   - The case where multiple rules are correct, and it is possible that the model has
//     learned some of the correct rules, but not the others.

// #let train = "train"
// #let val = "val"
// #let test = "test"
// #let yhat = $accent(y, hat)$

// == Results

// For each string length $N$, we generate a dataset of $2^N$ binary strings. I
// then create learning tasks from these strings by selecting the subset of strings
// that satisfy all rules or no rules in a set of rules $bold(cal(R)) = {R_1, R_2,
// ... R_r}$, where $r$ is the number of rules in the set. Strings satisfying all
// rules are labeled positive, and strings satisfying no rules are labeled
// negative. For any set of rules $bold(cal(R))$, each example in the training
// dataset has a defined label.

// #strong[In-Distribution Testing:]
// To confirm that the model can learn $bold(cal(R))$, we split the training data
// for each task into training and validation sets using an 80/20 split. I prompt
// the model with the training data and ask it to classify an unlabeled example
// drawn from the validation set. I then compare the model's prediction to the true
// label.

// 100% validation performance indicates that the model has learned a decision rule
// that is functionally equivalent to $bold(cal(R))$ on the in-distribution data.
// Given $bold(cal(R)) = {R_2, R_3}$, the model may have learned $R_2$, $R_3$, or $R_2
// and R_3$. I cannot differentiate between these cases using in-distribution
// testing, since the in-distribution data has $R_2 = R_3$ for all examples.

// #strong[Out-of-Distribution Testing:]

// Examples not in the training or validation datasets are mixed -- these examples
// satisfy some rules in $bold(cal(R))$ and not others. I use these examples to
// test how the learned rules generalize when the input example cannot be neatly
// classified using the rules in $bold(cal(R))$.

// For example, if $bold(cal(R)) = {R_2, R_3}$, then the training dataset will
// consist of binary strings that have the same value for $x_2$ and $x_3$ and the
// label. The test dataset will consist of unlabeled binary strings that have
// different values for $x_2$ and $x_3$.

// === Assessing Rule Learning

// For each task, the model makes predictions on the validation and test examples.
// I can compute a validation accuracy in the typical way, by comparing the model's
// predictions to the true labels. The validation accuracy is a measure of how well
// the model learns the rules in $bold(cal(R))$.

// I can also compute scores representing how much the model's predictions on the
// unlabeled examples agree with some rule combination $bold(cal(R))_c$ in the
// power set of $bold(cal(R))$. For example, if $bold(cal(R)) = {R_2, R_3}$, then
// $bold(cal(R))_c$ is drawn from ${{R_2}, {R_3}, {R_2, R_3}}$.

// $bold(cal(R))_c$ is the set of candidate rules that the model is likely to have
// learned. I cannot pinpoint the exact rule that the model has learned, but we can
// check how closely the model's behavior matches the behavior of each candidate
// rule on the test examples. I do this by computing the accuracy of the model
// predictions with respect to the labels obtained on the test examples by applying
// each candidate rule in $bold(cal(R))_c$.

// === Assessing Rule Articulation
// I ask the model to select the rule that it would use to classify the training
// data. I present the model with multiple options, including the correct rule.

// === Assessing Faithfulness
// After assessing articulation and assessing rule learning, we have some
// indication of what the model claims that it would learn, and some indication of
// what the model actually learns. At this point we can compare the model's claims
// to its behavior to assess its faithfulness.#footnote(["claims","faithfulness" used as convenient anthropormorphizations.])

// If the model were guaranteed to learn one rule from $"power"(bold(cal(R)))$,
// then we could assess faithfulness using an accuracy score. However, there are
// sources of stochasticity: the model may assign non-zero probability to multiple
// rules in $"power"(bold(cal(R)))$. A model is faithful if it is likely to assign
// high articulation probability to rules that describe its behavior well, and low
// articulation probability to rules that do not describe its behavior well. To
// formalize this, since rule scores and articulation scores are on different
// scales, we use a rank correlation metric.

// I compute faithfulness $bold(f)(t,m)$ for task $t$ and model $m$ as the rank
// correlation between the model token log probabilities for rulesets presented in
// the multiple choice answer set (model articulation confidences) and the
// accuracies of the rulesets with respect to the model behavior on the test
// examples. This results in a single scalar faithfulness score for each task and
// model.

// Given a set of tasks $bold(T)$, we can compute an average faithfulness score $bold(overline(f))$ for
// a model across all tasks:

// $ bold(overline(f))(m) = frac(1, |bold(T)|) sum_(t in bold(T)) bold(f)(t,m) $