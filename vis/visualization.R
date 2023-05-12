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

data <- read.csv(file.path(folder, "quantity_results.csv"))

hist_ke <-
  readPNG(file.path(folder, "data", "processed", "KEN", "kenya_flood_historical_model.png"))

model_ke <-
  readPNG(file.path(folder, "data", "processed", "KEN", "kenya_flood_hadgem_model.png"))

model_flood_pop <-
  readPNG(file.path(folder, "data", "processed", "KEN", "hadgem_pop_flood_fig.png"))

hist_flood_pop <-
  readPNG(file.path(folder, "data", "processed", "KEN", "historical_pop_flood_fig.png"))

### Historical flood map ###
hist_floods <- ggplot() + background_image(hist_ke) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Model flood map ###
model_floods <- ggplot() + background_image(model_ke) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) +
  ggspatial::annotation_north_arrow(location = "br")

### Combine the two maps ###
comb_map <- ggarrange(
  hist_floods,
  model_floods,
  ncol = 2,
  common.legend = T,
  legend = "bottom",
  labels = c("a", "b")
)

###. save the combined image ###
path = file.path(folder, "data", "flood_maps.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 8,
  height = 5,
  res = 300
)
print(comb_map)
dev.off()

### Model population flood map ###
pop_floods_model <- ggplot() + background_image(model_flood_pop) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) +
  ggspatial::annotation_north_arrow(location = "br")

### Historical population flood map ###
pop_floods_hist <- ggplot() + background_image(hist_flood_pop) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Combine the two maps ###
comb_map <- ggarrange(
  pop_floods_hist,
  pop_floods_model,
  ncol = 2,
  common.legend = T,
  legend = "bottom",
  labels = c("a", "b")
)

###. save the combined image ###
path = file.path(folder, "data", "pop_flood_maps.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 6,
  height = 3.5,
  res = 300
)
print(comb_map)
dev.off()

###FLOODING QUANTIFICATION ####
data$scenario = factor(
  data$scenario,
  levels = c('historical', 'rcp'),
  labels = c('Historical Baseline', 'RCP8.5 2080')
)

#####################################################
##plot1 = Riverine flooding by population with bars##
#####################################################
df1 = data %>%
  group_by(region, scenario) %>%
  summarize(mean = mean(population),
            sd = sd(population))
max_y_value = max(df1$mean)

flood_population <- ggplot(df1, 
                           aes(x=region, y=mean, fill=scenario)) + 
  geom_bar(stat="identity", position = position_dodge()) +
  geom_errorbar(data=df1, aes(y = mean, ymin = mean-sd/6, ymax = mean+sd/6),
                position = position_dodge(1),
                lwd = 0.2,
                show.legend = FALSE, width=0.5,  color="black") +
  geom_text(aes(label = format(round(after_stat(y), 0), scientific = FALSE)), size = 1.8,
            position = position_dodge(1), vjust =.6, hjust =-.7, angle = 90)+
  theme(legend.position = 'bottom',
        axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(colour=NULL,
       title = "Estimated Riverine Flooding Impact to Kenyan Population",
       subtitle = "Reported by Region, and Climate Scenario.", 
       x = NULL, y = "Population", 
       fill=NULL) + 
  theme(panel.spacing = unit(0.6, "lines")) + 
  expand_limits(y=0) +
  guides(fill = guide_legend(ncol = 3, title = 'Climate Scenario')) +
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(expand = c(0, 0), labels = function(y)
    format(y, scientific = FALSE), limits = c(0, 100000)) + 
  facet_wrap(~scenario, ncol = 2, nrow = 1)

#######################################
##plot2 = Riverine flooding by area ###
#######################################
df = data %>%
  group_by(region, scenario) %>%
  summarize(mean = mean(area*1e4),
            sd = sd(area*1e4))
max_y_value = max(df$mean)

flood_area <- ggplot(df, 
       aes(x=region, y=mean, fill=scenario)) + 
  geom_bar(stat="identity", position = position_dodge()) +
  geom_errorbar(data=df, aes(y = mean, ymin = mean-sd/15, ymax = mean+sd/15),
                position = position_dodge(1),
                lwd = 0.2,
                show.legend = FALSE, width=0.5,  color="black") +
  geom_text(aes(label = format(round(after_stat(y), 4), scientific = FALSE)), size = 1.8,
            position = position_dodge(1), vjust =.5, hjust =-.6, angle = 90)+
  theme(legend.position = 'bottom',
        axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(colour=NULL,
       title = "Riverine Flooded Mean Area for Exposed Regions in Kenya",
       subtitle = "Reported by Region, and Climate Scenario.", 
       x = NULL, y = "Mean Flooded Area (bquote(~m^2)", 
       fill=NULL) + ylab(bquote('Mean Area '*(m^2)*'')) +
  theme(panel.spacing = unit(0.6, "lines")) + 
  expand_limits(y=0) +
  guides(fill = guide_legend(ncol = 3, title = 'Climate Scenario')) +
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(expand = c(0, 0), labels = function(y)
      format(y, scientific = FALSE), limits = c(0, 6.5)) + 
  facet_wrap(~scenario, ncol = 2, nrow = 1)

###########################################
##plot2 = Riverine flooding by mean depth##
###########################################
df2 = data %>%
  group_by(region, scenario) %>%
  summarize(mean = mean(value),
            sd = sd(value))
max_y_value = max(df$mean)

flood_depth <- ggplot(df2, 
       aes(x = region, y = mean, fill = scenario)) + 
  geom_bar(stat = "identity", position = position_dodge()) +
  geom_errorbar(data = df2, aes(y = mean, ymin = mean-sd/10, ymax = mean+sd/10),
                position = position_dodge(1), lwd = 0.2,
                show.legend = FALSE, width=0.5,  color="black") +
  geom_text(aes(label = format(round(after_stat(y), 2), scientific = FALSE)), size = 1.8,
            position = position_dodge(1), vjust =.5, hjust =-.6, angle = 90) +
  theme(legend.position = 'bottom',
        axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(colour = NULL,
       title = "Estimated Mean Inudation Depth of the Riverine Flooded Areas in Kenya",
       subtitle = "Reported by Region, and Climate Scenario.", 
       x = NULL, y = "Mean Inudation Depth (m)", 
       fill=NULL) +
  theme(panel.spacing = unit(0.6, "lines")) + 
  expand_limits(y = 0) +
  guides(fill = guide_legend(ncol = 3, title = 'Climate Scenario')) +
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(expand = c(0, 0), labels = function(y)
    format(y, scientific = FALSE), limits = c(0, 3.5)) + 
  facet_wrap(~scenario, ncol = 2, nrow = 1)

### Combine the two maps ###
pop <- ggarrange(
  flood_population,
  nrow = 1,
  common.legend = T,
  legend = "bottom",
  labels = c("a")
)

path = file.path(folder, "data", "pop_plots.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 6,
  height = 5,
  res = 300
)
print(pop)
dev.off()

### Combine the two maps ###
comb_floods <- ggarrange(
  flood_area,
  flood_depth,
  nrow = 2,
  common.legend = T,
  legend = "bottom",
  labels = c("a", "b")
)

path = file.path(folder, "data", "flood_plots.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 7,
  height = 9,
  res = 300
)
print(comb_floods)
dev.off()

#### DATA TYPES ####
unconst <-
  readPNG(file.path(folder, "pic", "unconstrained.png"))

const <-
  readPNG(file.path(folder, "pic", "constrained.png"))

### Unconstrained ###
unconstrained <- ggplot() + background_image(unconst) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Constrained ###
constrained <- ggplot() + background_image(const) +
  theme(plot.margin = margin(
    t = 0,
    l = 0,
    r = 0,
    b = 0,
    unit = "cm"
  )) 

### Combine the two maps ###
comb_constrained <- ggarrange(
  unconstrained,
  constrained,
  ncol = 2,
  common.legend = T,
  legend = "bottom",
  labels = c("a", "b")
)

###. save the combined image ###
path = file.path(folder, "figures", "constrained.tiff")
dir.create(file.path(folder), showWarnings = FALSE)
tiff(
  path,
  units = "in",
  width = 6,
  height = 3.5,
  res = 300
)
print(comb_constrained)
dev.off()





















