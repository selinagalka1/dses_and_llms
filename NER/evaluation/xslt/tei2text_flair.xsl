<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei">
    
    <xsl:output method="text" encoding="UTF-8"/>
    
    <xsl:strip-space elements="*"></xsl:strip-space>
    
    <!-- Match root and start with paragraph content -->
    <xsl:template match="/">
        <xsl:apply-templates select="//tei:p"/>
    </xsl:template>
    
    <!-- Output paragraph text -->
    <xsl:template match="tei:p">
        <xsl:text>&lt;</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>&gt;</xsl:text>
        <xsl:text>&#10;&#10;</xsl:text> <!-- two line breaks between paragraphs -->
    </xsl:template>
    
    <!-- Normalize and output all text nodes -->
    <xsl:template match="text()">
        <xsl:value-of select="."/>
    </xsl:template>
    
    <!-- Handle persName: Surround text with brackets -->
    <xsl:template match="tei:rs">
        <xsl:choose>
            <xsl:when test="contains(@type, 'per')">
                <xsl:text>[</xsl:text>
                <xsl:apply-templates/>
                <xsl:text>]</xsl:text>
            </xsl:when>
            <xsl:when test="contains(@type, 'loc')">
                <xsl:text>{</xsl:text>
                <xsl:apply-templates/>
                <xsl:text>}</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-imports/>
            </xsl:otherwise>
        </xsl:choose>

    </xsl:template>
    
    <!-- Pass-through for app -->
    <xsl:template match="tei:app">
        <xsl:apply-templates/>
    </xsl:template>
    
    <!-- Pass-through for rdg -->
    <xsl:template match="tei:rdg">
        <xsl:apply-templates/>
    </xsl:template>
</xsl:stylesheet>
