var mapExplorer = new MapExplorer(window.location.protocol+"//"+window.location.host,60);

window.addEventListener("load",function() {

   mapExplorer.init(document.getElementById("map"),["2006-01"]);
   
},false)

function MapExplorer(server,resolution) {
   this.server = server;
   this.layers = {};
   this.resolution = typeof resolution == "undefined" ? 60 : resolution
}

MapExplorer.prototype.init = function(mapElement,months) {
   this.map = L.map('map').setView([37, -95], 5);
   L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
       attribution: '© <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
   }).addTo(this.map);
   for (var i=0; i<months.length; i++) {
      this.fetch(months[i]);
   }
}

MapExplorer.prototype.fetch = function(month) {
   var app = this;
   try {
      
      var startTime = new Date();
      var request = new XMLHttpRequest();
      request.onreadystatechange = function() {
         if (request.readyState==4) {
            fetchTime = new Date();
            setTimeout(function() {
               app.display(month,request.responseXML, { start: startTime, fetchEnd: fetchTime })
            },1);
         }
      }
      var url = this.server+"/data/"+month+"/"+this.resolution+"/";
      request.open("GET",url,true);
      console.log("Fetching "+url);
      request.send();
   } catch(ex) {
      console.log(ex);
   }
   
}

MapExplorer.prototype.display = function(month,xhtml,properties) {
   console.log("Displaying "+month);
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
   layerGroup.addTo(this.map);
   
   var items = xhtml.data.getValues(summary.data.id,"pan:item");
   var table = xhtml.getElementsBySubject(items[0])[0];
   for (row=1; row<table.rows.length; row++) {
      
      for (col=1; col<table.rows[row].cells.length; col++) {
         var s = table.rows[row].cells[col].textContent;
         var k = s.length>0 ? parseFloat(s) : 0.0;
         if (k>0) {
            var c = k - 273.15;
            var color = HeatMap.color(-10,30,c)
            var lat = box[0] - (row-1)*scale;
            var lon = box[1] + (col-1)*scale;
            var rect = L.rectangle([[lat,lon],[lat-scale,lon+scale]], {fill: true, color: "rgb("+color[0]+","+color[1]+","+color[2]+")", weight: 0});
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
