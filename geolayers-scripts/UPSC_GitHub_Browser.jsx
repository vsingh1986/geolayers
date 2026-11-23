/*
 * GEOlayers 3 native GitHub browser for your geographic feature catalog.
 * Run from GEOlayers 3's Scripts menu while the GEOlayers panel is open.
 *
 * Official API: https://github.com/GEOlayers/Help#geolayers3githubbrowseroptions
 */
(function () {
    if (typeof geolayers3 === "undefined" || !geolayers3.githubBrowser) {
        alert("Open the GEOlayers 3 panel and run this script from GEOlayers.");
        return;
    }

    geolayers3.githubBrowser({
        title: "UPSC Geography — GitHub Features",
        defaultUser: "vsingh1986",
        defaultRepo: "geolayers",
        fixedRepo: true,
        flatten: true,
        filterText: "",
        actionBtnText: "Import to GEOlayers"
        // Leave action and actionFilter unspecified. GEOlayers defaults
        // to accepting GeoJSON and importing it into its Feature Browser.
    });
}());
