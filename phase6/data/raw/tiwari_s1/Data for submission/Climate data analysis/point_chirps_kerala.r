
rm(list=ls())
library(raster)

rainfall_data=read.csv("C:/Users/amthapa/Desktop/delete/varun/kerala_chirps/kerala_point_flood.csv")
head(rainfall_data)

TIME = as.POSIXlt(rainfall_data$system.time_start)
YEAR=TIME$year+1900;head(YEAR)
MONTH = TIME$mon+1;head(MONTH)

rainfall<-rainfall_data[,-1]
head(rainfall)

jpeg(filename = "C:/Users/amthapa/Desktop/delete/varun/kerala_chirps/kerala_point_chirps.jpg",
     width = 6.18, height = 4.14, units = "in", pointsize = 12,res=600)
plot.new()
par(mfrow=c(2,3))
for(j in 1:6){

rainfall_i=rainfall[,j]
JJA_rain<-rainfall_i[MONTH==7|MONTH==8|MONTH==9]

ind<-seq(1,length(JJA_rain)+1,by=92);ind;length(ind)

library(randomcoloR)
n <- 9
my_col <- distinctColorPalette(n)
my_col=c('#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#000000') #https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/


par( mar=c(2,4,3,0.5) ,mgp=c(3,1,0), tck=-0.02 )
k=1
plot(1:92,cumsum(JJA_rain[ind[k]:(ind[k+1]-1)]),lwd=2,type="l",ylab="cumulative rain (mm)",pch=15,
                 xlab=" ",ylim=c(0,2200),col=my_col[k],main=colnames(rainfall)[j],xaxt="n")            
    
#axis(1,at=seq(1,92,1),labels = F)
abline(v=c(30,61),lty=2)

for(i in 2:(length(ind)-1)){
  #i=9
  lines(1:92,cumsum(JJA_rain[ind[i]:(ind[i+1]-1)]),type="l",col=my_col[i],lwd=2,pch=15) 
  #print(i)
}

if (j==1){
legend("topleft",legend=2010:2018,lty=1,col=my_col,lwd=2)
mtext(c("JUNE","JULY","AUGUST"),side=1, line =c(0.5),adj=c(0.15,0.5,0.9))
}else{
  mtext(c("JUNE","JULY","AUGUST"),side=1, line =c(0.5),adj=c(0.15,0.5,0.9))
  print('do nothing')}
print(j)
}
dev.off()



