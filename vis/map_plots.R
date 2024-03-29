library(sf)
library(ggpubr)
library(raster)
library(leaflet)
library(dplyr)
library(ggmap)
library(scales)
library(cvms)
library(tibble)
library(png)
library(ggimage)

suppressMessages(library(tidyverse))
folder <- dirname(rstudioapi::getSourceEditorContext()$path)

africa <-
  readPNG(file.path(folder, 'figures', 'Africa_global_map.png'))

s_america <-
  readPNG(file.path(folder, 'figures', 'South America_global_map.png'))

asia <-
  readPNG(file.path(folder, 'figures', 'Asia_global_map.png'))

n_america <-
  readPNG(file.path(folder, 'figures', 'North America_global_map.png'))

europe <-
  readPNG(file.path(folder, 'figures', 'Europe_global_map.png'))

### Africa map ###
africa <- ggplot() + background_image(africa) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### South America map ###
s_america <- ggplot() + background_image(s_america) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) +
  ggspatial::annotation_north_arrow(location = "br")

### Combine Africa and South America maps ###
africa_america <- ggarrange(
  africa,
  s_america,
  ncol = 2,
  common.legend = T,
  legend = "bottom",
  labels = c("A", "B")
)

###. save the combined image ###
path = file.path(folder, "figures", "africa_america.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 8,
  height = 4,
  res = 300
)
print(africa_america)
dev.off()

### Asia map ###
asia <- ggplot() + background_image(asia) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  ))
  

### North America map ###
n_america <- ggplot() + background_image(n_america) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) + ggspatial::annotation_north_arrow(location = "br")

### Europe map ###
europe <- ggplot() + background_image(europe) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 


### Combine the Asia maps ###
asia <- ggarrange(
  asia,
  nrow = 1,
  common.legend = T,
  legend = "bottom",
  labels = c('C')
)

###. save the combined image ###
path = file.path(folder, "figures", "asia.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 8,
  height = 7,
  res = 300
)
print(asia)
dev.off()


### Combine the Europe maps ###
n_america <- ggarrange(
  n_america,
  nrow = 1,
  common.legend = T,
  legend = "bottom",
  labels = c('D')
)

###. save the combined image ###
path = file.path(folder, "figures", "north_america.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 8,
  height = 7,
  res = 300
)
print(n_america)
dev.off()


### Combine the Europe maps ###
europe <- ggarrange(
  europe,
  nrow = 1,
  common.legend = T,
  legend = "bottom",
  labels = c('E')
)

###. save the combined image ###
path = file.path(folder, "figures", "europe.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 6,
  height = 5,
  res = 300
)
print(europe)
dev.off()



########################
##INDIVIDUAL COUNTRIES##
########################
rwanda <-
  readPNG(file.path(folder, 'figures', 'RWA_global_map.png'))

ukraine <-
  readPNG(file.path(folder, 'figures', 'UKR_global_map.png'))

bangladesh <-
  readPNG(file.path(folder, 'figures', 'BGD_global_map.png'))

mexico <-
  readPNG(file.path(folder, 'figures', 'MEX_global_map.png'))

peru <-
  readPNG(file.path(folder, 'figures', 'PER_global_map.png'))

timor <-
  readPNG(file.path(folder, 'figures', 'TLS_global_map.png'))


### Rwanda map ###
rwanda <- ggplot() + background_image(rwanda) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Ukraine map ###
ukraine <- ggplot() + background_image(ukraine) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Bangladesh map ###
bangladesh <- ggplot() + background_image(bangladesh) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Mexico map ###
mexico <- ggplot() + background_image(mexico) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Peru map ###
peru <- ggplot() + background_image(peru) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Timor map ###
timor <- ggplot() + background_image(timor) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Combine the Country maps ###
countries <- ggarrange(
  rwanda,
  ukraine,
  bangladesh,
  mexico,
  peru,
  timor,
  nrow = 3,
  ncol = 2,
  common.legend = T,
  legend = "bottom",
  labels = c('A', 'B', 'C', 'D', 'E', 'F')
) + ggspatial::annotation_north_arrow(location = "br")

###. save the combined image ###
path = file.path(folder, "figures", "individual_countries.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 9,
  height = 10,
  res = 300
)
print(countries)
dev.off()


#####################
##COASTAL FLOODING ##
#####################

###############
##CONTINENTS ##
###############
africa_coast <-
  readPNG(file.path(folder, 'figures', 'Africa_coastal_map.png'))

s_america_coast <-
  readPNG(file.path(folder, 'figures', 'South America_coastal_map.png'))

asia_coast <-
  readPNG(file.path(folder, 'figures', 'Asia_coastal_map.png'))

n_america_coast <-
  readPNG(file.path(folder, 'figures', 'North America_coastal_map.png'))

europe_coast <-
  readPNG(file.path(folder, 'figures', 'Europe_coastal_map.png'))

### Africa map ###
africa_coast <- ggplot() + background_image(africa_coast) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### South America map ###
s_america_coast <- ggplot() + background_image(s_america_coast) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) +
  ggspatial::annotation_north_arrow(location = "br")

### Combine Africa and South America maps ###
africa_america <- ggarrange(
  africa_coast,
  s_america_coast,
  ncol = 2,
  common.legend = T,
  legend = "bottom",
  labels = c("A", "B")
)

###. save the combined image ###
path = file.path(folder, "figures", "africa_america_coast.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 8,
  height = 3.5,
  res = 300
)
print(africa_america)
dev.off()

### Asia map ###
asia_coast <- ggplot() + background_image(asia_coast) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  ))


### North America map ###
n_america_coast <- ggplot() + background_image(n_america_coast) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) + ggspatial::annotation_north_arrow(location = "br")

### Europe map ###
europe_coast <- ggplot() + background_image(europe_coast) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 


### Combine the Asia maps ###
asia_coast <- ggarrange(
  asia_coast,
  nrow = 1,
  common.legend = T,
  legend = "bottom",
  labels = c('C')
)

###. save the combined image ###
path = file.path(folder, "figures", "asia_coast.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 8,
  height = 7,
  res = 300
)
print(asia_coast)
dev.off()

### Combine the North America maps ###
n_america_coast <- ggarrange(
  n_america_coast,
  nrow = 1,
  common.legend = T,
  legend = "bottom",
  labels = c('D')
)

###. save the combined image ###
path = file.path(folder, "figures", "north_america_coast.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 8,
  height = 7,
  res = 300
)
print(n_america_coast)
dev.off()

### Combine the Europe maps ###
europe_coast <- ggarrange(
  europe_coast,
  nrow = 1,
  common.legend = T,
  legend = "bottom",
  labels = c('D')
)

###. save the combined image ###
path = file.path(folder, "figures", "europe_coast.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 8,
  height = 7,
  res = 300
)
print(europe_coast)
dev.off()

########################################
##INDIVIDUAL COUNTRY COASTAL FLOODING ##
########################################
bangladesh <-
  readPNG(file.path(folder, 'figures', 'BGD_coastal_map.png'))

philipines <-
  readPNG(file.path(folder, 'figures', 'PHL_coastal_map.png'))

coasta_rica <-
  readPNG(file.path(folder, 'figures', 'CRI_coastal_map.png'))

ecuador <-
  readPNG(file.path(folder, 'figures', 'ECU_coastal_map.png'))

kenya <-
  readPNG(file.path(folder, 'figures', 'KEN_coastal_map.png'))

albania <-
  readPNG(file.path(folder, 'figures', 'ALB_coastal_map.png'))

### Bangladesh map ###
bangladesh <- ggplot() + background_image(bangladesh) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Phillipines map ###
philipines <- ggplot() + background_image(philipines) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Costa Rica map ###
coasta_rica <- ggplot() + background_image(coasta_rica) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Ecuador map ###
ecuador <- ggplot() + background_image(ecuador) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Kenya map ###
kenya <- ggplot() + background_image(kenya) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Albania map ###
albania <- ggplot() + background_image(albania) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Combine the Country maps ###
countries <- ggarrange(
  bangladesh,
  philipines,
  coasta_rica,
  kenya,
  ecuador,
  albania,
  nrow = 3,
  ncol = 2,
  common.legend = T,
  legend = "bottom",
  labels = c('A', 'B', 'C', 'D', 'E', 'F')
) + ggspatial::annotation_north_arrow(location = "br")

###. save the combined image ###
path = file.path(folder, "figures", "coastal_countries.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 9,
  height = 10,
  res = 300
)
print(countries)
dev.off()

