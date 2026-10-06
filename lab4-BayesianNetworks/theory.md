För att starta lab 4:
cd ~/Downloads
`/usr/libexec/java_home -v 1.8`/bin/java -jar bayes.jar

### Part 2
## 5 Use the applet and the loaded Bayesian Network to answer the following questions: 
## a) What is the risk of melt-down in the power plant during a day if no observations have been made? What if there is icy weather?

Without observation the probability for meltdown is 2.578%, but if it is icy weather the probabilty increases to 3.472%.

## b) Suppose that both warning sensors indicate failure. What is the risk of a meltdown in that case? Compare this result with the risk of a melt-down when there is an actual pump failure and water leak. What is the difference? The answers must be expressed as conditional probabilities of the observed variables, P(Meltdown|...).

P(Meltdown | PumpFailureWarning=None, WaterLeakWarning=None) = 2.578%
P(Meltdown | PumpFailureWarning=True, WaterLeakWarning=True) = 14.535%
P(Meltdown | PumpFailure=True, WaterLeak=True)               = 20%

## c) The conditional probabilities for the stochastic variables are often estimated by repeated experiments or observations. Why is it sometimes very difficult to get accurate numbers for these? What conditional probabilites in the model of the plant do you think are difficult or impossible to estimate?

The conditional probabilities can be hard to estimate if e.g. they depend on a lot of unkown variables or if it is extreamly rare or have not happened before. 

Meltdown is one stochastic variable that could be hard to estimate because it has alot of dependencies and (hopefully) happens very rarly. 

## d) Assume that the "IcyWeather" variable is changed to a more accurate "Temperature" variable instead (don't change your model). What are the different alternatives for the domain of this variable? What will happen with the probability distribution of P(WaterLeak | Temperature) in each alternative?

We have 2 primary options, we could either use discrete states/intervals or we can use continous domains.
A discrete example could be 3 tempature variables like hot, medium or cold. Another alternative could be to have a variable for each degree between -10 and +10 C.

A continous domain for this example would be a continous model or link function that we could use for ALL temperatures which would give us alot more precision.

The probability distribution in the different alteratives would get more complex the more variables structure contains. It would need more data but in exchange get better accrucy. So there is a trade-off to be made between complexity and simplicity.

## 6 To guide your understanding of how Bayesian networks work we provide a few theory questions below that should be answered using the lecture slides and/or book. When asked to calculate something manually show your calculations.
## a) What does a probability table in a Bayesian network represent? 

A probability table represents the probability distribution of a stochastic variable. If the variable has parent nodes, then the table will also contain the probability for each possible value of the variable given every combination of its parents.

For example:
The WaterLeak table represents P(WaterLeak | IcyWeather). It states that:
P(WaterLeak | IcyWeather = True) = 20% and P(WaterLeak | IcyWeather = False) = 80%

The possibilites in each row must add upp to one (100%)

## b) What is a joint probability distribution? Using the chain rule on the structure of the Bayesian network to rewrite the joint distribution as a product of P(child|parent) expressions, calculate manually the particular entry in the joint distribution of P(Meltdown=F, PumpFailureWarning=F, PumpFailure=F, WaterLeakWaring=F, WaterLeak=F, IcyWeather=F). Is this a common state for the nuclear plant to be in?

A joint probability distribution describes the probability of every possible combination of values for all variables in the network.

The joint distribution can be written as:

P(IcyWeather) · P(PumpFailure) · P(WaterLeak | IcyWeather) · P(PumpFailureWarning | PumpFailure) · P(WaterLeakWarning | WaterLeak) · P(Meltdown | PumpFailure, WaterLeak)

For the state where all variables are false, the calculation is:

P(IcyWeather=F) · P(PumpFailure=F) · P(WaterLeak=F | IcyWeather=F) · P(PumpFailureWarning=F | PumpFailure=F) · P(WaterLeakWarning=F | WaterLeak=F) · P(Meltdown=F | PumpFailure=F, WaterLeak=F)

= 0.95 · 0.9 · 0.9 · 0.95 · 0.95 · 0.999 = 0.69377927625 ≈ 69.38%

So this would be a common state for the nuclear plant, since it occurs with a probability of ≈ 69.38%.

## c) What is the probability of a meltdown if you know that there is both a water leak and a pump failure? Would knowing the state of any other variable matter? Explain your reasoning! 

If we know that both WaterLeak=True and PumpFailure=True, the probability of a meltdown is:

P(Meltdown=True | PumpFailure=True, WaterLeak=True) = 0.20

Knowing the state of the other variables does not change this probability. PumpFailure and WaterLeak are the direct parents of Meltdown, so Meltdown is conditionally independent of the other variables when the states of its parents are known.

For example, the warning variables are useful when we do not know whether there is a pump failure or water leak. However, when both failures have already been observed, the warnings provide no additional information about Meltdown. This is why observing IcyWeather and both warning variables does not change the probability from 20%.

## d) Calculate manually the probability of a meltdown when you happen to know that PumpFailureWarning=F, WaterLeak=F, WaterLeakWarning=F and IcyWeather=F but you are not really sure about a pump failure. 

We want to calculate:

P(Meltdown | PumpFailureWarning=F, WaterLeak=F, WaterLeakWarning=F, IcyWeather=F)

Since PumpFailure is unknown, we must consider both PumpFailure=True and PumpFailure=False.

For Meltdown=True:

q(T) = 
P(IcyWeather=F) · P(PumpFailure=T) · P(WaterLeak=F | IcyWeather=F) · P(PumpFailureWarning=F | PumpFailure=T) · P(WaterLeakWarning=F | WaterLeak=F) · P(Meltdown=T | PumpFailure=T, WaterLeak=F) +

P(IcyWeather=F) · P(PumpFailure=F) · P(WaterLeak=F | IcyWeather=F) · P(PumpFailureWarning=F | PumpFailure=F) · P(WaterLeakWarning=F | WaterLeak=F) · P(Meltdown=T | PumpFailure=F, WaterLeak=F)

= (0.95 · 0.1 · 0.9 · 0.1 · 0.95 · 0.15) + (0.95 · 0.9 · 0.9 · 0.95 · 0.95 · 0.001)
= 0.001218375 + 0.00069447375 = 0.00191284875


For Meltdown=False:

q(F) = 
P(IcyWeather=F) · P(PumpFailure=T) · P(WaterLeak=F | IcyWeather=F) · P(PumpFailureWarning=F | PumpFailure=T) · P(WaterLeakWarning=F | WaterLeak=F) · P(Meltdown=F | PumpFailure=T, WaterLeak=F) + 

P(IcyWeather=F) · P(PumpFailure=F) · P(WaterLeak=F | IcyWeather=F) · P(PumpFailureWarning=F | PumpFailure=F) · P(WaterLeakWarning=F | WaterLeak=F) · P(Meltdown=F | PumpFailure=F, WaterLeak=F)

= (0.95 · 0.1 · 0.9 · 0.1 · 0.95 · 0.85) + (0.95 · 0.9 · 0.9 · 0.95 · 0.95 · 0.999)
= 0.006904125 + 0.69377927625 = 0.70068340125


The results must then be normalized:

P(Meltdown=T | PumpFailureWarning=F, WaterLeak=F, WaterLeakWarning=F, IcyWeather=F)

= q(T) / (q(T) + q(F))
= 0.00191284875 / (0.00191284875 + 0.70068340125) ≈ 0.0027225 ≈ 0.27225%

Therefore, the probability of a meltdown given the observations is approximately 0.27225%.

### Part 3

## During the lunch break, the owner tries to show off for his employees by demonstrating the many features of his car stereo. To everyone's disappointment, it doesn't work. How did the owner's chances of surviving the day change after this observation?

It goes from P(Survival) = 99,001% to 98,116%.

## The owner buys a new bicycle that he brings to work every day. How does the bicycle change the owner's chances of survival?

It goes from P(Survival) = 99,001% to 99,505%

## It is possible to model any function in propositional logic with Bayesian Networks. What does this fact say about the complexity of exact inference in Bayesian Networks? What alternatives are there to exact inference? 

Since a Bayesian network can represent any function in propositional logic, it can also represent computationally difficult problems such as SAT. Therefore, exact inference in a general Bayesian network is computationally hard. Deciding certain probability questions is NP-hard, while calculating exact probabilities is generally #P-hard. The required computation can therefore grow exponentially as the network becomes larger and more connected.

An alternative is approximate inference, where probabilities are estimated instead of calculated exactly. Examples include Monte Carlo sampling, rejection sampling, likelihood weighting and MCMC methods such as Gibbs sampling. Exact inference can also remain practical if the network has a simple structure, such as a tree or a network with low treewidth.

## The owner had an idea that instead of employing a safety person, to replace the pump with a better one. Is it possible, in your model, to compensate for the lack of Mr H.S.'s expertise with a better pump?

The pump will only reduce the probebility of pump failure. This would lower the risk of meltdown, hence increasing the chances of survival which could be better the H.S. depending on how competent he is. However, it will not affect the water leak probebility which means only the pump will not eliminate the risk och meltdown altogether. 

## Mr H.S. fell asleep on one of the plant's couches. When he wakes up he hears someone scream: "There is one or more warning signals beeping in your control room!". Mr H.S. realizes that he does not have time to fix the error before it is to late (we can assume that he wasn't in the control room at all). What is the chance of survival for Mr H.S. if he has a car with the same properties as the owner? Hint: This question involves a disjunction (A or B) which can not be answered by querying the network as is. How could you answer such questions? Maybe something could be added or modified in the network.

The statement "one or more warning signals" means:

WaterLeakWarning=True OR PumpFailureWarning=True

To represent this disjunction, we can add a Boolean node called AnyWarning with WaterLeakWarning and PumpFailureWarning as parents. AnyWarning is deterministic and has the following probability table:

P(AnyWarning=T | WaterLeakWarning=T, PumpFailureWarning=T) = 1

P(AnyWarning=T | WaterLeakWarning=T, PumpFailureWarning=F) = 1

P(AnyWarning=T | WaterLeakWarning=F, PumpFailureWarning=T) = 1

P(AnyWarning=T | WaterLeakWarning=F, PumpFailureWarning=F) = 0

For this scenario we use the following observations:

AnyWarning=True

IsAsleep=True

HomerReacs=Slow

BicycleWorks=False

HomerReacs is set to Slow because he was asleep and realizes that he reacted too late. BicycleWorks is set to False because Mr H.S. is only given a car, not a bicycle.

Let E represent the observations IsAsleep=True, HomerReacs=Slow and BicycleWorks=False. The disjunction contains three possible and mutually exclusive warning combinations:

(WaterLeakWarning=T, PumpFailureWarning=T)
(WaterLeakWarning=T, PumpFailureWarning=F)
(WaterLeakWarning=F, PumpFailureWarning=T)

The probabilities calculated from our network for these cases are:

P(WLW=T, PFW=T, E) = 0.000921138750

P(Survives=T, WLW=T, PFW=T, E) = 0.000837605043

P(WLW=T, PFW=F, E) = 0.005902111250

P(Survives=T, WLW=T, PFW=F, E) = 0.005645968891

P(WLW=F, PFW=T, E) = 0.005693861250

P(Survives=T, WLW=F, PFW=T, E) = 0.005335221707

We add the three valid warning cases and normalize the result:

P(Survives=T | AnyWarning=T, E) = (0.000837605043 + 0.005645968891 + 0.005335221707) / (0.000921138750 + 0.005902111250 + 0.005693861250)
= 0.011818795641 / 0.012517111250 = 0.94421112 ≈ 94.421%

Therefore, the probability that Mr H.S. survives in this scenario is approximately 94.421%. Adding the AnyWarning node allows the same result to be obtained directly in the applet by observing AnyWarning=True and querying Survives.

## What unrealistic assumptions do you make when creating a Bayesian Network model of a person? 

The model assumes that a person's behaviour can be described using a small number of fixed states and probabilities. In reality, a person's reaction depends on many factors that are not included, such as stress, health, experience, communication and the exact situation. The model also assumes that the probabilities remain constant over time and that variables are conditionally independent whenever there is no connection between them in the network. A real person may learn, change behaviour and react differently in situations that appear identical in the model.

## Describe how you would model a more dynamic world where for example the "IcyWeather" is more likely to be true the next day if it was true the day before. You only have to consider a limited sequence of days. 

We could use a Dynamic Bayesian Network by creating one copy of the relevant variables for each day. For example, we could create IcyWeather_1, IcyWeather_2 and IcyWeather_3 and add arcs from IcyWeather_1 to IcyWeather_2 and from IcyWeather_2 to IcyWeather_3.

The first day would use a prior probability P(IcyWeather_1). The following days would use a transition table such as P(IcyWeather_t | IcyWeather_t-1), where the probability of icy weather is higher if the previous day was icy. The remaining plant variables could also be copied for each day and connected to the IcyWeather variable from the same day. Since only a limited sequence is required, the network can be unrolled for a fixed number of days.
