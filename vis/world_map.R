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
africa_basemap <- st_read(file.path(folder, '..', 'data', 'global_results', 'Africa_Boundaries', 'World_Countries.shp'))

shapefile_folder <- file.path(folder, '..', 'data', 'global_results', 'shapefiles', 'Africa')
shapefile_list <- list.files(shapefile_folder, pattern = ".shp$", full.names = TRUE)
shapefiles <- lapply(shapefile_list, st_read)

p <- ggplot() +
  geom_sf(data = africa_basemap)

for (i in 1:length(shapefiles)) {
  p <- p + geom_sf(data = shapefiles[[i]], fill = NA, color = "green")
}

print(p)




