<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:data="http://milowski.com/opennex/"
   xmlns="http://www.w3.org/1999/xhtml"
   exclude-result-prefixes="xs"
   version="2.0">
   
<xsl:variable name="size" select="number(/data:data/@size)"/>
   
<xsl:template match="data:data">
   <div typeof="Partition">
      <xsl:apply-templates/>
   </div>
</xsl:template>
   
<xsl:template match="data:table">
   <table typeof="IndexedTable">
      <xsl:apply-templates/>
   </table>
</xsl:template>
   
<xsl:template match="data:tr">
   <tr>
      <xsl:apply-templates></xsl:apply-templates>
   </tr>
</xsl:template>
<xsl:template match="data:td">
   <td>
      <xsl:apply-templates/>
   </td>
</xsl:template>
   
</xsl:stylesheet>