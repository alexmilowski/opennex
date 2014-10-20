var server = window.location.href.substring(0,window.location.href.lastIndexOf('/'));
server = server.substring(0,server.lastIndexOf('/'));
var mapExplorer = new MapExplorer(server+"/data/avg-rcp85/",60);

window.addEventListener("load",function() {

   var loading = document.getElementById("loading");
   formatYearMonth = function(year,month) {
      return year+"-"+(month<10 ? "0"+month : month)      
   };
   var now = new Date();
   var year = now.getFullYear()
   var prefetch = [formatYearMonth(year,now.getMonth()+1)];
   for (var i=0; i<12; i++) {
      if (i!=now.getMonth()) {
         prefetch.push(formatYearMonth(year,i+1));
      }
   }
   console.log("Current: "+prefetch[0]);
   mapExplorer.init(
      document.getElementById("map"),
      prefetch,
      function(month) {
         if (month == prefetch[0]) {
            mapExplorer.showMonth(month);
            loading.style.display = "none";
         }
      }
   );
   
   var currentMonth = document.getElementById("current-month");
   var slider = document.getElementById("months-control");
   slider.value = (now.getFullYear() - 2006)*12 + now.getMonth();
   var monthLabel = function(value) {
      var months = parseInt(value);
      var year = 2006 + Math.floor(months/12);
      var month = months % 12 + 1;
      return year+"-"+(month<10 ? "0"+month : month);
      
   }
   slider.addEventListener("input",function() {
      var selected = monthLabel(slider.value);
      currentMonth.innerHTML = selected
   },false);
   var lastSelected = null;
   slider.addEventListener("change",function() {
      if (slider.timer) {
         clearTimeout(slider.timer);
      }
      var selected = monthLabel(slider.value);
      slider.timer = setTimeout(function() {
         slider.timer = null;
         loading.style.display = "block";
         mapExplorer.showMonth(selected,true,function() {
            loading.style.display = "none";
         });
      },200);
      slider.focus();
   },false);
   var selectedMonth = monthLabel(slider.value);
   currentMonth.innerHTML = selectedMonth;
   
   slider.focus();

   var colorLegend = document.getElementById("color-legend");

   for (var t=MapExplorer.cmin; t<=MapExplorer.cmax; t+=5) {
      var box = document.createElement("div");
      var prefix = t==MapExplorer.cmin ? "< " : "";
      var suffix = t==MapExplorer.cmax ? " >" : "";
      span = document.createElement("span")
      box.appendChild(span);
      span.appendChild(document.createTextNode(prefix+t.toString()+suffix));
      colorLegend.appendChild(box);
      var color = HeatMap.color(MapExplorer.cmin,MapExplorer.cmax,MapExplorer.adjustTemperature(t))
      box.style.backgroundColor = "rgb("+color[0]+","+color[1]+","+color[2]+")";

   }
   
},false)

function MapExplorer(server,resolution) {
   this.server = server;
   this.layers = {};
   this.resolution = typeof resolution == "undefined" ? 60 : resolution
}

MapExplorer.cmin = -20;
MapExplorer.cmax = 40;
MapExplorer.adjustTemperature = function(c) {
   if (c<=MapExplorer.cmin) {
      return MapExplorer.cmin;
   }
   if (c>=MapExplorer.cmax) {
      return MapExplorer.cmax;
   }
   if (c>=30) { // [30,40] -> [20,40]
      return ((c - 30)/(MapExplorer.cmax-30))*(MapExplorer.cmax-20) + 20;
   } else if (c>=10 && c<30) { // [10,30] -> [5,20]
      return ((c-10)/20)*15 + 5;
   } else { // [-20,10] -> [-20,5]
      return ((c+20)/(10-MapExplorer.cmin))*(5-MapExplorer.cmin) + -20;
   }
}

MapExplorer.prototype.init = function(mapElement,months,onfinish) {
   this.map = L.map('map').setView([37, -95], 5);
   L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
       attribution: '© <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
   }).addTo(this.map);
   var app = this;
   if (months) {
      for (var i=0; i<months.length; i++) {
         this.fetch(months[i],onfinish);
      }
   }
   this.map.on("click",function(e) {
      setTimeout(function() {
         app.showDetail(e.latlng.lat,e.latlng.lng);
      },1);
   });
}

MapExplorer.prototype.fetch = function(month,onfinish) {
   var app = this;
   try {
      
      var startTime = new Date();
      var request = new XMLHttpRequest();
      request.onreadystatechange = function() {
         if (request.readyState==4) {
            fetchTime = new Date();
            setTimeout(function() {
               app.createLayer(month,request.responseXML, { start: startTime, fetchEnd: fetchTime })
               if (onfinish) {
                  onfinish(month);
               }
            },1);
         }
      }
      var url = this.server+month+"/"+this.resolution+"/";
      request.open("GET",url,true);
      console.log("Fetching "+url);
      request.send();
   } catch(ex) {
      console.log(ex);
   }
   
}

MapExplorer.prototype.createLayer = function(month,xhtml,properties) {
   console.log("Creating layer for "+month);
   window.xhtml = xhtml
   GreenTurtle.attach(xhtml);
   
   var latFacet = this.server+"/data/#latitude";
   
   xhtml.data.setMapping("pan","http://pantabular.org/");
   var summary = xhtml.getElementsByType("pan:PartitionSummary")[0];
   
   var quadRange = null;
   var ranges = xhtml.data.getValues(summary.data.id,"pan:range");
   for (var r=0; r<ranges.length; r++) {
      if (xhtml.data.getValues(ranges[r],"pan:facet").indexOf(latFacet)) {
         quadRange = ranges[r];
      }
   }
   var box = xhtml.data.getValues(xhtml.data.getValues(quadRange,"pan:shape")[0],"schema:box")[0].split(/\s+/).map(function(s) { return parseFloat(s); });
   
   var scale = parseFloat(xhtml.data.getValues(summary.data.id,"pan:scale")[0]);
   
   var layerGroup = L.layerGroup();
   
   var cmin = -20;
   var cmax = 40;
   
   var items = xhtml.data.getValues(summary.data.id,"pan:item");
   var table = xhtml.getElementsBySubject(items[0])[0];
   for (row=1; row<table.rows.length; row++) {
      
      for (col=1; col<table.rows[row].cells.length; col++) {
         var s = table.rows[row].cells[col].textContent;
         var k = s.length>0 ? parseFloat(s) : 0.0;
         if (k>0) {
            var c = k - 273.15;
            var color = HeatMap.color(MapExplorer.cmin,MapExplorer.cmax,MapExplorer.adjustTemperature(c))
            var lat = box[0] - (row-1)*scale;
            var lon = box[1] + (col-1)*scale;
            var rect = L.rectangle([[lat,lon],[lat-scale,lon+scale]], {fill: true, color: "rgb("+color[0]+","+color[1]+","+color[2]+")", weight: 0, fillOpacity: 0.5});
            layerGroup.addLayer(rect);
         }
      }
   }
   info = {
      end: new Date(),
      layer: layerGroup
   };
   for (k in properties) {
      info[k] = properties[k];
   }
   this.layers[month] = info;
   console.log("Fetch: "+(info.fetchEnd.getTime() - info.start.getTime()));
   console.log("Elapsed: "+(info.end.getTime() - info.start.getTime()));
}

MapExplorer.prototype.showMonth = function(month,fetch,onfinish) {
   var info = this.layers[month];
   if (info) {
      console.log("Showing "+month);
      if (this.currentLayer) {
         this.map.removeLayer(this.currentLayer);
      }
      this.currentLayer = info.layer;
      this.map.addLayer(info.layer);
      if (onfinish) {
         onfinish();
      }
   } else if (fetch) {
      var app = this;
      this.lastSelected = month;
      this.fetch(month,function() {
         app.showMonth(app.lastSelected);
         if (onfinish) {
            onfinish();
         }
      });
   }
   
}

MapExplorer.prototype.showDetail = function(lat,lon) {
   console.log(lat+","+lon);
}
