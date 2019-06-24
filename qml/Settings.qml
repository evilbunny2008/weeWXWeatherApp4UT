import io.thp.pyotherside 1.5
import QtQuick 2.5
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.1
import QtQuick.Window 2.2
import Ubuntu.Components 1.3

Page {
    id: authPage
    width: parent.width
    height: parent.height

    header: PageHeader {
        title: "weeWX Weather App"
    }

    ColumnLayout {
        width: parent.width
        anchors.top: header.bottom
        anchors.left: parent.left
        anchors.right: parent.right

        Label {
            text: "Enter the URL to your settings.txt"
        }

        TextField {
            id: settings_url
            text: root.settings_url
            Layout.fillWidth: true
        }

        RowLayout {
            Layout.fillWidth: true
            anchors.left: parent.left
            anchors.right: parent.right

            Label {
                text: "Show Indoor Readings?"
            }

            Switch {
                id: indoor_readings
                checked: root.indoor_readings == 1
                anchors.right: parent.right
            }
        }

        RowLayout {
            Layout.fillWidth: true
            anchors.left: parent.left
            anchors.right: parent.right

            Label {
                text: "Use Dark Theme? (requires restart)"
            }

            Switch {
                id: dark_theme
                checked: root.dark_theme == 1
                anchors.right: parent.right
            }
        }

        RowLayout {
            Layout.fillWidth: true
            anchors.left: parent.left
            anchors.right: parent.right

            Label {
                text: "Use Metric in Forecasts?"
            }

            Switch {
                id: metric
                checked: root.metric == 1
                anchors.right: parent.right
            }
        }

        RowLayout {
            Layout.fillWidth: true
            anchors.left: parent.left
            anchors.right: parent.right

            Label {
                text: "Use icons instead of glyphs?"
            }

            Switch {
                id: use_icons
                checked: root.use_icons == 1
                anchors.right: parent.right
            }
        }

        RowLayout {
            Layout.fillWidth: true
            anchors.left: parent.left
            anchors.right: parent.right

            Label {
                text: "Only update on Wifi?"
            }

            Switch {
                id: wifidownload
                checked: root.wifidownload == 1
                anchors.right: parent.right
            }
        }

        RowLayout {
            Layout.fillWidth: true
            anchors.left: parent.left
            anchors.right: parent.right
            height: units.gu(3)

            Label {
                text: "Update Frequency:"
            }

            ComboBox {
                id: updateTime
                anchors.right: parent.right
                Layout.minimumWidth: units.dp(150)
                Layout.minimumHeight: units.gu(3)
                model: [ "Manual Updates", "Every 5 Minutes", "Every 10 Minutes", "Every 15 Minutes", "Every 30 Minutes", "Every Hour" ]

                Component.onCompleted: {
                    updateTime.currentIndex = Number(root.update_freq)
                    // updateTime.text = updateTime.get(currentIndex).text
                }
            }
        }

        Label {
            text: "Radar or Forecast on main screen"
        }

        ButtonGroup {
            buttons: column.children
        }

        Column {
            id: column

            RadioButton {
                id: show_radar
                checked: root.show_radar == 1
                text: "Show Radar"
            }

            RadioButton {
                id: show_forecasts
                checked: root.show_radar != 1
                text: "Show Forecasts"
            }
        }

        Button {
            id: processButton
            Layout.fillWidth: true
            text: "Save"
            color: "#3EB34F"
            onClicked: {
                busyIndicator.running = true
                processButton.enabled = false
                pytest.call("main.save_config",
                            [settings_url.text, indoor_readings.checked, dark_theme.checked,
                             metric.checked, show_radar.checked, use_icons.checked, updateTime.currentIndex,
                             wifidownload.checked],
                            function(results) {
                    busyIndicator.running = false
                    processButton.enabled = true

                    if(results[0] == false) {
                        console.log(results[1])
                        toast.show(results[1], 5000)
                        return
                    } else {
                        root.settings_url = settings_url.text
                        root.indoor_readings = indoor_readings.checked ? "1":"0"
                        root.dark_theme = dark_theme.checked ? "1":"0"
                        root.metric = metric.checked ? "1":"0"
                        root.show_radar = show_radar.checked ? "1":"0"
                        root.use_icons = use_icons.checked ? "1":"0"
                        root.saved = "1"
                        root.rad_type = results[2]
                        root.radar_url = results[3]
                        root.fctype = results[4]
                        root.update_freq = updateTime.currentIndex.toString()
                        root.wifidownload = wifidownload ? "1":"0"

                        root.afterSettings()
                    }
                })
            }
        }
    }
}