window.addEventListener("load",function() {
   window.map = L.map('map').setView([37, -95], 5);
   L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
       attribution: '© <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
   }).addTo(map);
   
   try {
      
      var request = new XMLHttpRequest();
      request.onreadystatechange = function() {
         if (request.readyState==4) {
            setTimeout(function() {
               display(request.responseXML)
            },1);
         }
      }
      request.open("GET","/data/2006-01/60/",true);
      request.send();
   } catch(ex) {
      console.log(ex);
   }
},false)

function display(xhtml) {
   window.xhtml = xhtml
   GreenTurtle.attach(xhtml);
   
   var latFacet = window.location.protocol+"//"+window.location.host+"/data/#latitude";
   
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
   
   console.log(box+" at "+scale)
   
   L.rectangle([ [box[0],box[1]], [box[6],box[7]] ], {color: "rgb(0,0,0)", weight: 0}).addTo(map);
   
   
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
            L.rectangle([[lat,lon],[lat-scale,lon+scale]], {fill: true, color: "rgb("+color[0]+","+color[1]+","+color[2]+")", weight: 0}).addTo(map);
         }
      }
   }
}
