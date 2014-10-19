<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:xs="http://www.w3.org/2001/XMLSchema"
   xmlns:data="http://milowski.com/opennex/"
   xmlns="http://www.w3.org/1999/xhtml"
   exclude-result-prefixes="xs"
   version="2.0">

<xsl:param name="p1"/>
<xsl:param name="p2"/>
<xsl:param name="p3"/>
<xsl:param name="p4"/>
   
<xsl:template name="merge">
   <div typeof="Partition">
      <table typeof="IndexedTable">
         <xsl:for-each select="collection()/data:data[@sequence eq $p1]/data:table/data:tr">
            <xsl:variable name="row" select="position()"/>
            <tr><xsl:apply-templates/><xsl:apply-templates select="collection()/data:data[@sequence eq $p2]/data:table/data:tr[position() eq $row]/data:td"/></tr>
         </xsl:for-each>
         <xsl:for-each select="collection()/data:data[@sequence eq $p3]/data:table/data:tr">
            <xsl:variable name="row" select="position()"/>
            <tr><xsl:apply-templates/><xsl:apply-templates select="collection()/data:data[@sequence eq $p4]/data:table/data:tr[position() eq $row]/data:td"/></tr>
         </xsl:for-each>
      </table>
   </div>
</xsl:template>
   
<xsl:template match="data:td">
   <td>
      <xsl:apply-templates/>
   </td>
</xsl:template>
   
</xsl:stylesheet>