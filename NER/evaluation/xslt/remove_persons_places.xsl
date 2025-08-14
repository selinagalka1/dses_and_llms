<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
    xmlns:tei="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="xsl tei">
    
    <!-- Identity transformation: copies everything by default, including attributes and elements -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    
    <xsl:template match="tei:persName">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="tei:placeName">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="@ref"></xsl:template>
    <xsl:template match="@instant"></xsl:template>
    <xsl:template match="@full"></xsl:template>
    <xsl:template match="@part"></xsl:template>
    
    
    
  
</xsl:stylesheet>
