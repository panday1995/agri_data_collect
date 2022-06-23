# Agriculture balance

## Table of contents

- [Nutrient balance](#nutrient-balance)

  - [Nutrient requirements](#nutrient-requirements)
  - [Nutrient mass balance](#nutrient-mass-balance)
  - [Data sources](#data-sources)

## Nutrient balance

### Nutrient requirements

__Nutrient uptake requirement__</br>
is expressed in ($kg_{nutrient}*ha_{-1}$), is the amount of a nutrient that must be absorbed in aboveground crop biomass to realize a certain target yield $Y^T$ ($kg*ha_{-1}$).

__Nutrient input requirement__</br>
$A^T$, is the amount of a nutrient applied per season, which supplements soil nutrients.</br>

$$
A^T=Y^T*AE^{EQ}
$$

$AE^{EQ}$ is also called agronomic efficiency, which indicates $kg$ yield per $kg$ nutrient applied. The efficiency could be decomposed into two components:</br>
$$
AE^{EQ} = IE^{EQ}*RE^{EQ}
$$

$IE^{EQ}$ is the extra yield per unit of nutrient uptake;</br>
$RE^{EQ}$ is the extra unit nutrient uptake per unit of nutrient input.</br>

Macronutrients

- Nitrogen
- Phosphorus
- Potassium

### Nutrient mass balance

$$
Nu_{fert} + \Delta Nu_{soil} + Nu_{manu} = Nu_{harv} + Nu_{resid} + Nu_{emis}  
$$

Knowns:

- $Nu_{fert}$ from [IFA and others](nutri_data/doi_10.5061_dryad.2rbnzs7qh__v3/Global_data_on_fertilizer_use_by_crop_and_by_country_2022.csv)
- $Nu_{resid}$ from FAOstat
- $Nu_{soil}$ assumed no change in Tier 1 approach
  
Unknowns:

- $Nu_{manu}$ acquired from animal system <!--animal balance first assumes 0-->
- $Nu_{harv}$ Nutrient absorbation rate <!--value from Stefano do some basic search, part of IPCC N2O, IPCC meeting before starting-->
- $Nu_{emis}$ fertilizer use efficiency: fertilizers not absorbed by crops

### Data sources

[Table 11.1 of IPCC data](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch11_Soils_N2O_CO2.pdf)

## Other balances

<!--
what are other balances to achieve a mass balance of crops?
we have N, K, P balances
C balance?
H balance?
-->

<!--
Currently, I am only working on data collection. Do we also need some sort of data pipeline to connect collected data to data input into core modules?

unit test, documentation

https://pyscaffold.org/en/stable/

A pipeline is needed
Thurday or friday
Full picture of dataflow in the project
-->
