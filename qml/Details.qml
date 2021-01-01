import io.thp.pyotherside 1.5
import Ubuntu.Components 1.3
import QtLocation 5.9
import QtPositioning 5.9
import QtQuick 2.6
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.1
import QtQuick.Window 2.2
import QtWebEngine 1.5
import Ubuntu.Connectivity 1.0

Page {
    id: detailsPage
    
    width: parent.width
    height: parent.height

    header: PageHeader
    {
        id: pageHeader
        title: "weeWX Weather App"

        trailingActionBar
        {
            actions: [
                Action
                {
                    iconName: "info"
                    text: "About App"

                    onTriggered: aboutPopup1.open()
                },
                Action
                {
                    iconName: "settings"
                    text: "Settings"

                    onTriggered: showSettings()
                },
                Action
                {
                    iconSource: "../assets/refresh.png"
                    text: "Refresh"

                    onTriggered: displayall(true)
                }
            ]
        }
    }

    TabBar
    {
        id: tabBar
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: units.gu(5)
        currentIndex: swipeView.currentIndex

        TabButton
        {
            id: weatherTab
            font.pointSize: units.gu(2)
            height: units.gu(5)
            width: units.gu(12)

            contentItem: Text
            {
                color: tabBar.currentIndex == 0 ? "#ffffff" : "#000000"
                text: "Weather"
                font: weatherTab.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle
            {
                color: tabBar.currentIndex == 0 ? "#000000" : "#ffffff"
            }
        }

        TabButton
        {
            font.pointSize: units.gu(2)
            height: units.gu(5)
            width: units.gu(12)

            contentItem: Text
            {
                color: tabBar.currentIndex == 1 ? "#ffffff" : "#000000"
                text: "Statistics"
                font: weatherTab.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle
            {
                color: tabBar.currentIndex == 1 ? "#000000" : "#ffffff"
            }
        }

        TabButton
        {
            id: rftab
            text: "Forecast"
            font.pointSize: units.gu(2)
            height: units.gu(5)
            width: units.gu(12)

            contentItem: Text
            {
                color: tabBar.currentIndex == 2 ? "#ffffff" : "#000000"
                text: rftab.text
                font: weatherTab.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle
            {
                color: tabBar.currentIndex == 2 ? "#000000" : "#ffffff"
            }
        }

        TabButton
        {
            height: units.gu(5)
            width: units.gu(12)

            contentItem: Text
            {
                color: tabBar.currentIndex == 3 ? "#ffffff" : "#000000"
                text: "Webcam"
                font: weatherTab.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle
            {
                color: tabBar.currentIndex == 3 ? "#000000" : "#ffffff"
            }
        }

        TabButton
        {
            height: units.gu(5)
            width: units.gu(12)

            contentItem: Text
            {
                color: tabBar.currentIndex == 4 ? "#ffffff" : "#000000"
                text: "Custom"
                font: weatherTab.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            background: Rectangle
            {
                color: tabBar.currentIndex == 4 ? "#000000" : "#ffffff"
            }
        }
    }

    function showSettings()
    {
        root.loadSettings()
    }

    Popup
    {
        id: aboutPopup1
        padding: 10
        width: units.gu(37)
        height: about1a.height + about1b.height + about1Button.height + units.gu(1)
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
        z: detailsPage.z + 6
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        Text
        {
            id: about1a
            anchors.top: parent.top
            anchors.left: parent.left
            font.bold: true
            font.pixelSize: units.gu(4.5)
            text: "About this app"
        }

        Text
        {
            id: about1b
            padding: units.gu(1)
            anchors.top: about1a.bottom
            width: parent.width
            wrapMode: Text.Wrap
            onLinkActivated: Qt.openUrlExternally(link)
            text: "<html><body>Big thanks to the <a href='http://weewx.com'>weeWX project</a>, as this app " +
			    "wouldn't be possible otherwise.<br><br>" +
			    "Weather Icons from <a href='https://www.flaticon.com/'>FlatIcon</a> and " +
			    "is licensed under <a href='http://creativecommons.org/licenses/by/3.0/'>CC 3.0 BY</a> and " +
			    "<a href='https://github.com/erikflowers/weather-icons'>Weather Font</a> by Erik Flowers" +
			    "<br><br>" +
			    "Forecasts by" +
			    "<a href='https://www.yahoo.com/?ilc=401'>Yahoo!</a>, " +
			    "<a href='https://weatherzone.com.au'>weatherzone</a>, " +
			    "<a href='https://hjelp.yr.no/hc/en-us/articles/360001940793-Free-weather-data-service-from-Yr'>yr.no</a>, " +
			    "<a href='https://bom.gov.au'>Bureau of Meteorology</a>, " +
			    "<a href='https://www.weather.gov'>Weather.gov</a>, " +
			    "<a href='https://worldweather.wmo.int/en/home.html'>World Meteorology Organisation</a>, " +
			    "<a href='https://weather.gc.ca'>Environment Canada</a>, " +
			    "<a href='https://www.metoffice.gov.uk'>UK Met Office</a>, " +
			    "<a href='https://www.aemet.es'>La Agencia Estatal de Meteorología</a>, " +
			    "<a href='https://www.dwd.de'>Deutscher Wetterdienst</a>, " +
			    "<a href='https://metservice.com'>MetService.com</a>, " +
			    "<a href='https://meteofrance.com'>MeteoFrance.com</a>, " +
			    "<a href='https://darksky.net'>DarkSky.net</a>" +
			    "<br><br>" +
                "weeWX Weather App is by <a href='https://odiousapps.com'>OdiousApps</a>.</body</html>"
        }

        Button
        {
            id: about1Button
            anchors.top: about1b.bottom
            width: parent.width
            text: "Okay"
            // color: Ubuntu.green
            onClicked: aboutPopup1.close()
        }
    }

    SwipeView
    {
        id: swipeView
        anchors.top: tabBar.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        currentIndex: tabBar.currentIndex

        Item
        {
            id: weatherPage
            width: swipeView.width
            height: swipeView.height

            WebEngineView
            {
                id: currentConditions
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                height: parent.height / 2 - units.gu(1)
            }

            WebEngineView
            {
                id: radarForecast
                anchors.top: currentConditions.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                height: parent.height / 2 + units.gu(1)
            }
        }

        Item
        {
            id: statsPage
            width: swipeView.width
            height: swipeView.height

            WebEngineView
            {
                id: statsData
                anchors.fill: parent
            }
        }

        Item
        {
            id: forecastRadarPage
            width: swipeView.width
            height: swipeView.height

            WebEngineView
            {
                id: forecastRadar
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
            }
        }

        Item
        {
            id: webcamPage
            width: swipeView.width
            height: swipeView.height

            WebEngineView
            {
                id: webcam
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
            }
        }

        Item
        {
            id: customPage
            width: swipeView.width
            height: swipeView.height

            WebEngineView
            {
                id: custom
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
            }
        }
    }

    Timer
    {
        id: updateTimer
        interval: 300000
        repeat: true
        running: false
        onTriggered:
        {
            displayall(false)
        }
    }

    Component.onCompleted:
    {
        busyIndicator.running = true
        updateTimer.running = false
        switch(root.update_freq)
        {
            case "0":
                break
            case "2":
                updateTimer.interval = 600000
                updateTimer.running = true
                break
            case "3":
                updateTimer.interval = 900000
                updateTimer.running = true
                break
            case "4":
                updateTimer.interval = 1800000
                updateTimer.running = true
                break
            case "5":
                updateTimer.interval = 3600000
                updateTimer.running = true
                break
            default:
                updateTimer.interval = 300000
                updateTimer.running = true
                break
        }
        
        downloadall(false)
    }

    function downloadall(force_download)
    {
        if(Connectivity.online)
        {
            pytest.call("main.download_data", ["", force_download], function(results)
            {
                updateDisplay(results)
            })

            refreshData(force_download)
            loadWebcam(force_download)
            loadCustom()
        } else {
            toast.show("Failed to update, not connected to the internet.", 5000)
        }
    }

    function displayall(force_download)
    {
        if(force_download || root.wifidownload == false)
        {
            downloadall(force_download)
            return
        }
        
        if(Connectivity.wifiEnabled)
            downloadall(false)
        else
            toast.show("Wifi is disabled, and only wifi downloads was selected. Skipping update.", 5000)
    }

    function loadCustom()
    {
        custom.zoomFactor = 2.8
        var html = htmlheader + "<div style='text-align:center;vertical-align:middle;font-size:" + units.dp(12) + "pt;'>" 
        html += "This screen is still loading.</div>" + htmlfooter
        webcam.loadHtml(html, "file:///")

        pytest.call("main.get_custom", [], function(results)
        {
            custom.url = results[1]
        })
    }

    function loadWebcam(force_download)
    {
        var html = htmlheader + "<div style='text-align:center;vertical-align:middle;font-size:" + units.dp(12) + "pt;'>" 
        html += "Webcam is still loading.</div>" + htmlfooter
        webcam.loadHtml(html, "file:///")

        pytest.call("main.get_webcam", ["", force_download], function(results)
        {
            var html = htmlheader + "<img style='height:99vh;width:99vw;' src='file://" + root.cachebase + "/webcam.jpg'>"
            html += htmlfooter

            webcam.loadHtml(html, "file:///")
            busyIndicator.running = false
        })
    }

    function refreshData(force_download)
    {
        if(root.show_radar == "1")
        {
            var html = htmlheader + "<div style='text-align:center;vertical-align:middle;font-size:" + units.dp(12) + "pt;'>"
            html += "Radar URL is still loading.</div>" + htmlfooter
            radarForecast.loadHtml(html, "file:///")

            html = htmlheader + "<div style='text-align:center;vertical-align:middle;font-size:" + units.dp(12) + "pt;'>"
            html += "Forecast Data is still downloading.</div>" + htmlfooter
            forecastRadar.loadHtml(html, "file:///")

            if(root.radar_url != "")
            {
                if(root.rad_type == "image")
                {
                    pytest.call("main.get_radar", ["", "", force_download], function(results)
                    {
                        var html = htmlheader + "<div style='position:absolute;top:0px;left:0px;width:100%'>" 
                        html += "<img style='max-width:100%;width:1300px;' src='file://" + root.cachebase + "/radar.gif'>"
                        html += "</div>" + htmlfooter
                        radarForecast.loadHtml(html, "file:///")
                        busyIndicator.running = false
                    })
                } else {
                    radarForecast.url = root.radar_url
                    busyIndicator.running = false
                }
            } else {
                var html = htmlheader + "<div style='text-align:center;vertical-align:middle;font-size:" + units.dp(12) + "pt;'>"
                html += "Radar URL not set. Go to settings to change.</div>" + htmlfooter
                radarForecast.loadHtml(html, "file:///")
            }

            pytest.call("main.process_forecast", [force_download], function(results)
            {
                updateForecastRadar(results)
                busyIndicator.running = false
            })
        } else {
            var html = htmlheader + "<div style='text-align:center;vertical-align:middle;font-size:" + units.dp(12) + "pt;'>"
            html += "Radar URL is still loading.</div>" + htmlfooter
            forecastRadar.loadHtml(html, "file:///")

            html = htmlheader + "<div style='text-align:center;vertical-align:middle;font-size:" + units.dp(12) + "pt;'>"
            html += "Forecast data is still downloading.</div>" + htmlfooter
            radarForecast.loadHtml(html, "file:///")

            if(root.rad_type == "image")
            {
                pytest.call("main.get_radar", ["", "", force_download], function(results)
                {
                    var html = htmlheader + "<div style='position:absolute;top:300px;left:-100px;width:100%'>" 
                    html += "<img style='transform:rotate(90deg);width:1300px;'"
                    html += " src='file://" + root.cachebase + "/radar.gif'>"
                    html += "</div>" + htmlfooter

                    forecastRadar.loadHtml(html, "file:///")
                    busyIndicator.running = false
                })
            } else {
                forecastRadar.url = root.radar_url
                busyIndicator.running = false
            }

            rftab.text = "Radar"
            pytest.call("main.process_forecast", [force_download], function(results)
            {
                updateRadarForecast(results)
                busyIndicator.running = false
            })
        }
    }

    function doForecastBanner(fctype, ftime, desc, showHeader)
    {
        var html = ""

        if(fctype == "yahoo")
        {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/purple.png'/></div></br>"
        } else if(fctype == "weatherzone") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/wz.png'/></div></br>"
        } else if(fctype == "yr.no") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/yrno.png'/></div></br>"
        } else if(fctype == "bom.gov.au") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/bom.png'/></div></br>"
        } else if(fctype == "wmo.int") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/wmo.png'/></div></br>"
        } else if(fctype == "weather.gov") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/wgov.png'/></div></br>"
        } else if(fctype == "weather.gc.ca") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/wca.png'/></div></br>"
        } else if(fctype == "weather.gc.ca-fr") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/wca.png'/></div></br>"
        } else if(fctype == "metoffice.gov.uk") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/met.png'/></div></br>"
        } else if(fctype == "bom2") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/bom.png'/></div></br>"
        } else if(fctype == "aemet.es") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/aemet.jpg'/></div></br>"
        } else if(fctype == "dwd.de") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/dwd.jpg'/></div></br>"
        } else if(fctype == "metservice.com") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/metservice.png'/></div></br>"
        } else if(fctype == "meteofrance.com") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/mf.png'/></div></br>"
        } else if(fctype == "darksky.net") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/darksky.png'/></div></br>"
        } else if(fctype == "openweathermap.org") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/owm.png'/></div></br>"
        } else if(fctype == "apixu.com") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/apixu.png'/></div></br>"
        } else if(fctype == "weather.com") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/weather_com.png'/></div></br>"
        } else if(fctype == "met.ie") {
            html = "<div style='text-align:center;'><img style='display:block;margin:0 auto;' height='" + units.dp(29) +
                    "px' src='file://" + root.app_dir + "/assets/met_ie.png'/></div></br>"
        } else {
            html = "<div style='text-align:center;font-size:" + units.dp(16) + "pt;'>Error occured...</div><br>"
        }

        if(showHeader)
            html += "<div style='text-align:center;font-size:" + units.dp(18) + "pt;'>" + desc + "</div><br>"

        html += "<div style='text-align:center;font-size:" + units.dp(12) + "pt;'>" + ftime + "</div><br>"

        return html
    }

    function doForecastRow(JsonObject)
    {
        var html = ""

        if(root.use_icons == "1" && root.fctype != "wmo.int" && root.fctype != "darksky.net" && root.fctype != "openweathermap.org")
            if(JsonObject['icon'] == null)
                html = "<tr><td style='width:10%;vertical-align:top;' rowspan='2'><i style='font-size:" + units.dp(20) + "pt;'>N/A</i></td>"
            else if(!JsonObject['icon'].startsWith("data:image") && !JsonObject['icon'].startsWith("http"))
                html = "<tr><td style='width:10%;vertical-align:top;' rowspan='2'><img width='" + units.dp(40) + "pt' src='file://" + root.cachebase + "/" + JsonObject['icon'] + "'></td>"
            else
                html = "<tr><td style='width:10%;vertical-align:top;' rowspan='2'><img width='" + units.dp(40) + "pt' src='" + JsonObject['icon'] + "'></td>"
        else
            html = "<tr><td style='width:10%;vertical-align:top;' rowspan='2'><i style='font-size:" + units.dp(30) + "pt;' class='" + JsonObject['icon'] + "'></i></td>"

        html += "<td style='width:80%;'><b>" + JsonObject['day'] + "</b></td>"

        if(JsonObject['max'] != "&deg;C" && JsonObject['max'] != "&deg;F")
            html += "<td style='width:10%;text-align:right;vertical-align:top;'><b>" + JsonObject['max'] + "</b></td></tr>"
        else
            html += "<td style='width:10%;'><b>&nbsp;</b></td></tr>"

        if(JsonObject['min'] != "&deg;C" && JsonObject['min'] != "&deg;F")
            html += "<tr><td>" + JsonObject['text'] + "</td>" + "<td style='width:10%;text-align:right;vertical-align:top;'>" + JsonObject['min'] + "</td></tr>"
        else
            html += "<tr><td colspan='2'>" + JsonObject['text'] + "</td></tr>"

        html += "<tr><td colspan='2'>&nbsp;</td></tr>"

        return html
    }

    function updateForecastRadar(results)
    {
        if(results[0] == false)
        {
            busyIndicator.running = false
            toast.show(results[1], 5000)
            return
        }

        var fctype = results[2]
        var ftime = results[3]
        var desc = results[4]
        var html = htmlheader

        html += doForecastBanner(fctype, ftime, desc, true)

        var JsonArray = JSON.parse(results[1])        

        for(var i in JsonArray)
        {
            var JsonObject = JsonArray[i]

            if(i != 0)
            {
                html += doForecastRow(JsonObject)
            } else {
                html += "<table style='width:100%;border:0px;'>"

                if(JsonObject['max'] == "&deg;C" || JsonObject['max'] == "&deg;F")
                    html += "<tr><td style='width:50%;font-size:" + units.dp(48) + "pt;'>&nbsp;</td>"
			    else
				    html += "<tr><td style='width:50%;font-size:" + units.dp(48) + "pt;'>" + JsonObject['max'] + "</td>"

                if(root.use_icons == "1" && root.fctype != "wmo.int")
                    if(!JsonObject['icon'].startsWith("data:image") && !JsonObject['icon'].startsWith("http"))
                        html += "<td style='width:50%;text-align:right;'><img width='" + units.dp(80) + "pt' src='file://" + root.cachebase + "/" + JsonObject['icon'] + "'></td></tr>"
                    else
                        html += "<td style='width:50%;text-align:right;'><img width='" + units.dp(80) + "pt' src='" + JsonObject['icon'] + "'></td></tr>";
                else
				    html += "<td style='width:50%;text-align:right;'><i style='font-size:" + units.dp(80) + "pt;' class='" + JsonObject['icon'] + "'></i></td></tr>"

                if(JsonObject['min'] == "&deg;C" || JsonObject['min'] == "&deg;F")
    			{
	    			html += "<tr><td style='text-align:right;" + units.dp(16) + "pt;' colspan='2'>" + JsonObject['text'] + "</td></tr></table><br />"
	    		} else {
		    		html += "<tr><td style='font-size:" + units.dp(16) + "pt;'>" + JsonObject['min'] + "</td>";
    				html += "<td style='text-align:right;font-size:" + units.dp(16) + "pt;'>" + JsonObject['text'] + "</td></tr></table><br />"
                }

                html += "<table style='width:100%;border:0px;'>"
            }
        }

        html += "</table>"

        html += htmlfooter

        forecastRadar.loadHtml(html, "file:///")
    }

    function updateRadarForecast(results)
    {
        if(results[0] == false)
        {
            busyIndicator.running = false
            toast.show(results[1], 5000)
            return
        }

        var fctype = results[2]
        var ftime = results[3]
        var desc = results[4]
        var html = htmlheader

        html += doForecastBanner(fctype, ftime, desc)

        var JsonArray = JSON.parse(results[1])

        html += "<table style='width:100%;'>\n"

        for(var i in JsonArray)
        {
            var JsonObject = JsonArray[i]
            html += doForecastRow(JsonObject)
        }

        html += "</table>"

        html += htmlfooter

        radarForecast.loadHtml(html, "file:///")
    }

    function updateDisplay(results)
    {
        if(results[0] == false)
        {
            toast.show(results[1], 5000)
            return
        }

        var html = ""
        var bits = results[1].split('|')
        // bits[60] = bits[60].replace('Â', '')
        var iw = units.dp(16)

        html = htmlheader +
            "<div style='text-align:center;font-size:" + units.dp(20) + "pt'>" + bits[56] + "</div><br/>" + 
            "<div style='text-align:center;font-size:" + units.dp(12) + "pt''>" + bits[54] + " " + bits[55] + "</div>" + 
            "<table style='width:100%;border:0px;'>" + 
            "<tr><td style='font-size:" + units.dp(36) + "pt;text-align:right;'>" + bits[0] + bits[60] + "</td>"

        if(bits.length > 204)
        {
            html += "<td style='font-size:" + units.dp(18) + "pt;text-align:right;vertical-align:bottom;'>AT: "
            html += bits[203] + bits[60] +"</td></tr></table>"
        } else {
            html += "<td>&nbsp</td></tr></table>"
        }

        html += "<table style='width:100%;border:0px;'>"
        html += "<tr><td><i style='font-size:" + iw + "pt;' class='flaticon-windy'></i></td><td>" + bits[25] + bits[61] + "</td>" +
            "<td style='text-align:right;'>" + bits[37] + bits[63] + "</td><td style='text-align:right;'><i style='font-size:" + iw + "pt;' class='wi wi-barometer'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "pt;' class='wi wi-wind wi-towards-" + bits[30].toLowerCase() + "'></i></td><td>" + bits[30] + "</td>"
        html += "<td style='text-align:right;'>" + bits[6] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='wi wi-humidity'></i></td></tr>"

        var rain = bits[20] + bits[62] + " since mn";
        if(bits.length > 160 && bits[160] != "")
            rain = bits[158] + bits[62] + " since " + bits[160]

        html += "<tr><td><i style='font-size:" + iw + "pt;' class='wi wi-umbrella'></i></td><td>" + rain + "</td>"
        html += "<td style='text-align:right;'>" + bits[12] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + (iw * 1.4) + "pt;' class='wi wi-raindrop'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "pt;' class='flaticon-women-sunglasses'></i></td><td>" + bits[45] + "UVI</td>"
        html += "<td style='text-align:right;'>" + bits[43] + "W/m\u00B2</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='flaticon-women-sunglasses'></i></td></tr>"

        if(bits.length > 202 && root.indoor_readings == "1")
        {
            html += "<tr><td><i style='font-size:" + iw + "pt;' class='flaticon-home-page'></i></td><td>" + bits[161] + bits[60] + "</td>"
            html += "<td style='text-align:right;'>" + bits[166] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='flaticon-home-page'></i></td></tr>"
        }

        html += "</table>"

        html += "<table style='width:100%;border:0px;'>"

        html += "<tr><td><i style='font-size:" + iw + "pt;' class='wi wi-sunrise'></i></td><td style='font-size:" + units.dp(10) + "pt'>" + bits[57] + "</td>"
        html += "<td><i style='font-size:" + iw + "pt;' class='wi wi-sunset'></i></td><td style='font-size:" + units.dp(10) + "pt'>" + bits[58] + "</td>"
        html += "<td><i style='font-size:" + iw + "pt;' class='wi wi-moonrise'></i></td><td style='font-size:" + units.dp(10) + "pt'>" + bits[47] + "</td>"
        html += "<td><i style='font-size:" + iw + "pt;' class='wi wi-moonset'></i></td><td style='font-size:" + units.dp(10) + "pt'>" + bits[48] + "</td></tr>"
        
        html += "</table>"

        html += htmlfooter

        currentConditions.loadHtml(html, "file:///")

        html = htmlheader + "<body>"

//      Today's stats

        html += "<div style='text-align:center;font-size:" + units.dp(20) + "pt'>" + bits[56] + "</div><br/>"
        html += "<div style='text-align:center;font-size:" + units.dp(12) + "pt'>" + bits[54] + " " + bits[55] + "</div>"

        html += "<div style='text-align:center;font-size:" + units.dp(18) + "pt;font-weight:bold;'>Today's Statistics</div>"
        html += "<table style='width:100%;border:0px;'>"

        html += "<tr><td><i style='font-size:" + iw + "pt;' class='flaticon-temperature'></i></td><td>" + bits[3] + bits[60] + "</td><td>" + convert(bits[4])
        html += "</td><td style='text-align:right;'>" + convert(bits[2]) + "</td><td style='text-align:right;'>" + bits[1] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='flaticon-temperature'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + (iw * 1.4) + "px;' class='wi wi-raindrop'></i></td><td>" + bits[15] + bits[60] + "</td><td>" + convert(bits[16])
        html += "</td><td style='text-align:right;'>" + convert(bits[14]) + "</td><td style='text-align:right;'>" + bits[13] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + (iw * 1.4) + "pt;' class='wi wi-raindrop'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "pt;' class='wi wi-humidity'></i></td><td>" + bits[9] + bits[64] + "</td><td>" + convert(bits[10])
        html += "</td><td style='text-align:right;'>" + convert(bits[8]) + "</td><td style='text-align:right;'>" + bits[6] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='wi wi-humidity'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "pt;' class='wi wi-barometer'></i></td><td>" + bits[39] + bits[63] + "</td><td>" + convert(bits[40])
        html += "</td><td style='text-align:right;'>" + convert(bits[42]) + "</td><td style='text-align:right;'>" + bits[41] + bits[63] + "</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='wi wi-barometer'></i></td></tr>"

        if(root.indoor_readings == "1")
        {
            html += "<tr><td><i style='font-size:" + iw + "pt;' class='flaticon-home-page'></i></td><td>" + bits[164] + bits[60] + "</td><td>" + convert(bits[165])
            html += "</td><td style='text-align:right;'>" + convert(bits[163]) + "</td><td style='text-align:right;'>" + bits[162] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='flaticon-home-page'></i></td></tr>"

            html += "<tr><td><i style='font-size:" + iw + "pt;' class='flaticon-home-page'></i></td><td>" + bits[169] + bits[64] + "</td><td>" + convert(bits[170])
            html += "</td><td style='text-align:right;'>" + convert(bits[168]) + "</td><td style='text-align:right;'>" + bits[167] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='flaticon-home-page'></i></td></tr>"
        }

        if(bits.length > 205 && bits[205] != "")
        {
            html += "<tr><td><i style='font-size:" + iw + "pt;' class='flaticon-women-sunglasses'></i></td><td>" + bits[205] + "UVI</td><td>" + convert(bits[206])
            html += "</td><td style='text-align:right;'>" + convert(bits[208]) + "</td><td style='text-align:right;'>" + bits[207] + "W/m\u00B2</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='flaticon-women-sunglasses'></i></td></tr>"
        }

        var rain = bits[20]
        var since = "since mn"

        if(bits.length > 160 && bits[160] != "")
            rain = bits[158]

        if(bits.length > 160 && bits[158] != "" && bits[160] != "")
            since = "since " + bits[160]

        html += "<tr><td><i style='font-size:" + iw + "pt;' class='flaticon-windy'></i></td><td colspan='3'>" + bits[19] + bits[61] + " " + bits[32] + " " + convert(bits[33])
        html += "</td><td style='text-align:right;'>" + rain + bits[62] + "</td><td style='text-align:right'><i style='font-size:" + iw + "pt;' class='wi wi-umbrella'></i></td></tr>"
        html += "<tr><td colspan='4'>&nbsp;</td><td style='text-align:right;' colspan='2'>" + since + "</td></tr>"

        html += "</table><br>"

//      Yesterday's stats

        html += "<div style='text-align:center;font-size:" + units.dp(18) + "pt;font-weight:bold;'>Yesterday's Statistics</div>"
        html += "<table style='width:100%;border:0px;'>"
        
        html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-temperature'></i></td><td>" + bits[67] + bits[60] + "</td><td>" + convert(bits[68])
        html += "</td><td style='text-align:right;'>" + convert(bits[66]) + "</td><td style='text-align:right;'>" + bits[65] + bits[60] + "</td><td><i style='text-align:right;font-size:" + iw + "px;' class='flaticon-temperature'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + (iw * 1.4) + "pt;' class='wi wi-raindrop'></td><td>" + bits[78] + bits[60] + "</td><td>" + convert(bits[79])
        html += "</td><td style='text-align:right;'>" + convert(bits[77]) + "</td><td style='text-align:right;'>" + bits[76] + bits[60] + "</td><td style='text-align:right;'><i style='font-size:" + (iw * 1.4) + "pt;' class='wi wi-raindrop'></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='wi wi-humidity'></i></td><td>" + bits[82] + bits[64] + "</td><td>" + convert(bits[83])
        html += "</td><td style='text-align:right;'>" + convert(bits[81]) + "</td><td style='text-align:right;'>" + bits[80] + bits[64] + "</td><td style='text-align:right;'><i style='font-size:" + iw + "px;' class='wi wi-humidity'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='wi wi-barometer'></i></td><td>" + bits[84] + bits[63] + "</td><td>" + convert(bits[85])
        html += "</td><td style='text-align:right;'>" + convert(bits[87]) + "</td><td style='text-align:right;'>" + bits[86] + bits[63] + "</td><td style='text-align:right;'><i style='font-size:" + iw + "px;' class='wi wi-barometer'></i></td></tr>"

        if(bits.length > 202 && root.indoor_readings == "1")
        {
            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td><td>" + bits[173] + bits[60] + "</td><td>" + convert(bits[174])
            html += "</td><td style='text-align:right;'>" + convert(bits[172]) + "</td><td style='text-align:right;'>" + bits[171] + bits[60] + "</td><td style='text-align:right;'><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td></tr>";

            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td><td>" + bits[177] + bits[64] + "</td><td>" + convert(bits[178])
            html += "</td><td style='text-align:right'>" + convert(bits[176]) + "</td><td style='text-align:right;'>" + bits[175] + bits[64] + "</td><td style='text-align:right;'><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td></tr>";
        }

        if(bits.length > 209 && bits[209] != "")
        {
            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-women-sunglasses'></i></td><td>" + bits[209] + "UVI</td><td>" + convert(bits[210])
            html += "</td><td style='text-align:right'>" + convert(bits[212]) + "</td><td style='text-align:right;'>" + bits[211] + "W/m\u00B2</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-women-sunglasses'></i></td></tr>"
        }

        rain = bits[21];
        since = "before mn"

        if(bits.length > 160 && bits[159] !="")
            rain = bits[159]

        html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-windy'></i></td><td colspan='3'>" + bits[69] + bits[61] + " " + bits[70] + " " + convert(bits[71])
        html += "</td><td style='text-align:right'>" + rain + bits[62] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-umbrella'></i></td></tr>"

        if(bits.length > 160 && bits[159] != "" && bits[160] != "")
            since = "before " + bits[160]

        html += "<tr><td colspan='4'>&nbsp;</td><td style='text-align:right' colspan='2'>" + since + "</td></tr>";
        html += "</table><br>";

//      This month's stats

        html += "<div style='text-align:center;font-size:" + units.dp(18) + "pt;font-weight:bold;'>This Month's Statistics</div>";
        html += "<table style='width:100%;border:0px;'>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-temperature'></i></td><td>" + bits[90] + bits[60] + "</td><td>" + getTime(bits[91])
        html += "</td><td style='text-align:right'>" + getTime(bits[89]) + "</td><td style='text-align:right'>" + bits[88] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-temperature'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + (iw * 1.4) + "pt;' class='wi wi-raindrop'></td><td>" + bits[101] + bits[60] + "</td><td>" + getTime(bits[102])
        html += "</td><td style='text-align:right'>" + getTime(bits[100]) + "</td><td style='text-align:right'>" + bits[99] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + (iw * 1.4) + "pt;' class='wi wi-raindrop'></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='wi wi-humidity'></i></td><td>" + bits[105] + bits[64] + "</td><td>" + getTime(bits[106])
        html += "</td><td style='text-align:right'>" + getTime(bits[104]) + "</td><td style='text-align:right'>" + bits[103] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-humidity'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='wi wi-barometer'></i></td><td>" + bits[107] + bits[63] + "</td><td>" + getTime(bits[108])
        html += "</td><td style='text-align:right'>" + getTime(bits[110]) + "</td><td style='text-align:right'>" + bits[109] + bits[63] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-barometer'></i></td></tr>"

        if(bits.length > 202 && root.indoor_readings == "1")
        {
            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td><td>" + bits[181] + bits[60] + "</td><td>" + getTime(bits[182])
            html += "</td><td style='text-align:right'>" + getTime(bits[180]) + "</td><td style='text-align:right'>" + bits[179] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td></tr>"

            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td><td>" + bits[185] + bits[64] + "</td><td>" + getTime(bits[186])
            html += "</td><td style='text-align:right'>" + getTime(bits[184]) + "</td><td style='text-align:right'>" + bits[183] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td></tr>"
        }

        if(bits.length > 213 && bits[213] != "")
        {
            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-women-sunglasses'></i></td><td>" + bits[213] + "UVI</td><td>" + getTime(bits[214])
            html += "</td><td style='text-align:right'>" + getTime(bits[216]) + "</td><td style='text-align:right'>" + bits[215] + "W/m\u00B2</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-women-sunglasses'></i></td></tr>"
        }

        html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-windy'></i></td><td colspan='3'>" + bits[92] + bits[61] + " " + bits[93] + " " + getTime(bits[94])
        html += "</td><td style='text-align:right'>" + bits[22] + bits[62] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-umbrella'></i></td></tr>"

        html += "</table><br>";

//      This years stats

        html += "<div style='text-align:center;font-size:" + units.dp(18) + "pt;font-weight:bold;'>This Year's Statistics</div>"
        html += "<table style='width:100%;border:0px;'>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-temperature'></i></td><td>" + bits[113] + bits[60] + "</td><td>" + getTime(bits[114])
        html += "</td><td style='text-align:right'>" + getTime(bits[112]) + "</td><td style='text-align:right'>" + bits[111] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-temperature'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + (iw * 1.4) + "px;' class='wi wi-raindrop'></td><td>" + bits[124] + bits[60] + "</td><td>" + getTime(bits[125])
        html += "</td><td style='text-align:right'>" + getTime(bits[123]) + "</td><td style='text-align:right'>" + bits[122] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + (iw * 1.4) + "px;' class='wi wi-raindrop'></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='wi wi-humidity'></i></td><td>" + bits[128] + bits[64] + "</td><td>" + getTime(bits[129])
        html += "</td><td style='text-align:right'>" + getTime(bits[127]) + "</td><td style='text-align:right'>" + bits[126] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-humidity'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='wi wi-barometer'></i></td><td>" + bits[130] + bits[63] + "</td><td>" + getTime(bits[131])
        html += "</td><td style='text-align:right'>" + getTime(bits[133]) + "</td><td style='text-align:right'>" + bits[132] + bits[63] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-barometer'></i></td></tr>"

        if(bits.length > 202 && root.indoor_readings == "1")
        {
            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td><td>" + bits[189] + bits[60] + "</td><td>" + getTime(bits[190])
            html += "</td><td style='text-align:right'>" + getTime(bits[188]) + "</td><td style='text-align:right'>" + bits[187] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td></tr>"

            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td><td>" + bits[193] + bits[64] + "</td><td>" + getTime(bits[194])
            html += "</td><td style='text-align:right'>" + getTime(bits[192]) + "</td><td style='text-align:right'>" + bits[191] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td></tr>"
        }

        if(bits.length > 217 && bits[217] != "")
        {
            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-women-sunglasses'></i></td><td>" + bits[217] + "UVI</td><td>" + getTime(bits[218])
            html += "</td><td style='text-align:right'>" + getTime(bits[220]) + "</td><td style='text-align:right'>" + bits[219] + "W/m\u00B2</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-women-sunglasses'></i></td></tr>"
        }

        html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-windy'></i></td><td colspan='3'>" + bits[115] + bits[61] + " " + bits[116] + " " + getTime(bits[117])
        html += "</td><td style='text-align:right'>" + bits[23] + bits[62] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-umbrella'></i></td></tr>"

        html += "</table><br>";

//      All time stats

        html += "<div style='text-align:center;font-size:" + units.dp(18) + "pt;font-weight:bold;'>All Time Statistics</div>"
        html += "<table style='width:100%;border:0px;'>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-temperature'></i></td><td>" + bits[136] + bits[60] + "</td><td>" + getTime(bits[137])
        html += "</td><td style='text-align:right'>" + getTime(bits[135]) + "</td><td style='text-align:right'>" + bits[134] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-temperature'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + (iw * 1.4) + "px;' class='wi wi-raindrop'></td><td>" + bits[147] + bits[60] + "</td><td>" + getTime(bits[148])
        html += "</td><td style='text-align:right'>" + getTime(bits[146]) + "</td><td style='text-align:right'>" + bits[145] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + (iw * 1.4) + "px;' class='wi wi-raindrop'></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='wi wi-humidity'></i></td><td>" + bits[151] + bits[64] + "</td><td>" + getTime(bits[152])
        html += "</td><td style='text-align:right'>" + getTime(bits[150]) + "</td><td style='text-align:right'>" + bits[149] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-humidity'></i></td></tr>"

        html += "<tr><td><i style='font-size:" + iw + "px;' class='wi wi-barometer'></i></td><td>" + bits[153] + bits[63] + "</td><td>" + getTime(bits[154])
        html += "</td><td style='text-align:right'>" + getTime(bits[156]) + "</td><td style='text-align:right'>" + bits[155] + bits[63] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-barometer'></i></td></tr>"

        if(bits.length > 202 && root.indoor_readings == "1")
        {
            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td><td>" + bits[197] + bits[60] + "</td><td>" + getTime(bits[198])
            html += "</td><td style='text-align:right'>" + getTime(bits[196]) + "</td><td style='text-align:right'>" + bits[195] + bits[60] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td></tr>"

            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td><td>" + bits[201] + bits[64] + "</td><td>" + getTime(bits[202])
            html += "</td><td style='text-align:right'>" + getTime(bits[200]) + "</td><td style='text-align:right'>" + bits[199] + bits[64] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-home-page'></i></td></tr>"
        }

        if(bits.length > 221 && bits[221] != "")
        {
            html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-women-sunglasses'></i></td><td>" + bits[221] + "UVI</td><td>" + getTime(bits[222])
            html += "</td><td style='text-align:right'>" + getTime(bits[224]) + "</td><td style='text-align:right'>" + bits[223] + "W/m\u00B2</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='flaticon-women-sunglasses'></i></td></tr>"
        }

        html += "<tr><td><i style='font-size:" + iw + "px;' class='flaticon-windy'></i></td><td colspan='3'>" + bits[138] + bits[61] + " " + bits[139] + " " + getTime(bits[140])
        html += "</td><td style='text-align:right'>" + bits[157] + bits[62] + "</td><td style='text-align:right'><i style='font-size:" + iw + "px;' class='wi wi-umbrella'></i></td></tr>"

        html += "</table><br>"

        html += htmlfooter

        statsData.loadHtml(html, "file:///")
    }

    function getTime(str)
    {
    	str = str.trim()

    	if(!str.includes(" "))
    		return str

        return str.split(" ", 2)[0].trim()
    }

    function convert(cur)
    {
        cur = cur.trim()
        if(!cur.includes(" "))
            return cur

        var bits = cur.split(" ")
        if(bits.length < 2)
            return cur

        var time = bits[0].trim().split(":")
        if(time.length < 3)
            return cur

        var hours = parseInt(time[0])
        var mins = parseInt(time[1])
        var secs = parseInt(time[2])
        var pm = bits[1].trim().toLowerCase() == "pm"

        if(!pm && hours == 12)
	    	hours = 0;
	    else if(pm && hours != 12)
	    	hours = hours + 12;

        return zeroPad(hours, 10) + zeroPad(mins, 10) + zeroPad(secs, 10)
    }

    function zeroPad(nr, base)
    {
        var len = (String(base).length - String(nr).length) + 1;
        return len > 0 ? new Array(len).join('0') + nr : nr;
    }
}