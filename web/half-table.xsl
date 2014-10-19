<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:data="http://milowski.com/opennex/"
   xmlns="http://www.w3.org/1999/xhtml"
   exclude-result-prefixes="xs"
   version="2.0">
   
<xsl:import href="table.xsl"/>
   
<xsl:param name="partitionRow"/>
<xsl:param name="partitionCol"/>

<xsl:template match="data:table">
   <table typeof="IndexedTable">
      <xsl:call-template name="columnHeaders"/>
      <xsl:choose>
         <xsl:when test="number($partitionRow) mod 2 eq 0">
            <xsl:for-each select="data:tr[position() le 30]">
               <xsl:apply-templates select=".">
                  <xsl:with-param name="position" select="position()"/>
               </xsl:apply-templates>
            </xsl:for-each>
         </xsl:when>
         <xsl:otherwise>
            <xsl:for-each select="data:tr[position() gt 30]">
               <xsl:apply-templates select=".">
                  <xsl:with-param name="position" select="position()"/>
               </xsl:apply-templates>
            </xsl:for-each>
         </xsl:otherwise>
      </xsl:choose>
   </table>
</xsl:template>

<xsl:template match="data:tr">
   <xsl:param name="position"/>
   <tr>
      <xsl:call-template name="rowIndex">
         <xsl:with-param name="position" select="$position - 1"/>
      </xsl:call-template>
      <xsl:choose>
         <xsl:when test="number($partitionCol) mod 2 eq 0">
            <xsl:apply-templates select="data:td[position() gt 30]"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:apply-templates select="data:td[position() le 30]"/>
         </xsl:otherwise>
      </xsl:choose>
   </tr>
</xsl:template>
   
</xsl:stylesheet>