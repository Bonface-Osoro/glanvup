library(ggpubr)
library(ggplot2)
library(tidyverse)
library(ggtext)

suppressMessages(library(tidyverse))
folder <- dirname(rstudioapi::getSourceEditorContext()$path)
data <- read.csv(file.path(folder, '..', 'data', 'global_results', 'vulnerable_riverine_results.csv'))

#####################################################
##Global Unconnected people Under Riverine Flooding##
#####################################################

df = data %>%
  group_by(period, scenario, region) %>%
  summarize(mean = sum(value_1),
            sd = sd(value_1))

df$region = factor(
  df$region,
  levels = c('EAP', 'ECA', 'LAC', 'MENA', 'NA', 'SA', 'SSA'),
  labels = c(
    'East Asia \n& Pacific',
    'Europe & \nCentral Asia',
    'Latin America \n& the Caribbean',
    'Middle East \n& North Africa',
    'North America',
    'South Asia',
    'Sub-Saharan \nAfrica'
  )
)

df$period = factor(
  df$period,
  levels = c('rp00100', 'rp01000'),
  labels = c('0.1%', '0.01%')
)
df$scenario = factor(
  df$scenario,
  levels = c('historical', 'rcp4p5', 'rcp8p5'),
  labels = c(
    'Historical (Baseline Condition)',
    'RCP4.5 (2050 Projection)',
    'RCP8.5 (2080 Projection)'
  )
)

max_y_value = (max(df$mean)) / 1e9

riverine_flood_population <-
  ggplot(df,  aes(x = period, y = mean / 1e9, fill = region)) +
  geom_bar(stat = "identity", position = position_dodge(0.9)) +
  geom_errorbar(data = df, 
      aes(y = (mean / 1e9), ymin = (mean / 1e9) - (sd / 1e5),
      ymax = (mean / 1e9) + (sd / 1e5)), 
      position = position_dodge(0.9),
      lwd = 0.2, show.legend = FALSE, width = 0.5, color = "red") +
  geom_text(aes(label = format(round(after_stat(y), 3), 
    scientific = FALSE)),
    size = 1.8, position = position_dodge(0.9), 
    vjust = .5, hjust = -.43, angle = 90) +
  labs(colour = NULL, 
       title = "Estimated Number of Vulnerable Global Population to Riverine Flooding",
       subtitle = "Reported by Climate Scenario, Annual Probability and World Bank Classification of Regions",
       x = 'Annual Probability', y = "Population (billions)", fill = NULL) +
  theme(legend.position = 'bottom', 
        axis.text.x = element_text(hjust = 1, size = 8),
        panel.spacing = unit(0.6, "lines"), 
        axis.text.y = element_text(size = 8),
        axis.title.y = element_text(size = 8), 
        axis.title.x = element_text(size = 8)) +
  expand_limits(y = 0) + 
  guides(fill = guide_legend(nrow = 1, title = 'Regions')) +
  scale_fill_viridis_d(direction = 1) + 
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(expand = c(0, 0), 
  labels = function(y) format(y, scientific = FALSE),
  limits = c(0, 1.0)) + facet_wrap( ~ scenario)

#################################################
##Estimated Global Area Under Riverine Flooding##
#################################################

df = data %>%
  group_by(period, scenario, region) %>%
  summarize(mean = sum(area),
            sd = sd(area))

df$region = factor(
  df$region,
  levels = c('EAP', 'ECA', 'LAC', 'MENA', 'NA', 'SA', 'SSA'),
  labels = c(
    'East Asia \n& Pacific',
    'Europe & \nCentral Asia',
    'Latin America \n& the Caribbean',
    'Middle East \n& North Africa',
    'North America',
    'South Asia',
    'Sub-Saharan \nAfrica'
  )
)

df$period = factor(
  df$period,
  levels = c('rp00100', 'rp01000'),
  labels = c('0.1%', '0.01%')
)
df$scenario = factor(
  df$scenario,
  levels = c('historical', 'rcp4p5', 'rcp8p5'),
  labels = c(
    'Historical (Baseline Condition)',
    'RCP4.5 (2050 Projection)',
    'RCP8.5 (2080 Projection)'
  )
)

max_y_value = (max(df$mean)) / 1e12

riverine_flood_area <-
  ggplot(df,  aes(x = period, y = mean / 1e12, fill = region)) +
  geom_bar(stat = "identity", position = position_dodge(0.9)) +
  geom_errorbar(data = df, 
      aes(y = (mean/ 1e12), ymin = (mean / 1e12) - (sd / 1e7),
      ymax = (mean / 1e12) + (sd / 1e7)), 
      position = position_dodge(0.9),
      lwd = 0.2, show.legend = FALSE, width = 0.5, color = "red") +
  geom_text(aes(label = format(round(after_stat(y), 3), 
      scientific = FALSE)),
      size = 1.8, position = position_dodge(0.9), 
      vjust = .5, hjust = -1.35, angle = 90) +
  labs(colour = NULL, 
       title = "Estimated Global Area Under Riverine Flooding",
       subtitle = "Reported by Climate Scenario, Annual Probability and World Bank Classification of Regions",
       x = 'Annual Probability', y = "Flooded Area (millions)", fill = NULL) + 
       ylab("Flooded Area (Millions km<sup>2)") +
  theme(legend.position = 'bottom', 
        axis.text.x = element_text(hjust = 1, size = 8),
        panel.spacing = unit(0.6, "lines"), 
        axis.text.y = element_text(size = 8),
        axis.title.y = element_markdown(size = 8),
        axis.title.x = element_text(size = 8)) +
  expand_limits(y = 0) + 
  guides(fill = guide_legend(nrow = 1, title = 'Regions')) +
  scale_fill_viridis_d(direction = 1) + 
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(expand = c(0, 0), 
  labels = function(y) format(y, scientific = FALSE),
  limits = c(0, 1.7)) + facet_wrap( ~ scenario)


####################################################
##Global Population Vulnerable to Coastal Flooding##
####################################################
data <- read.csv(file.path(folder, '..', 'data', 'global_results', "vulnerable_coastal_results.csv"))

df = data %>%
  group_by(region, scenario, period) %>%
  summarize(mean = sum(value_1),
            sd = sd(value_1))

df$period = factor(
  df$period,
  levels = c('rp00100', 'rp01000'),
  labels = c('0.1%', '0.01%')
)
df$scenario = factor(
  df$scenario,
  levels = c('historical', 'rcp4p5', 'rcp8p5'),
  labels = c(
    'Historical (Baseline Condition)',
    'RCP4.5 (2050 Projection)',
    'RCP8.5 (2080 Projection)'
  )
)

max_y_value = (max(df$mean)) / 1e9

coastal_flood_population <-
  ggplot(df,  aes(x = period, y = mean / 1e9, fill = region)) +
  geom_bar(stat = "identity", position = position_dodge(0.9)) +
  geom_errorbar(data = df, 
      aes(y = (mean / 1e9), ymin = (mean / 1e9) - (sd / 1e5),
      ymax = (mean / 1e9) + (sd / 1e5)), 
      position = position_dodge(0.9),
      lwd = 0.2, show.legend = FALSE, width = 0.5, color = "red") +
  geom_text(aes(label = format(round(after_stat(y), 3), 
      scientific = FALSE)),
      size = 1.8, position = position_dodge(0.9), 
      vjust = .5, hjust = -.43, angle = 90) +
  labs(colour = NULL, 
       title = "Estimated Number of Vulnerable Global Population to Riverine Flooding",
       subtitle = "Reported by Climate Scenario, Annual Probability and World Bank Classification of Regions",
       x = 'Annual Probability', y = "Population (billions)", fill = NULL) +
  theme(legend.position = 'bottom', 
        axis.text.x = element_text(hjust = 1, size = 8),
        panel.spacing = unit(0.6, "lines"), 
        axis.text.y = element_text(size = 8),
        axis.title.y = element_text(size = 8), 
        axis.title.x = element_text(size = 8)) +
  expand_limits(y = 0) + 
  guides(fill = guide_legend(nrow = 1, title = 'Regions')) +
  scale_fill_viridis_d(direction = 1) + 
  scale_x_discrete(expand = c(0, 0.15)) +
  scale_y_continuous(expand = c(0, 0), 
                     labels = function(y) format(y, scientific = FALSE),
                     limits = c(0, 1.0)) + facet_wrap( ~ scenario)


#################################
##Riverine Flooding panel plots##
#################################

global_riverine_flooding <-
  ggarrange(
    riverine_flood_area,
    riverine_flood_population,
    nrow = 2,
    ncol = 1,
    labels = c("A", "B"),
    legend = 'bottom',
    common.legend = TRUE
    
  )

path = file.path(folder, 'figures', 'global_riverine_flooding.png')
dir.create(file.path(folder, 'figures'), showWarnings = FALSE)
png(
  path,
  units = "in",
  width = 7.5,
  height = 7.5,
  res = 480
)
print(global_riverine_flooding)
dev.off()







