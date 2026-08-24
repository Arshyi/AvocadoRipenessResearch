# Appendix E - Candidate Mathematical and Scientific-ML Models

## E.1 Status and purpose

Every model in this appendix is **PROPOSED** unless a cited source is stated.
The equations are candidate representations to compare against data. They are
not asserted as complete avocado physiology, and no biological rate constant is
estimated from the public RGB dataset because that dataset lacks the required
states and interventions.

Prior avocado kinetic modeling already exists. In particular, Gwanpua et al.
modeled autocatalytic ethylene and linked ethylene to softening and colour using
temperature-dependent kinetics
([DOI 10.1016/j.postharvbio.2017.10.002](https://doi.org/10.1016/j.postharvbio.2017.10.002)).
Sierra et al. also reported temperature-dependent quality kinetics
([DOI 10.1177/1082013219826825](https://doi.org/10.1177/1082013219826825)).
Van der Sman, Guo, and Pedreschi have since applied a physics-informed neural
network to postharvest avocado firmness using literature datasets, enzymatic
softening, and metabolic-rate structure
([DOI 10.1016/j.postharvbio.2025.113898](https://doi.org/10.1016/j.postharvbio.2025.113898)).
Guo et al. also published a generic SciML framework for fruit and vegetable
quality prediction
([DOI 10.1016/j.postharvbio.2025.114103](https://doi.org/10.1016/j.postharvbio.2025.114103)).
Hernández et al. used metabolites measured at harvest as physiological markers
in a model of batch-specific Hass softening across postharvest logistics
([DOI 10.1016/j.postharvbio.2020.111457](https://doi.org/10.1016/j.postharvbio.2020.111457)).
The proposed contribution is therefore not to claim the first avocado equation
or PINN. It is to observe multiple coupled states under a leakage-resistant,
externally validated design and test whether additional complexity is
identifiable and useful.

## E.2 Notation

| Symbol | Meaning | Typical unit | Measurement/latent status |
|---|---|---|---|
| \(t\) | Time after defined study baseline | h or d | Direct |
| \(T_K\) | Fruit/chamber absolute temperature | K | Direct air; fruit-core optional |
| \(RH\) | Fractional ambient relative humidity | 0-1 | Direct |
| \(v\) | Local airflow or mixing condition | m/s or fixed level | Assigned/logged |
| \(M\) | Whole-fruit mass | g | Direct |
| \(M_w\) | Fruit water mass | g | Latent longitudinal; destructive calibration |
| \(W\) | Local or bulk water concentration | mass fraction | Destructive calibration/latent |
| \(F\) | Standardized firmness | N | Destructive reference/latent sentinel state |
| \(E\) | Tissue or production-related ethylene state | chosen normalized or physical unit | Latent unless reference method |
| \(C_E\) | Chamber ethylene concentration | ppm or umol/mol | Reference measurement |
| \(C_C\) | Chamber CO2 concentration | ppm or mol fraction | Direct NDIR |
| \(C_{chl}\) | Peel chlorophyll state | concentration | Destructive subset/latent |
| \(A_{anth}\) | Peel anthocyanin state | concentration | Destructive subset/latent |
| \(S_{starch}\) | Starch mass/state | g or concentration | Destructive |
| \(S_{sol}\) | Soluble-solid mass/state | g | Destructive/model state |
| \(M_L\) | Lipid mass | g | Destructive calibration |
| \(R\) | Dimensionless latent progression state | 0-1 | Latent |
| \(V_h\) | Free chamber headspace volume | L or m3 | Calibrated geometry |
| \(A_f\) | Effective fruit surface area | m2 | Geometry estimate |
| \(R_g\) | Universal gas constant | consistent units | Constant |
| \(y_i\) | Sensor observation for channel \(i\) | channel-specific | Direct |

Units must be frozen and checked before fitting. A model that mixes days and
seconds, percentage and fraction, or ppm and mole fraction is invalid even if
its optimizer converges.

## E.3 Environmental rate modifier

### E.3.1 Arrhenius candidate

\[
k_j(T_K)=A_j\exp\left(-\frac{E_{a,j}}{R_gT_K}\right)
\]

**Interpretation:** apparent process rate \(j\) increases with temperature under
an Arrhenius approximation.

**Assumptions:** a stable mechanism over the studied temperature range;
temperature is measured on an appropriate scale; storage history is included;
no unmodeled chilling injury or phase change.

**Limitation:** a narrow temperature range can make \(A_j\) and \(E_{a,j}\)
strongly correlated. Estimate a reference-temperature rate and apparent
activation energy, or use a Q10 form, rather than extrapolating.

### E.3.2 Q10 candidate

\[
k_j(T)=k_j(T_{ref})Q_{10,j}^{(T-T_{ref})/10}
\]

This is often easier to estimate across a narrow practical range but remains an
empirical approximation. Compare it with Arrhenius behavior on held-out
temperature conditions.

## E.4 Water transport and total mass

### E.4.1 Lumped water-loss ODE

\[
\frac{dM_w}{dt}
=-k_w(T,RH,v)A_f
\left[a_w(M_w,T)-RH\right]
\]

Possible rate modifier:

\[
k_w(T,RH,v)=k_{w,ref}
\exp\left[-\frac{E_{a,w}}{R_g}
\left(\frac{1}{T_K}-\frac{1}{T_{ref,K}}\right)\right]
g(v).
\]

**Interpretation:** water flux is driven by an effective surface-to-air vapor
activity difference and affected by temperature, RH, airflow, area, and skin.

**Required observations:** repeated mass, continuous T/RH, airflow setting,
fruit geometry, and destructive moisture/dry matter at matched times.

**Non-claim:** scale loss is not automatically water loss. Respiration removes
carbon, condensation can add mass, and handling deposits can alter the scale.

### E.4.2 Total mass balance

\[
\frac{dM}{dt}
=\frac{dM_w}{dt}
-r_{C}(T,R,E)
+r_{\mathrm{deposit}}.
\]

If CO2 production is measured in mol/time, a stoichiometric carbon-loss term
can be explored, but the substrate and respiratory quotient must not be assumed
without evidence.

### E.4.3 Spatial diffusion PDE

\[
\frac{\partial W(\mathbf{x},t)}{\partial t}
=\nabla\cdot\left[D_W(W,T)\nabla W\right]-q_W,
\]

with convective boundary condition

\[
-D_W\nabla W\cdot\mathbf{n}
=h_m\left[W_s-W_{eq}(T,RH)\right].
\]

**Boundary conditions:** symmetry or zero flux at the geometric center; a
convective skin boundary; initial spatial water field from destructive matched
fruit or a justified homogeneous approximation.

**Identifiability warning:** whole-fruit mass and one NIR surface observation
cannot identify a spatial diffusion coefficient and boundary coefficient
simultaneously. Use spatial destructive samples, tomography, informative priors,
or retain the lumped ODE.

## E.5 Firmness and softening

### E.5.1 First-order model

\[
\frac{dF}{dt}=-k_F(T)(F-F_\infty).
\]

Solution:

\[
F(t)=F_\infty+(F_0-F_\infty)e^{-k_Ft}.
\]

This is parsimonious and should be a baseline even if it underfits the
climacteric transition.

### E.5.2 Weibull/stretched-exponential model

\[
F(t)=F_\infty+(F_0-F_\infty)
\exp[-(k_Ft)^n].
\]

The shape parameter \(n\) can express acceleration or deceleration, but it may
be confounded with \(k_F\) for short trajectories.

### E.5.3 Ethylene-modulated softening

\[
\frac{dF}{dt}
=-k_F(T)
\frac{E^h}{K_{E,F}^h+E^h}
(F-F_\infty).
\]

Alternative Michaelis-Menten form:

\[
\frac{dF}{dt}
=-k_F(T)\frac{E}{K_{E,F}+E}(F-F_\infty).
\]

**Required observations:** independently calibrated ethylene trajectory and a
standardized firmness method. A low-cost cross-sensitive sensor cannot identify
this coupling without reference comparison.

## E.6 Ethylene production and headspace observation

### E.6.1 Autocatalytic tissue/production state

\[
\frac{dE}{dt}
=k_{E,0}(T)
+k_{E,a}(T)\frac{E^h}{K_E^h+E^h}
-k_{E,l}(T)E.
\]

This candidate represents basal production, autocatalytic induction, and loss.
It is related in concept to published avocado ethylene kinetics but is not a
transcription of one fitted source model.

### E.6.2 Chamber mass balance

\[
\frac{dC_E}{dt}
=\frac{m_f r_E(E,T)}{V_h}
-k_{\mathrm{leak},E}(C_E-C_{E,amb})
-k_{\mathrm{ads},E}C_E
-q_{\mathrm{sensor},E}.
\]

**Initial condition:** measured ambient/baseline concentration after the defined
flush/equilibration protocol.

**Boundary/operating conditions:** known free headspace, fixed mixing, recorded
pressure/temperature, defined seal/vent times, and no instrument saturation.

**Measurement model:**

\[
y_E(t)=b_E+s_E C_E(t-\tau_E)+\epsilon_E(t),
\]

where \(b_E\), \(s_E\), and \(\tau_E\) capture offset, sensitivity, and response
delay. Cross-sensitivity terms must be added for the low-cost channel.

## E.7 Respiration and CO2

For a short, well-mixed accumulation interval:

\[
r_{CO_2}\approx
\frac{V_h}{m_f}
\frac{P}{R_gT_K}
\frac{dx_{CO_2}}{dt}.
\]

A fuller balance is:

\[
\frac{dC_C}{dt}
=\frac{m_f r_C(R,T,E)}{V_h}
-k_{\mathrm{leak},C}(C_C-C_{C,amb}).
\]

Candidate climacteric response:

\[
r_C(R,T,E)=r_{C,0}(T)
+r_{C,peak}(T)\exp\left[
-\frac{(R-R_{peak})^2}{2\sigma_R^2}
\right].
\]

**Required corrections:** chamber free volume after fruit displacement,
temperature, pressure, empty-chamber drift, leakage, sensor response, and range.
If the NDIR channel exceeds specification, shorten the interval or change the
chamber; do not extrapolate the sensor.

## E.8 Peel chlorophyll, anthocyanin, and colour

### E.8.1 Chlorophyll loss

\[
\frac{dC_{chl}}{dt}=-k_{chl}(T)C_{chl}.
\]

### E.8.2 Anthocyanin accumulation

\[
\frac{dA_{anth}}{dt}
=k_A(T)f_A(R)(A_{\max}-A_{anth})
-k_{A,d}A_{anth}.
\]

One activation choice is

\[
f_A(R)=\frac{R^h}{K_A^h+R^h}.
\]

### E.8.3 Colour observation

\[
\mathbf{y}_{colour}
=g(C_{chl},A_{anth},\mathrm{surface},
\mathrm{illumination},\mathrm{camera},\mathrm{zone})
+\boldsymbol{\epsilon}.
\]

The observation vector can include L*, a*, b*, hue, chroma, and calibrated
spectral ratios. The function \(g\) may be linear/PLS, monotone spline, or a
small learned observation network. Chemical pigment assays are required to
interpret states as concentrations.

Published Hass work supports early chlorophyll decline and later
cyanidin-3-O-glucoside accumulation
([Cox et al.](https://doi.org/10.1016/j.postharvbio.2003.09.008)).
Temperature-related darkening can desynchronize colour and internal readiness
([Sibeko et al.](https://doi.org/10.17221/72/2023-HORTSCI)).

## E.9 Carbohydrate and soluble-solid balance

\[
\frac{dS_{starch}}{dt}=-k_S(T)S_{starch},
\]

\[
\frac{dS_{sol}}{dt}
=Y_S k_S(T)S_{starch}
-r_{\mathrm{resp,sol}}
-r_{\mathrm{other}}.
\]

Approximate measured concentration:

\[
C_{sol}
=\frac{S_{sol}}
{M_w+S_{sol}+M_{\mathrm{other,sol}}}.
\]

**Interpretation:** Brix is a concentration influenced by carbohydrate
conversion/consumption and water change. It cannot independently identify
starch conversion.

**Required observations:** moisture or water mass, Brix, and a validated
starch/carbohydrate assay on matched tissue. Sampling location matters because
the fruit may be heterogeneous.

## E.10 Lipid and fresh-basis concentration

Most avocado lipid deposition occurs before harvest. A conservative postharvest
candidate is:

\[
\frac{dM_L}{dt}=-r_L(T,R),
\qquad
C_{L,fresh}=\frac{M_L}{M}.
\]

A rise in \(C_{L,fresh}\) can occur when water/total mass falls, even if
\(M_L\) is constant. Do not insert a postharvest "oil accumulation" term without
independent evidence. Oil extraction or a validated reference method is needed
for calibration. Broad NIR alone does not guarantee oil specificity because
water and scattering overlap.

## E.11 Latent ripeness models

### E.11.1 Logistic state

\[
\frac{dR}{dt}=k_R(T,RH,E)R(1-R).
\]

### E.11.2 Gompertz state

\[
R(t)=\exp[-\exp\{-k_R(t-t_0)\}].
\]

### E.11.3 Multistate alternative

A single \(R\) may be inadequate. A minimal vector state could be:

\[
\mathbf{x}
=[F,M_w,C_{chl},A_{anth},E,r_C]^T,
\]

\[
\frac{d\mathbf{x}}{dt}
=\mathbf{f}(\mathbf{x},T,RH,v;\boldsymbol{\theta}_p)
+\boldsymbol{\eta},
\]

with fruit-specific parameters

\[
\log\boldsymbol{\theta}_p
=\boldsymbol{\mu}
+\mathbf{B}_{batch}
+\mathbf{b}_{fruit}.
\]

This nonlinear mixed-effects construction separates population, batch, and
fruit variation. It should be compared with the one-state model on held-out
batches and posterior predictive checks.

## E.12 Sensor observation model

For sensor channel \(i\):

\[
y_{i,t}
=h_i(\mathbf{x}_t,\mathbf{u}_t,
\mathrm{device}_i,\mathrm{zone})
+b_i(t)+\epsilon_{i,t},
\]

where \(\mathbf{u}_t\) contains environment and protocol inputs, \(b_i(t)\) is
drift, and \(\epsilon_{i,t}\) is measurement noise.

Examples:

- RGB depends on pigments, surface state, illumination, camera, and zone.
- 970-nm response depends on water absorption, scattering, geometry,
  temperature, and detector/source behavior.
- scale mass depends on fruit state, tare, temperature, creep, and off-axis load.
- MOX resistance depends on mixed volatiles, RH, T, baseline, and heater history.
- chamber gas depends on production, volume, mixing, leaks, adsorption, and
  sensor dynamics.

Calibrations and blank/reference observations belong in the likelihood, not only
in a preprocessing spreadsheet.

## E.13 Remaining-useful-life formulation

Define a prespecified acceptable region \(\mathcal{A}\) over firmness, internal
condition, and any required sensory endpoint. At observation time \(t\):

\[
\mathrm{RUL}(t)
=\inf_{\tau>0}
\{\tau:\mathbf{x}(t+\tau)\notin\mathcal{A}\}.
\]

The entry and exit times are interval-censored when fruit is inspected only at
sessions. For destructive states, the sentinel fruit endpoint is latent and
informed by matched sacrifice cohorts. Forecasts should be distributions:

\[
p(\mathrm{RUL}(t)\mid \mathbf{y}_{1:t},
\mathbf{u}_{1:t},\mathcal{D}_{train}),
\]

not a single number without uncertainty.

## E.14 Estimation methods

| Method | Recommended use | Required safeguard |
|---|---|---|
| Nonlinear least squares | Simple single-fruit/mean trajectory diagnostics | Cluster-aware uncertainty and residual checks |
| Nonlinear mixed effects | Population rates plus fruit/batch variability | Structural identifiability and random-effect diagnostics |
| Bayesian state-space/MCMC | Latent states, missing data, full uncertainty | Prior sensitivity, convergence, posterior predictive checks |
| Extended/unscented Kalman filter | Sequential online update | Test nonlinearity and non-Gaussian failure |
| Particle filter | Nonlinear/non-Gaussian sequential inference | Effective sample size and resampling diagnostics |
| Gaussian process | Small-data trajectory smoothing and uncertainty | Avoid derivative overconfidence |
| SINDy | Sparse candidate rate terms | Smooth/noise study, units, stability, external refit |
| Symbolic regression | Alternative human-readable functions | Constrained search, dimensional consistency, held-out confirmation |
| Neural ODE | Flexible irregular-time latent dynamics | Independent trajectories, regularization, interpretability boundary |
| Universal differential equation | Known balance plus learned residual | Ensure residual does not silently absorb confounding |
| PINN | Defensible ODE/PDE with boundary information | Optimization diagnostics and comparison with classical solvers |

## E.15 Identifiability workflow

1. Draw the causal/measurement graph and list measured, latent, controlled, and
   unobserved variables.
2. Nondimensionalize or enforce units.
3. Perform structural identifiability analysis for each proposed equation set.
4. Use synthetic parameter-recovery tests only as **pipeline verification**.
5. Fit the simplest candidate to pilot data.
6. Inspect profile likelihood or posterior geometry, parameter correlations,
   residuals, and state uncertainty.
7. Add one coupling only when the relevant state is independently observed.
8. compare candidates on leave-one-batch/condition-out prediction;
9. test intervention prediction at withheld T/RH;
10. reject or simplify models with nonphysical states, weak recovery, wide
    parameters, or failed external forecasts.

## E.16 Candidate initial/boundary conditions

| Process | Initial condition | Boundary/forcing information |
|---|---|---|
| Mass/water | First stable mass; matched initial moisture distribution | T, RH, airflow, area; skin convective boundary if PDE |
| Firmness | Matched batch/initial destructive distribution | Temperature and optional ethylene state |
| Ethylene | Post-flush chamber baseline and latent basal production | Seal/vent schedule, free volume, leaks, adsorption |
| CO2 | Ambient/empty-chamber baseline | Seal time, volume, pressure, T, leaks, sensor response |
| Pigments | Initial calibrated colour plus chemical subset | Illumination/device/zone observation model |
| Carbohydrate | Initial starch/Brix/moisture distribution | Respiration/carbohydrate consumption assumptions |
| Latent \(R\) | Batch-informed distribution, not arbitrary zero for all fruit | Recorded T/RH/handling history |

## E.17 Model-selection decision rule

A dynamic model advances only if it:

1. passes numerical and unit tests;
2. produces physically admissible states;
3. has identifiable or decision-useful parameter combinations;
4. improves batch-held-out forecast error, calibration, interval coverage, or
   temporal consistency over a simpler baseline;
5. remains stable under plausible initial-condition and measurement-error
   perturbations;
6. reports uncertainty and abstains outside its validated domain.

A visually plausible fitted curve is not sufficient evidence of a governing
law.
