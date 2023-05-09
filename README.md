# Candidacy
This repository is for answering question 2 of the candidacy exams.

Here is the question.

Using the Aqueduct data layers, estimate the number of people vulnerable to riverine flooding in Kenya, comparing the historical baseline against the RCP8.5 2080 projection from the HadGEM2-ES model for a 1-in-in-1000-year event. Produce a set of plots showing the results and discuss the findings. Please provide the associated code with relevant annotations and numpy docstrings explaining the code. Write the analysis code in the PEP8 style.

### Methodology
The results are based on the data for historical baseline from 1980 and the Representative Concentration Pathway 8.5 (rising carbon emissions) (RCP8.5) scenarios obtained from the World Resource Institute [1]. The population data used in the study is from the WorldPop website [2]. WorldPop provides different sets of data. In this work, the population count data was used. Through the attached codebase, the raster population count data layer was processed in python to estimate the number of people within a given polygon. The processing was done for each sub-regional level of the 47 counties of Kenya. The results are then aggregated into 47 counties of Kenya before being grouped into eight regions.

Example Results
==============

### Figure 1 Spatial distribution of vulnerable Kenyan population due to riverine flooding.
<p align="center">
  <img src="/docs/pop_flood_maps.tiff" />
</p>

### Figure 2 Average mean area and inudation depth of riverine flooding for 8 Kenyan regions
<p align="center">
  <img src="/docs/flood_plots.tiff" />
</p>

Required Data
==============

[1]	“World Resources Institute | Making Big Ideas Happen.” http://wri-projects.s3.amazonaws.com/AqueductFloodTool/download/v2/index.html (accessed May 08, 2023).
[2]	“Open Spatial Demographic Data and Research,” WorldPop. https://www.worldpop.org/ (accessed May 08, 2023).