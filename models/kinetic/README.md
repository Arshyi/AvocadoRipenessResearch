# Candidate kinetic model scaffold

`candidate_models.py` implements units-conscious right-hand-side functions for
the **proposed** coupled ODE system in Appendix E. It contains no fitted avocado
parameters and produces no scientific result by itself.

The scaffold exists to make the following requirements testable before fitting:

- explicit state order;
- nonnegative state and parameter-domain checks;
- measured temperature/RH/airflow forcing;
- reference-temperature Arrhenius rates;
- separated water, firmness, pigment, ethylene, carbohydrate, and lipid states.

Before fitting biological data:

1. freeze units and observation models;
2. test structural identifiability;
3. add fruit, batch, chamber, and measurement-error hierarchy;
4. run synthetic recovery only as a labelled pipeline test;
5. fit the simplest candidate first;
6. validate on a withheld batch/condition.

See
[`appendices/appendix-e-mathematical-models.md`](../../appendices/appendix-e-mathematical-models.md)
for equations, assumptions, boundary conditions, and decision rules.

