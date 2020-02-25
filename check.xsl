<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	version="1.0">
    
  <xsl:output method="xml" indent="yes"/>

  <xsl:key name="title_key" match="DOC" use="TITLE"/>
  
  <xsl:template match="/DATA">
      <xsl:copy>
        <xsl:apply-templates select="DOC[generate-id() = generate-id(key('title_key', TITLE)[1])]"/>
      </xsl:copy>
  </xsl:template>
  
    <xsl:template match="DOC">
        <xsl:copy>
            <xsl:copy-of select="*"/>
        </xsl:copy>
  </xsl:template>
  
</xsl:stylesheet>