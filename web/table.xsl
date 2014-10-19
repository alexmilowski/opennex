<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:data="http://milowski.com/opennex/"
   xmlns="http://www.w3.org/1999/xhtml"
   exclude-result-prefixes="xs data"
   version="2.0">
   
<xsl:param name="requestSize"/>
<xsl:param name="requestSeq"/>

<xsl:variable name="requestSeqN" select="number($requestSeq)"/>
   
<xsl:variable name="size" select="number(/data:data/@size)"/>
<xsl:variable name="rowSize" select="360 * 120 div number($requestSize)"/>
<xsl:variable name="row" select="number(/data:data/@sequence) idiv 720"/>
<xsl:variable name="col" select="number(/data:data/@sequence) - number($row) * 720 - 1"/>
<xsl:variable name="requestDim" select="number($requestSize) div 120.0"/>
<xsl:variable name="dim" select="$size div 120.0"/>
<xsl:variable name="resolution" select="1 div 120.0"/>
<xsl:variable name="lat" select="90 - $row * $dim"/>
<xsl:variable name="lon" select="if ($col * $dim > 180) then $col * $dim - 360 else $col * $dim"/>
<xsl:variable name="month" select="substring-after(/data:data/@yearMonth,'-')"/>
<xsl:variable name="year" select="substring-before(/data:data/@yearMonth,'-')"/>
<xsl:variable name="previous" select="if ($month eq '01') then concat(number($year)-1,'-','12') else concat($year,'-',format-number(number($month)-1,'00'))"/>
<xsl:variable name="next" select="if ($month eq '12') then concat(number($year)+1,'-','01') else concat($year,'-',format-number(number($month)+1,'00'))"/>

<xsl:template name="partitionHeader">
   <xsl:param name="count"/>
   <h1><span property="count"><xsl:value-of select="$count"/></span> Temperature Predictions </h1>
   <h2>
      <span property="range" typeof="FacetPartition">
         <span property="facet" resource="/data/#yearMonth"/>
         <span property="start"><xsl:value-of select="@yearMonth"/></span>
         <span property="length" content="PT1M"/>
      </span>    
      in region [
      <span property="range" typeof="FacetPartition">
         <span property="facet" resource="/data/#latitude"/>
         <span property="facet" resource="/data/#longitude"/>
         <span property="shape" typeof="schema:GeoShape">
            <span property="schema:box">
               <xsl:value-of select="$lat"/>
               <xsl:text> </xsl:text>
               <xsl:value-of select="$lon"/>
               <xsl:text> </xsl:text>
               <xsl:value-of select="$lat - $requestDim"/>
               <xsl:text> </xsl:text>
               <xsl:value-of select="$lon"/>
               <xsl:text> </xsl:text>
               <xsl:value-of select="$lat"/>
               <xsl:text> </xsl:text>
               <xsl:value-of select="$lon + $requestDim"/>
               <xsl:text> </xsl:text>
               <xsl:value-of select="$lat - $requestDim"/>
               <xsl:text> </xsl:text>
               <xsl:value-of select="$lon + $requestDim"/>
            </span>
         </span>
      </span>
      ]
      scale <span property="scale"><xsl:value-of select="$resolution"/></span>
   </h2>
   <h3><a rel="previous" href="/data/{$previous}/{$requestSize}/{$requestSeq}" typeof="Partition">
      <span property="range" typeof="FacetPartition">
         <span property="facet" resource="/data/#yearMonth"/>
         <span property="start"><xsl:value-of select="$previous"/></span>
         <span property="length" content="PT1M"/>
      </span>         
   </a>
      <div>
         <table>
            <tr>
               <td><a typeof="Partition" rel="nearby" href="./{$requestSeqN - $rowSize - 1}"><xsl:value-of select="$requestSeqN - $rowSize - 1"/></a></td>
               <td><a typeof="Partition" rel="nearby" href="./{$requestSeqN - $rowSize}"><xsl:value-of select="$requestSeqN - $rowSize"/></a></td>
               <td><a typeof="Partition" rel="nearby" href="./{$requestSeqN - $rowSize + 1}"><xsl:value-of select="$requestSeqN - $rowSize + 1"/></a></td>
            </tr>
            <tr>
               <td><a typeof="Partition" rel="nearby" href="./{$requestSeqN - 1}"><xsl:value-of select="$requestSeqN - 1"/></a></td>
               <td property="sequence"><xsl:value-of select="$requestSeq"/></td>
               <td><a typeof="Partition" rel="nearby" href="./{$requestSeqN + 1}"><xsl:value-of select="$requestSeqN + 1"/></a></td>
            </tr>
            <tr>
               <td><a typeof="Partition" rel="nearby" href="./{$requestSeqN + $rowSize - 1}"><xsl:value-of select="$requestSeqN + $rowSize - 1"/></a></td>
               <td><a typeof="Partition" rel="nearby" href="./{$requestSeqN + $rowSize}"><xsl:value-of select="$requestSeqN + $rowSize"/></a></td>
               <td><a typeof="Partition" rel="nearby" href="./{$requestSeqN + $rowSize + 1}"><xsl:value-of select="$requestSeqN + $rowSize + 1"/></a></td>
            </tr>
         </table>
      </div>
      <a rel="next" href="/data/{$next}/{$requestSize}/{$requestSeq}" typeof="Partition">
         <span property="range" typeof="FacetPartition">
            <span property="facet" resource="/data/#yearMonth"/>
            <span property="start"><xsl:value-of select="$next"/></span>
            <span property="length" content="PT1M"/>
         </span>         
      </a>
   </h3>
</xsl:template>
   
<xsl:template match="data:data">
   <div typeof="Partition" resource="/data/{@yearMonth}/{$requestSize}/{$requestSeq}">
      <xsl:call-template name="partitionHeader">
         <xsl:with-param name="count" select="count(data:table/data:tr/data:td[node()])"/>
      </xsl:call-template>
      <xsl:apply-templates/>
   </div>
</xsl:template>

<xsl:template name="columnHeaders">
   <tr>
      <th><xsl:value-of select="format-number($resolution,'0.00000')"/>° lon / <xsl:value-of select="format-number($resolution,'0.00000')"/>° lat</th>
      <xsl:for-each select="(0 to number($requestSize) idiv 1 - 1)">
         <th property="index" typeof="ColumnIndex"><span property="value"><xsl:value-of select="format-number($lon + . * $resolution,'0.000')"/></span>°</th>
      </xsl:for-each>
   </tr>
</xsl:template>
   
<xsl:template match="data:table">
   <table property="item" typeof="IndexedTable">
      <xsl:call-template name="columnHeaders"/>
      <xsl:apply-templates/>
   </table>
</xsl:template>

<xsl:template name="rowIndex">
   <xsl:param name="position"/>
   <th property="index" typeof="RowIndex"><span property="value"><xsl:value-of select="format-number($lat - $position * $resolution,'0.000')"/></span>°</th>
</xsl:template>
<xsl:template match="data:tr">
   <tr>
      <xsl:call-template name="rowIndex">
         <xsl:with-param name="position" select="count(preceding-sibling::data:tr)"/>
      </xsl:call-template>
      <xsl:apply-templates/>
   </tr>
</xsl:template>
<xsl:template match="data:td">
   <td>
      <xsl:apply-templates/>
   </td>
</xsl:template>
   
</xsl:stylesheet>