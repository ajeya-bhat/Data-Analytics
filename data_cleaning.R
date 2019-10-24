library(dplyr)
library(tidyverse)
library(data.table)

data_19 = read.csv("players_19.csv",header = TRUE,stringsAsFactors = FALSE)
data_19$player_url <- NULL
data_19$dob <- NULL
data_19$real_face <- NULL
data_19$player_traits <- NULL
data_19$long_name <- NULL
data_19$player_tags <- NULL
data_19$body_type <- NULL


data_19 <- data_19[-c(72:98)]


data_19$primary_position <- map(data_19$player_positions,function(x) trimws(unlist(strsplit(x,",")))[1])
data_19_strikers <- data_19 %>% filter(data_19$primary_position %in% c("ST","RW","LW","CF","RF","LF","RS","LS"))
data_19_midfielders <-  data_19 %>% filter(data_19$primary_position %in% c("RCM","LCM","CM","LM","RM","CDM","LDM","RDM","LAM","CAM","RAM"))
data_19_defenders <- data_19 %>% filter(data_19$primary_position %in% c("CB","LB","RB","RCB","LCB","RWB","LWB"))
data_19_goalkeepers <- data_19 %>% filter(data_19$primary_position %in% c("GK"))

q <- colnames(data_19_defenders)
q <- grep("^gk_+",q,value = TRUE)
p <- c("pace","shooting","passing","dribbling","defending","physic")

data_19_strikers <- data_19_strikers[,!names(data_19_strikers) %in% q]
data_19_defenders <- data_19_defenders[,!names(data_19_defenders) %in% q]
data_19_midfielders <- data_19_midfielders[,!names(data_19_midfielders) %in% q]
data_19_goalkeepers <- data_19_goalkeepers[,!names(data_19_goalkeepers) %in% p]




#data_19_strikers <- ldply(data_19_strikers,data.frame)


#write.csv(data_19_strikers,"D:\\5th sem\\data_analytics\\project\\changed_dataset\\players_19_strikers.csv",row.names = FALSE)

#data_19_pca_strikers <- na.omit(data_19_strikers[,-c(1:3,6,7,12:19,20:26,34)])
#data_19_pca_strikers <- sapply(data_19_pca_strikers,function(y) data_clean(y))
#data_19_pca_strikers <- sapply(data_19_pca_strikers,as.numeric)

#data_19_pca_strikers <-  prcomp(as.data.frame(data_19_pca_strikers),center = TRUE,scale. = TRUE)

