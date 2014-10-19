<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:data="http://milowski.com/opennex/"
   xmlns="http://www.w3.org/1999/xhtml"
   exclude-result-prefixes="xs data"
   version="2.0">
   
   
   
<xsl:variable name="size" select="number(/data:data/@size)"/>
   
<xsl:template match="data:data">
   <div typeof="PartitionSummary" resource="">
      <xsl:variable name="month" select="substring-after(@yearMonth,'-')"/>
      <xsl:variable name="year" select="substring-before(@yearMonth,'-')"/>
      <xsl:variable name="previous" select="if ($month eq '01') then concat(number($year)-1,'-','12') else concat($year,'-',format-number(number($month)-1,'00'))"/>
      <xsl:variable name="next" select="if ($month eq '12') then concat(number($year)+1,'-','01') else concat($year,'-',format-number(number($month)+1,'00'))"/>
      <h1>Summary of Temperature (<span property="count"><xsl:value-of select="count(data:table/data:tr/data:td[node()])"/></span> quadrangles) </h1>
      <h2>
         <span property="range" typeof="FacetPartition">
            <span property="facet" resource="../../../#yearMonth"/>
            <span property="start"><xsl:value-of select="@yearMonth"/></span>
            <span property="length" content="PT1M"/>
         </span>    
         in region [
         <span property="range" typeof="FacetPartition">
            <span property="facet" resource="../../../#latitude"/>
            <span property="facet" resource="../../../#longitude"/>
            <span property="shape" typeof="schema:GeoShape">
               <span property="schema:box">50 -126 24 -126 50 -66 24 -66</span>
            </span>
         </span>
         ]
         scale <span property="scale"><xsl:value-of select="$size div 120.0"/></span>
      </h2>
      <h3><a rel="previous" href="../../{$previous}/{$size}/" typeof="PartitionSummary">
            <span property="range" typeof="FacetPartition">
               <span property="facet" resource="/data/#yearMonth"/>
               <span property="start"><xsl:value-of select="$previous"/></span>
               <span property="length" content="PT1M"/>
            </span>         
         </a>
         <xsl:text> </xsl:text>
         <a rel="next" href="../../{$next}/{$size}/" typeof="PartitionSummary">
            <span property="range" typeof="FacetPartition">
               <span property="facet" resource="/data/#yearMonth"/>
               <span property="start"><xsl:value-of select="$next"/></span>
               <span property="length" content="PT1M"/>
            </span>         
         </a>
      </h3>
      <xsl:apply-templates/>
   </div>
</xsl:template>
   
<xsl:template match="data:table">
   <xsl:variable name="quadSize" select="$size div 120"/>
   <table property="item" typeof="IndexedTable">
      <caption>
         <span property="entry" typeof="Entry">
            <span property="description">Temperature</span>
            <span property="valueSpace" typeof="ValueDescription">
               <span property="datatype" resource="xsd:float"/>
               <span property="quantity" resource="quantity:ThermodynamicTemperature"/>
               <span property="unit" resource="unit:DegreeKelvin"/>
               (<span property="symbol">K</span>)
            </span>
         </span>
      </caption>
      <tr>
         <th><xsl:value-of select="$quadSize"/>° lon / <xsl:value-of select="$quadSize"/>° lat</th>
         <xsl:for-each select="(0 to (58 * 120) idiv $size - 1)">
            <th property="index" typeof="ColumnIndex"><span property="value"><xsl:value-of select="-126.0 + . * $quadSize"/></span>°</th>
         </xsl:for-each>
      </tr>
      <xsl:apply-templates/>
   </table>
</xsl:template>
   
<xsl:template match="data:tr">
   <tr>
      <th property="index" typeof="RowIndex"><span property="value"><xsl:value-of select="50 - count(preceding-sibling::data:tr) * $size div 120"/></span>°</th>
      <xsl:apply-templates></xsl:apply-templates>
   </tr>
</xsl:template>
<xsl:template match="data:td">
   <td>
      <xsl:choose>
         <xsl:when test="$size = 30">
            <a href="./{231345 + count(preceding-sibling::data:td) + 1440 * count(parent::data:tr/preceding-sibling::data:tr)}"><xsl:apply-templates/></a>
         </xsl:when>
         <xsl:when test="$size = 60">
            <a href="./{58073 + count(preceding-sibling::data:td) + 720 * count(parent::data:tr/preceding-sibling::data:tr)}"><xsl:apply-templates/></a>
         </xsl:when>
         <xsl:when test="$size = 120">
            <a href="./{14637 + count(preceding-sibling::data:td) + 360 * count(parent::data:tr/preceding-sibling::data:tr)}"><xsl:apply-templates/></a>
         </xsl:when>
         <xsl:otherwise>
            <xsl:apply-templates/>
         </xsl:otherwise>
      </xsl:choose>
   </td>
</xsl:template>
   
</xsl:stylesheet>