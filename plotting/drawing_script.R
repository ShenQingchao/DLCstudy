library(ggplot2)
library(readxl)
library(plyr)
library(patchwork)
library(corrplot)

bugs <-  read_excel(path = 'dataset.xlsx', sheet="ALL")
bugs$project=factor(bugs$project, levels = c("TVM","Glow","nGraph"))
#bugs$`root causes` = factor(bugs$`root causes`, levels = c("Crash","Wrong Code","Bad Performance","Hang","Build Failure","Unreported"))
tvm_bugs = subset(bugs, project=="TVM")
glow_bugs = subset(bugs, project=="Glow")
ngraph_bugs = subset(bugs, project=="nGraph")
bugs_number = as.vector(table(bugs$project))
bugs_number = c()
bugs_number[1:6] <- 318  # tvm
bugs_number[7:12] <- 145  #glow
bugs_number[13:17] <- 140 # nGraph no hang

sym_palette <- c("#F4ACB7","#FFD3DB","#DDEEF4","#ACD9E9","#74ADD1","#4575B4") 
sym_palette <- rev(sym_palette)

my_axis_size <- 9.5
my_title_size <- 12
my_legend_size <- 9.5
my_axis_color="black"


# plot root causes_stack


# order in my order
causes_data <- table(bugs$`root causes`)
causes_data <- sort(causes_data, decreasing = F)
causes_name <- as.data.frame(causes_data)$Var1
causes_name <- as.array(causes_name)

bugs$`root causes` = factor(bugs$`root causes`, levels = causes_name)

causes_palette <- c("#D2E6F1","#9ECAE1","#3182BD") #blue 
bugs$project=factor(bugs$project, levels = c("nGraph","Glow","TVM"))
p <- ggplot(bugs, aes(y=`root causes`, fill = project))
p + geom_bar( alpha = 0.9) + 
  xlab("") + 
  ylab("") + 
  scale_fill_manual(values = causes_palette, guide = guide_legend(reverse=TRUE))+
  theme(panel.background = element_rect(fill = "#efefef")
        ,axis.text = element_text( face="bold", 
                                   size = my_axis_size, 
                                   colour = my_axis_color),
        legend.position = "bottom"
        ,legend.title=element_blank()
        ,legend.text = element_text(size = my_legend_size, 
                                    face = "bold"),
  )+
  geom_text(aes(label=..count..),
            stat = 'count',
            position = position_stack(vjust = 0.5))

ggsave("causes.pdf")


################ plot stage_pie ##########################
stage_palette <- c("#DEEBF7","#9ECAE1","#3182BD") #blue !!!


pie_function <- function(input_data, title_){
  temp <- subset(input_data, !is.na(input_data$stages))
  total_ <- sum(table(temp$stages)) # bug number in each stage
  pie1 <- ggplot(temp, aes(x=1 ,fill=stages))
  pie1 <- pie1 + geom_bar() + 
    coord_polar(theta = "y")+
    scale_fill_manual(values = stage_palette,
                      breaks = c("Model Loading","High-Level IR Transformation","Low-Level IR Transformation"),
    )+
    labs(title=title_)+
    theme_void() +
    theme(axis.text=element_blank(),
          axis.ticks=element_blank(),
          plot.title = element_text(hjust = 0.5, 
                                    vjust = -60, 
                                    face = "bold",
                                    size = my_title_size,
                                    colour = my_axis_color),
          legend.title=element_blank(),
          legend.text = element_text(size = my_legend_size, face = "bold"),
          legend.position = "right") +  
    # guides(fill=FALSE)+
    geom_text(aes(label=paste(round(..count.. / total_,4)*100,"%", sep = ''),x=1.1), 
              stat = 'count', size=4.8, position = position_stack(vjust =0.5 ))
  
}

pie1 <- pie_function(tvm_bugs,"TVM")
pie2 <- pie_function(glow_bugs, "Glow")
pie3 <- pie_function(ngraph_bugs, "nGraph")

p <- pie1 +pie2 +pie3 +plot_layout(ncol=3, guides = 'collect')
p
ggsave("stage.pdf", height=4)



# ################### correlation ###########################

bugs <-  read_excel(path = 'bug_github2 (16).xlsx', sheet="All in one")
tvm_bugs = subset(bugs, project=="TVM")
glow_bugs = subset(bugs, project=="Glow")
ngraph_bugs = subset(bugs, project=="nGraph")
bugs_number = as.vector(table(bugs$project))
bugs_number = c()
bugs_number[1:12] <- as.vector(table(bugs$project))[1]  # 12 categories of root causes, including: other
bugs_number[13:24] <- as.vector(table(bugs$project))[2]
bugs_number[25:36] <- as.vector(table(bugs$project))[3]

row_name <- c("TVM", "Glow", "nGraph")
########################## root causes ##########################
a <- table(bugs$`root causes`, bugs$project)
a <- a/bugs_number
glow_ <- a[1:12]
ngraph_ <- a[13:24]
tvm_ <- a[25:36]

cor_tvm_glow_causes <- cor(glow_,tvm_, method = "spearman")    
cor_tvm_ngraph_causes <- cor(tvm_,ngraph_,method = "spearman")    
cor_glow_ngraph_causes <- cor(ngraph_,glow_,method = "spearman")  

res_causes <- c(1, cor_tvm_glow_causes, cor_tvm_ngraph_causes, 
                cor_tvm_glow_causes, 1, cor_glow_ngraph_causes, 
                cor_tvm_ngraph_causes, cor_glow_ngraph_causes, 1)

my_color <- c()
my_color[1:16] <- "grey"
#my_color[17:20] <- c("#E6F5D0","#B8E186","#7FBC41","#4D9221") # green!!!!!!
my_color[17:20]<- c("white","#9ECAE1","#438DC3","#3182BD") #blue !!!


col_my=colorRampPalette(my_color)

res_cor <- matrix(data=res_causes, nrow = 3, ncol = 3, dimnames = list(row_name, row_name))
p1 <- corrplot::corrplot(corr=res_cor,
                         method = "color",
                         order = "AOE",
                         col = col_my(400),
                         addCoef.col = "black",
                         type = "lower",
                         diag=T,
                         bg="white",
                         outline=TRUE,
                         rect.col="blue",
                         number.cex=1.1,
                         
                         tl.srt = 0, 
                         tl.offset=1, 
                         tl.pos = "ld",
                         tl.col="black",
                         tl.cex = 1.2,
                         
                         cl.lim = c(.7, 1),
                         cl.pos = "b", # legend in the bottom
                         cl.ratio = .3, # legend width
                         #cl.align.text = "l",
                         cl.length=4,
                         cl.cex = 1,)
p1

###################### symptoms ####################################
b <- table(bugs$`symptoms`, bugs$project)
# b <- b/bugs_number
glow_symptoms <- b[1:6]
ngraph_symptoms <- b[7:12]
tvm_symptoms <- b[13:18]


cor_tvm_glow_sym <- cor(glow_symptoms,tvm_symptoms, method = "spearman")    
cor_tvm_ngraph_sym <- cor(tvm_symptoms,ngraph_symptoms,method = "spearman")   
cor_glow_ngraph_sym <- cor(ngraph_symptoms,glow_symptoms,method = "spearman")  

res <- c(1, cor_tvm_glow_sym, cor_tvm_ngraph_sym, 
         cor_tvm_glow_sym, 1, cor_glow_ngraph_sym, 
         cor_tvm_ngraph_sym, cor_glow_ngraph_sym, 1)


res_cor <- matrix(data=res, nrow = 3, ncol = 3, dimnames = list(row_name, row_name))


p1 <- corrplot::corrplot(corr=res_cor,
                         method = "color",
                         order = "AOE",
                         col = col_my(400),
                         addCoef.col = "black",
                         type = "lower",
                         diag=T,
                         bg="white",
                         outline=TRUE,
                         rect.col="blue",
                         number.cex=1.1,
                         
                         tl.srt = 0, 
                         tl.offset=1, 
                         tl.pos = "ld",
                         tl.col="black",
                         tl.cex = 1.2,
                         
                         cl.lim = c(.7, 1),
                         cl.pos = "b", # legend in the right
                         cl.ratio = .3, # legend width
                         #cl.align.text = "l",
                         
                         cl.length=4,
                         cl.cex = 1,)
p1


