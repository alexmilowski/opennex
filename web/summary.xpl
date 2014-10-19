<?xml version="1.0" encoding="UTF-8"?>
<p:declare-step xmlns:p="http://www.w3.org/ns/xproc"
   xmlns:c="http://www.w3.org/ns/xproc-step" version="1.0" xmlns:h="http://www.w3.org/1999/xhtml">
   <p:option name="base"/>
   <p:option name="dset"/>
   <p:option name="monthday"/>
   <p:option name="size"/>
   <p:output port="result"/>
   <p:load href="summary.xhtml"/>
   <p:viewport match="h:content">
      <p:load>
         <p:with-option name="href" select="concat($base,$dset,'/',$monthday,'/',$size,'.xml')"/>
      </p:load>
      <p:xslt>
         <p:input port="parameters">
            <p:empty/>
         </p:input>
         <p:input port="stylesheet">
            <p:document href="summary.xsl"/>
         </p:input>
      </p:xslt>
   </p:viewport>
</p:declare-step>