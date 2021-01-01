import io.thp.pyotherside 1.5
import QtPositioning 5.9
import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.1
import QtQuick.Window 2.2
import QtSystemInfo 5.0
import Ubuntu.Components 1.3

MainView {
    id: root
    objectName: "mainView"
    applicationName: "weewxweatherapp.evilbunny"

    width: units.gu(50)
    height: units.gu(80)

    property var settings_url: "https://example.com/weewx/inigo-settings.txt"
    property var indoor_readings: "0"
    property var dark_theme: "0"
    property var metric: "1"
    property var show_radar: "1"
    property var use_icons: "0"
    property var saved: "0"
    property var htmlheader: ""
    property var ssheader
    property var htmlfooter: "</body></html>"
    property var cachebase
    property var rad_type: "image"
    property var radar_url
    property var fctype: "yahoo"
    property var app_dir
    property var update_freq: "1"
    property var wifidownload: "0"
    property var booted: false

    Component.onCompleted: {
        pytest.call("main.get_config", [], function(results)
        {
            settings_url = results[0]
            indoor_readings = results[1]
            dark_theme = results[2]
            metric = results[3]
            show_radar = results[4]
            use_icons = results[5]
            saved = results[6]
            cachebase = results[7]
            rad_type = results[8]
            radar_url = results[9]
            fctype = results[10]
            app_dir = results[11]
            update_freq = results[12]
            wifidownload = results[13]
            

            ssheader = "<link rel='stylesheet' type='text/css' href='file://" + app_dir + "/assets/weathericons.css'>" +
                           "<link rel='stylesheet' type='text/css' href='file://" + app_dir + "/assets/weathericons_wind.css'>" +
                           "<link rel='stylesheet' type='text/css' href='file://" + app_dir + "/assets/flaticon.css'>"

            htmlheader = "<html><head><meta charset='utf-8'/><style>html { overflow: scroll; overflow-x: hidden; } " + 
                         "table tbody tr td {font-size:" + units.dp(11.5) + "pt}</style>" + ssheader + "</head><body>" 
            if(dark_theme == "1")
                htmlheader = "<html><head><meta charset='utf-8'/><style>body{color: #fff; background-color: #000;}" + 
                             "html { overflow: scroll; overflow-x: hidden; } table tbody tr td {font-size:" + units.dp(12) + "pt}</style>" + ssheader + "</head>"

            if(saved == 0 || settings_url == "https://example.com/weewx/inigo-settings.txt")
                loadSettings()
            else
                loadDetails()
        })
    }

    function afterSettings()
    {
        if(stack.depth == 1)
            loadDetails()
        else
            stack.pop()
    }

    function loadSettings()
    {
        stack.push(Qt.resolvedUrl("Settings.qml"))
    }

    function loadDetails()
    {
        stack.push(Qt.resolvedUrl("Details.qml"))
    }

    ToastManager {
        id: toast
    }

    PageStack {
        id: stack
    }

    BusyIndicator {
        id: busyIndicator
        z: root.z + 6
        width: units.gu(20)
        height: units.gu(20)
        anchors.centerIn: parent
        running: false
    }

    Python {
        id: pytest
        Component.onCompleted: {
            addImportPath(Qt.resolvedUrl('.'))
            importModule("main", function() {})
        }
    }
}