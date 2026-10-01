För att starta lab 4:
cd ~/Downloads
`/usr/libexec/java_home -v 1.8`/bin/java -jar bayes.jar


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