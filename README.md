# Global Assessment of Natural Hazards towards Vulnerable and Unconnected Population (glanhavup)
Over the next century we are expected to experience an increase in the frequency and severity of climate-related hazards, including coastal flooding, riverine flooding, and tropical storms. Dealing with extreme events is considerably easy for the affluent, who have the resources to vacate to a safer location and replace damaged property. In contrast, those living on the poverty line (US$ 2 per day) often must shelter in place and may have their entire livelihood disrupted from storm damage. 

Owning a cell phone is one way that vulnerable people can mitigate their vulnerability to extreme weather events. For example, voice and data connectivity can help in accessing early warning messages, calling for emergency services, and obtaining post-event financial aid via mobile money transfer (Opitz-Stapleton et al., 2019). However, there are still vast global disparities in those who have easy access to mobile cellular services, and those who do not.

Consequently, we are not aware of any study which has hitherto sought to simultaneously quantify the number of (i) unconnected mobile users globally, (ii) those living on the poverty line (<$2 per day), and (iii) the population exposed to climate-related hazards. Therefore, the purpose of this study is to undertake such an assessment and try to answer the following research questions: 

1.	What portion of the global poverty-line population is unconnected (to 2G, 3G, 4G and 5G) and where are they?
2.	Who is vulnerable to different climate-driven natural hazards (such as coastal flooding, riverine flooding, and tropical cyclones) and where are they?
3.	How many of the unconnected poverty-line population are simultaneously increasingly exposed to increasing climate-driven natural hazards?

Such a topic is worthy of investigation as the analytics produced help inform universal broadband and poverty-alleviation policies. 

Methodology
==============
The method (see Figure 1) will utilize 47 million OpenCelliD data points to inform 2G, 3G, 4G and 5G coverage. Income estimates for low and middle income countries will be utilized for poverty estimation at the 1 km2 level (Chi et al., 2022). Additionally, multiple hazard models will be utilized, for flooding from the World Resource Institute Aqueduct platform, and for tropical cyclones from recently developed maximum wind speed estimates. Hazard impacts will be compared for a historical scenario (1980) and compared to a worst-case (RCP8.5) representing no emissions abatement, for different event probabilities. 

## Method Box

### Figure 1 Proposed Method.
<p align="center">
  <img src="/docs/method.png" />
</p>

The results are based on the data for historical baseline from 1980 and the Representative Concentration Pathway 8.5 (rising carbon emissions) (RCP8.5) scenarios obtained from the World Resource Institute [1]. The population data used in the study is from the WorldPop website [2]. WorldPop provides different sets of data. In this work, the population count data was used. Through the attached codebase, the raster population count data layer was processed in python to estimate the number of people within a given polygon. The processing was done for each sub-regional level of the 47 counties of Kenya. The results are then aggregated into 47 counties of Kenya before being grouped into eight regions.

## Example Results

### Figure 1 Spatial distribution of vulnerable Kenyan population due to riverine flooding.
<p align="center">
  <img src="/docs/pop_flood_maps.png" />
</p>

### Figure 2 Average mean area and inudation depth of riverine flooding for 8 Kenyan regions
<p align="center">
  <img src="/docs/flood_plots.png" />
</p>

## Required Data

[1]	“World Resources Institute | Making Big Ideas Happen.” http://wri-projects.s3.amazonaws.com/AqueductFloodTool/  download/v2/index.html (accessed May 08, 2023).

[2]	“Open Spatial Demographic Data and Research,” WorldPop. https://www.worldpop.org/ (accessed May 08, 2023).

[3] Country metadafile. Contained in `/data/countries.csv`
