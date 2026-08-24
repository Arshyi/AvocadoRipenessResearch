# Scientific-machine-learning implementation plan

## Preferred sequence

1. nonlinear mixed-effects kinetic baselines;
2. Bayesian state-space model with explicit sensor observation equations;
3. Gaussian-process smoothing and uncertainty diagnostics;
4. SINDy or constrained symbolic regression on sufficiently dense measured
   states;
5. Neural ODE or universal differential equation only when independent
   trajectories support the extra flexibility;
6. PINN only when a defensible ODE/PDE, boundary conditions, and observations
   make the inverse problem identifiable.

## Required evaluation

- fruit- and batch-held-out forecasts;
- parameter/posterior recovery diagnostics;
- physical state constraints and unit checks;
- residual autocorrelation and posterior predictive checks;
- prediction interval coverage;
- intervention transfer across temperature/RH;
- comparison with a simpler empirical model;
- abstention outside the validated domain.

Synthetic trajectories may verify code and recovery, but must be labelled
`PIPELINE TEST - NOT BIOLOGICAL EVIDENCE`. No synthetic data may replace missing
experimental measurements in a scientific result.

