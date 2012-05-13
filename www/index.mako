## -*- coding: utf-8 -*-
<%inherit file="index.html"/>
<%block name="leftbuttons">
    <a href="#" id="newchar_btn" class="btn btn-info btn-small hide" >+Char</a>
</%block>
<%block name="middle">
    <div id="boxarena"></div>
    <%include file="loginbox.html"/>
</%block>
<%block name="sidebar">
    <%include file="chatinbox.html"/>
    <%include file="dicebox.html"/>
</%block>
<%block name="modals">
    <%include file="modals.html"/>
</%block>
