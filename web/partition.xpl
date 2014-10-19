<?xml version="1.0" encoding="UTF-8"?>
<p:declare-step xmlns:p="http://www.w3.org/ns/xproc"
   xmlns:c="http://www.w3.org/ns/xproc-step" version="1.0" xmlns:h="http://www.w3.org/1999/xhtml">
   <p:option name="base"/>
   <p:option name="dset"/>
   <p:option name="monthday"/>
   <p:option name="size"/>
   <p:option name="partition"/>
   <p:output port="result"/>
   <p:load href="partition.xhtml"/>
   <p:viewport match="h:content">
      <p:choose>
         <p:when test="$size = 30">
            <p:variable name="row" select="number($partition) idiv 1440"/>
            <p:variable name="col" select="number($partition) - number($row) * 1440"/>
            <p:variable name="rseq" select="(number($row) idiv 2) * 720 + ceiling(number($col) div 2)"/>
            <p:load>
               <p:with-option name="href" select="concat($base,$dset,'/',$monthday,'/60/',$rseq,'.xml')"/>
            </p:load>
            <p:xslt>
               <p:with-param name="partitionRow" select="$row"/>
               <p:with-param name="partitionCol" select="$col"/>
               <p:with-param name="requestSize" select="$size"/>
               <p:with-param name="requestSeq" select="$partition"/>
               <p:input port="stylesheet">
                  <p:document href="half-table.xsl"/>
               </p:input>
            </p:xslt>
         </p:when>
         <p:when test="$size = 60">
            <p:load>
               <p:with-option name="href" select="concat($base,$dset,'/',$monthday,'/60/',$partition,'.xml')"/>
            </p:load>
            <p:xslt>
               <p:with-param name="requestSize" select="$size"/>
               <p:with-param name="requestSeq" select="$partition"/>
               <p:input port="stylesheet">
                  <p:document href="table.xsl"/>
               </p:input>
            </p:xslt>
         </p:when>
         <p:when test="$size = 120">
            <p:variable name="row" select="number($partition) idiv 360 + 1"/>
            <p:variable name="col" select="number($partition) - number($row) * 360"/>
            <p:variable name="p1" select="(number($row)*2 - 1) * 720 + number($col)*2 - 1"/>
            <p:variable name="p2" select="(number($row)*2 - 1) * 720 + number($col)*2"/>
            <p:variable name="p3" select="number($row)*2 * 720 + number($col)*2 - 1"/>
            <p:variable name="p4" select="number($row)*2 * 720 + number($col)*2"/>
            <p:load name="p1">
               <p:with-option name="href" select="concat($base,$dset,'/',$monthday,'/60/',$p1,'.xml')"/>
            </p:load>
            <p:load name="p2">
               <p:with-option name="href" select="concat($base,$dset,'/',$monthday,'/60/',$p2,'.xml')"/>
            </p:load>
            <p:load name="p3">
               <p:with-option name="href" select="concat($base,$dset,'/',$monthday,'/60/',$p3,'.xml')"/>
            </p:load>
            <p:load name="p4">
               <p:with-option name="href" select="concat($base,$dset,'/',$monthday,'/60/',$p4,'.xml')"/>
            </p:load>
            <p:xslt template-name="merge">
               <p:with-param name="p1" select="$p1"/>
               <p:with-param name="p2" select="$p2"/>
               <p:with-param name="p3" select="$p3"/>
               <p:with-param name="p4" select="$p4"/>
               <p:with-param name="requestSize" select="$size"/>
               <p:with-param name="requestSeq" select="$partition"/>
               <p:input port="source">
                  <p:pipe port="result" step="p1"/>
                  <p:pipe port="result" step="p2"/>
                  <p:pipe port="result" step="p3"/>
                  <p:pipe port="result" step="p4"/>
               </p:input>
               <p:input port="stylesheet">
                  <p:document href="merge-table.xsl"/>
               </p:input>
            </p:xslt>
         </p:when>
      </p:choose>
   </p:viewport>
</p:declare-step>