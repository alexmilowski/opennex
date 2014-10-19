<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:data="http://milowski.com/opennex/"
   xmlns="http://www.w3.org/1999/xhtml"
   exclude-result-prefixes="xs"
   version="2.0">

<xsl:param name="row"/>
<xsl:param name="col"/>
   
<xsl:variable name="size" select="number(/data:data/@size)"/>
   
<xsl:template match="data:data">
   <div typeof="Partition">
      <xsl:apply-templates/>
   </div>
</xsl:template>
   
<xsl:template match="data:table">
   <table typeof="IndexedTable">
      <xsl:choose>
         <xsl:when test="number($row) mod 2 eq 0">
            <xsl:apply-templates select="data:tr[position() le 30]"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:apply-templates select="data:tr[position() gt 30]"/>
         </xsl:otherwise>
      </xsl:choose>
   </table>
</xsl:template>
   
<xsl:template match="data:tr">
   <tr>
      <xsl:choose>
         <xsl:when test="number($col) mod 2 eq 0">
            <xsl:apply-templates select="data:td[position() gt 30]"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:apply-templates select="data:td[position() le 30]"/>
         </xsl:otherwise>
      </xsl:choose>
   </tr>
</xsl:template>
   
<xsl:template match="data:td">
   <td>
      <xsl:apply-templates/>
   </td>
</xsl:template>
   
</xsl:stylesheet>